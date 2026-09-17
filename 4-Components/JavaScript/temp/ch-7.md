# 📘 JavaScript Complete Book — Chapter 7

# Scope & Hoisting — Scope এবং Hoisting

Chapter 6-এ আমরা **Functions** শিখেছি। এখন JavaScript-এর খুব গুরুত্বপূর্ণ একটি বিষয় হলো **Scope** এবং **Hoisting**।

এই chapter ভালোভাবে বুঝলে পরবর্তীতে **Closures, Modules, Async JavaScript, React, Node.js**—সবকিছু বুঝতে অনেক সহজ হবে।

---

# 7.1 Scope কী?

**Scope** মানে হলো—কোন variable বা function-কে **কোথা থেকে access করা যাবে**, সেই সীমা বা area।

সহজভাবে:

> **Scope = কোন জায়গা থেকে কোন variable ব্যবহার করা যাবে।**

### 🌍 Real-life Example

ধরো একটি বিশ্ববিদ্যালয়ে:

* University-এর main gate → সবাই access করতে পারে
* Department-এর room → শুধু department-এর মানুষ
* Teacher's personal room → আরও limited access

JavaScript-এও variable-এর access একইভাবে সীমাবদ্ধ হতে পারে।

---

# 7.2 JavaScript-এ Scope-এর প্রধান ধরন

JavaScript-এ আমরা প্রধানত এগুলো দেখতে পাই:

1. Global Scope
2. Function Scope
3. Block Scope
4. Lexical Scope
5. Module Scope

---

# 7.3 Global Scope

যে variable কোনো function বা block-এর বাইরে declare করা হয়, সেটি সাধারণত **Global Scope**-এ থাকে।

### Code

```javascript
let name = "Shariar";

function showName() {
    console.log(name);
}

showName();
console.log(name);
```

### Output

```text
Shariar
Shariar
```

### Explanation

```javascript
let name = "Shariar";
```

এটি function-এর বাইরে আছে।

তাই function-এর ভেতর থেকেও:

```javascript
console.log(name);
```

access করা যাচ্ছে।

### Real-life Example

University-এর notice board-এ যদি কোনো notice দেওয়া থাকে, তাহলে অনেক department-এর মানুষ সেটা দেখতে পারে।

ঠিক তেমনি global variable অনেক জায়গা থেকে accessible হতে পারে।

---

# 7.4 Global Variable-এর সমস্যা

Global variable বেশি ব্যবহার করা ভালো practice নয়।

```javascript
let username = "Ripon";

function changeName() {
    username = "Shariar";
}

changeName();

console.log(username);
```

### Output

```text
Shariar
```

Function-এর ভিতর থেকে global variable পরিবর্তন হয়ে গেছে।

বড় application-এ এমন অনেক global variable থাকলে debugging কঠিন হয়ে যেতে পারে।

---

# 7.5 Function Scope

কোনো variable যদি function-এর ভিতরে declare করা হয়, তাহলে সেটি সাধারণত সেই function-এর মধ্যেই accessible।

```javascript
function test() {
    let message = "Hello JavaScript";

    console.log(message);
}

test();
```

### Output

```text
Hello JavaScript
```

কিন্তু:

```javascript
function test() {
    let message = "Hello JavaScript";
}

test();

console.log(message);
```

### Output

```text
ReferenceError
```

কারণ `message` function-এর বাইরে accessible নয়।

---

# 7.6 `var` এবং Function Scope

`var` হলো function-scoped।

```javascript
function test() {
    var x = 10;

    if (true) {
        var x = 20;
    }

    console.log(x);
}

test();
```

### Output

```text
20
```

কারণ `var` block scope মানে না।

---

# 7.7 Block Scope

`{ }` দ্বারা তৈরি block-এর ভিতরে থাকা scope-কে **Block Scope** বলা হয়।

উদাহরণ:

```javascript
if (true) {
    let message = "Hello";
    console.log(message);
}
```

### Output

```text
Hello
```

কিন্তু:

```javascript
if (true) {
    let message = "Hello";
}

console.log(message);
```

### Output

```text
ReferenceError
```

কারণ `message` শুধু ওই block-এর ভিতরে accessible।

---

# 7.8 `let` এবং `const` হলো Block Scoped

```javascript
if (true) {
    let a = 10;
    const b = 20;

    console.log(a);
    console.log(b);
}
```

### Output

```text
10
20
```

কিন্তু বাইরে:

```javascript
console.log(a);
console.log(b);
```

access করা যাবে না।

---

# 7.9 `var` vs `let` vs `const`

| Feature              | `var`    | `let` | `const` |
| -------------------- | -------- | ----- | ------- |
| Scope                | Function | Block | Block   |
| Reassign             | ✅        | ✅     | ❌       |
| Redeclare same scope | ✅        | ❌     | ❌       |
| Hoisted              | ✅        | ✅*    | ✅*      |
| TDZ                  | ❌        | ✅     | ✅       |

`*` এখানে hoisting হয়, কিন্তু `let`/`const` declaration initialization-এর আগে access করা যায় না।

এটা আমরা একটু পরেই বিস্তারিত দেখব।

---

# 7.10 Block Scope-এর Real-life Example

ধরো একটি company-তে:

```text
Company
│
├── HR Department
│
├── Development Department
│
└── Marketing Department
```

Development department-এর private variable Marketing department সরাসরি ব্যবহার করতে পারবে না।

JavaScript:

```javascript
{
    let developer = "Ripon";
}

console.log(developer);
```

এখানে `developer` block-এর বাইরে পাওয়া যাবে না।

---

# 7.11 Nested Scope

একটি scope-এর ভিতরে আরেকটি scope থাকতে পারে।

```javascript
let university = "DIU";

function department() {

    let dept = "CSE";

    function student() {

        let studentName = "Ripon";

        console.log(university);
        console.log(dept);
        console.log(studentName);
    }

    student();
}

department();
```

### Output

```text
DIU
CSE
Ripon
```

এখানে:

```text
Global Scope
    ↓
department Scope
    ↓
student Scope
```

---

# 7.12 Scope Chain

JavaScript কোনো variable খুঁজলে প্রথমে **বর্তমান scope**-এ খোঁজে।

না পেলে outer scope-এ যায়।

আবার না পেলে আরও outer scope-এ যায়।

এটাকে বলা হয়:

> **Scope Chain**

### Example

```javascript
let university = "DIU";

function department() {

    let dept = "CSE";

    function student() {

        let name = "Ripon";

        console.log(name);
        console.log(dept);
        console.log(university);
    }

    student();
}

department();
```

JavaScript `name` খুঁজবে:

```text
student scope
    ↓
department scope
    ↓
global scope
```

---

# 7.13 Scope Chain Real-life Example

ধরো তুমি তোমার room-এ একটি mobile খুঁজছো।

প্রথমে:

```text
নিজের Room
```

না পেলে:

```text
বাসার অন্য জায়গা
```

তারপর:

```text
অন্য জায়গা
```

JavaScript variable খোঁজার ক্ষেত্রেও একই ধরনের ধারণা কাজ করে।

---

# 7.14 Inner Scope → Outer Scope Access

Inner scope outer variable access করতে পারে।

```javascript
let x = 10;

function test() {

    let y = 20;

    console.log(x);
    console.log(y);
}

test();
```

### Output

```text
10
20
```

কিন্তু outer scope inner variable access করতে পারে না।

```javascript
function test() {
    let y = 20;
}

test();

console.log(y);
```

### Output

```text
ReferenceError
```

---

# 7.15 Lexical Scope

JavaScript-এর scope **code কোথায় লেখা হয়েছে** তার ওপর নির্ভর করে।

এটাকে বলা হয়:

> **Lexical Scope**

### Example

```javascript
let name = "Ripon";

function outer() {

    let university = "DIU";

    function inner() {
        console.log(name);
        console.log(university);
    }

    inner();
}

outer();
```

`inner()` function যেখানে লেখা হয়েছে, সেই জায়গার lexical environment অনুযায়ী সে outer variable access করতে পারে।

---

# 7.16 Important: Function কোথায় Call করা হচ্ছে সেটা নয়

JavaScript lexical scope follow করে।

```javascript
let x = "Global";

function show() {
    console.log(x);
}

function test() {
    let x = "Local";
    show();
}

test();
```

### Output

```text
Global
```

অনেকে ভাবতে পারে:

```text
test()
  ↓
show()
```

তাই `show()` local `x` পাবে।

কিন্তু তা নয়।

`show()` কোথায় **defined** হয়েছে সেটাই গুরুত্বপূর্ণ।

---

# 7.17 Shadowing

Outer scope এবং inner scope-এ একই নামের variable থাকলে inner variable outer variable-কে **shadow** করতে পারে।

```javascript
let name = "Global";

function test() {

    let name = "Local";

    console.log(name);
}

test();

console.log(name);
```

### Output

```text
Local
Global
```

### কী হলো?

Function-এর ভিতরের:

```javascript
let name = "Local";
```

outer:

```javascript
let name = "Global";
```

কে shadow করেছে।

---

# 7.18 Real-life Shadowing Example

ধরো:

```text
University Name = DIU
Department Name = CSE
```

কোনো department-এর ভিতরে আবার:

```text
Department Name = SWE
```

Department-এর ভিতরে জিজ্ঞেস করলে local নাম পাওয়া যাবে।

---

# 7.19 Illegal Shadowing

`let` এবং `var` একসাথে কিছু scope situation-এ conflict করতে পারে।

```javascript
let x = 10;

{
    var x = 20;
}
```

এটি error দেবে।

কারণ `var` block scope মানে না এবং একই scope binding conflict তৈরি করে।

---

# 7.20 Hoisting কী?

এখন আসি JavaScript-এর খুব famous concept:

# 🚀 Hoisting

সহজ ভাষায়:

> JavaScript execution শুরু হওয়ার আগে কিছু declaration-এর জন্য memory setup করে রাখে।

তাই কিছু ক্ষেত্রে declaration-এর আগে code লিখলেও JavaScript error না দিয়ে কাজ করতে পারে।

---

# 7.21 `var` Hoisting

দেখো:

```javascript
console.log(x);

var x = 10;
```

### Output

```text
undefined
```

এখানে error হয়নি।

Conceptually JavaScript এটাকে এমনভাবে দেখে:

```javascript
var x;

console.log(x);

x = 10;
```

তাই প্রথমে `x`-এর value:

```text
undefined
```

---

# 7.22 `let` Hoisting

এবার:

```javascript
console.log(x);

let x = 10;
```

### Output

```text
ReferenceError
```

অনেকে বলে:

> "`let` hoist হয় না।"

এটি পুরোপুরি accurate নয়।

`let` declaration-ও execution context তৈরি হওয়ার সময় binding পায়, কিন্তু initialization-এর আগে access করা যায় না।

এই সময়টাকে বলা হয়:

# Temporal Dead Zone — TDZ

---

# 7.23 Temporal Dead Zone — TDZ

**TDZ** হলো:

> `let` বা `const` declaration শুরু হওয়ার আগের সেই সময়, যখন variable-কে access করলে error হয়।

### Example

```javascript
console.log(name);

let name = "Ripon";
```

`name` declaration-এর আগে access করা হয়েছে।

তাই:

```text
ReferenceError
```

---

# 7.24 TDZ Visual

```text
let name = "Ripon";

        ↑
        |
   Declaration
```

Declaration-এর আগে:

```text
TDZ
```

Declaration-এর পরে:

```text
Accessible
```

---

# 7.25 `const` এবং Hoisting

```javascript
console.log(age);

const age = 23;
```

### Output

```text
ReferenceError
```

কারণ `const`-ও TDZ-এর মধ্যে থাকে declaration-এর আগে।

---

# 7.26 Function Declaration Hoisting

Function declaration hoisted হয়।

```javascript
sayHello();

function sayHello() {
    console.log("Hello!");
}
```

### Output

```text
Hello!
```

এটি কাজ করে।

---

# 7.27 Function Expression Hoisting

কিন্তু:

```javascript
sayHello();

const sayHello = function () {
    console.log("Hello!");
};
```

### Output

```text
ReferenceError
```

কারণ এখানে `sayHello` একটি `const` variable-এর মধ্যে function রাখা হয়েছে।

---

# 7.28 `var` দিয়ে Function Expression

```javascript
sayHello();

var sayHello = function () {
    console.log("Hello!");
};
```

এখানে সাধারণত:

```text
TypeError: sayHello is not a function
```

কারণ conceptually:

```javascript
var sayHello;

sayHello();

sayHello = function () {
    console.log("Hello!");
};
```

Call করার সময় `sayHello`-এর value এখনো function হয়নি।

---

# 7.29 Hoisting Summary

### `var`

```javascript
console.log(x);
var x = 10;
```

Output:

```text
undefined
```

### `let`

```javascript
console.log(x);
let x = 10;
```

Output:

```text
ReferenceError
```

### `const`

```javascript
console.log(x);
const x = 10;
```

Output:

```text
ReferenceError
```

### Function Declaration

```javascript
hello();

function hello() {
    console.log("Hello");
}
```

Output:

```text
Hello
```

---

# 7.30 Declaration বনাম Initialization

এই দুইটা একই জিনিস নয়।

```javascript
let age = 23;
```

এখানে:

```text
let age
```

= Declaration

আর:

```text
age = 23
```

= Initialization/Assignment

সহজভাবে:

> Declaration = variable-এর নাম তৈরি করা
> Initialization = প্রথম value দেওয়া

---

# 7.31 Hoisting-এর সময় `var`

```javascript
var age = 23;
```

Conceptually:

```javascript
var age;   // declaration

age = 23;  // initialization
```

Hoisting-এর কারণে declaration অংশ আগে setup হয়।

---

# 7.32 `var` Redeclaration

```javascript
var x = 10;

var x = 20;

console.log(x);
```

### Output

```text
20
```

`var` একই scope-এ redeclare করতে পারে।

---

# 7.33 `let` Redeclaration

```javascript
let x = 10;

let x = 20;
```

### Output

```text
SyntaxError
```

একই scope-এ `let` redeclare করা যায় না।

---

# 7.34 `const` Redeclaration

```javascript
const x = 10;

const x = 20;
```

এটিও:

```text
SyntaxError
```

---

# 7.35 `let` Reassignment

```javascript
let age = 23;

age = 24;

console.log(age);
```

### Output

```text
24
```

`let` reassign করা যায়।

---

# 7.36 `const` Reassignment

```javascript
const age = 23;

age = 24;
```

### Output

```text
TypeError
```

কারণ `const` binding reassign করা যায় না।

---

# 7.37 কিন্তু `const` Object পরিবর্তন করা যায় কেন?

এটা খুব গুরুত্বপূর্ণ।

```javascript
const user = {
    name: "Ripon"
};

user.name = "Shariar";

console.log(user.name);
```

### Output

```text
Shariar
```

কারণ `const` object-এর reference পরিবর্তন করতে দেয় না, কিন্তু object-এর property পরিবর্তন করা যায়।

---

# 7.38 Example

এটা করা যাবে না:

```javascript
const user = {
    name: "Ripon"
};

user = {
    name: "Shariar"
};
```

কারণ পুরো reference পরিবর্তন করা হচ্ছে।

কিন্তু:

```javascript
user.name = "Shariar";
```

allowed।

---

# 7.39 Global Scope বনাম Block Scope

```javascript
let name = "Global";

if (true) {

    let name = "Block";

    console.log(name);
}

console.log(name);
```

### Output

```text
Block
Global
```

---

# 7.40 Function Scope বনাম Block Scope

```javascript
function test() {

    if (true) {
        var a = 10;
        let b = 20;
    }

    console.log(a);
    console.log(b);
}

test();
```

### Output

```text
10
ReferenceError
```

কারণ:

```text
var → function scoped
let → block scoped
```

---

# 7.41 Scope + Hoisting একসাথে

এখন একটি গুরুত্বপূর্ণ example:

```javascript
var x = 10;

function test() {

    console.log(x);

    var x = 20;

    console.log(x);
}

test();
```

অনেকে ভাবতে পারে প্রথম `console.log(x)` এ `10` আসবে।

কিন্তু output:

```text
undefined
20
```

কেন?

কারণ function-এর ভিতরের:

```javascript
var x;
```

hoisted হয়ে যায়।

Conceptually:

```javascript
var x = 10;

function test() {

    var x;

    console.log(x);

    x = 20;

    console.log(x);
}

test();
```

---

# 7.42 খুব গুরুত্বপূর্ণ Interview Question

### Question:

Output কী হবে?

```javascript
var x = 10;

function test() {

    console.log(x);

    var x = 20;
}

test();
```

### Answer:

```text
undefined
```

### কারণ:

Function scope-এর local `x` hoisted হয়েছে।

---

# 7.43 `let` দিয়ে একই Example

```javascript
let x = 10;

function test() {

    console.log(x);

    let x = 20;
}

test();
```

### Output

```text
ReferenceError
```

কারণ local `x` TDZ-এর মধ্যে রয়েছে।

---

# 7.44 Scope-এর Golden Rule 🏆

মনে রাখবে:

```text
Global
   ↓
Outer Function
   ↓
Inner Function
   ↓
Block
```

Inner scope সাধারণত outer scope access করতে পারে।

কিন্তু outer scope inner scope-এর variable সরাসরি access করতে পারে না।

---

# 7.45 Scope-এর Real-life Full Example

ধরো একটি e-commerce website:

```javascript
let shopName = "Tech Shop";

function customer() {

    let customerName = "Ripon";

    function order() {

        let product = "Laptop";

        console.log(shopName);
        console.log(customerName);
        console.log(product);
    }

    order();
}

customer();
```

### Output

```text
Tech Shop
Ripon
Laptop
```

এখানে:

```text
Global
  shopName

customer()
  customerName

order()
  product
```

`order()` সব outer scope access করতে পারে।

---

# 7.46 কেন Scope গুরুত্বপূর্ণ?

Real-world application-এ scope ব্যবহার হয়:

### 1. Data protection

সব variable global না রেখে নির্দিষ্ট জায়গায় রাখা যায়।

### 2. Name conflict কমানো

```javascript
let name = "A";
```

অন্য scope-এ আবার:

```javascript
let name = "B";
```

থাকতে পারে।

### 3. Code maintainability

বড় project-এ কোন variable কোথায় ব্যবহার করা যাবে তা পরিষ্কার থাকে।

### 4. Security/encapsulation

Internal data বাইরে expose না করে রাখা যায়।

---

# 7.47 Best Practice

Modern JavaScript-এ সাধারণত:

```javascript
const
```

প্রথম পছন্দ।

Value পরিবর্তন করতে হলে:

```javascript
let
```

আর:

```javascript
var
```

সাধারণত avoid করা হয় modern code-এ।

### Example

❌ পুরোনো style:

```javascript
var username = "Ripon";
```

✅ Modern:

```javascript
const username = "Ripon";
```

যদি value পরিবর্তন হয়:

```javascript
let score = 0;

score = 10;
```

---

# 🧠 Quick Cheat Sheet

| Concept        | সহজ অর্থ                                              |
| -------------- | ----------------------------------------------------- |
| Scope          | Variable কোথায় accessible                             |
| Global Scope   | প্রায় পুরো script/module-এর top-level scope           |
| Function Scope | Function-এর ভিতরের scope                              |
| Block Scope    | `{ }` block-এর scope                                  |
| Scope Chain    | এক scope থেকে outer scope-এ variable খোঁজা            |
| Lexical Scope  | Code কোথায় লেখা হয়েছে তার ভিত্তিতে scope              |
| Shadowing      | Inner variable outer variable-কে আড়াল করে             |
| Hoisting       | Execution-এর আগে declaration setup                    |
| TDZ            | `let`/`const` declaration-এর আগের inaccessible period |
| `var`          | Function scoped                                       |
| `let`          | Block scoped                                          |
| `const`        | Block scoped + reassignment করা যায় না                |

---

# 🔥 Chapter 7 — Must Know

এই chapter থেকে অবশ্যই এগুলো ভালোভাবে জানতে হবে:

```text
1. Scope কী?
2. Global Scope
3. Function Scope
4. Block Scope
5. var vs let vs const
6. Nested Scope
7. Scope Chain
8. Lexical Scope
9. Shadowing
10. Hoisting
11. var Hoisting
12. let/const + TDZ
13. Function Hoisting
14. Function Declaration vs Function Expression
15. Declaration vs Initialization
```

---

# 📝 Practice Set

### Practice 1

Output কী হবে?

```javascript
let x = 10;

function test() {
    let x = 20;
    console.log(x);
}

test();
console.log(x);
```

---

### Practice 2

Output কী হবে?

```javascript
var x = 10;

if (true) {
    var x = 20;
}

console.log(x);
```

---

### Practice 3

Output কী হবে?

```javascript
let x = 10;

if (true) {
    let x = 20;
    console.log(x);
}

console.log(x);
```

---

### Practice 4

Output কী হবে?

```javascript
console.log(a);

var a = 100;
```

---

### Practice 5

Output কী হবে?

```javascript
console.log(a);

let a = 100;
```

---

### Practice 6

Output কী হবে?

```javascript
hello();

function hello() {
    console.log("Hello JavaScript");
}
```

---

### Practice 7

Output কী হবে?

```javascript
var x = 10;

function test() {
    console.log(x);

    var x = 20;
}

test();
```

---

### Practice 8

এই code-এ error কেন হচ্ছে?

```javascript
function test() {
    let name = "Ripon";
}

test();

console.log(name);
```

---

## 🎯 Chapter 7-এর মূল ধারণা এক লাইনে

> **Scope বলে variable কোথায় ব্যবহার করা যাবে, আর Hoisting বোঝায় JavaScript execution-এর আগে declaration কীভাবে setup করে।**

পরের chapter হবে:

# 📘 Chapter 8 — Strings

**String তৈরি → indexing → length → methods → slicing → searching → replacing → splitting → joining → template literals → escape characters → Unicode → string immutability → practical projects**.
