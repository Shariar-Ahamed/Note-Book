# 📘 JavaScript Complete Book — Chapter 1

## JavaScript Fundamentals — JavaScript-এর ভিত্তি

এই Chapter-এ আমরা JavaScript-এর একদম foundation তৈরি করব। পরের chapter-গুলো বুঝতে এই অংশগুলো ভালোভাবে বোঝা খুব important।

---

# 1. What is JavaScript?

### English Definition

**JavaScript is a high-level, interpreted/programming language mainly used to make web pages interactive and dynamic.**

### বাংলা ব্যাখ্যা

সহজ ভাষায়, **JavaScript হলো এমন একটি programming language যার মাধ্যমে আমরা একটি website-কে শুধু static না রেখে interactive এবং dynamic করতে পারি।**

HTML দিয়ে আমরা webpage-এর **structure** তৈরি করি।

CSS দিয়ে webpage-এর **design/style** করি।

আর JavaScript দিয়ে webpage-এর **behavior/functionality** তৈরি করি।

### 🏠 Real-Life Example

ধরো তুমি একটা house বানাচ্ছো:

| Technology | কাজ       | Real-life analogy         |
| ---------- | --------- | ------------------------- |
| HTML       | Structure | বাড়ির কাঠামো             |
| CSS        | Design    | রং, furniture, decoration |
| JavaScript | Behavior  | দরজা খোলা, light on/off   |

যেমন একটি button:

```html
<button>Click Me</button>
```

HTML শুধু button তৈরি করবে।

CSS দিয়ে button সুন্দর করা যাবে।

কিন্তু button click করলে কিছু ঘটাতে JavaScript ব্যবহার করা যায়।

```html
<button onclick="alert('Hello!')">
    Click Me
</button>
```

Button-এ click করলে:

```text
Hello!
```

দেখাবে।

---

# 2. Why Do We Need JavaScript?

একটি webpage JavaScript ছাড়াও তৈরি করা যায়।

কিন্তু JavaScript ছাড়া অনেক interactive functionality তৈরি করা কঠিন বা অসম্ভব হয়ে যায়।

### JavaScript দিয়ে আমরা করতে পারি:

* Button click handling
* Form validation
* Dropdown menu
* Modal
* Image slider
* Calculator
* To-do application
* Dark/light mode
* Dynamic content
* API থেকে data নেওয়া
* Search functionality
* Real-time updates
* Authentication-related frontend logic
* Browser storage
* Web applications

### Example

```html
<button onclick="changeText()">Click Me</button>

<p id="message">Hello</p>

<script>
function changeText() {
    document.getElementById("message").textContent = "Welcome!";
}
</script>
```

### Output

প্রথমে:

```text
Hello
```

Button click করার পর:

```text
Welcome!
```

এখানেই JavaScript-এর power দেখা যায়।

---

# 3. JavaScript vs Java

এটা beginner-দের একটা common confusion।

**JavaScript এবং Java একই language নয়।**

নাম কাছাকাছি হলেও দুটো আলাদা programming language।

| JavaScript                       | Java                                                 |
| -------------------------------- | ---------------------------------------------------- |
| Mainly web development-এ ব্যবহৃত | General-purpose/backend/enterprise ইত্যাদিতে ব্যবহৃত |
| Browser-এ directly run করতে পারে | সাধারণত JVM-এর মাধ্যমে চলে                           |
| Dynamic language                 | Statically typed language                            |
| `.js` file                       | `.java` source file                                  |
| Frontend + Backend               | Backend + Enterprise + Android history ইত্যাদি       |

### Example

JavaScript:

```javascript
let name = "Ripon";

console.log(name);
```

Java:

```java
String name = "Ripon";

System.out.println(name);
```

দুটো completely different language।

---

# 4. JavaScript-এর ইতিহাস

JavaScript-এর শুরু হয় **1995 সালে** Netscape-এর web browser environment-এ।

প্রথমদিকে এর নাম ছিল **Mocha**, পরে **LiveScript**, এবং শেষ পর্যন্ত **JavaScript** নামটি জনপ্রিয় হয়।

JavaScript-এর creator হিসেবে সাধারণত **Brendan Eich**-কে উল্লেখ করা হয়।

তিনি Netscape-এ JavaScript-এর প্রথম version তৈরি করেন।

### Timeline — সহজভাবে

```text
1995
 ↓
JavaScript introduced
 ↓
Browser scripting becomes popular
 ↓
ECMAScript standardization
 ↓
ES5
 ↓
ES6 / ES2015
 ↓
Modern JavaScript
```

---

# 5. What is ECMAScript?

এটা খুব important concept।

### English

**ECMAScript is the standardized specification that defines how JavaScript should work.**

### বাংলা

**ECMAScript হলো JavaScript-এর standard/specification।**

সহজভাবে:

> **JavaScript হলো language implementation, আর ECMAScript হলো তার standard/specification।**

### Example

ECMAScript specification-এর বিভিন্ন version এসেছে:

```text
ES1
ES2
ES3
ES5
ES6 / ES2015
ES2016
ES2017
...
Modern ECMAScript
```

---

# 6. What is ES6?

**ES6** হলো JavaScript-এর একটি অত্যন্ত গুরুত্বপূর্ণ version, যেটার official নাম **ECMAScript 2015 (ES2015)**।

ES6 JavaScript-এ অনেক গুরুত্বপূর্ণ feature নিয়ে আসে।

যেমন:

```javascript
let name = "Ripon";
const age = 22;

const greet = () => {
    console.log("Hello");
};
```

আরও এসেছে:

* `let`
* `const`
* Arrow Functions
* Classes
* Template Literals
* Destructuring
* Spread Operator
* Rest Parameters
* Promises
* Modules
* অনেক নতুন syntax ও feature

তাই modern JavaScript শেখার ক্ষেত্রে **ES6+ খুব গুরুত্বপূর্ণ।**

---

# 7. How JavaScript Works?

এখন একটু ভিতরের দিকে যাই।

যখন তুমি লিখো:

```javascript
console.log("Hello");
```

Browser সরাসরি এই text-টা execute করে না।

Browser-এর ভিতরে একটি **JavaScript Engine** থাকে।

Engine JavaScript code বুঝে execute করে।

### Simplified process

```text
JavaScript Code
      ↓
JavaScript Engine
      ↓
Parsing / Compilation
      ↓
Execution
      ↓
Output
```

### Example

```javascript
let x = 10;
let y = 20;

console.log(x + y);
```

Engine code process করে এবং output দেয়:

```text
30
```

---

# 8. What is a JavaScript Engine?

### English

**A JavaScript engine is a program that parses, compiles/interprets, and executes JavaScript code.**

### বাংলা

JavaScript Engine হলো এমন একটি software component যা JavaScript code-কে process করে এবং execute করে।

### Popular JavaScript Engines

| Engine         | Used by                  |
| -------------- | ------------------------ |
| V8             | Google Chrome, Node.js   |
| SpiderMonkey   | Firefox                  |
| JavaScriptCore | Safari                   |
| Chakra         | Older Microsoft browsers |

### ⭐ Important

তুমি যদি Chrome ব্যবহার করো, Chrome-এর JavaScript engine হলো:

> **V8**

আর Node.js-ও **V8 engine** ব্যবহার করে।

---

# 9. JavaScript কোথায় Run করতে পারে?

JavaScript শুধু browser-এ চলে—এটা এখন আর পুরোপুরি correct নয়।

JavaScript বিভিন্ন environment-এ run করতে পারে।

### 1. Browser

যেমন:

* Chrome
* Firefox
* Edge
* Safari

### 2. Server

**Node.js** ব্যবহার করে JavaScript server-side-এ run করা যায়।

### 3. অন্যান্য Runtime

যেমন:

* Deno
* Bun

### Basic concept

```text
JavaScript
   │
   ├── Browser
   │
   ├── Node.js
   │
   ├── Deno
   │
   └── Bun
```

---

# 10. JavaScript in Browser

Browser-এ JavaScript চালানোর সবচেয়ে simple example:

```html
<!DOCTYPE html>
<html>
<head>
    <title>JavaScript</title>
</head>
<body>

    <h1>Hello JavaScript</h1>

    <script>
        console.log("Hello JavaScript!");
    </script>

</body>
</html>
```

Browser-এ page open করলে webpage-এ থাকবে:

```text
Hello JavaScript
```

আর Developer Console-এ:

```text
Hello JavaScript!
```

---

# 11. How to Open Browser Console?

Chrome-এ:

```text
Right Click
   ↓
Inspect
   ↓
Console
```

অথবা:

```text
F12
```

তারপর Console tab।

সেখানে লিখতে পারো:

```javascript
console.log("Hello World");
```

Output:

```text
Hello World
```

এটা JavaScript শেখার সময় তোমার সবচেয়ে বেশি ব্যবহৃত tools-এর একটি হবে।

---

# 12. Three Ways to Add JavaScript to HTML

HTML-এর সাথে JavaScript connect করার তিনটি common উপায় আছে।

---

## 12.1 Inline JavaScript

HTML element-এর ভিতর directly JavaScript লেখা।

```html
<button onclick="alert('Hello')">
    Click Me
</button>
```

Click করলে:

```text
Hello
```

### ❌ Problem

বড় project-এ inline JavaScript maintain করা কঠিন।

তাই সাধারণত professional project-এ এটা avoid করা হয়।

---

# 13. Internal JavaScript

HTML-এর `<script>` tag-এর ভিতরে JavaScript লেখা।

```html
<!DOCTYPE html>
<html>
<body>

    <h1>My Website</h1>

    <script>
        console.log("Hello JavaScript");
    </script>

</body>
</html>
```

এখানে JavaScript HTML file-এর মধ্যেই রয়েছে।

---

# 14. External JavaScript

Professional development-এ সবচেয়ে common approach।

একটি আলাদা `.js` file তৈরি করি।

### `index.html`

```html
<!DOCTYPE html>
<html>
<body>

    <h1>My Website</h1>

    <script src="script.js"></script>

</body>
</html>
```

### `script.js`

```javascript
console.log("Hello from JavaScript!");
```

Browser console:

```text
Hello from JavaScript!
```

### কেন External JavaScript ভালো?

কারণ:

* Code organized থাকে
* Maintain করা সহজ
* Reuse করা যায়
* HTML clean থাকে
* বড় project manage করা সহজ

---

# 15. The `<script>` Tag

HTML-এ JavaScript load করার জন্য ব্যবহার করি:

```html
<script>
    // JavaScript
</script>
```

External file:

```html
<script src="script.js"></script>
```

এখানে:

```text
script
```

হলো HTML element/tag।

আর:

```text
src
```

হলো attribute।

---

# 16. `defer` Attribute

External JavaScript load করার সময় খুব useful:

```html
<script src="script.js" defer></script>
```

### `defer` কী করে?

Browser HTML parse করতে থাকে এবং JavaScript file load করতে পারে, কিন্তু script execution সাধারণত HTML parsing শেষ হওয়ার পরে হয়।

সহজভাবে:

```text
HTML parsing
     +
JS downloading
     ↓
HTML parsing complete
     ↓
JS execution
```

Modern frontend development-এ `defer` খুব useful।

---

# 17. `async` Attribute

আরেকটি option:

```html
<script src="script.js" async></script>
```

এখানে JavaScript file download HTML parsing-এর সাথে parallel হতে পারে এবং download শেষ হলে script execute হতে পারে।

তাই:

### `defer`

```text
Download ──────────┐
HTML parsing ──────┼──→ HTML complete → JS execute
```

### `async`

```text
HTML parsing ───────────────→
       ↓
JS download → JS execute
```

`async` এবং `defer` কখন ব্যবহার করবে—এটা আমরা পরে **Browser Loading & Performance** chapter-এ বিস্তারিত দেখব।

---

# 18. JavaScript Comments

Comment হলো এমন text যা JavaScript engine সাধারণত execute করে না।

Comments code explain করতে ব্যবহার করা হয়।

---

## Single-line Comment

```javascript
// This is a comment

console.log("Hello");
```

Output:

```text
Hello
```

---

## Multi-line Comment

```javascript
/*
    This is a
    multi-line comment
*/

console.log("Hello");
```

Output:

```text
Hello
```

### Real-life example

```javascript
// Store user's name
let name = "Ripon";

console.log(name);
```

Comment দেখে developer বুঝতে পারে variable-টির উদ্দেশ্য কী।

---

# 19. JavaScript Statements

### English

A **statement** is an instruction that tells JavaScript to perform an action.

### বাংলা

Statement হলো JavaScript-কে দেওয়া একটি instruction।

Example:

```javascript
let name = "Ripon";
```

আর:

```javascript
console.log(name);
```

এগুলো JavaScript-এর instruction।

একাধিক statement:

```javascript
let name = "Ripon";
let age = 22;

console.log(name);
console.log(age);
```

Output:

```text
Ripon
22
```

---

# 20. Semicolon `;`

JavaScript statement-এর শেষে semicolon ব্যবহার করা যায়।

```javascript
let name = "Ripon";
console.log(name);
```

তবে JavaScript-এ অনেক ক্ষেত্রে semicolon optional, কারণ language-এর **Automatic Semicolon Insertion (ASI)** mechanism আছে।

তবুও consistent coding style-এর জন্য semicolon ব্যবহার করা অনেক project-এ common।

### Recommended beginner style

```javascript
let age = 22;
console.log(age);
```

---

# 21. Expressions

এখন Statement এবং Expression-এর difference বুঝি।

### Expression

**An expression is code that produces a value.**

Example:

```javascript
10 + 20
```

এর value:

```text
30
```

আর:

```javascript
5 * 10
```

এর value:

```text
50
```

Variable:

```javascript
let x = 10;
```

এখানে:

```javascript
10
```

একটি value।

আর:

```javascript
x + 5
```

একটি expression।

---

# 22. Statement vs Expression

সহজভাবে:

### Expression

যেটা একটি value produce করে।

```javascript
10 + 20
```

Result:

```text
30
```

### Statement

যেটা JavaScript-কে কোনো কাজ করার instruction দেয়।

```javascript
let result = 10 + 20;
```

এটা একটি statement।

এখানে:

```javascript
10 + 20
```

হলো expression।

---

# 23. `console.log()`

JavaScript শেখার সময় এটি অত্যন্ত important।

```javascript
console.log("Hello World");
```

এটি console-এ value দেখায়।

### Example

```javascript
console.log(10);
console.log("JavaScript");
console.log(true);
```

Output:

```text
10
JavaScript
true
```

একাধিক value:

```javascript
let name = "Ripon";
let age = 22;

console.log(name, age);
```

Output:

```text
Ripon 22
```

---

# 24. Variables

এখন JavaScript-এর অন্যতম important concept:

> **Variable**

### English

A variable is a named container/reference used to store or hold a value.

### বাংলা

Variable হলো এমন একটি নাম/identifier যার মাধ্যমে আমরা কোনো value ধরে রাখতে বা reference করতে পারি।

### Real-life example

ধরো তোমার কাছে একটা box আছে।

Box-এর label:

```text
name
```

Box-এর ভিতরে:

```text
Ripon
```

JavaScript:

```javascript
let name = "Ripon";
```

এখানে:

```text
name → variable
"Ripon" → value
```

---

# 25. Creating a Variable

JavaScript-এ variable তৈরি করার প্রধান keyword:

```javascript
var
let
const
```

Example:

```javascript
let name = "Ripon";

console.log(name);
```

Output:

```text
Ripon
```

---

# 26. `let`

`let` ব্যবহার করে এমন variable তৈরি করা যায় যার value পরে পরিবর্তন করা যেতে পারে।

```javascript
let age = 22;

console.log(age);

age = 23;

console.log(age);
```

Output:

```text
22
23
```

অর্থাৎ:

```text
age
 ↓
22

পরবর্তীতে

age
 ↓
23
```

---

# 27. `const`

`const` ব্যবহার করে এমন binding তৈরি করা হয় যেটাকে পরে reassign করা যায় না।

```javascript
const country = "Bangladesh";

console.log(country);
```

Output:

```text
Bangladesh
```

কিন্তু:

```javascript
const country = "Bangladesh";

country = "India";
```

এখানে error হবে।

কারণ `const` binding-কে আবার assign করা যায় না।

---

# 28. `var`

`var` হলো JavaScript-এর পুরোনো variable declaration keyword।

```javascript
var name = "Ripon";

console.log(name);
```

Output:

```text
Ripon
```

`var` এখনও language-এর অংশ, কিন্তু modern JavaScript code-এ সাধারণত নতুন code লেখার সময় `let` এবং `const` বেশি ব্যবহার করা হয়।

`var`-এর scope এবং hoisting behavior `let`/`const` থেকে আলাদা—এটা আমরা পরে **Scope & Hoisting** chapter-এ deeply দেখব।

---

# 29. `let` vs `const` vs `var`

| Feature              | `var`            | `let` | `const` |
| -------------------- | ---------------- | ----- | ------- |
| Modern code          | কম ব্যবহৃত       | বেশি  | বেশি    |
| Reassign             | ✅                | ✅     | ❌       |
| Block scoped         | ❌                | ✅     | ✅       |
| Redeclare same scope | সাধারণভাবে সম্ভব | ❌     | ❌       |
| Hoisting behavior    | আলাদা            | আলাদা | আলাদা   |

### Beginner Rule ⭐

সাধারণত:

```javascript
const
```

দিয়ে শুরু করবে।

যদি value পরে reassign করতে হয়:

```javascript
let
```

ব্যবহার করবে।

`var` আপাতত legacy behavior বোঝার জন্য শিখবে।

---

# 30. Variable Naming Rules

Variable name লেখার কিছু rules আছে।

### Valid:

```javascript
let name;
let userName;
let user_name;
let age2;
let $price;
let _value;
```

### Invalid:

```javascript
let 2age;
```

কারণ variable name number দিয়ে শুরু করা যায় না।

এটা invalid:

```javascript
let user-name;
```

কারণ `-` variable name-এর সাধারণ identifier অংশ নয়।

---

# 31. JavaScript Case Sensitive

JavaScript **case-sensitive**।

অর্থাৎ:

```javascript
name
```

এবং:

```javascript
Name
```

একই নয়।

Example:

```javascript
let name = "Ripon";

console.log(name);
console.log(Name);
```

প্রথমটি কাজ করবে, কিন্তু `Name` আলাদা identifier হওয়ায় error হবে যদি সেটি declare করা না থাকে।

### মনে রাখবে:

```text
name ≠ Name
name ≠ NAME
Name ≠ NAME
```

---

# 32. Naming Convention

JavaScript-এ সাধারণত **camelCase** convention খুব common।

### Good:

```javascript
let firstName = "Shariar";
let lastName = "Ahamed";
let userAge = 22;
let totalPrice = 500;
```

### Avoid:

```javascript
let firstname;
let FirstName;
let first_name;
```

`snake_case` valid হলেও JavaScript ecosystem-এ variable/function naming-এর ক্ষেত্রে camelCase খুব common।

---

# 33. Multiple Variables

একাধিক variable:

```javascript
let name = "Ripon";
let age = 22;
let country = "Bangladesh";

console.log(name);
console.log(age);
console.log(country);
```

Output:

```text
Ripon
22
Bangladesh
```

---

# 34. Variable Reassignment

`let`:

```javascript
let score = 50;

score = 80;

console.log(score);
```

Output:

```text
80
```

এখানে প্রথম value:

```text
50
```

পরে পরিবর্তন হয়ে:

```text
80
```

হয়েছে।

---

# 35. Constant Value

```javascript
const pi = 3.14159;

console.log(pi);
```

Output:

```text
3.14159
```

`const` ব্যবহার করলে পরে:

```javascript
pi = 4;
```

করা যাবে না।

---

# 36. Primitive Data Types — Introduction

JavaScript-এ বিভিন্ন ধরনের data/value আছে।

প্রধান primitive types:

```text
String
Number
BigInt
Boolean
Undefined
Null
Symbol
```

এবং একটি important non-primitive category:

```text
Object
```

এগুলো আমরা পরের chapter-এ একেকটা করে deeply দেখব।

এখন basic example:

```javascript
let name = "Ripon";       // String
let age = 22;             // Number
let isStudent = true;     // Boolean
let result;               // Undefined
let data = null;          // Null
```

---

# 37. `typeof`

কোন value কোন type-এর তা জানার জন্য:

```javascript
typeof
```

ব্যবহার করা হয়।

Example:

```javascript
console.log(typeof "Hello");
```

Output:

```text
string
```

আর:

```javascript
console.log(typeof 100);
```

Output:

```text
number
```

আর:

```javascript
console.log(typeof true);
```

Output:

```text
boolean
```

---

# 38. Complete `typeof` Example

```javascript
console.log(typeof "Ripon");
console.log(typeof 22);
console.log(typeof true);
console.log(typeof undefined);
console.log(typeof 123n);
```

Output:

```text
string
number
boolean
undefined
bigint
```

`null`-এর ক্ষেত্রে JavaScript-এর একটি historical quirk আছে:

```javascript
console.log(typeof null);
```

Output:

```text
object
```

এটা JavaScript-এর একটি well-known historical behavior; `null` আসলে সাধারণ অর্থে object নয়।

এটা পরে **Data Types** chapter-এ বিস্তারিত দেখব।

---

# 39. Basic JavaScript Example

এখন আমরা কয়েকটা concept একসাথে ব্যবহার করি।

```javascript
const name = "Shariar";
let age = 22;
const country = "Bangladesh";

console.log("Name:", name);
console.log("Age:", age);
console.log("Country:", country);
```

Output:

```text
Name: Shariar
Age: 22
Country: Bangladesh
```

এখানে আমরা ব্যবহার করেছি:

* `const`
* `let`
* String
* Number
* Variable
* `console.log()`

---

# 40. Mini Real-Life Example — Student Information

ধরো একটি student-এর information রাখতে হবে।

```javascript
const studentName = "Shariar Ahamed Ripon";
const studentId = "231-15-010";
let semester = 8;
const department = "CSE";

console.log("Student Name:", studentName);
console.log("Student ID:", studentId);
console.log("Semester:", semester);
console.log("Department:", department);
```

Output:

```text
Student Name: Shariar Ahamed Ripon
Student ID: 231-15-010
Semester: 8
Department: CSE
```

এটাই programming-এর basic idea:

> **Data → Store → Process → Output**

---

# 41. JavaScript-এর Basic Mental Model

এখন এই concept-টা মাথায় রাখো:

```text
          JavaScript
               │
               ↓
        Write Code
               │
               ↓
        JavaScript Engine
               │
               ↓
        Process / Execute
               │
               ↓
            Result
```

আর একটা website-এর ক্ষেত্রে:

```text
HTML
 ↓
Structure

CSS
 ↓
Design

JavaScript
 ↓
Behavior + Logic
```

এই তিনটা একসাথে:

```text
HTML + CSS + JavaScript
          ↓
      Web Application
```

---

# 🧠 Chapter 1 — Quick Revision

আজকের chapter-এ আমরা শিখলাম:

| Topic             | মূল কথা                                                |
| ----------------- | ------------------------------------------------------ |
| JavaScript        | Webpage-কে dynamic ও interactive করতে ব্যবহৃত language |
| ECMAScript        | JavaScript-এর standardized specification               |
| ES6               | ECMAScript 2015; modern JS-এর গুরুত্বপূর্ণ milestone   |
| JavaScript Engine | JavaScript code execute করে                            |
| V8                | Chrome ও Node.js-এর JavaScript engine                  |
| Browser           | JavaScript run করার একটি environment                   |
| Node.js           | Browser-এর বাইরে JavaScript runtime                    |
| `<script>`        | HTML-এর সাথে JS যুক্ত করার element                     |
| `defer`           | HTML parsing শেষের পর script execute করতে সাহায্য করে  |
| Comment           | Code explanation-এর জন্য                               |
| Statement         | JavaScript-এর instruction                              |
| Expression        | Value produce করে                                      |
| Variable          | Value/reference রাখার জন্য named binding               |
| `let`             | Reassign করা যায়                                      |
| `const`           | Reassign করা যায় না                                   |
| `var`             | পুরোনো variable declaration mechanism                  |
| `typeof`          | Value-এর type জানতে সাহায্য করে                        |
| Case Sensitive    | `name` এবং `Name` আলাদা                                |

---

# 📝 Chapter 1 Practice

নিজে হাতে এগুলো লিখে run করবে।

### Practice 1

তোমার:

* Name
* Age
* University
* Department
* Country

variable-এ store করো এবং `console.log()` দিয়ে print করো।

---

### Practice 2

এই values-এর type বের করো:

```javascript
"Hello"
100
true
undefined
null
123n
```

---

### Practice 3

একটি `let` variable তৈরি করো:

```text
score = 50
```

তারপর সেটাকে:

```text
80
```

এ পরিবর্তন করো।

---

### Practice 4

একটি `const` variable তৈরি করে পরে পরিবর্তন করার চেষ্টা করো এবং browser console-এ কী error আসে দেখো।

---

### Practice 5 — Mini Project

Student information system:

```text
Name
ID
Department
Semester
CGPA
University
```

সব data variable-এ রাখবে এবং সুন্দরভাবে console-এ print করবে।

---

## ⭐ Chapter 1-এর সবচেয়ে গুরুত্বপূর্ণ takeaway

এখন আপাতত এই flow-টা মাথায় ভালোভাবে বসাও:

```text
JavaScript
   ↓
Variables
   ↓
Data
   ↓
Expressions
   ↓
Statements
   ↓
JavaScript Engine
   ↓
Execution
   ↓
Output
```

**Chapter 2-এ আমরা JavaScript-এর `Variables, Data Types & Type System` আরও গভীরভাবে ধরব**—`String`, `Number`, `Boolean`, `Undefined`, `Null`, `BigInt`, `Symbol`, `Object`, `typeof`, primitive vs non-primitive, memory/reference ধারণা, এবং type conversion/coercion ধাপে ধাপে code + output সহ।
