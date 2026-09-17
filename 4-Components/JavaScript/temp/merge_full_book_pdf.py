import os
import re
import sys
import time
import pymupdf
import shutil

sys.stdout.reconfigure(encoding='utf-8')

CHAPTER_TITLES = {
    1: "Chapter 01: JavaScript Fundamentals — JavaScript-এর ভিত্তি",
    2: "Chapter 02: Variables, Data Types & Type System",
    3: "Chapter 03: Operators & Expressions",
    4: "Chapter 04: Control Flow & Decision Making",
    5: "Chapter 05: Loops & Iteration",
    6: "Chapter 06: Functions — Complete Mastery",
    7: "Chapter 07: Scope, Execution Context & Hoisting",
    8: "Chapter 08: Strings & String Manipulation",
    9: "Chapter 09: Arrays & Array Methods",
    10: "Chapter 10: Objects & Property Descriptors",
    11: "Chapter 11: Prototypes & Prototypal Inheritance",
    12: "Chapter 12: Map, Set, WeakMap & WeakSet",
    13: "Chapter 13: Built-in Objects, Math, Date & Internationalization",
    14: "Chapter 14: Error Handling & Debugging",
    15: "Chapter 15: Document Object Model (DOM)",
    16: "Chapter 16: Events & Event-Driven Architecture",
    17: "Chapter 17: Forms & Data Validation",
    18: "Chapter 18: Browser Storage & Cookies",
    19: "Chapter 19: JSON Architecture & Serialization",
    20: "Chapter 20: ES Modules & Modular Architecture",
    21: "Chapter 21: Asynchronous JavaScript, Promises & Async/Await",
    22: "Chapter 22: HTTP, Network Requests & Fetch API",
    23: "Chapter 23: Regular Expressions (RegEx)",
    24: "Chapter 24: Object-Oriented Programming (OOP) & Classes",
    25: "Chapter 25: Functional Programming with JavaScript",
    26: "Chapter 26: Closures, IIFE, Currying & Advanced Scoping",
    27: "Chapter 27: Iterators, Generators & Async Iteration",
    28: "Chapter 28: Symbols, Proxy & Reflect API",
    29: "Chapter 29: Event Loop, Microtasks & Macrotasks",
    30: "Chapter 30: Memory Management & Garbage Collection",
    31: "Chapter 31: JavaScript Web Security & Defense",
    32: "Chapter 32: Advanced Browser APIs",
    33: "Chapter 33: Web Performance & Optimization",
    34: "Chapter 34: NPM, Package Management & Tooling",
    35: "Chapter 35: Testing JavaScript (Jest & Vitest)",
    36: "Chapter 36: Modern ECMAScript (ES2020 – ESNext)",
    37: "Chapter 37: JavaScript Design Patterns",
    38: "Chapter 38: Advanced JavaScript for React",
    39: "Chapter 39: Advanced JavaScript for Node.js",
    40: "Chapter 40: Real-World Projects & Interview Preparation",
}

def merge_all_chapters():
    pdf_dir = '3-JavaScript/2-chapter-pdfs'
    out_dir = '3-JavaScript/3-full-book-pdf'
    os.makedirs(out_dir, exist_ok=True)
    out_name = 'JavaScript-Master-Study-Documentation-Full-Book.pdf'
    out_path = os.path.join(out_dir, out_name)

    # Find and sort all 40 PDFs
    pattern = re.compile(r'Chapter-(\d+)-')
    files_with_num = []
    for f in os.listdir(pdf_dir):
        if f.endswith('.pdf') and f.startswith('Chapter-'):
            m = pattern.search(f)
            if m:
                ch_num = int(m.group(1))
                files_with_num.append((ch_num, os.path.join(pdf_dir, f)))

    files_with_num.sort(key=lambda x: x[0])
    print(f"[INFO] Found {len(files_with_num)} chapters to merge.")

    merged_doc = pymupdf.open()
    toc = []
    current_page = 1

    start_time = time.time()

    for ch_num, file_path in files_with_num:
        doc = pymupdf.open(file_path)
        page_count = len(doc)
        title = CHAPTER_TITLES.get(ch_num, f"Chapter {ch_num:02d}")
        
        # Add to Table of Contents: [level, title, page_number]
        # Level 1 is root bookmark
        toc.append([1, title, current_page])

        print(f"  Merging Ch {ch_num:02d}: {os.path.basename(file_path)} ({page_count} pages) -> Starts at page {current_page}", flush=True)
        merged_doc.insert_pdf(doc)
        doc.close()

        current_page += page_count

    # Set interactive bookmarks / TOC
    merged_doc.set_toc(toc)

    # Save final combined document
    print(f"[INFO] Saving merged PDF to {out_path}...", flush=True)
    merged_doc.save(out_path, deflate=True)
    total_pages = len(merged_doc)
    merged_doc.close()

    file_size_mb = os.path.getsize(out_path) / (1024 * 1024)
    elapsed = time.time() - start_time

    print(f"[SUCCESS] Merged {len(files_with_num)} chapters into {out_path}")
    print(f"          Total Pages: {total_pages}")
    print(f"          File Size:   {file_size_mb:.2f} MB")
    print(f"          Elapsed:     {elapsed:.2f} seconds")

    # Dual-sync to secondary drive
    sec_repo = r'e:\Git All Repo\Note-Book\3-JavaScript\3-full-book-pdf'
    if os.path.exists(os.path.dirname(sec_repo)):
        os.makedirs(sec_repo, exist_ok=True)
        sec_dest = os.path.join(sec_repo, out_name)
        shutil.copy2(out_path, sec_dest)
        print(f"[SYNC] Successfully copied merged PDF to {sec_dest}")

if __name__ == '__main__':
    merge_all_chapters()
