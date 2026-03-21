"""
rag_engine.py — Welding Standards RAG Engine (v3)
==================================================
New in v3:
  - Improvement 3: Metadata Enrichment
    Regex extracts clause numbers, table numbers, and technical terms
    from each chunk and stores them as searchable metadata.
    The AI can now cite exact clause references from retrieved text.

  - Improvement 4: Hybrid Search (BM25 + Vector)
    BM25 keyword search layer runs alongside vector search.
    Technical terms like "E7018", "A572", "Clause 5.11" are matched
    exactly rather than semantically. Results are merged and re-ranked
    using Reciprocal Rank Fusion (RRF).

  Everything from v2 is preserved:
  - PDF and TXT file support
  - Line-by-line chunking for knowledge files
  - Page number stripping
"""

import os
import re
import math
from pathlib import Path
from typing import List, Dict, Optional
from collections import defaultdict

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

try:
    from rank_bm25 import BM25Okapi
    BM25_OK = True
except ImportError:
    BM25_OK = False


# ── Constants ─────────────────────────────────────────────────────────────────
CHROMA_PATH   = "chroma_db"
COLLECTION    = "welding_standards"
EMBED_MODEL   = "all-MiniLM-L6-v2"
CHUNK_SIZE    = 400
CHUNK_OVERLAP = 80

# Welding-specific technical term patterns for metadata extraction
CLAUSE_PATTERN  = re.compile(r'\b(?:Clause|clause|Section|section)\s+(\d+(?:\.\d+)*)', re.IGNORECASE)
TABLE_PATTERN   = re.compile(r'\b(?:Table|table)\s+([\d\.]+[A-Za-z]?)', re.IGNORECASE)
FIGURE_PATTERN  = re.compile(r'\b(?:Figure|figure|Fig\.?)\s+([\d\.]+)', re.IGNORECASE)
STEEL_PATTERN   = re.compile(r'\b(A36|A572|A588|A709|A992|A913|A1066|A516|A53|A106|S235|S275|S355|S420|S460|S690|API\s*5L|HPS70W)\b', re.IGNORECASE)
ELECTRODE_PATTERN = re.compile(r'\b(E\d{4,5}[-\w]*|ER\d{2,3}[-\w]*|F\d{1,2}[A-Z]{1,2}[-\w]*)\b')
PROCESS_PATTERN = re.compile(r'\b(SMAW|SAW|GMAW|FCAW|GTAW|TIG|MIG|MAG|FCAW-S|FCAW-G)\b', re.IGNORECASE)
TEMP_PATTERN    = re.compile(r'\b(\d{1,3})\s*°?\s*[CF]\b')


# ── Text extraction ───────────────────────────────────────────────────────────

def extract_text_from_pdf(pdf_path: str) -> str:
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
    text = re.sub(r"-\n", "", text)
    text = re.sub(r" {2,}", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = re.sub(r"^\s*\d{1,4}\s*$", "", text, flags=re.MULTILINE)
    lines = [l for l in text.split("\n") if len(l.strip()) > 4 or l.strip() == ""]
    return "\n".join(lines).strip()


# ── Improvement 3: Metadata Enrichment ───────────────────────────────────────

def extract_metadata(text: str, source: str, chunk_index: int) -> Dict:
    """
    Extract welding-specific metadata from chunk text using regex.
    This allows the AI to cite exact clause/table references and
    enables filtering by technical term in future queries.
    """
    clauses   = list(set(CLAUSE_PATTERN.findall(text)))
    tables    = list(set(TABLE_PATTERN.findall(text)))
    figures   = list(set(FIGURE_PATTERN.findall(text)))
    steels    = list(set(STEEL_PATTERN.findall(text)))
    electrodes = list(set(ELECTRODE_PATTERN.findall(text)))
    processes = list(set(PROCESS_PATTERN.findall(text)))

    # Build a human-readable citation string for the AI to use
    citation_parts = []
    if clauses:
        citation_parts.append("Clause " + ", ".join(clauses[:3]))
    if tables:
        citation_parts.append("Table " + ", ".join(tables[:3]))
    citation = " | ".join(citation_parts) if citation_parts else ""

    # Flatten all technical terms into a searchable string for BM25
    terms = clauses + tables + figures + steels + electrodes + processes
    terms_str = " ".join(terms)

    return {
        "source":      source,
        "chunk_index": chunk_index,
        "clauses":     ", ".join(clauses[:5])    if clauses    else "",
        "tables":      ", ".join(tables[:5])     if tables     else "",
        "steels":      ", ".join(steels[:5])     if steels     else "",
        "electrodes":  ", ".join(electrodes[:5]) if electrodes else "",
        "processes":   ", ".join(processes[:5])  if processes  else "",
        "citation":    citation,
        "tech_terms":  terms_str[:200],  # ChromaDB metadata values must be strings
    }


# ── Chunking ──────────────────────────────────────────────────────────────────

def chunk_txt_file(text: str, source_name: str) -> List[Dict]:
    chunks = []
    for i, line in enumerate(text.split("\n")):
        line = line.strip()
        if not line or line.startswith("SOURCE:"):
            continue
        meta = extract_metadata(line, source_name, i)
        chunks.append({
            "id":      f"{source_name}_{i}",
            "text":    line,
            "metadata": meta,
        })
    return chunks


def chunk_pdf_text(text: str, source_name: str,
                   chunk_size: int = CHUNK_SIZE,
                   overlap: int = CHUNK_OVERLAP) -> List[Dict]:
    paragraphs  = re.split(r"\n{2,}", text)
    chunks      = []
    buffer      = ""
    chunk_index = 0

    def flush(buf):
        nonlocal chunk_index
        if buf.strip():
            meta = extract_metadata(buf.strip(), source_name, chunk_index)
            chunks.append({
                "id":       f"{source_name}_{chunk_index}",
                "text":     buf.strip(),
                "metadata": meta,
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


# ── Improvement 4: BM25 Keyword Search ───────────────────────────────────────

def tokenize_for_bm25(text: str) -> List[str]:
    """
    Tokenise text for BM25, preserving welding technical terms.
    E7018, A572, 5.11 are kept intact as single tokens.
    """
    # Keep alphanumeric sequences including dots and hyphens (for clause numbers)
    tokens = re.findall(r'[A-Za-z0-9][A-Za-z0-9.\-]*', text.lower())
    return [t for t in tokens if len(t) > 1]


class BM25Index:
    """
    Lightweight BM25 index built in memory from chunk texts.
    Rebuilt each time the app starts — fast enough for 7,000 chunks.
    """

    def __init__(self):
        self.chunks    = []   # list of {id, text, metadata}
        self.bm25      = None
        self._built    = False

    def build(self, chunks: List[Dict]):
        self.chunks = chunks
        tokenized   = [tokenize_for_bm25(c["text"]) for c in chunks]
        if BM25_OK and tokenized:
            self.bm25   = BM25Okapi(tokenized)
            self._built = True

    def search(self, query: str, n: int = 10) -> List[Dict]:
        """Return top-n chunks by BM25 score with rank position."""
        if not self._built or not self.bm25:
            return []
        tokens = tokenize_for_bm25(query)
        if not tokens:
            return []
        scores  = self.bm25.get_scores(tokens)
        top_idx = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:n]
        results = []
        for rank, idx in enumerate(top_idx):
            if scores[idx] > 0:
                results.append({
                    **self.chunks[idx],
                    "bm25_score": float(scores[idx]),
                    "bm25_rank":  rank,
                })
        return results

    @property
    def is_ready(self):
        return self._built


def reciprocal_rank_fusion(
    vector_results: List[Dict],
    bm25_results:   List[Dict],
    k: int = 60,
    vector_weight: float = 0.6,
    bm25_weight:   float = 0.4,
) -> List[Dict]:
    """
    Merge vector and BM25 results using Reciprocal Rank Fusion.
    RRF score = Σ weight / (k + rank)
    Higher weight on vector (semantic) than BM25 (keyword) by default.
    """
    scores  = defaultdict(float)
    by_id   = {}

    # Vector results
    for rank, chunk in enumerate(vector_results):
        cid = chunk.get("id") or f"v_{rank}"
        scores[cid]  += vector_weight / (k + rank + 1)
        by_id[cid]    = chunk

    # BM25 results
    for rank, chunk in enumerate(bm25_results):
        cid = chunk.get("id") or f"b_{rank}"
        scores[cid]  += bm25_weight / (k + chunk.get("bm25_rank", rank) + 1)
        if cid not in by_id:
            by_id[cid] = chunk

    # Sort by fused score
    ranked = sorted(scores.keys(), key=lambda cid: scores[cid], reverse=True)
    results = []
    for cid in ranked:
        chunk = dict(by_id[cid])
        chunk["rrf_score"] = round(scores[cid], 6)
        results.append(chunk)

    return results


# ── Main RAG class ────────────────────────────────────────────────────────────

class WeldingRAG:
    """
    Welding standards RAG engine with hybrid search and metadata enrichment.

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
        self._bm25       = BM25Index()
        self._bm25_built = False

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

    def _ensure_bm25(self):
        """Load all chunks from ChromaDB into the BM25 index (done once per session)."""
        if self._bm25_built:
            return
        try:
            col    = self._get_collection()
            total  = col.count()
            if total == 0:
                return
            # Fetch all chunks in batches
            all_chunks = []
            batch_size = 500
            offset     = 0
            while offset < total:
                result = col.get(limit=batch_size, offset=offset,
                                 include=["documents", "metadatas"])
                for doc_id, doc, meta in zip(
                    result["ids"], result["documents"], result["metadatas"]
                ):
                    all_chunks.append({
                        "id":       doc_id,
                        "text":     doc,
                        "metadata": meta,
                    })
                offset += batch_size

            self._bm25.build(all_chunks)
            self._bm25_built = True
        except Exception:
            pass  # BM25 is optional — vector search still works

    # ── Index management ──────────────────────────────────────────────────────

    def build_index(self, file_paths: List[str],
                    reset: bool = False,
                    progress_cb=None) -> int:
        col = self._get_collection()

        if reset:
            self._client.delete_collection(COLLECTION)
            self._collection = None
            self._bm25_built = False
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
                    ids       = [c["id"]       for c in batch],
                    documents = [c["text"]     for c in batch],
                    metadatas = [c["metadata"] for c in batch],
                )

            total_added += len(chunks)
            if progress_cb:
                progress_cb(f"   ✅ {source_name}: {len(chunks)} chunks indexed "
                            f"(with clause/table metadata).")

        # Reset BM25 so it rebuilds on next query
        self._bm25_built = False
        return total_added

    def index_count(self) -> int:
        try:
            return self._get_collection().count()
        except Exception:
            return 0

    def is_ready(self) -> bool:
        return self.index_count() > 0

    # ── Query ─────────────────────────────────────────────────────────────────

    def query(self, question: str, n: int = 5,
              source_filter: Optional[str] = None) -> List[Dict]:
        """
        Hybrid search: vector + BM25, merged with Reciprocal Rank Fusion.

        Returns list of dicts with keys:
            text, source, chunk_index, citation, clauses, tables,
            steels, electrodes, processes, distance, rrf_score
        """
        col   = self._get_collection()
        where = {"source": source_filter} if source_filter else None

        # ── Vector search ─────────────────────────────────────────────────────
        vec_n = min(n * 3, 20)  # fetch more candidates for fusion
        vec_results_raw = col.query(
            query_texts = [question],
            n_results   = vec_n,
            where       = where,
            include     = ["documents", "metadatas", "distances"],
        )

        vector_chunks = []
        if vec_results_raw and vec_results_raw["documents"]:
            for doc_id, doc, meta, dist in zip(
                vec_results_raw["ids"][0],
                vec_results_raw["documents"][0],
                vec_results_raw["metadatas"][0],
                vec_results_raw["distances"][0],
            ):
                vector_chunks.append({
                    "id":          doc_id,
                    "text":        doc,
                    "source":      meta.get("source", "unknown"),
                    "chunk_index": meta.get("chunk_index", 0),
                    "citation":    meta.get("citation", ""),
                    "clauses":     meta.get("clauses", ""),
                    "tables":      meta.get("tables", ""),
                    "steels":      meta.get("steels", ""),
                    "electrodes":  meta.get("electrodes", ""),
                    "processes":   meta.get("processes", ""),
                    "distance":    round(dist, 4),
                })

        # ── BM25 keyword search ───────────────────────────────────────────────
        self._ensure_bm25()
        bm25_chunks_raw = self._bm25.search(question, n=vec_n) if self._bm25.is_ready else []

        # Enrich BM25 results with metadata fields
        bm25_chunks = []
        for c in bm25_chunks_raw:
            meta = c.get("metadata", {})
            bm25_chunks.append({
                "id":          c["id"],
                "text":        c["text"],
                "source":      meta.get("source", "unknown"),
                "chunk_index": meta.get("chunk_index", 0),
                "citation":    meta.get("citation", ""),
                "clauses":     meta.get("clauses", ""),
                "tables":      meta.get("tables", ""),
                "steels":      meta.get("steels", ""),
                "electrodes":  meta.get("electrodes", ""),
                "processes":   meta.get("processes", ""),
                "distance":    1.0,  # BM25 has no distance concept
                "bm25_rank":   c.get("bm25_rank", 0),
            })

        # ── Reciprocal Rank Fusion ────────────────────────────────────────────
        if bm25_chunks:
            fused = reciprocal_rank_fusion(vector_chunks, bm25_chunks)
        else:
            fused = vector_chunks  # fall back to vector only

        return fused[:n]

    def format_context(self, chunks: List[Dict]) -> str:
        """
        Format retrieved chunks into a prompt-ready context block.
        Now includes exact clause/table citations from metadata.
        """
        if not chunks:
            return "No relevant clauses found in the indexed standards."

        lines = ["RETRIEVED STANDARD CLAUSES", "━" * 40]
        for i, chunk in enumerate(chunks, 1):
            # Build citation line from metadata
            source   = chunk.get("source", "unknown")
            citation = chunk.get("citation", "")
            cite_str = f"{source}"
            if citation:
                cite_str += f" — {citation}"

            # Show relevance score
            rrf   = chunk.get("rrf_score")
            dist  = chunk.get("distance", 1.0)
            if rrf:
                score_str = f"hybrid score: {rrf:.4f}"
            else:
                score_str = f"relevance: {1 - dist:.0%}"

            lines.append(f"\n[{i}] {cite_str} ({score_str})")
            lines.append(chunk["text"])
            lines.append("─" * 40)

        return "\n".join(lines)