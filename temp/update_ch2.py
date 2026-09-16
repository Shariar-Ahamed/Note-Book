import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open(r'c:\Users\User\Desktop\Note-Book\Code\Chapter-02-Variables-DataTypes-TypeSystem.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Update CSS: Add @page and upgrade @media print to match proven Chapter 1 rules
old_print_css = """    @media print {
      body { background: white; font-size: 11.5px; }
      .action-bar { display: none !important; }
      .doc-page { max-width: 100% !important; margin: 0 !important; padding: 14mm 16mm !important; border: none !important; box-shadow: none !important; }
      .study-card { page-break-inside: avoid; break-inside: avoid; border: 1px solid #cbd5e1; }
      .part-banner { page-break-after: avoid; break-after: avoid; }
      .code-box, pre, .ascii-tree-container { page-break-inside: avoid; break-inside: avoid; }
    }"""

new_print_css = """    @page {
      size: A4;
      margin: 8mm 10mm;
    }

    @media print {
      body {
        background: white;
        font-size: 11px;
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
      .study-card {
        page-break-inside: avoid !important;
        break-inside: avoid !important;
        border: 1px solid #cbd5e1;
      }
      .part-banner {
        page-break-after: avoid;
        break-after: avoid;
      }
      .code-box, pre, .ascii-tree-container, .table-wrap, .def-box, .memory-box, .warn-box {
        page-break-inside: avoid;
        break-inside: avoid;
      }
      pre {
        overflow-x: hidden !important;
        white-space: pre-wrap !important;
        word-break: break-word !important;
      }
    }"""

if old_print_css in html:
    html = html.replace(old_print_css, new_print_css)
    print("Print CSS updated successfully!")
else:
    print("Could not find old print CSS exactly, trying regex...")
    html = re.sub(r'@media print\s*\{.*?\}\s*\}', new_print_css.strip(), html, flags=re.DOTALL)
    print("Replaced print CSS via regex.")

# 2. Section 27: Add Symbol uniqueness formula
old_sec27 = """    <!-- 27 -->
    <div class="study-card">
      <div class="card-title"><span class="badge-num">27</span> Symbols are Unique</div>
      <div class="code-box">
        <div class="code-top"><span>JavaScript</span><span>Symbol Uniqueness</span></div>
        <pre><span class="syn-kw">const</span> a = Symbol(<span class="syn-str">"id"</span>);
<span class="syn-kw">const</span> b = Symbol(<span class="syn-str">"id"</span>);

console.log(a === b); <span class="syn-com">// false (প্রতিটি Symbol সম্পূর্ণ ইউনিক!)</span></pre>
      </div>
      <p class="text-p">যদিও description একই (<code>"id"</code>), তবুও মেমোরিতে দুটো প্রতীক সম্পূর্ণ স্বতন্ত্র ও গোপন।</p>
    </div>"""

new_sec27 = """    <!-- 27 -->
    <div class="study-card">
      <div class="card-title"><span class="badge-num">27</span> Symbols are Unique</div>
      <div class="code-box">
        <div class="code-top"><span>JavaScript</span><span>Symbol Uniqueness</span></div>
        <pre><span class="syn-kw">const</span> a = Symbol(<span class="syn-str">"id"</span>);
<span class="syn-kw">const</span> b = Symbol(<span class="syn-str">"id"</span>);

console.log(a === b);</pre>
      </div>
      <span class="tag-label amber">Output</span>
      <div class="output-box">false</div>
      <p class="text-p">যদিও description একই (<code>"id"</code>), তবুও দুটো Symbol আলাদা।</p>
      <div class="memory-box">
        <strong>সহজভাবে:</strong> <code>Symbol("id") ≠ Symbol("id")</code> (দুটো Symbol সম্পূর্ণ স্বতন্ত্র। এটা advanced JavaScript-এ অবজেক্ট প্রোপার্টি লুকিয়ে রাখতে কাজে লাগে)।
      </div>
    </div>"""

if old_sec27 in html:
    html = html.replace(old_sec27, new_sec27)
    print("Section 27 updated!")
else:
    print("Section 27 old content mismatch!")

# 3. Section 30: Explicit Index Diagram
old_sec30 = """    <!-- 30 -->
    <div class="study-card">
      <div class="card-title"><span class="badge-num">30</span> Array</div>
      <p class="text-p">Array হলো একাধিক মান সুশৃঙ্খলভাবে (Ordered collection) ইনডেক্স আকারে রাখার কাঠামো:</p>
      <div class="code-box">
        <div class="code-top"><span>JavaScript</span><span>Array</span></div>
        <pre><span class="syn-kw">const</span> fruits = [<span class="syn-str">"Apple"</span>, <span class="syn-str">"Mango"</span>, <span class="syn-str">"Banana"</span>];
console.log(fruits);</pre>
      </div>
      <span class="tag-label amber">Output</span>
      <div class="output-box">["Apple", "Mango", "Banana"] (Index: 0: Apple, 1: Mango, 2: Banana)</div>
    </div>"""

new_sec30 = """    <!-- 30 -->
    <div class="study-card">
      <div class="card-title"><span class="badge-num">30</span> Array</div>
      <p class="text-p">Array হলো একাধিক value ordered collection হিসেবে রাখার জন্য ব্যবহৃত structure। প্রতিটি element-এর শূন্যভিত্তিক index থাকে:</p>
      <div class="code-box">
        <div class="code-top"><span>JavaScript</span><span>Array Structure</span></div>
        <pre><span class="syn-kw">const</span> fruits = [<span class="syn-str">"Apple"</span>, <span class="syn-str">"Mango"</span>, <span class="syn-str">"Banana"</span>];
console.log(fruits);</pre>
      </div>
      <span class="tag-label amber">Output</span>
      <div class="output-box">["Apple", "Mango", "Banana"]</div>
      <div class="ascii-tree-container">Array Element Index Mapping:
Apple   → 0
Mango   → 1
Banana  → 2</div>
    </div>"""

if old_sec30 in html:
    html = html.replace(old_sec30, new_sec30)
    print("Section 30 updated!")
else:
    print("Section 30 old content mismatch!")

# 4. Section 44: Clean comment line wraps
old_sec44 = """    <!-- 44 -->
    <div class="study-card">
      <div class="card-title"><span class="badge-num">44</span> `+` Operator-এর Interesting Behavior</div>
      <div class="code-box">
        <div class="code-top"><span>JavaScript</span><span>Coercion Contrast</span></div>
        <pre>console.log(<span class="syn-str">"10"</span> + <span class="syn-num">5</span>); <span class="syn-com">// 105 (+ স্ট্রিং কনক্যাট করে)</span>
console.log(<span class="syn-str">"10"</span> - <span class="syn-num">5</span>); <span class="syn-com">// 5 (- কেবল পাটিগণিত করে, তাই "10" কে সংখ্যা বানিয়ে নেয়)</span></pre>
      </div>
      <span class="tag-label amber">Output</span>
      <div class="output-box">105<br>5</div>
    </div>"""

new_sec44 = """    <!-- 44 -->
    <div class="study-card">
      <div class="card-title"><span class="badge-num">44</span> `+` Operator-এর Interesting Behavior</div>
      <div class="code-box">
        <div class="code-top"><span>JavaScript</span><span>Coercion Contrast</span></div>
        <pre><span class="syn-com">// + অপারেটর স্ট্রিং পেলে কনক্যাট (যোগ) করে:</span>
console.log(<span class="syn-str">"10"</span> + <span class="syn-num">5</span>); <span class="syn-com">// "105"</span>

<span class="syn-com">// - অপারেটর কেবল সংখ্যা বোঝে, তাই "10"-কে Number বানিয়ে বিয়োগ করে:</span>
console.log(<span class="syn-str">"10"</span> - <span class="syn-num">5</span>); <span class="syn-com">// 5</span></pre>
      </div>
      <span class="tag-label amber">Output</span>
      <div class="output-box">105<br>5</div>
    </div>"""

if old_sec44 in html:
    html = html.replace(old_sec44, new_sec44)
    print("Section 44 updated!")
else:
    print("Section 44 old content mismatch!")

# 5. Section 46: Clean explicit vs implicit blocks
old_sec46 = """    <!-- 46 -->
    <div class="study-card">
      <div class="card-title"><span class="badge-num">46</span> Explicit vs Implicit Conversion</div>
      <div class="code-box">
        <div class="code-top"><span>JavaScript</span><span>Explicit vs Implicit</span></div>
        <pre><span class="syn-kw">const</span> explicitAge = Number(<span class="syn-str">"22"</span>); <span class="syn-com">// Developer নিজে রূপান্তর করছে</span>
console.log(<span class="syn-str">"22"</span> - <span class="syn-num">2</span>);           <span class="syn-com">// Engine নিজে "22" কে সংখ্যা বানাচ্ছে (Implicit)</span></pre>
      </div>
    </div>"""

new_sec46 = """    <!-- 46 -->
    <div class="study-card">
      <div class="card-title"><span class="badge-num">46</span> Explicit vs Implicit Conversion</div>
      <span class="tag-label cyan">Explicit Conversion (Developer নিজে রূপান্তর করছে)</span>
      <div class="code-box">
        <pre><span class="syn-kw">const</span> age = Number(<span class="syn-str">"22"</span>);</pre>
      </div>

      <span class="tag-label purple">Implicit Conversion (JavaScript Engine নিজে রূপান্তর করছে)</span>
      <div class="code-box">
        <pre>console.log(<span class="syn-str">"22"</span> - <span class="syn-num">2</span>);</pre>
      </div>
      <span class="tag-label amber">Output</span>
      <div class="output-box">20</div>
    </div>"""

if old_sec46 in html:
    html = html.replace(old_sec46, new_sec46)
    print("Section 46 updated!")
else:
    print("Section 46 old content mismatch!")

# 6. Section 47: Full verbatim restoration from MD
old_sec47 = """    <!-- 47 -->
    <div class="study-card">
      <div class="card-title"><span class="badge-num">47</span> Equality: `==` vs `===`</div>
      <div class="table-wrap">
        <table>
          <thead>
            <tr><th>Loose Equality <code>==</code></th><th>Strict Equality <code>===</code></th></tr>
          </thead>
          <tbody>
            <tr><td>তুলনার আগে টাইপ কনভার্সন (Coercion) করে</td><td>মান এবং টাইপ উভয়ই কঠোরভাবে পরীক্ষা করে</td></tr>
            <tr><td><code>5 == "5"</code> → <strong>true</strong></td><td><code>5 === "5"</code> → <strong>false</strong></td></tr>
          </tbody>
        </table>
      </div>
      <div class="memory-box">
        <strong>⭐ Golden Rule:</strong> সবসময় <code>===</code> ব্যবহার করবে।
      </div>
    </div>"""

new_sec47 = """    <!-- 47 -->
    <div class="study-card">
      <div class="card-title"><span class="badge-num">47</span> Equality-এর Basic Introduction</div>
      <p class="text-p">JavaScript-এ দুই ধরনের equality operator আছে: <code>==</code> এবং <code>===</code>। এগুলো অত্যন্ত গুরুত্বপূর্ণ এবং পরবর্তী <strong>Chapter 3 (Operators)</strong>-এ বিস্তারিত আলোচনা করা হবে। নিচে এদের মৌলিক পার্থক্য তুলে ধরা হলো:</p>

      <span class="tag-label cyan">Loose Equality `==` (Type Coercion করে)</span>
      <div class="code-box">
        <pre>console.log(<span class="syn-num">5</span> == <span class="syn-str">"5"</span>);</pre>
      </div>
      <span class="tag-label amber">Output</span>
      <div class="output-box">true</div>

      <span class="tag-label purple">Strict Equality `===` (Value ও Type দুটোই Compare করে)</span>
      <div class="code-box">
        <pre>console.log(<span class="syn-num">5</span> === <span class="syn-str">"5"</span>);</pre>
      </div>
      <span class="tag-label amber">Output</span>
      <div class="output-box">false</div>

      <div class="table-wrap" style="margin-top: 8px;">
        <table>
          <thead>
            <tr><th>Loose Equality <code>==</code></th><th>Strict Equality <code>===</code></th></tr>
          </thead>
          <tbody>
            <tr><td>তুলনার আগে স্বয়ংক্রিয় টাইপ রূপান্তর (Coercion) ঘটায়</td><td>মান (Value) এবং টাইপ (Type) উভয়ই কঠোরভাবে পরীক্ষা করে</td></tr>
            <tr><td><code>5 == "5"</code> → <strong>true</strong></td><td><code>5 === "5"</code> → <strong>false</strong></td></tr>
          </tbody>
        </table>
      </div>

      <div class="memory-box">
        <strong>⭐ Beginner Rule:</strong> Modern JavaScript-এ সাধারণত comparison-এর জন্য সর্বদা <code>===</code> ব্যবহার করা বেশি predictable ও নিরাপদ।
      </div>
    </div>"""

if old_sec47 in html:
    html = html.replace(old_sec47, new_sec47)
    print("Section 47 updated!")
else:
    print("Section 47 old content mismatch!")

# 7. Section 48: Add reassignment explanation
old_sec48 = """    <!-- 48 -->
    <div class="study-card">
      <div class="card-title"><span class="badge-num">48</span> Primitive Values are Immutable</div>
      <p class="text-p">প্রিমিটিভ ভ্যালু সরাসরি মিউটেট বা পরিবর্তন করা যায় না; নতুন মান তৈরি করে এসাইন করতে হয়:</p>
      <div class="code-box">
        <div class="code-top"><span>JavaScript</span><span>Immutability</span></div>
        <pre><span class="syn-kw">let</span> name = <span class="syn-str">"Ripon"</span>;
name[<span class="syn-num">0</span>] = <span class="syn-str">"X"</span>; <span class="syn-com">// সাইলেন্টলি ইগনোর হবে</span>
console.log(name); <span class="syn-com">// "Ripon" (অপরিবর্তিত থাকবে!)</span></pre>
      </div>
      <span class="tag-label amber">Output</span>
      <div class="output-box">Ripon</div>
    </div>"""

new_sec48 = """    <!-- 48 -->
    <div class="study-card">
      <div class="card-title"><span class="badge-num">48</span> Primitive Values are Immutable</div>
      <p class="text-p">Primitive values-কে সাধারণভাবে immutable বলা হয়। এর মানে primitive value-কে সরাসরি modify করা যায় না; নতুন value তৈরি হয়।</p>
      <div class="code-box">
        <div class="code-top"><span>JavaScript</span><span>Immutability</span></div>
        <pre><span class="syn-kw">let</span> name = <span class="syn-str">"Ripon"</span>;
name[<span class="syn-num">0</span>] = <span class="syn-str">"X"</span>; <span class="syn-com">// String-এর character এভাবে modify হয় না</span>
console.log(name);</pre>
      </div>
      <span class="tag-label amber">Output</span>
      <div class="output-box">Ripon</div>
      <p class="text-p">যদি নতুন value দিতে চাও, তবে নতুন value assign করতে হবে:</p>
      <div class="code-box">
        <pre>name = <span class="syn-str">"Xipon"</span>; <span class="syn-com">// এখানে নতুন String value assign হচ্ছে — আগের String পরিবর্তন হচ্ছে না</span></pre>
      </div>
    </div>"""

if old_sec48 in html:
    html = html.replace(old_sec48, new_sec48)
    print("Section 48 updated!")
else:
    print("Section 48 old content mismatch!")

# 8. Section 51: Fix long comment wrap
old_sec51 = """    <!-- 51 -->
    <div class="study-card">
      <div class="card-title"><span class="badge-num">51</span> `const` Object নিয়ে Important বিষয়</div>
      <p class="text-p">অনেকে ভাবে <code>const</code> হলে অবজেক্টের ভিতরের প্রপার্টি বদলানো যায় না। <strong>এটা ভুল ধারণা!</strong></p>
      <div class="code-box">
        <div class="code-top"><span>JavaScript</span><span>Mutating const Object</span></div>
        <pre><span class="syn-kw">const</span> user = { name: <span class="syn-str">"Ripon"</span> };
user.name = <span class="syn-str">"Shariar"</span>; <span class="syn-com">// সম্পূর্ণ বৈধ! প্রোপার্টি পরিবর্তন করা যাবে</span>
console.log(user.name);

<span class="syn-com">// user = {}; // TypeError: Assignment to constant variable! (নতুন অবজেক্টে reassign নিষিদ্ধ)</span></pre>
      </div>
      <span class="tag-label amber">Output</span>
      <div class="output-box">Shariar</div>
    </div>"""

new_sec51 = """    <!-- 51 -->
    <div class="study-card">
      <div class="card-title"><span class="badge-num">51</span> `const` Object নিয়ে Important বিষয়</div>
      <p class="text-p">অনেকে ভাবে: <code>const</code> হলে object-এর ভিতরের value change করা যাবে না। <strong>এটা পুরোপুরি ঠিক নয়।</strong></p>
      <div class="code-box">
        <div class="code-top"><span>JavaScript</span><span>Mutating const Object</span></div>
        <pre><span class="syn-kw">const</span> user = {
  name: <span class="syn-str">"Ripon"</span>
};

user.name = <span class="syn-str">"Shariar"</span>; <span class="syn-com">// প্রোপার্টি পরিবর্তন করা সম্পূর্ণ বৈধ!</span>
console.log(user.name);</pre>
      </div>
      <span class="tag-label amber">Output</span>
      <div class="output-box">Shariar</div>
      <p class="text-p">কাজ করেছে। কিন্তু অবজেক্টের ভ্যারিয়েবল বাইন্ডিং রি-অ্যাসাইন করা যাবে না:</p>
      <div class="code-box">
        <pre><span class="syn-com">// user = {};</span>
<span class="syn-com">// ❌ TypeError: Assignment to constant variable!</span>
<span class="syn-com">// কারণ const binding-কে নতুন object-এ reassign করা যাবে না।</span></pre>
      </div>
    </div>"""

if old_sec51 in html:
    html = html.replace(old_sec51, new_sec51)
    print("Section 51 updated!")
else:
    print("Section 51 old content mismatch!")

with open(r'c:\Users\User\Desktop\Note-Book\Code\Chapter-02-Variables-DataTypes-TypeSystem.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Saved updated HTML file successfully!")
