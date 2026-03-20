"""
rag_engine.py — Welding Standards RAG Engine (v2)
==================================================
Fixes vs v1:
  - Supports both .pdf AND .txt files
  - Smaller chunk size (400 chars) — dense technical PDFs no longer swallowed
  - .txt files chunked line-by-line (one fact per chunk, perfect for knowledge files)
  - Better paragraph detection for EN ISO / BS EN style PDFs
  - Page numbers stripped from extracted text
"""

import os
import re
from pathlib import Path
from typing import List, Dict, Optional

# ── Optional imports ──────────────────────────────────────────────────────────
try:
    import fitz
    PYMUPDF_OK = True
except ImportError:
    PYMUPDF_OK = False

try:
    import chromadb
    from chromadb.utils import embedding_functions
    CHROMA_OK = True
except ImportError:
    CHROMA_OK = False

try:
    from sentence_transformers import SentenceTransformer
    ST_OK = True
except ImportError:
    ST_OK = False


# ── Constants ─────────────────────────────────────────────────────────────────
CHROMA_PATH   = "chroma_db"
COLLECTION    = "welding_standards"
EMBED_MODEL   = "all-MiniLM-L6-v2"
CHUNK_SIZE    = 400    # reduced from 600 — better clause-level splits
CHUNK_OVERLAP = 80


# ── Text extraction ───────────────────────────────────────────────────────────

def extract_text_from_pdf(pdf_path: str) -> str:
    """Extract all text from a PDF page by page, joining with double newlines."""
    if not PYMUPDF_OK:
        raise ImportError("PyMuPDF not installed. Run: pip install pymupdf")
    doc   = fitz.open(pdf_path)
    pages = []
    for page in doc:
        text = page.get_text("text").strip()
        if text:
            pages.append(text)
    doc.close()
    return "\n\n".join(pages)


def extract_text_from_txt(txt_path: str) -> str:
    with open(txt_path, "r", encoding="utf-8") as f:
        return f.read()


def extract_text(file_path: str) -> str:
    ext = Path(file_path).suffix.lower()
    if ext == ".pdf":
        return extract_text_from_pdf(file_path)
    elif ext == ".txt":
        return extract_text_from_txt(file_path)
    else:
        raise ValueError(f"Unsupported file type: {ext}")


def clean_text(text: str) -> str:
    text = re.sub(r"-\n", "", text)                          # rejoin hyphenated breaks
    text = re.sub(r" {2,}", " ", text)                       # collapse spaces
    text = re.sub(r"\n{3,}", "\n\n", text)                   # collapse extra newlines
    text = re.sub(r"^\s*\d{1,4}\s*$", "", text, flags=re.MULTILINE)  # strip page numbers
    lines = [l for l in text.split("\n") if len(l.strip()) > 4 or l.strip() == ""]
    return "\n".join(lines).strip()


# ── Chunking ──────────────────────────────────────────────────────────────────

def chunk_txt_file(text: str, source_name: str) -> List[Dict]:
    """
    For .txt knowledge files: each non-empty line becomes its own chunk.
    This keeps every fact as a separate retrievable unit.
    """
    chunks = []
    for i, line in enumerate(text.split("\n")):
        line = line.strip()
        if not line or line.startswith("SOURCE:"):
            continue
        chunks.append({
            "id":          f"{source_name}_{i}",
            "text":        line,
            "source":      source_name,
            "chunk_index": i,
        })
    return chunks


def chunk_pdf_text(text: str, source_name: str,
                   chunk_size: int = CHUNK_SIZE,
                   overlap: int = CHUNK_OVERLAP) -> List[Dict]:
    """
    For PDF text: split at paragraph boundaries, then by sentence if needed.
    Overlapping windows preserve clause context across chunk boundaries.
    """
    paragraphs  = re.split(r"\n{2,}", text)
    chunks      = []
    buffer      = ""
    chunk_index = 0

    def flush(buf):
        nonlocal chunk_index
        if buf.strip():
            chunks.append({
                "id":          f"{source_name}_{chunk_index}",
                "text":        buf.strip(),
                "source":      source_name,
                "chunk_index": chunk_index,
            })
            chunk_index += 1

    for para in paragraphs:
        para = para.strip()
        if not para:
            continue

        if len(buffer) + len(para) + 1 <= chunk_size:
            buffer += (" " if buffer else "") + para
        else:
            flush(buffer)
            tail   = buffer[-overlap:] if overlap and buffer else ""
            buffer = ""

            if len(para) <= chunk_size:
                buffer = (tail + " " + para).strip() if tail else para
            else:
                sentences = re.split(r"(?<=[.!?])\s+", para)
                for sent in sentences:
                    if len(buffer) + len(sent) + 1 <= chunk_size:
                        buffer += (" " if buffer else "") + sent
                    else:
                        flush(buffer)
                        tail   = buffer[-overlap:] if overlap and buffer else ""
                        buffer = (tail + " " + sent).strip() if tail else sent

    flush(buffer)
    return chunks


def chunk_text(text: str, source_name: str, is_txt: bool = False) -> List[Dict]:
    if is_txt:
        return chunk_txt_file(text, source_name)
    return chunk_pdf_text(text, source_name)


# ── Main RAG class ────────────────────────────────────────────────────────────

class WeldingRAG:
    """
    Welding standards RAG engine.

    Typical workflow:
        rag = WeldingRAG()
        rag.build_index(["standards/AWS_D1_1_2025.pdf",
                         "standards/welding_knowledge.txt"])
        results = rag.query("preheat A572 Gr50 SMAW 25mm", n=5)
    """

    def __init__(self, chroma_path: str = CHROMA_PATH):
        self._check_deps()
        self.chroma_path = chroma_path
        self._client     = None
        self._collection = None

    def _check_deps(self):
        missing = []
        if not PYMUPDF_OK: missing.append("pymupdf")
        if not CHROMA_OK:  missing.append("chromadb")
        if not ST_OK:      missing.append("sentence-transformers")
        if missing:
            raise ImportError(
                f"Missing packages: {', '.join(missing)}\n"
                f"Run: pip install {' '.join(missing)}"
            )

    def _get_collection(self):
        if self._collection is None:
            self._client = chromadb.PersistentClient(path=self.chroma_path)
            emb_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
                model_name=EMBED_MODEL
            )
            self._collection = self._client.get_or_create_collection(
                name               = COLLECTION,
                embedding_function = emb_fn,
                metadata           = {"hnsw:space": "cosine"},
            )
        return self._collection

    def build_index(self, file_paths: List[str],
                    reset: bool = False,
                    progress_cb=None) -> int:
        col = self._get_collection()

        if reset:
            self._client.delete_collection(COLLECTION)
            self._collection = None
            col = self._get_collection()
            if progress_cb:
                progress_cb("🗑️ Existing index cleared.")

        total_added = 0

        for file_path in file_paths:
            source_name = Path(file_path).stem
            is_txt      = Path(file_path).suffix.lower() == ".txt"

            if progress_cb:
                progress_cb(f"📄 Processing {source_name}…")

            existing = col.get(where={"source": source_name}, limit=1)
            if existing["ids"]:
                if progress_cb:
                    progress_cb(f"   ✅ {source_name} already indexed — skipping.")
                continue

            try:
                raw_text = extract_text(file_path)
                clean    = clean_text(raw_text)
                chunks   = chunk_text(clean, source_name, is_txt=is_txt)
            except Exception as e:
                if progress_cb:
                    progress_cb(f"   ❌ Failed: {source_name}: {e}")
                continue

            if not chunks:
                if progress_cb:
                    progress_cb(f"   ⚠️ No content extracted from {source_name}")
                continue

            batch_size = 200
            for i in range(0, len(chunks), batch_size):
                batch = chunks[i : i + batch_size]
                col.upsert(
                    ids       = [c["id"]   for c in batch],
                    documents = [c["text"] for c in batch],
                    metadatas = [{"source":      c["source"],
                                  "chunk_index": c["chunk_index"]} for c in batch],
                )

            total_added += len(chunks)
            if progress_cb:
                progress_cb(f"   ✅ {source_name}: {len(chunks)} chunks indexed.")

        return total_added

    def index_count(self) -> int:
        try:
            return self._get_collection().count()
        except Exception:
            return 0

    def is_ready(self) -> bool:
        return self.index_count() > 0

    def query(self, question: str, n: int = 5,
              source_filter: Optional[str] = None) -> List[Dict]:
        col   = self._get_collection()
        where = {"source": source_filter} if source_filter else None

        results = col.query(
            query_texts = [question],
            n_results   = n,
            where       = where,
        )

        output = []
        if results and results["documents"]:
            for doc, meta, dist in zip(
                results["documents"][0],
                results["metadatas"][0],
                results["distances"][0],
            ):
                output.append({
                    "text":        doc,
                    "source":      meta.get("source", "unknown"),
                    "chunk_index": meta.get("chunk_index", 0),
                    "distance":    round(dist, 4),
                })
        return output

    def format_context(self, chunks: List[Dict]) -> str:
        if not chunks:
            return "No relevant clauses found in the indexed standards."

        lines = ["RETRIEVED STANDARD CLAUSES", "━" * 40]
        for i, chunk in enumerate(chunks, 1):
            lines.append(
                f"\n[{i}] Source: {chunk['source']} "
                f"(relevance: {1 - chunk['distance']:.0%})"
            )
            lines.append(chunk["text"])
            lines.append("─" * 40)

        return "\n".join(lines)