# JavaScript Master Study Documentation Rules

Always follow the comprehensive production and styling rules defined in [.AGENT/agent.md](file:///e:/Git%20All%20Repo/Note-Book/.AGENT/agent.md) for generating HTML and PDF book chapters:
- 100% Zero-Skipping policy (Never compress, summarize or skip any section, question, or code).
- Page 1 balance: Master Banner + Intro + Part 1 Banner + Section 1 all fit unbroken on Page 1.
- Zero mid-card page splits (`page-break-inside: avoid !important`).
- Strict margins: `@page { size: A4; margin: 8mm 10mm; }` and `.doc-page { padding: 0 !important; margin: 0 !important; }`.
- No horizontal scrollbars in code blocks (`overflow-x: hidden !important; white-space: pre-wrap !important; word-break: break-word !important;`).
- Clean up all temporary `.png` files in `temp/` immediately after inspection.
