with open(r'Code/Chapter-02-Variables-DataTypes-TypeSystem.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Replace Section 27
old_27 = """<!-- 27 -->
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
      <p class="text-p">ডেসক্রিপশন একই হলেও প্রতিবার <code>Symbol()</code> সম্পূর্ণ নতুন ও অদ্বিতীয় আইডেন্টিফায়ার তৈরি করে।</p>
    </div>"""

new_27 = """<!-- 27 -->
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

assert old_27 in html, 'old_27 not found'
html = html.replace(old_27, new_27)

# Replace Section 51
old_51 = """<!-- 51 -->
    <div class="study-card">
      <div class="card-title"><span class="badge-num">51</span> `const` Object নিয়ে Important বিষয়</div>
      <p class="text-p">অনেকে ভাবে <code>const</code> হলে অবজেক্টের ভিতরের প্রোপার্টি বদলানো যায় না। <strong>এটা ভুল ধারণা!</strong></p>
      <div class="code-box">
        <div class="code-top"><span>JavaScript</span><span>Mutating Const Object</span></div>
        <pre><span class="syn-kw">const</span> user = { name: <span class="syn-str">"Ripon"</span> };
user.name = <span class="syn-str">"Shariar"</span>; <span class="syn-com">// সম্পূর্ণ বৈধ! প্রোপার্টি পরিবর্তন করা যাবে</span>
console.log(user.name);

<span class="syn-com">// user = {}; // TypeError: Assignment to constant variable! (নতুন অবজেক্টে reassign নিষিদ্ধ)</span></pre>
      </div>
      <span class="tag-label amber">Output</span>
      <div class="output-box">Shariar</div>
    </div>"""

new_51 = """<!-- 51 -->
    <div class="study-card">
      <div class="card-title"><span class="badge-num">51</span> `const` Object নিয়ে Important বিষয়</div>
      <p class="text-p">অনেকে ভাবে: <code>const</code> হলে object-এর ভিতরের value change করা যাবে না। <strong>এটা পুরোপুরি ঠিক নয়।</strong></p>
      <div class="code-box">
        <div class="code-top"><span>JavaScript</span><span>Mutating Const Object</span></div>
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

assert old_51 in html, 'old_51 not found'
html = html.replace(old_51, new_51)

with open(r'Code/Chapter-02-Variables-DataTypes-TypeSystem.html', 'w', encoding='utf-8') as f:
    f.write(html)

print('Updated 27 and 51 successfully!')
