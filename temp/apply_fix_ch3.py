import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open(r'Code/Chapter-03-Operators-Expressions.html', 'r', encoding='utf-8') as f:
    text = f.read()

print("Original length:", len(text))

# 1. Unescape \n and \"
text = text.replace(r'\n', '\n').replace(r'\"', '"')
print("After unescaping length:", len(text))

# 2. Fix empty def-boxes in Section 1 and Section 3
# Section 1
s1_old = """<div class="def-box english"><strong>English:</strong> </div>
<p class="text-p">An <strong>operator</strong> is a symbol or keyword that tells JavaScript to perform an operation.</p>
<div class="def-box bangla"><strong>বাংলা:</strong> </div>
<p class="text-p">Operator হলো এমন একটি symbol বা keyword যা JavaScript-কে কোনো নির্দিষ্ট operation করতে বলে।</p>"""

s1_new = """<div class="def-box english"><strong>English:</strong> An <strong>operator</strong> is a symbol or keyword that tells JavaScript to perform an operation.</div>
<div class="def-box bangla"><strong>বাংলা:</strong> Operator হলো এমন একটি symbol বা keyword যা JavaScript-কে কোনো নির্দিষ্ট operation করতে বলে।</div>"""

if s1_old in text:
    text = text.replace(s1_old, s1_new)
    print("Section 1 def-box fixed!")
else:
    print("Section 1 def-box old string not found!")

# Section 3
s3_old = """<div class="def-box english"><strong>English:</strong> </div>
<p class="text-p">An <strong>expression</strong> is a piece of code that produces a value.</p>
<div class="def-box bangla"><strong>বাংলা:</strong> </div>
<p class="text-p">Expression হলো এমন code যা একটি value produce করে।</p>"""

s3_new = """<div class="def-box english"><strong>English:</strong> An <strong>expression</strong> is a piece of code that produces a value.</div>
<div class="def-box bangla"><strong>বাংলা:</strong> Expression হলো এমন code যা একটি value produce করে।</div>"""

if s3_old in text:
    text = text.replace(s3_old, s3_new)
    print("Section 3 def-box fixed!")
else:
    print("Section 3 def-box old string not found!")

# 3. Upgrade CSS: Add @page and upgrade @media print to standard proven rules
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

if old_print_css in text:
    text = text.replace(old_print_css, new_print_css)
    print("Print CSS replaced cleanly!")
else:
    print("Old print CSS not found by exact string, replacing via regex...")
    text = re.sub(r'@media print\s*\{.*?\}\s*\}', new_print_css.strip(), text, flags=re.DOTALL)
    print("Print CSS replaced via regex!")

# 4. Replace unparsed raw markdown after Section 89 with beautiful styled cards
end_target = '<div class="study-card" style="border-left: 4px solid var(--amber-accent); background: #fffbeb;">'
idx_end = text.find(end_target)
if idx_end != -1:
    print(f"Found end section at index {idx_end}")
    
    new_end_html = """    <!-- QUICK REVISION -->
    <div class="study-card" style="border-left: 4px solid var(--amber-accent); background: #fffbeb;">
      <h3 style="font-size: 13.5px; margin-bottom: 8px; color: #92400e;">🧠 Chapter 3 — Quick Revision</h3>
      <p class="text-p"><strong>এক লাইনে মনে রাখো:</strong></p>
      <div class="memory-box">
        <strong>মৌলিক সারমর্ম:</strong> Operator data-এর উপর operation করে, আর expression সেই operation-এর মাধ্যমে একটি value produce করতে পারে।
      </div>
      <div class="code-box">
        <div class="code-top"><span>Expression Structure</span><span>10 + 20</span></div>
        <pre>10 + 20</pre>
      </div>
      <div class="ascii-tree-container">এখানে:
10  → Operand
+   → Operator
20  → Operand
30  → Result</div>
      <p class="text-p" style="font-weight: 700; margin-top: 8px;">Operators-এর বড় পিকচার (Mental Architecture):</p>
      <div class="ascii-tree-container">                    Operators
                        │
       ┌────────────────┼────────────────┐
       │                │                │
   Arithmetic       Comparison       Logical
       │                │                │
   + - * / % **     &gt; &lt; === !==     &amp;&amp; || !
       │                │                │
       └────────────────┼────────────────┘
                        │
                Assignment
                        │
              = += -= *= /= %=
                        │
                  Modern JS
                        │
                ??   ?.   ?:</div>
    </div>

    <!-- PRACTICE SET -->
    <div class="study-card">
      <h3 style="font-size: 13.5px; color: var(--navy-mid); margin-bottom: 8px;">🧪 Chapter 3 — Practice Set</h3>
      <p class="text-p" style="margin-bottom: 10px;">এগুলো আগে <strong>নিজে output predict করবে</strong>, তারপর browser console-এ run করবে:</p>

      <div style="margin-bottom: 8px; padding: 8px 12px; background: #f8fafc; border-left: 3px solid #0284c7; border-radius: 4px;">
        <strong>Practice 1 (Basic Arithmetic &amp; Modulus):</strong>
        <div class="code-box"><pre>console.log(20 + 10);
console.log(20 - 10);
console.log(20 * 10);
console.log(20 / 10);
console.log(20 % 3);
console.log(2 ** 5);</pre></div>
      </div>

      <div style="margin-bottom: 8px; padding: 8px 12px; background: #f8fafc; border-left: 3px solid #0284c7; border-radius: 4px;">
        <strong>Practice 2 (Compound Assignment Flow):</strong>
        <div class="code-box"><pre>let score = 100;

score += 20;
score -= 10;
score *= 2;
score /= 2;

console.log(score);</pre></div>
        <p class="text-p">Final output কী হবে?</p>
      </div>

      <div style="margin-bottom: 8px; padding: 8px 12px; background: #f8fafc; border-left: 3px solid #0284c7; border-radius: 4px;">
        <strong>Practice 3 (Comparison &amp; Equality Contrast):</strong>
        <div class="code-box"><pre>console.log(10 &gt; 5);
console.log(10 &lt; 5);
console.log(10 &gt;= 10);
console.log(10 &lt;= 9);
console.log(10 == "10");
console.log(10 === "10");</pre></div>
        <p class="text-p">প্রতিটির output explain করো।</p>
      </div>

      <div style="margin-bottom: 8px; padding: 8px 12px; background: #f8fafc; border-left: 3px solid #0284c7; border-radius: 4px;">
        <strong>Practice 4 (Logical Truth Tables):</strong>
        <div class="code-box"><pre>console.log(true &amp;&amp; false);
console.log(true || false);
console.log(!true);
console.log(!false);</pre></div>
      </div>

      <div style="margin-bottom: 8px; padding: 8px 12px; background: #f8fafc; border-left: 3px solid #0284c7; border-radius: 4px;">
        <strong>Practice 5 (String vs Number Arithmetic Coercion):</strong>
        <div class="code-box"><pre>console.log("5" + 2);
console.log("5" - 2);
console.log("5" * 2);
console.log("5" / 2);</pre></div>
        <p class="text-p"><strong>কেন প্রথমটার behavior অন্যগুলোর থেকে আলাদা—নিজে explain করার চেষ্টা করো।</strong></p>
      </div>

      <div style="margin-bottom: 8px; padding: 8px 12px; background: #f8fafc; border-left: 3px solid #0284c7; border-radius: 4px;">
        <strong>Practice 6 (Ternary Operator):</strong>
        <div class="code-box"><pre>const age = 17;
const result = age &gt;= 18 ? "Adult" : "Minor";
console.log(result);</pre></div>
      </div>

      <div style="margin-bottom: 8px; padding: 8px 12px; background: #f8fafc; border-left: 3px solid #0284c7; border-radius: 4px;">
        <strong>Practice 7 (Optional Chaining `?.`):</strong>
        <div class="code-box"><pre>const user = {
  profile: {
    name: "Ripon"
  }
};

console.log(user.profile?.name);
console.log(user.address?.city);</pre></div>
      </div>

      <div style="margin-bottom: 6px; padding: 8px 12px; background: #f8fafc; border-left: 3px solid #0284c7; border-radius: 4px;">
        <strong>Practice 8 — Real Project Logic:</strong>
        <div class="ascii-tree-container">ধরো:
Product Price = 1500
Quantity = 3
Discount = 500
Delivery = 100</div>
        <p class="text-p">JavaScript দিয়ে <strong>Subtotal</strong> ও <strong>Final Total</strong> বের করো।</p>
      </div>
    </div>

    <!-- MINI PROJECT -->
    <div class="study-card" style="background: #f0fdf4; border-left: 4px solid var(--green-accent);">
      <h3 style="font-size: 13.5px; color: #166534; margin-bottom: 8px;">🎯 Chapter 3 Mini Project — Shopping Cart Calculator</h3>
      <p class="text-p">নিজে এই logic তৈরি করার চেষ্টা করো:</p>
      <div class="ascii-tree-container">Cart Calculation Structure:
Product Price
Quantity
Discount
Delivery Charge
----------------
Subtotal   = (Price * Quantity)
Final Total = Subtotal - Discount + Delivery Charge</div>

      <div class="memory-box" style="margin: 8px 0;">
        <strong>Example Data:</strong><br>
        Product Price: <code>800</code> | Quantity: <code>2</code> | Discount: <code>100</code> | Delivery: <code>60</code><br>
        <strong>Expected:</strong> Subtotal: <code>1600</code> | Final Total: <code>1560</code>
      </div>

      <div class="code-box">
        <div class="code-top"><span>JavaScript</span><span>Shopping Cart Calculator Implementation</span></div>
        <pre><span class="syn-kw">const</span> productPrice = <span class="syn-num">800</span>;
<span class="syn-kw">const</span> quantity = <span class="syn-num">2</span>;
<span class="syn-kw">const</span> discount = <span class="syn-num">100</span>;
<span class="syn-kw">const</span> deliveryCharge = <span class="syn-num">60</span>;

<span class="syn-com">// 1. Subtotal calculation</span>
<span class="syn-kw">const</span> subtotal = productPrice * quantity;

<span class="syn-com">// 2. Final Total calculation</span>
<span class="syn-kw">const</span> finalTotal = subtotal - discount + deliveryCharge;

console.log(<span class="syn-str">"Subtotal:"</span>, subtotal);       <span class="syn-com">// 1600</span>
console.log(<span class="syn-str">"Final Total:"</span>, finalTotal);   <span class="syn-com">// 1560</span></pre>
      </div>
      <p class="text-p" style="color: #166534; font-size: 11px;">এখানে ব্যবহৃত হয়েছে: Variables, Arithmetic operators, Assignment এবং <code>console.log()</code></p>
    </div>

    <!-- MUST KNOW CONCEPTS -->
    <div class="study-card">
      <h3 style="font-size: 13px; color: var(--navy-mid); margin-bottom: 6px;">⭐ Chapter 3-এর Must-Know Concepts</h3>
      <div class="ascii-tree-container">+  -  *  /  %  **
=  += -= *= /=
&gt;  &lt;  &gt;= &lt;=
== === != !==
&amp;&amp; || !
++ --
? :
??
?.
typeof</div>
      <p class="text-p" style="margin-top: 6px; font-weight: 600; color: #0369a1;">
        এর মধ্যে <code>===</code>, <code>&amp;&amp;</code>, <code>||</code>, <code>??</code>, <code>?.</code>, <code>%</code>, <code>++/--</code>, ternary এবং <strong>operator precedence</strong> বিশেষভাবে ভালোভাবে practice করবে।
      </p>
    </div>

    <!-- NEXT CHAPTER PREVIEW -->
    <div class="study-card" style="background: #eff6ff; border-left: 4px solid #0284c7;">
      <h3 style="font-size: 13px; color: #0369a1; margin-bottom: 6px;">📌 পরবর্তী অধ্যায় — Chapter 4 Preview</h3>
      <h4 style="font-size: 12px; color: var(--navy-mid); margin-bottom: 4px;">Chapter 4 — Control Flow &amp; Decision Making</h4>
      <p class="text-p">এখানে JavaScript কীভাবে <strong>decision নেয়</strong> সেটা শুরু হবে:</p>
      <div class="ascii-tree-container">if, else, else if, nested if
switch, case, default, break, fall-through
truthy, falsy, logical conditions, ternary</div>
      <p class="text-p" style="font-size: 11.5px; color: #334155; margin-top: 6px;">
        এরপর আমরা ধাপে ধাপে <strong>Loops → Functions → Strings → Arrays → Objects → Scope → DOM → Events → Async JavaScript → APIs → OOP → Advanced JavaScript → JavaScript Internals</strong>-এর দিকে এগিয়ে যাব।
      </p>
    </div>

  </div>
</body>
</html>
"""
    text = text[:idx_end] + new_end_html
    print("Replaced end section with complete formatted HTML cards!")
else:
    print("Could not find end target!")

with open(r'Code/Chapter-03-Operators-Expressions.html', 'w', encoding='utf-8') as f:
    f.write(text)

print("Saved fixed Chapter 3 HTML file!")
