# 📘 Master Study Note-Book (মাল্টি-ল্যাঙ্গুয়েজ স্টাডি নোটবুক)

> 🚀 **Live Interactive Web Book:** [https://shariar-ahamed.github.io/Note-Book/](https://shariar-ahamed.github.io/Note-Book/)  
> 📖 **Direct JavaScript Track:** [https://shariar-ahamed.github.io/Note-Book/JavaScript/code/](https://shariar-ahamed.github.io/Note-Book/JavaScript/code/)

A production-grade, highly structured multi-language software engineering documentation repository. Built with strict formatting standards, deep architectural diagrams, and a **100% Zero-Skipping Policy**.

---

## 🌐 Language Curriculums & Tracks

| Language / Track | Scope & Content | Documentation Index | Status |
| :--- | :--- | :---: | :---: |
| **💛 JavaScript (Full Stack)** | 40 Chapters • Fundamentals to React/Node.js Architecture • 1200+ Pages | [🌐 Live Web Book](https://shariar-ahamed.github.io/Note-Book/JavaScript/code/) • [Browse Track](Components/JavaScript/README.md) | ✅ **100% Complete** (HTML & Print-Ready PDF) |
| **💙 TypeScript** | Type Systems, Generics, Utility Types, Enterprise Architecture | *In Pipeline* | ⏳ Upcoming |
| **🐍 Python** | Core Mechanics, AsyncIO, Metaprogramming & Web Architecture | *In Pipeline* | ⏳ Upcoming |
| **🦀 Go / Rust** | Systems Programming, Concurrency, Memory Safety & Cloud Native | *In Pipeline* | ⏳ Upcoming |

---

## 📂 Repository Structure

```
Note-Book/
├── HTML/                       # 📂 HTML Curriculum & Tracks
├── CSS/                        # 📂 CSS Curriculum & Tracks
├── JavaScript/                 # 📂 Published JavaScript Track (Production Distribution)
│   ├── code/                   # Live Interactive Web Book (HTML, CSS, JS)
│   ├── chapter-pdfs/           # 40 Print-ready vectorized A4 PDFs (Chapter-01 to 40)
│   └── full-book-pdf/          # Complete Omnibus Master PDF (1,212 Pages)
├── Components/                 # 📂 Development & Modular Source Components
│   ├── HTML/                   # HTML source components & drafts
│   ├── CSS/                    # CSS source components & drafts
│   └── JavaScript/             # JavaScript source files & generators
│       ├── .AGENT/             # Formatting rules, print engine & theme guides
│       ├── .agents/            # IDE instructions & customization
│       ├── Code/               # 40 Single-chapter HTML source documents
│       ├── temp/               # Markdown source drafts & build scripts
│       ├── all-ch.md           # Master curriculum & syllabus
│       ├── last-update.md      # Chapter revision history
│       └── README.md           # Dedicated JavaScript chapter index & table
├── index.html                  # Root landing & auto-redirect engine
└── README.md                   # Multi-language master hub (this file)
```

---

## 🎯 Production & Publishing Standards ([Rulebook](Components/JavaScript/.AGENT/agent.md))

- **100% Zero-Skipping Policy:** All technical definitions, language edge cases, deep code samples, ASCII diagrams, and interview problems are rendered verbatim.
- **Page 1 Balance:** Master Banner + Chapter Intro + Part 01 Banner + Section 1 Card fit unbroken on Page 1.
- **Zero Mid-Card Page Splits:** Strict CSS page-break rules preventing code or study cards from breaking across physical pages.
- **Precision Print Margins:** A4 format with `@page { size: A4; margin: 8mm 10mm; }` and zero container padding leakage.
- **Overflow Prevention:** Code blocks and ASCII trees with auto-wrap to eliminate horizontal scrollbars in both web view and print.