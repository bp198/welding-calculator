import fitz
import os

files = [
    'standards/AWS D1.1 2025.pdf',
    'standards/AWS D1.1_D1.1M-2020.pdf',
    'standards/BS EN 1011-1 - 2009.pdf',
    'standards/BS EN 1011-3-2018--[2019-01-06--09-25-56 AM].pdf',
    'standards/BS EN 1011-6-2018--[2019-01-06--09-13-40 AM].pdf',
    'standards/BS EN ISO 15614-1-2017.pdf · versión 1.pdf',
    'standards/EN-1011-2.pdf',
]

for path in files:
    if not os.path.exists(path):
        print(f"NOT FOUND: {path}")
        continue
    doc = fitz.open(path)
    total = len(doc)
    text_pages = sum(1 for page in doc if len(page.get_text('text').strip()) > 100)
    doc.close()
    print(f"{os.path.basename(path)[:40]:<40} | {total:>4} pages | {text_pages:>4} text | {total-text_pages:>4} image")