# 🌌 Dark Developer / Obsidian Cyber Edition Theme (Preset)

এই কালার প্যালেটটি আধুনিক ডার্ক-মোড, ডেভেলপার আইডিই (IDE) এবং সাইবার নান্দনিকতার জন্য তৈরি করা হয়েছে। পরবর্তীতে ডার্ক এডিশন বই, ওয়েবসাইট বা স্পেশাল চ্যাপ্টারে ব্যবহারের জন্য নিচে সম্পূর্ণ CSS ভেরিয়েবল, কালার কোড এবং কম্পোনেন্ট স্টাইলিং সংরক্ষণ করা হলো।

---

## 🎨 1. Core Color Variables (CSS Root Tokens)

```css
:root {
    /* Page & Surfaces */
    --bg-body: #0a0d14;            /* Deep Obsidian Slate (পৃষ্ঠার মূল ব্যাকগ্রাউন্ড) */
    --bg-card: #111722;            /* Dark Sapphire Slate (স্টাডি কার্ডের ব্যাকগ্রাউন্ড) */
    --bg-card-hover: #151d2c;      /* কার্ড হোভার এফেক্ট */
    --border-card: #1f293d;        /* কার্ডের চারপাশের সূক্ষ্ম বর্ডার */
    --border-focus: #38bdf8;       /* ফোকাস ও অ্যাক্টিভ বর্ডার */

    /* Typography & Text */
    --text-main: #e2e8f0;          /* মূল টেক্সট (উজ্জ্বল ও পড়ার জন্য আরামদায়ক) */
    --text-muted: #94a3b8;         /* সেকেন্ডারি বা সাব-টেক্সট */
    --text-dim: #64748b;           /* ফুটার ও মেটাডাটা টেক্সট */
    --text-heading: #f8fafc;       /* প্রধান শিরোনাম */

    /* Brand Accents */
    --accent-blue: #38bdf8;        /* স্কাই ব্লু (সাব-হেডিং, লিঙ্ক) */
    --accent-purple: #c084fc;      /* পার্পল (পার্ট ব্যানার ও স্পেশাল হাইলাইট) */
    --accent-emerald: #34d399;     /* এমারেল্ড গ্রিন (সফলতা, ভ্যালিড কোড) */
    --accent-amber: #fbbf24;       /* অ্যাম্বার গোল্ড (সতর্কতা, ইন্টারমিডিয়েট ব্যাজ) */
    --accent-rose: #f43f5e;        /* রোজ রেড (ভুল কোড, এরর, ক্রিটিক্যাল নোট) */

    /* Code Terminal & Editors */
    --code-bg: #070a0f;            /* ডিপ টার্মিনাল ব্ল্যাক */
    --code-header: #0d121c;        /* টার্মিনাল বার হেডার */
    --code-border: #1e293b;        /* কোড ব্লকের বর্ডার */
}
```

---

## 🖥️ 2. Syntax Highlighting Token Colors

কোড ব্লকের প্রতিটি টোকেনের সুনির্দিষ্ট কালার কোড:

| টোকেন টাইপ | কালার কোড | নমুনা ও ব্যবহার |
| :--- | :--- | :--- |
| **Keywords** | `#ff7b72` | `class`, `extends`, `const`, `function`, `return`, `super` |
| **Class Names** | `#ffa657` | `Student`, `BankAccount`, `Product`, `Order` |
| **Private Fields (`#`)** | `#f0883e` | `#password`, `#balance` |
| **Functions / Methods** | `#7ee787` | `showInfo()`, `deposit()`, `calculateTotal()` |
| **Strings (Single/Double/Tmpl)** | `#a5d6a7` | `"Toyota"`, `'Shariar'`, `` `Total: ${sum}` `` |
| **Numbers & Booleans** | `#79c0ff` | `1024`, `3.14`, `true`, `false`, `null` |
| **Built-in Objects** | `#d2a8ff` | `console`, `Math`, `Object`, `Array`, `Promise` |
| **Comments** | `#94a3b8` (italic) | `// This is an inline comment` |
| **❌ Invalid Token Highlight** | `#fca5a5` + Red Wavy | `text-decoration: underline wavy #ef4444; background: rgba(239, 68, 68, 0.18);` |

---

## 📦 3. UI Component Styles

### A. Master Banner (হিরো হেডার)
```css
.master-banner {
    background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 50%, #0f172a 100%);
    border: 1px solid #312e81;
    border-radius: 12px;
    padding: 14px 20px;
    box-shadow: 0 6px 20px -4px rgba(0, 0, 0, 0.5);
}
.banner-logo {
    background: #f7df1e;
    color: #000000;
    font-weight: 800;
    border-radius: 8px;
}
```

### B. Part Banner (পার্ট রিবন)
```css
.part-banner {
    background: linear-gradient(90deg, #1e1b4b 0%, #0f172a 100%);
    border-left: 4px solid #c084fc;
    border-radius: 8px;
    padding: 9px 15px;
    color: #f1f5f9;
    font-weight: 700;
}
```

### C. Study Card (স্টাডি কার্ড)
```css
.study-card {
    background: #111722;
    border: 1px solid #1f293d;
    border-radius: 10px;
    padding: 14px 18px;
    box-shadow: 0 3px 10px rgba(0, 0, 0, 0.25);
    page-break-inside: avoid !important;
}
```

### D. ASCII Concept Map Container
```css
.ascii-tree-container {
    background: #090e17;
    border: 1px solid #1e293b;
    border-left: 3px solid #38bdf8;
    border-radius: 8px;
    color: #38bdf8;
    font-family: 'Fira Code', monospace;
}
```

### E. Console Output Box
```css
.output-box {
    background: #070a0e;
    border: 1px solid #1f2937;
    border-left: 3px solid #22c55e;
    border-radius: 8px;
}
.output-header {
    background: #0b111a;
    color: #86efac;
}
```

---

## 💡 4. যখন এই থিমটি ব্যবহার করা যাবে:
1. **Developer Edition / Night Mode Edition** হিসেবে কোনো চ্যাপ্টার বা পুরো বই পাবলিশ করার সময়।
2. **ড্যাশবোর্ড, ওয়েবহুক বা অনলাইন ডকুমেন্টেশন সাইট** তৈরির সময়।
3. **প্রেজেন্টেশন বা স্ক্রিন রিডিং**-এর সময় যেখানে ডার্ক ব্যাকগ্রাউন্ড চোখে কম চাপ ফেলে।
