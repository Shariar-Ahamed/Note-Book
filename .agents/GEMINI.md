# JavaScript Master Study Documentation Rules

Always follow the comprehensive production and styling rules defined in [.AGENT/agent.md](file:///e:/Git%20All%20Repo/Note-Book/.AGENT/agent.md) for generating HTML and PDF book chapters:
- 100% Zero-Skipping policy (Never compress, summarize or skip any section, question, or code).
- **Semantic Code & Technical Correctness Policy**: Never blindly copy authoring typos or copy-paste duplicates from markdown. Proactively audit, validate, and fix any copy-paste duplication between ✅ Correct and ❌ Invalid/Incorrect blocks, syntax errors, or mismatched code outputs in 	emp/ch-*.md before PDF generation. Ensure invalid tokens are visually marked with red wavy styling so learners immediately see what is wrong.
- Page 1 balance: Master Banner + Intro + Part 1 Banner + Section 1 all fit unbroken on Page 1.
- Zero mid-card page splits (page-break-inside: avoid !important).
- Strict margins: @page { size: A4; margin: 8mm 10mm; } and .doc-page { padding: 0 !important; margin: 0 !important; }.
- No horizontal scrollbars in code blocks (overflow-x: hidden !important; white-space: pre-wrap !important; word-break: break-word !important;).
- Clean up all temporary .png files in temp/ immediately after inspection.
- **Git Commit & Push Policy**: Do NOT automatically commit or push to Git. Only commit and push when the user explicitly instructs to do so.
