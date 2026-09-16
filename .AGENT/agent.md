# 📘 JavaScript Master Study Documentation — Production & PDF Generation Rulebook

> **File:** `.AGENT/agent.md`  
> **Purpose:** এই ফাইলটিতে Note-Book প্রজেক্টের প্রতিটি চ্যাপ্টারের Markdown থেকে প্রফেশনাল HTML এবং প্রিন্ট-রেডি PDF তৈরির শতভাগ প্রমাণিত নিয়মাবলী, সিএসএস আর্কিটেকচার, লেআউট স্ট্যান্ডার্ড এবং ভেরিফিকেশন প্রসেস বিস্তারিতভাবে লিপিবদ্ধ করা হলো। পরবর্তী সব চ্যাপ্টার তৈরির সময় এই নির্দেশিকা বাধ্যতামূলকভাবে অনুসরণ করতে হবে।

---

## 🎯 ১. গোল্ডেন রুলস ও জিরো-স্কিপিং নীতি (Zero-Skipping Policy)

1. **১০০% কনটেন্ট অখণ্ডতা:**
   - মূল `temp/ch-*.md` ফাইলের কোনো একটি শব্দ, নম্বরযুক্ত সেকশন, কোড ব্লক, আউটপুট, বাংলা/ইংরেজি সংজ্ঞা, টেবিল, সতর্কতা বা প্র্যাকটিস প্রশ্ন **কখনো সামারাইজ, শর্টকাট বা বাদ দেওয়া যাবে না**।
   - সব সেকশন (যেমন: 1 থেকে N পর্যন্ত), `🧠 Core Concepts / Must Remember`, `🧪 Practice Problems`, `🎯 Mini Project`, `📌 Final Mental Map` এবং `Next Chapter Preview` সম্পূর্ণ উপস্থিত থাকতে হবে।
2. **ভাষা ও টোন:**
   - মূল ফাইলের সহজ বাংলা ও ইংরেজির মিশ্রণ (Benglish/Bangla tech explanation) অবিকৃত রাখতে হবে।

---

## 📄 ২. পেজ ১-এর লেআউট স্ট্যান্ডার্ড (Page 1 Balance)

- **প্রথম পেজে কোনো বিশ্রী খালি জায়গা রাখা যাবে না:**
  - `Master Banner` (নীল গ্র্যাডিয়েন্ট হেডার ও মেটাডাটা গ্রিড)
  - `Opening Statement Card` (চ্যাপ্টারের ভূমিকা)
  - `Part 01 Banner`
  - `Section 1 Card` (প্রথম টপিকের পূর্ণাঙ্গ কার্ড)
- এই চারটি উপাদান যেন পেজ ১-এই সম্পূর্ণ অক্ষত অবস্থায় চমৎকারভাবে ফিট হয়। এর জন্য ব্যানারের প্যাডিং এবং কার্ডের মার্জিন কম্প্যাক্ট রাখতে হবে।
- সেকশন ২ পরিষ্কারভাবে পেজ ২ থেকে শুরু হবে।

---

## ✂️ ৩. কার্ড পেজ-ব্রেক প্রতিরোধ (Zero Mid-Card Page Splits)

- **সবচেয়ে গুরুত্বপূর্ণ নিয়ম:** কোনো কার্ড, কোড ব্লক বা টেবিল পেজের সীমানায় মাঝখান দিয়ে দ্বিখণ্ডিত হওয়া কঠোরভাবে নিষিদ্ধ।
- প্রিন্ট সিএসএস-এ নিচের ক্লাসগুলোতে অবশ্যই `page-break-inside: avoid !important; break-inside: avoid !important;` থাকতে হবে:
  ```css
  .study-card,
  .practice-item,
  .code-box,
  pre,
  .ascii-tree-container,
  .table-wrap,
  .def-box,
  .memory-box,
  .warn-box {
    page-break-inside: avoid !important;
    break-inside: avoid !important;
  }

  .part-banner {
    page-break-after: avoid !important;
    break-after: avoid !important;
  }
  ```

---

## 📐 ৪. সুষম পেজ মার্জিন ও প্যাডিং আর্কিটেকচার

- ব্রাউজার ডিফল্ট মার্জিনের উপর বাড়তি প্যাডিং যোগ হলে চারপাশে বিশাল সাদা ফাঁকা জায়গা তৈরি হয়।
- তাই নিচের মার্জিন স্ট্যান্ডার্ড কঠোরভাবে প্রযোজ্য:

```css
@page {
  size: A4;
  margin: 8mm 10mm; /* Top/Bottom: 8mm, Left/Right: 10mm */
}

@media print {
  body {
    background: white;
    font-size: 11px;
    color: #0f172a;
  }
  .action-bar {
    display: none !important;
  }
  .doc-page {
    max-width: 100% !important;
    margin: 0 !important;
    padding: 0 !important;
    border: none !important;
    box-shadow: none !important;
  }
}
```

---

## 💻 ৫. কোড বক্স, কমেন্ট ও ডায়াগ্রাম রেন্ডারিং সতর্কতা

1. **কোনো হরাইজন্টাল স্ক্রলবার বা ওভারফ্লো থাকবে না:**
   - কোডের ভেতরে অতিরিক্ত দীর্ঘ কমেন্ট (যেমন বাংলা ব্যাখ্যা বা ত্রুটির মেসেজ) এক লাইনে না লিখে একাধিক লাইনে ভাগ করতে হবে:
     ```javascript
     // ❌ ভুল: এক লাইনে অনেক বড় কমেন্ট যা স্ক্রলবার তৈরি করে
     // user = {}; // TypeError: Assignment to constant variable! (নতুন অবজেক্টে reassign নিষিদ্ধ)

     // ✅ সঠিক: ক্লিন মাল্টি-লাইন কমেন্ট
     // user = {};
     // ❌ TypeError: Assignment to constant variable!
     // (নতুন অবজেক্টে reassign নিষিদ্ধ)
     ```
   - সিএসএস-এ নিশ্চিত করতে হবে:
     ```css
     pre {
       overflow-x: hidden !important;
       white-space: pre-wrap !important;
       word-break: break-word !important;
     }
     ```

2. **ডায়াগ্রামে ব্যাকস্ল্যাশ (`\`) প্রটেকশন:**
   - ASCII আর্ট বা ট্রি ডায়াগ্রামে ব্যাকস্ল্যাশ (`\`) ব্যবহারের সময় সতর্ক থাকতে হবে যাতে পাইথন স্ক্রিপ্ট বা রেজেক্স রিপ্লেসমেন্টে `\` চরিত্রটি হারিয়ে না যায়।
   - সম্ভব হলে বক্স-ড্রয়িং ক্যারেক্টার (`┌ ─ ┬ ┐ │ └ ┴ ┘ ├ ┤ ▼`) ব্যবহার করতে হবে, যা দেখতে দৃষ্টিনন্দন এবং কখনো ভাঙে না।

3. **নো লিটারেল এস্কেপস (`\n` বা `\"`):**
   - স্ক্রিপ্টের মাধ্যমে HTML জেনারেট করার সময় কোনো আক্ষরিক `\n` বা `\"` যেন ডকুমেন্টে না বসে। সবসময় প্রকৃত নিউলাইন ও কোটস থাকবে।

---

## 🎨 ৬. কালার প্যালেট ও কম্পোনেন্ট গাইড

- **Master Banner:** `linear-gradient(135deg, #0b2545 0%, #0d3b66 55%, #0284c7 100%)`
- **Part Banner:** `background: #e0f2fe; border-left: 4px solid #0284c7; color: #0369a1;`
- **English Def Box:** `background: #f0f9ff; border-left: 3px solid #0284c7; color: #0c4a6e;`
- **Bangla Def Box:** `background: #faf5ff; border-left: 3px solid #9333ea; color: #581c87;`
- **Memory Box (Tips):** `background: #fefce8; border-left: 4px solid #eab308; color: #713f12;`
- **Warn Box (Gotchas):** `background: #fef2f2; border-left: 4px solid #ef4444; color: #7f1d1d;`
- **Mini Project Card:** `background: #f0fdf4; border-left: 4px solid #10b981;`
- **Practice Box:** `background: #f8fafc; border-left: 3px solid #0284c7; border-radius: 4px;`
- **Code Syntax Colors:**
  - Keywords: `#f43f5e`
  - Variables/Functions: `#38bdf8`
  - Strings: `#34d399`
  - Numbers: `#fbbf24`
  - Comments: `#64748b` (italic)
  - Booleans: `#f59e0b`

---

## ⚙️ ৭. PDF কম্পাইলেশন কমান্ড (Headless Chrome)

PowerShell-এ হেডলেস ক্রোমের মাধ্যমে নির্ভুল A4 ভেক্টরাইজড PDF কম্পাইল করার স্ট্যান্ডার্ড কমান্ড:

```powershell
Start-Process -FilePath "C:\Program Files\Google\Chrome\Application\chrome.exe" -ArgumentList "--headless=new --disable-gpu --no-pdf-header-footer --print-to-pdf=`"C:\Users\User\Desktop\Note-Book\PDF\<Chapter-Name>.pdf`" `"C:\Users\User\Desktop\Note-Book\Code\<Chapter-Name>.html`"" -Wait -PassThru
```

---

## 🔍 ৮. ভেরিফিকেশন ও কোয়ালিটি চেকলিস্ট

প্রতিটি চ্যাপ্টারের কাজ শেষে নিচের চেকলিস্ট সম্পূর্ণ পূরণ করতে হবে:
1. **সেকশন কাউন্ট অডিট:** `ch-*.md`-এর সবকটি নম্বরযুক্ত সেকশন HTML-এ আছে কি না স্ক্রিপ্ট দিয়ে নিশ্চিত করা।
2. **পেজ ১ চেক:** পেজ ১-এ ব্যানার ও সেকশন ১ অক্ষতভাবে ফিট হয়েছে কি না দেখা।
3. **পেজ ব্রেক স্ক্রিনিং:** PyMuPDF দিয়ে প্রতিটি পেজের শীর্ষ এবং পাদদেশ স্ক্যান করে নিশ্চিত করা যে কোনো কার্ড মাঝখান থেকে কাটা পড়েনি।
4. **টেম্প ইমেজ ক্লিনআপ ডিসিপ্লিন:** চেকিংয়ের জন্য ব্যবহৃত সবকটি সাময়িক ইমেজ ফাইল (`temp/*.png`) কাজ শেষ হওয়ামাত্র মুছে ফেলা:
   ```powershell
   Remove-Item -Path "c:\Users\User\Desktop\Note-Book\temp\*.png" -Force
   ```
