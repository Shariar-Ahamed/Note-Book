# JavaScript Master Study Documentation Rules

Always follow the comprehensive production and styling rules defined in [.AGENT/agent.md](file:///e:/Git%20All%20Repo/Note-Book/.AGENT/agent.md) for generating HTML and PDF book chapters:
- 100% Zero-Skipping policy (Never compress, summarize or skip any section, question, or code).
- **Semantic Code & Technical Correctness Policy**: Never blindly copy authoring typos or copy-paste duplicates from markdown. Proactively audit, validate, and fix any copy-paste duplication between ✅ Correct and ❌ Invalid/Incorrect blocks, syntax errors, or mismatched code outputs in JavaScript/temp/ch-*.md before PDF generation. Ensure invalid tokens are visually marked with red wavy styling so learners immediately see what is wrong.
- Page 1 balance: Master Banner + Intro + Part 1 Banner + Section 1 all fit unbroken on Page 1.
- Zero mid-card page splits (page-break-inside: avoid !important).
- Strict margins: @page { size: A4; margin: 8mm 10mm; } and .doc-page { padding: 0 !important; margin: 0 !important; }.
- No horizontal scrollbars in code blocks (overflow-x: hidden !important; white-space: pre-wrap !important; word-break: break-word !important;).
- Clean up all temporary .png files in temp/ or JavaScript/temp/ immediately after inspection.
- **Git Commit & Push Policy**: Do NOT automatically commit or push to Git. Only commit and push when the user explicitly instructs to do so.

## 🏷️ Chapter Renovation Guidelines (Top-Right Badge & Custom Title Standard)
When updating/renovating chapters (e.g. Chapter 01 - 25):
1. **Banner Heading Replacement**: Remove generic "JAVASCRIPT MASTER STUDY DOCUMENTATION" as the main banner title (`.banner-title`) and replace it with the specific **Chapter Name** (e.g., `JAVASCRIPT FUNDAMENTALS — JAVASCRIPT-এর ভিত্তি`).
2. **Top-Right Yellow Chapter Badge**: Place a bright yellow badge at the top-right of `.banner-top` (e.g., `<span class="chapter-badge">Chapter 01</span>`) using `#f7df1e` background and bold black `#000000` text, matching Chapter 39 & 40 style.
3. **JS Logo Theme Matching**: Style the left-side `JS` logo (`.banner-icon`) with matching JavaScript brand colors (`background: #f7df1e; color: #000000; font-weight: 800;`).
4. **Enhanced Diagrams**: Retain 100% of the diagram content and logic intact, while upgrading visual presentation to match Chapter 39 & 40 standards (sleek dark `#090d16` background, clean `#1e293b` borders, and color accents).
5. **CRITICAL ZERO CONTENT MODIFICATION POLICY**: Absolutely DO NOT alter, skip, rewrite, or remove any other single word, code snippet, explanation, question, or text in the PDF. Everything else remains 100% identical.

