"""
Build Full-Book: Generates modular Full-Book/ folder with index.html, css/style.css, and js/app.js
incorporating all 40 chapters of the JavaScript Master Study Documentation.
"""
import glob
import re
import os
import sys
import shutil
from bs4 import BeautifulSoup

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

def get_master_css():
    return """/* ==========================================================================
   JAVASCRIPT MASTER STUDY DOCUMENTATION — COMPLETE BOOK (CHAPTERS 01 - 40)
   MASTER STYLESHEET
   ========================================================================== */

/* --------------------------------------------------------------------------
   1. Root Design Tokens & Variables
   -------------------------------------------------------------------------- */
:root {
  --navy-deep: #0f172a;
  --navy-mid: #1e293b;
  --navy-light: #334155;
  --blue-accent: #0284c7;
  --blue-light: #e0f2fe;
  --blue-dark: #0369a1;
  --emerald: #059669;
  --amber: #d97706;
  --rose: #e11d48;
  --purple: #8b5cf6;
  --cyan: #06b6d4;
  --js-yellow: #f7df1e;
  
  --bg-page: #f8fafc;
  --bg-card: #ffffff;
  --border-card: #e2e8f0;
  --text-main: #0f172a;
  --text-muted: #64748b;
  
  --font-code: 'Fira Code', monospace;
  --font-body: 'Hind Siliguri', 'Inter', sans-serif;
  --font-heading: 'Plus Jakarta Sans', sans-serif;
}

/* --------------------------------------------------------------------------
   2. Reset & Base Typography
   -------------------------------------------------------------------------- */
*, *::before, *::after {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
  -webkit-print-color-adjust: exact !important;
  print-color-adjust: exact !important;
}

html {
  scroll-behavior: smooth;
}

body {
  background-color: #0b0f19;
  font-family: var(--font-body);
  font-size: 11px;
  line-height: 1.55;
  color: var(--text-main);
  margin: 0;
  padding: 0;
}

/* --------------------------------------------------------------------------
   3. Top Reading Progress Bar
   -------------------------------------------------------------------------- */
.reading-progress-container {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 3px;
  background: rgba(255, 255, 255, 0.1);
  z-index: 100001;
}

.reading-progress-bar {
  height: 100%;
  width: 0%;
  background: linear-gradient(90deg, #f7df1e, #38bdf8);
  transition: width 0.1s ease-out;
}

/* --------------------------------------------------------------------------
   4. Sticky Omnibus Navigation Bar
   -------------------------------------------------------------------------- */
.omnibus-navbar {
  position: sticky;
  top: 0;
  z-index: 100000;
  background: rgba(15, 23, 42, 0.96);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  border-bottom: 1px solid rgba(255, 255, 255, 0.12);
  padding: 8px 18px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 15px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.5);
}

.omnibus-brand {
  display: flex;
  align-items: center;
  gap: 10px;
  color: #ffffff;
  font-family: var(--font-heading);
  font-size: 12.5px;
  font-weight: 800;
  letter-spacing: 0.5px;
  text-transform: uppercase;
  white-space: nowrap;
  text-decoration: none;
}

.omnibus-logo {
  background: var(--js-yellow);
  color: #000000;
  font-family: var(--font-heading);
  font-weight: 800;
  font-size: 12px;
  padding: 2px 7px;
  border-radius: 4px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
}

.omnibus-controls {
  display: flex;
  align-items: center;
  gap: 10px;
  flex-wrap: wrap;
}

.chapter-select {
  background: #1e293b;
  color: #f8fafc;
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 6px;
  padding: 6px 10px;
  font-size: 11.5px;
  font-family: var(--font-body);
  cursor: pointer;
  outline: none;
  max-width: 300px;
  transition: border-color 0.2s;
}

.chapter-select:focus {
  border-color: #38bdf8;
}

.search-wrapper {
  position: relative;
  display: flex;
  align-items: center;
}

.omnibus-search {
  background: #1e293b;
  color: #f8fafc;
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 6px;
  padding: 6px 28px 6px 10px;
  font-size: 11.5px;
  width: 170px;
  outline: none;
  transition: all 0.2s ease;
}

.omnibus-search:focus {
  border-color: #38bdf8;
  width: 230px;
  background: #0f172a;
}

.search-count {
  position: absolute;
  right: 8px;
  font-size: 9.5px;
  color: #94a3b8;
  pointer-events: none;
}

.omnibus-print-btn {
  background: var(--js-yellow);
  color: #000000;
  font-family: var(--font-heading);
  font-size: 11.5px;
  font-weight: 800;
  border: none;
  border-radius: 6px;
  padding: 6px 12px;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  gap: 5px;
  box-shadow: 0 2px 6px rgba(247, 223, 30, 0.3);
  white-space: nowrap;
  transition: all 0.15s ease;
}

.omnibus-print-btn:hover {
  background: #fde047;
  transform: translateY(-1px);
}

/* --------------------------------------------------------------------------
   5. Master Table of Contents (Cover Card & Grid)
   -------------------------------------------------------------------------- */
.master-toc-wrapper {
  max-width: 210mm;
  margin: 20px auto 30px auto;
  padding: 0 10px;
}

.master-toc-card {
  background: linear-gradient(135deg, #090d16 0%, #111c2e 100%);
  border: 1px solid #1e293b;
  border-radius: 12px;
  padding: 22px;
  color: #ffffff;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
}

.master-toc-header {
  text-align: center;
  margin-bottom: 18px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  padding-bottom: 14px;
}

.master-toc-title {
  font-family: var(--font-heading);
  font-size: 20px;
  font-weight: 800;
  color: #ffffff;
  letter-spacing: 0.5px;
  margin: 0 0 5px 0;
}

.master-toc-subtitle {
  font-size: 11.5px;
  color: #94a3b8;
  margin: 0;
}

.master-toc-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 7px;
}

@media (min-width: 850px) {
  .master-toc-grid {
    grid-template-columns: repeat(4, 1fr);
  }
}

.toc-item {
  background: rgba(30, 41, 59, 0.75);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 6px;
  padding: 7px 9px;
  text-decoration: none;
  color: #e2e8f0;
  font-size: 11px;
  display: flex;
  align-items: center;
  gap: 7px;
  transition: all 0.15s ease;
}

.toc-item:hover {
  background: rgba(56, 189, 248, 0.18);
  border-color: #38bdf8;
  color: #ffffff;
  transform: translateY(-1px);
}

.toc-ch-num {
  background: var(--js-yellow);
  color: #000000;
  font-weight: 800;
  font-family: var(--font-code);
  font-size: 9.5px;
  padding: 1px 5px;
  border-radius: 4px;
  white-space: nowrap;
}

.toc-ch-name {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  font-family: var(--font-heading);
  font-size: 10.5px;
}

/* --------------------------------------------------------------------------
   6. Chapter Containers & Navigation Anchors
   -------------------------------------------------------------------------- */
.chapter-wrapper {
  margin-bottom: 40px;
  position: relative;
}

.chapter-nav-anchor {
  display: flex;
  justify-content: flex-end;
  max-width: 210mm;
  margin: 0 auto 6px auto;
  padding: 0 10px;
}

.back-to-toc-link {
  color: #94a3b8;
  font-size: 10.5px;
  text-decoration: none;
  background: rgba(15, 23, 42, 0.85);
  padding: 3px 9px;
  border-radius: 4px;
  border: 1px solid rgba(255, 255, 255, 0.12);
  transition: all 0.15s ease;
}

.back-to-toc-link:hover {
  color: #38bdf8;
  border-color: #38bdf8;
}

/* --------------------------------------------------------------------------
   7. A4 Document Container (.doc-page)
   -------------------------------------------------------------------------- */
.doc-page {
  max-width: 210mm;
  margin: 0 auto;
  background: var(--bg-page);
  padding: 12mm 14mm;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.35);
  border-radius: 4px;
}

/* --------------------------------------------------------------------------
   8. Master Banners & Badges
   -------------------------------------------------------------------------- */
.master-banner {
  background: linear-gradient(135deg, #075985 0%, #0369a1 50%, #0284c7 100%);
  color: white;
  padding: 12px 18px;
  border-radius: 8px;
  margin-bottom: 8px;
  box-shadow: 0 4px 12px rgba(3, 105, 161, 0.2);
}

.banner-top {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 8px;
}

.banner-left {
  display: flex;
  align-items: center;
  gap: 10px;
}

.banner-icon {
  background: var(--js-yellow);
  color: #000000;
  font-family: var(--font-heading);
  font-weight: 800;
  font-size: 12px;
  padding: 2px 7px;
  border-radius: 4px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.25);
  display: inline-flex;
  align-items: center;
  justify-content: center;
}

.banner-title {
  font-family: var(--font-heading);
  font-size: 13.5px;
  font-weight: 800;
  letter-spacing: 0.5px;
  color: #ffffff;
  text-transform: uppercase;
}

.banner-sub {
  font-family: var(--font-heading);
  font-size: 11px;
  font-weight: 600;
  color: #e0f2fe;
}

.chapter-badge {
  background: var(--js-yellow);
  color: #000000;
  font-family: var(--font-heading);
  font-size: 12px;
  font-weight: 800;
  padding: 2px 8px;
  border-radius: 4px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
  letter-spacing: 0.5px;
  white-space: nowrap;
}

.meta-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 8px;
  background: rgba(15, 23, 42, 0.35);
  padding: 6px 10px;
  border-radius: 6px;
  border: 1px solid rgba(255, 255, 255, 0.12);
}

.meta-item {
  font-size: 8.5px;
}

.meta-label {
  color: #93c5fd;
  text-transform: uppercase;
  font-weight: 600;
  font-size: 7.5px;
  letter-spacing: 0.5px;
}

.meta-val {
  font-weight: 600;
  color: #ffffff;
}

/* --------------------------------------------------------------------------
   9. Chapter Opening Statement Cards & Roadmaps
   -------------------------------------------------------------------------- */
.opening-card {
  background: #f0f9ff;
  border: 1px solid #bae6fd;
  border-left: 3px solid var(--blue-accent);
  border-radius: 6px;
  padding: 8px 12px;
  margin-bottom: 8px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.03);
}

.opening-title {
  font-family: var(--font-heading);
  font-size: 11.5px;
  font-weight: 700;
  color: var(--blue-dark);
  margin-bottom: 4px;
  display: flex;
  align-items: center;
  gap: 6px;
}

.doc-statement {
  font-size: 10px;
  color: #334155;
  line-height: 1.5;
}

.roadmap-grid {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 4px;
  margin-top: 5px;
  padding-top: 5px;
  border-top: 1px dashed #bae6fd;
}

.roadmap-item {
  background: white;
  border: 1px solid #e0f2fe;
  border-radius: 4px;
  padding: 3px 5px;
  font-size: 8.5px;
  color: #0369a1;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 3px;
}

.goals-flex {
  display: flex;
  flex-wrap: wrap;
  gap: 5px;
  margin-top: 4px;
}

.goal-tag {
  background: #e0f2fe;
  color: #0369a1;
  font-size: 8.5px;
  padding: 2px 6px;
  border-radius: 3px;
  font-weight: 600;
}

/* --------------------------------------------------------------------------
   10. Part Banners
   -------------------------------------------------------------------------- */
.part-banner {
  background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
  color: #ffffff;
  font-family: var(--font-heading);
  font-size: 10px;
  font-weight: 700;
  letter-spacing: 0.6px;
  padding: 5px 10px;
  border-radius: 5px;
  margin: 8px 0 6px 0;
  border-left: 3px solid #38bdf8;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.08);
  page-break-after: avoid !important;
  break-after: avoid !important;
  page-break-inside: avoid !important;
  break-inside: avoid !important;
}

.sub-badge {
  background: #38bdf8;
  color: #0f172a;
  font-size: 8.5px;
  font-weight: 800;
  padding: 1px 5px;
  border-radius: 3px;
  margin-right: 5px;
}

/* --------------------------------------------------------------------------
   11. Study Cards & Headings
   -------------------------------------------------------------------------- */
.study-card {
  background: #ffffff;
  border: 1px solid var(--border-card);
  border-radius: 6px;
  padding: 8px 11px;
  margin-bottom: 7px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.03);
  page-break-inside: avoid !important;
  break-inside: avoid !important;
}

.card-title {
  font-family: var(--font-heading);
  font-size: 11px;
  font-weight: 700;
  color: var(--navy-deep);
  border-bottom: 1px solid #f1f5f9;
  padding-bottom: 4px;
  margin-bottom: 6px;
  display: flex;
  align-items: center;
  gap: 6px;
}

.badge-num {
  background: #e0f2fe;
  color: #0369a1;
  font-family: var(--font-code);
  font-weight: 700;
  font-size: 9px;
  padding: 1px 5px;
  border-radius: 3px;
  border: 1px solid #bae6fd;
}

.section-subhead {
  font-family: var(--font-heading);
  font-size: 10.5px;
  font-weight: 700;
  color: var(--blue-dark);
  margin: 6px 0 3px 0;
  display: flex;
  align-items: center;
  gap: 5px;
}

.text-p {
  margin-bottom: 5px;
  text-align: justify;
  color: #334155;
  font-size: 10.5px;
  line-height: 1.5;
}

.text-p strong {
  color: #0f172a;
  font-weight: 600;
}

.bullet-list, ul.clean-list {
  margin: 4px 0 6px 14px;
  color: #334155;
  font-size: 10px;
  line-height: 1.45;
}

.bullet-list li, ul.clean-list li {
  margin-bottom: 3px;
}

/* --------------------------------------------------------------------------
   12. Callout Boxes (Definition, Warning, Memory, Practice)
   -------------------------------------------------------------------------- */
.def-box {
  background: #f8fafc;
  border-left: 3px solid var(--blue-accent);
  padding: 5px 9px;
  border-radius: 0 4px 4px 0;
  margin: 4px 0 6px 0;
  font-size: 10px;
  color: #1e293b;
}

.def-box.bangla {
  border-left-color: #059669;
  background: #f0fdf4;
}

.def-box.english {
  border-left-color: #0284c7;
  background: #f0f9ff;
}

.def-text {
  font-size: 9.5px;
  line-height: 1.45;
}

.warn-box {
  background: #fffbeb;
  border-left: 3px solid var(--amber);
  padding: 5px 9px;
  border-radius: 0 4px 4px 0;
  margin: 4px 0 6px 0;
  font-size: 9.5px;
  color: #92400e;
}

.memory-box {
  background: #faf5ff;
  border-left: 3px solid var(--purple);
  padding: 5px 9px;
  border-radius: 0 4px 4px 0;
  margin: 4px 0 6px 0;
  font-size: 9.5px;
  color: #6b21a8;
}

.practice-item {
  background: #f8fafc;
  border: 1px dashed #cbd5e1;
  border-radius: 4px;
  padding: 5px 8px;
  margin: 4px 0;
  font-size: 9.5px;
}

/* --------------------------------------------------------------------------
   13. Code Blocks & Syntax Highlighting
   -------------------------------------------------------------------------- */
.code-box {
  background: #0f172a;
  border-radius: 6px;
  margin: 5px 0;
  overflow: hidden;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.15);
  border: 1px solid #1e293b;
  page-break-inside: avoid !important;
  break-inside: avoid !important;
}

.code-box-correct {
  border-left: 3px solid #10b981 !important;
}

.code-box-error {
  border-left: 3px solid #ef4444 !important;
}

.code-top {
  background: #1e293b;
  padding: 3px 8px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-family: var(--font-code);
  font-size: 8.5px;
  color: #94a3b8;
  border-bottom: 1px solid #334155;
}

.tag-label {
  font-weight: 700;
  font-size: 8px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.tag-label.green { color: #34d399; }
.tag-label.red { color: #f87171; }
.tag-label.cyan { color: #38bdf8; }
.tag-label.amber { color: #fbbf24; }
.tag-label.purple { color: #c084fc; }

pre {
  margin: 0;
  padding: 7px 10px;
  overflow-x: hidden !important;
  white-space: pre-wrap !important;
  word-break: break-word !important;
  font-family: var(--font-code) !important;
  font-size: 9.5px !important;
  line-height: 1.4 !important;
  color: #e2e8f0;
}

code {
  font-family: var(--font-code);
  font-size: 9.5px;
}

p code, li code {
  background: #f1f5f9;
  color: #0f172a;
  padding: 1px 4px;
  border-radius: 3px;
  border: 1px solid #e2e8f0;
  font-size: 9px;
}

/* Syntax Tokens */
.syn-kw { color: #f43f5e; font-weight: 600; }
.syn-fn { color: #38bdf8; font-weight: 600; }
.syn-str { color: #34d399; }
.syn-num { color: #fbbf24; }
.syn-com { color: #64748b; font-style: italic; }
.syn-bool { color: #c084fc; font-weight: 600; }
.syn-op { color: #38bdf8; }
.syn-regex { color: #f472b6; }
.syn-async { color: #a78bfa; font-weight: 600; }
.syn-class { color: #fb923c; font-weight: 600; }
.syn-priv { color: #e879f9; }
.syn-gen { color: #2dd4bf; }
.syn-proxy { color: #f43f5e; }
.syn-fp { color: #818cf8; }

.invalid-token {
  text-decoration: underline wavy #ef4444;
  color: #f87171 !important;
  font-weight: bold;
}

/* Output Console Box */
.output-box {
  background: #020617;
  border-radius: 5px;
  margin: 4px 0;
  border: 1px solid #1e293b;
  overflow: hidden;
}

.out-label {
  background: #0f172a;
  color: #94a3b8;
  font-family: var(--font-code);
  font-size: 8px;
  padding: 2px 6px;
  font-weight: 600;
  border-bottom: 1px solid #1e293b;
}

/* --------------------------------------------------------------------------
   14. ASCII Diagrams & Trees
   -------------------------------------------------------------------------- */
.ascii-tree-container {
  background: #090d16;
  border: 1px solid #1e293b;
  border-radius: 6px;
  margin: 5px 0;
  overflow: hidden;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.18);
  page-break-inside: avoid !important;
  break-inside: avoid !important;
}

.ascii-tree-header {
  background: #111c2e;
  color: #38bdf8;
  font-family: var(--font-code);
  font-size: 9px;
  font-weight: 700;
  padding: 4px 10px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  border-bottom: 1px solid #1e293b;
}

.ascii-tree-content {
  color: #e2e8f0 !important;
  font-family: var(--font-code) !important;
  font-size: 9px !important;
  line-height: 1.25 !important;
  padding: 6px 10px !important;
  background: transparent !important;
  border: none !important;
  white-space: pre !important;
  overflow-x: hidden !important;
  word-break: normal !important;
  margin: 0 !important;
}

/* --------------------------------------------------------------------------
   15. Master Tables & Checklists
   -------------------------------------------------------------------------- */
.table-container, .table-wrap {
  margin: 6px 0;
  border-radius: 6px;
  overflow: hidden;
  border: 1px solid #e2e8f0;
}

.master-table, table {
  width: 100%;
  border-collapse: collapse;
  font-size: 9.5px;
}

.master-table th, th, thead th {
  background: #1e293b;
  color: #f8fafc;
  font-weight: 700;
  padding: 5px 8px;
  text-align: left;
  border-bottom: 1px solid #334155;
}

.master-table td, td, tbody td {
  padding: 5px 8px;
  border-bottom: 1px solid #f1f5f9;
  color: #334155;
}

.master-table tr:nth-child(even), tr:nth-child(even), tbody tr:nth-child(even) {
  background: #f8fafc;
}

/* Checklists */
.checklist-container {
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 6px;
  padding: 8px 10px;
  margin: 5px 0;
}

.checklist-header {
  font-family: var(--font-heading);
  font-size: 10px;
  font-weight: 700;
  color: var(--navy-deep);
  margin-bottom: 6px;
}

.checklist-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 5px;
}

.check-item {
  display: flex;
  align-items: center;
  gap: 5px;
  font-size: 9.5px;
  color: #334155;
}

.check-box {
  color: #10b981;
  font-weight: 800;
}

.check-text {
  font-size: 9.5px;
}

/* --------------------------------------------------------------------------
   16. Floating Back to Top Button
   -------------------------------------------------------------------------- */
.floating-top-btn {
  position: fixed;
  bottom: 24px;
  right: 24px;
  width: 42px;
  height: 42px;
  border-radius: 50%;
  background: #0f172a;
  color: #f7df1e;
  border: 1px solid rgba(255, 255, 255, 0.2);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 18px;
  font-weight: bold;
  cursor: pointer;
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.4);
  opacity: 0;
  visibility: hidden;
  transition: all 0.25s ease;
  z-index: 99999;
}

.floating-top-btn.visible {
  opacity: 1;
  visibility: visible;
}

.floating-top-btn:hover {
  background: #f7df1e;
  color: #000000;
  transform: translateY(-3px);
}

/* Highlighted match during search */
.search-highlight {
  background-color: #fef08a !important;
  color: #000000 !important;
  padding: 1px 2px;
  border-radius: 2px;
}

/* --------------------------------------------------------------------------
   17. Strict Print Optimization Rules (A4 Strict & Unbroken)
   -------------------------------------------------------------------------- */
@page {
  size: A4;
  margin: 8mm 10mm;
}

@media print {
  body {
    background: #ffffff !important;
    font-size: 10px !important;
    color: #000000 !important;
  }
  
  .reading-progress-container,
  .omnibus-navbar,
  .master-toc-wrapper,
  .chapter-nav-anchor,
  .action-bar,
  .floating-top-btn {
    display: none !important;
  }
  
  .chapter-wrapper {
    margin-bottom: 0 !important;
    page-break-before: always !important;
    break-before: page !important;
  }
  
  .chapter-wrapper:first-of-type {
    page-break-before: avoid !important;
    break-before: avoid !important;
  }
  
  .doc-page {
    max-width: 100% !important;
    margin: 0 !important;
    padding: 0 !important;
    border: none !important;
    box-shadow: none !important;
  }
  
  .study-card {
    page-break-inside: avoid !important;
    break-inside: avoid !important;
    border: 1px solid #cbd5e1 !important;
  }
  
  .part-banner {
    page-break-after: avoid !important;
    break-after: avoid !important;
    page-break-inside: avoid !important;
    break-inside: avoid !important;
  }
  
  .code-box, pre, .ascii-tree-container, .table-container, .def-box, .output-box {
    page-break-inside: avoid !important;
    break-inside: avoid !important;
  }
}
"""

def get_app_js():
    return """/* ==========================================================================
   JAVASCRIPT MASTER STUDY DOCUMENTATION — COMPLETE BOOK (CHAPTERS 01 - 40)
   INTERACTIVE APP SCRIPT (js/app.js)
   ========================================================================== */

document.addEventListener('DOMContentLoaded', () => {
  initReadingProgressBar();
  initSearchFilter();
  initChapterJump();
  initScrollSpy();
  initBackToTop();
  initKeyboardShortcuts();
});

/* --------------------------------------------------------------------------
   1. Reading Progress Bar
   -------------------------------------------------------------------------- */
function initReadingProgressBar() {
  const progressBar = document.getElementById('readingProgressBar');
  if (!progressBar) return;

  window.addEventListener('scroll', () => {
    const scrollTop = window.scrollY || document.documentElement.scrollTop;
    const docHeight = document.documentElement.scrollHeight - window.innerHeight;
    const scrollPercent = docHeight > 0 ? (scrollTop / docHeight) * 100 : 0;
    progressBar.style.width = scrollPercent + '%';
  }, { passive: true });
}

/* --------------------------------------------------------------------------
   2. Real-Time Search & Card Filter
   -------------------------------------------------------------------------- */
let searchDebounceTimer = null;

function initSearchFilter() {
  const searchInput = document.getElementById('cardFilter');
  const searchCount = document.getElementById('searchCount');
  if (!searchInput) return;

  searchInput.addEventListener('input', () => {
    clearTimeout(searchDebounceTimer);
    searchDebounceTimer = setTimeout(() => {
      filterTopics(searchInput.value.trim().toLowerCase(), searchCount);
    }, 150);
  });
}

function filterTopics(query, countEl) {
  const cards = document.querySelectorAll('.study-card');
  const chapters = document.querySelectorAll('.chapter-wrapper');

  if (!query) {
    cards.forEach(card => {
      card.style.display = '';
    });
    chapters.forEach(ch => {
      ch.style.display = '';
    });
    if (countEl) countEl.textContent = '';
    return;
  }

  let matchCount = 0;

  cards.forEach(card => {
    const text = card.textContent.toLowerCase();
    if (text.includes(query)) {
      card.style.display = '';
      matchCount++;
    } else {
      card.style.display = 'none';
    }
  });

  // Hide chapters that have zero visible study cards during an active query
  chapters.forEach(ch => {
    const visibleCards = ch.querySelectorAll('.study-card:not([style*="display: none"])');
    if (visibleCards.length === 0) {
      ch.style.display = 'none';
    } else {
      ch.style.display = '';
    }
  });

  if (countEl) {
    countEl.textContent = `${matchCount} found`;
  }
}

/* --------------------------------------------------------------------------
   3. Chapter Quick Jump
   -------------------------------------------------------------------------- */
function initChapterJump() {
  const select = document.getElementById('chapterSelect');
  if (!select) return;

  select.addEventListener('change', (e) => {
    const targetId = e.target.value;
    if (!targetId) return;

    if (targetId === '#top') {
      window.scrollTo({ top: 0, behavior: 'smooth' });
      return;
    }

    const targetEl = document.querySelector(targetId);
    if (targetEl) {
      const navOffset = 60;
      const elPosition = targetEl.getBoundingClientRect().top + window.pageYOffset;
      window.scrollTo({
        top: elPosition - navOffset,
        behavior: 'smooth'
      });
    }
  });
}

/* --------------------------------------------------------------------------
   4. ScrollSpy: Update Active Chapter in Dropdown while Scrolling
   -------------------------------------------------------------------------- */
function initScrollSpy() {
  const select = document.getElementById('chapterSelect');
  const chapters = document.querySelectorAll('.chapter-wrapper');
  if (!select || chapters.length === 0) return;

  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const id = '#' + entry.target.id;
        if (select.value !== id) {
          select.value = id;
        }
      }
    });
  }, {
    rootMargin: '-20% 0px -70% 0px',
    threshold: 0
  });

  chapters.forEach(ch => observer.observe(ch));
}

/* --------------------------------------------------------------------------
   5. Back to Top Floating Button
   -------------------------------------------------------------------------- */
function initBackToTop() {
  const btn = document.getElementById('floatingTopBtn');
  if (!btn) return;

  window.addEventListener('scroll', () => {
    if (window.scrollY > 400) {
      btn.classList.add('visible');
    } else {
      btn.classList.remove('visible');
    }
  }, { passive: true });

  btn.addEventListener('click', () => {
    window.scrollTo({ top: 0, behavior: 'smooth' });
  });
}

/* --------------------------------------------------------------------------
   6. Keyboard Shortcuts: Ctrl+K or / to Focus Search, Esc to Clear
   -------------------------------------------------------------------------- */
function initKeyboardShortcuts() {
  const searchInput = document.getElementById('cardFilter');
  if (!searchInput) return;

  window.addEventListener('keydown', (e) => {
    if ((e.ctrlKey && e.key.toLowerCase() === 'k') || (e.key === '/' && document.activeElement !== searchInput)) {
      e.preventDefault();
      searchInput.focus();
      searchInput.select();
    } else if (e.key === 'Escape' && document.activeElement === searchInput) {
      searchInput.value = '';
      searchInput.blur();
      filterTopics('', document.getElementById('searchCount'));
    }
  });
}
"""

def build_full_book():
    src_dir = 'JavaScript/Code'
    full_book_dir = 'JavaScript/Full-Book'
    css_dir = os.path.join(full_book_dir, 'css')
    js_dir = os.path.join(full_book_dir, 'js')
    
    os.makedirs(css_dir, exist_ok=True)
    os.makedirs(js_dir, exist_ok=True)
    
    # 1. Write css/style.css
    css_path = os.path.join(css_dir, 'style.css')
    with open(css_path, 'w', encoding='utf-8') as f:
        f.write(get_master_css())
    print(f"[CSS] Generated {css_path} ({len(get_master_css())} bytes)")

    # 2. Write js/app.js
    js_path = os.path.join(js_dir, 'app.js')
    with open(js_path, 'w', encoding='utf-8') as f:
        f.write(get_app_js())
    print(f"[JS] Generated {js_path} ({len(get_app_js())} bytes)")

    # 3. Read and parse all 40 chapters
    files = sorted(glob.glob(f'{src_dir}/Chapter-*.html'))
    print(f"[CH] Found {len(files)} chapters to assemble.")
    assert len(files) == 40, f"Expected 40 chapters, found {len(files)}"

    chapters_data = []
    
    for f in files:
        num_m = re.search(r'Chapter-(\d+)-', f)
        ch_num = int(num_m.group(1))
        
        with open(f, 'r', encoding='utf-8') as fp:
            content = fp.read()
            
        m_title = re.search(r'class="banner-title">\s*(.*?)\s*</span>', content)
        title_text = m_title.group(1).strip() if m_title else f"Chapter {ch_num:02d}"
        
        m_badge = re.search(r'class="chapter-badge">\s*(.*?)\s*</span>', content)
        badge_text = m_badge.group(1).strip() if m_badge else f"Chapter {ch_num:02d}"
        
        m_doc = re.search(r'<div class="doc-page">\n?(.*?)\n?</div>\s*(?:<!--.*?-->\s*)*</body>', content, re.DOTALL)
        assert m_doc is not None, f"doc-page not found in {f}"
        doc_inner = m_doc.group(1).rstrip()
        
        chapters_data.append({
            'num': ch_num,
            'id': f"ch-{ch_num:02d}",
            'badge': badge_text,
            'title': title_text,
            'content': doc_inner
        })
        print(f"Processed Chapter {ch_num:02d}: {badge_text} - {title_text[:40]}")

    # 4. Generate Chapter Select Options & Master TOC Grid
    select_options = []
    toc_grid_items = []
    
    for ch in chapters_data:
        opt = f'        <option value="#{ch["id"]}">{ch["badge"]}: {ch["title"]}</option>'
        select_options.append(opt)
        
        grid_item = f'''        <a href="#{ch["id"]}" class="toc-item">
          <span class="toc-ch-num">{ch["num"]:02d}</span>
          <span class="toc-ch-name">{ch["title"]}</span>
        </a>'''
        toc_grid_items.append(grid_item)

    options_html = "\n".join(select_options)
    toc_grid_html = "\n".join(toc_grid_items)

    # 5. Build Chapters Section HTML
    chapters_html_list = []
    for ch in chapters_data:
        ch_section = f'''  <!-- CHAPTER {ch["num"]:02d} SECTION -->
  <section id="{ch["id"]}" class="chapter-wrapper">
    <div class="chapter-nav-anchor">
      <a href="#top" class="back-to-toc-link">↑ Back to Table of Contents</a>
    </div>
    <div class="doc-page">
      {ch["content"]}
    </div>
  </section>'''
        chapters_html_list.append(ch_section)

    all_chapters_html = "\n\n".join(chapters_html_list)

    # 6. Assemble Full Book index.html
    index_html = f'''<!DOCTYPE html>
<html lang="bn">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>JavaScript Master Study Documentation — Complete Book (Chapters 01 – 40)</title>
  
  <!-- Google Fonts -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Fira+Code:wght@400;500;600;700&family=Hind+Siliguri:wght@400;500;600;700&family=Inter:wght@400;500;600;700;800&family=Plus+Jakarta+Sans:wght@500;600;700;800&display=swap" rel="stylesheet">
  
  <!-- Modular Stylesheet -->
  <link rel="stylesheet" href="css/style.css">
</head>
<body id="top">

  <!-- Top Reading Progress Bar -->
  <div class="reading-progress-container">
    <div class="reading-progress-bar" id="readingProgressBar"></div>
  </div>

  <!-- Sticky Omnibus Navigation Bar -->
  <nav class="omnibus-navbar">
    <a href="#top" class="omnibus-brand">
      <span class="omnibus-logo">JS</span>
      <span>Master Study Documentation — Complete Book</span>
    </a>
    
    <div class="omnibus-controls">
      <select id="chapterSelect" class="chapter-select" aria-label="Jump to Chapter">
        <option value="#top">📑 Jump to Chapter (01 – 40)...</option>
{options_html}
      </select>
      
      <div class="search-wrapper">
        <input type="text" id="cardFilter" class="omnibus-search" placeholder="🔍 Search topics (Ctrl+K)..." autocomplete="off">
        <span id="searchCount" class="search-count"></span>
      </div>
      
      <button class="omnibus-print-btn" onclick="window.print()">
        <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="6 9 6 2 18 2 18 9"></polyline><path d="M6 18H4a2 2 0 0 1-2-2v-5a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2v5a2 2 0 0 1-2 2h-2"></path><rect x="6" y="14" width="12" height="8"></rect></svg>
        Print Book / PDF
      </button>
    </div>
  </nav>

  <!-- Master Table of Contents (Cover & Jump Grid) -->
  <div class="master-toc-wrapper">
    <div class="master-toc-card">
      <div class="master-toc-header">
        <h1 class="master-toc-title">📘 JAVASCRIPT COMPLETE MASTER BOOK</h1>
        <p class="master-toc-subtitle">Chapters 01 – 40 • 2,640 Modules &amp; Labs • Complete Full-Stack Engineering Curriculum</p>
      </div>
      
      <div class="master-toc-grid">
{toc_grid_html}
      </div>
    </div>
  </div>

  <!-- All 40 Chapters Content -->
{all_chapters_html}

  <!-- Floating Back to Top Button -->
  <button id="floatingTopBtn" class="floating-top-btn" title="Back to Top">↑</button>

  <!-- Modular Interactive Script -->
  <script src="js/app.js"></script>

</body>
</html>
'''

    index_path = os.path.join(full_book_dir, 'index.html')
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(index_html)
    print(f"[HTML] Generated {index_path} ({len(index_html)} bytes)")

    # 7. Mirror to root Full-Book/ folder
    root_full_book = 'Full-Book'
    if os.path.exists(root_full_book):
        shutil.rmtree(root_full_book)
    shutil.copytree(full_book_dir, root_full_book)
    print(f"[MIRROR] Mirrored to root {root_full_book}/ folder.")

    # 8. Dual-Sync to Secondary Repo: e:/Git All Repo/Note-Book/
    sec_repo = 'e:/Git All Repo/Note-Book'
    if os.path.exists(sec_repo):
        sec_js_fb = os.path.join(sec_repo, 'JavaScript', 'Full-Book')
        sec_root_fb = os.path.join(sec_repo, 'Full-Book')
        
        if os.path.exists(sec_js_fb):
            shutil.rmtree(sec_js_fb)
        shutil.copytree(full_book_dir, sec_js_fb)
        
        if os.path.exists(sec_root_fb):
            shutil.rmtree(sec_root_fb)
        shutil.copytree(full_book_dir, sec_root_fb)
        print(f"[DUAL-SYNC] Successfully synced to {sec_js_fb} and {sec_root_fb}")

    print("\n✅ Full-Book successfully generated and structured into HTML, CSS, and JS!")

if __name__ == '__main__':
    build_full_book()
