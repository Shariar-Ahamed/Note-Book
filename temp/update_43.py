with open(r'Code/Chapter-02-Variables-DataTypes-TypeSystem.html', 'r', encoding='utf-8') as f:
    html = f.read()

old_43 = """<!-- 43 -->
    <div class="study-card">
      <div class="card-title"><span class="badge-num">43</span> Type Coercion</div>
      <p class="text-p"><strong>Conversion:</strong> যখন প্রোগ্রামার নিজে ফাংশন দিয়ে টাইপ পরিবর্তন করে (Explicit)।<br>
      <strong>Coercion:</strong> যখন জাভাস্ক্রিপ্ট ইঞ্জিন নিজে কনটেক্সট অনুযায়ী স্বয়ংক্রিয়ভাবে টাইপ রূপান্তর করে (Implicit)।</p>
      <div class="code-box">
        <div class="code-top"><span>JavaScript</span><span>Coercion</span></div>
        <pre>console.log(<span class="syn-str">"10"</span> + <span class="syn-num">5</span>); <span class="syn-com">// "105" (String concatenation)</span></pre>
      </div>
      <span class="tag-label amber">Output</span>
      <div class="output-box">105</div>
    </div>"""

new_43 = """<!-- 43 -->
    <div class="study-card">
      <div class="card-title"><span class="badge-num">43</span> Type Coercion</div>
      <p class="text-p">Type conversion এবং coercion-এর মধ্যে সূক্ষ্ম কিন্তু মৌলিক পার্থক্য রয়েছে:</p>

      <span class="tag-label cyan">Type Conversion (Explicit — প্রোগ্রামার নিজে করে)</span>
      <div class="code-box">
        <pre>Number(<span class="syn-str">"100"</span>); <span class="syn-com">// 100 (Explicitly সংখ্যায় রূপান্তর)</span></pre>
      </div>

      <span class="tag-label purple">Type Coercion (Implicit — ইঞ্জিন নিজে করে)</span>
      <div class="code-box">
        <pre>console.log(<span class="syn-str">"10"</span> + <span class="syn-num">5</span>);</pre>
      </div>
      <span class="tag-label amber">Output</span>
      <div class="output-box">105</div>
      <p class="text-p">কারণ এখানে জাভাস্ক্রিপ্ট কনটেক্সট বুঝে <code>5</code>-কে স্ট্রিং বানিয়ে কনক্যাট করেছে।</p>
    </div>"""

assert old_43 in html, 'old_43 not found'
html = html.replace(old_43, new_43)

with open(r'Code/Chapter-02-Variables-DataTypes-TypeSystem.html', 'w', encoding='utf-8') as f:
    f.write(html)

print('Section 43 updated!')
