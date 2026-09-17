# 📘 JavaScript Complete Book

# Chapter 2 — Variables, Data Types & Type System

### JavaScript-এর Data কীভাবে কাজ করে

Chapter 1-এ আমরা JavaScript কী, কীভাবে run করে, variable কী এবং `let`, `const`, `var` সম্পর্কে basic ধারণা নিয়েছি।

এখন আমরা JavaScript-এর **সবচেয়ে গুরুত্বপূর্ণ foundation-এর একটি — Data Types & Type System** শিখব।

এই chapter ভালোভাবে বুঝলে পরের chapter-এর **Operators, Conditions, Functions, Arrays, Objects, DOM, API**—সবকিছু বুঝতে অনেক সহজ হবে।

---

# 1. What is Data?

### English

**Data is information that a program can store, process, and use.**

### বাংলা

Data হলো এমন information যেটা একটি program store, process বা ব্যবহার করতে পারে।

### Real-life Example

একজন student-এর:

```text
Name       → "Ripon"
Age        → 22
CGPA       → 3.75
Student    → true
```

এগুলো সবই data।

JavaScript-এ:

```javascript
const name = "Ripon";
const age = 22;
const cgpa = 3.75;
const isStudent = true;
```

এখানে JavaScript বিভিন্ন ধরনের data নিয়ে কাজ করছে।

---

# 2. What is a Data Type?

### English

**A data type defines what kind of value a piece of data is and what operations can be performed on it.**

### বাংলা

Data Type বলে দেয় কোনো value **কী ধরনের data** এবং সেই data-এর সাথে কী ধরনের কাজ করা যায়।

উদাহরণ:

```javascript
"Hello"
```

এটা String।

```javascript
100
```

এটা Number।

```javascript
true
```

এটা Boolean।

---

# 3. JavaScript Data Types

JavaScript-এ data types-কে broadly দুই ভাগে দেখা হয়:

```text
Data Types
│
├── Primitive
│
└── Non-Primitive / Reference
```

### Primitive Types

JavaScript-এর প্রধান 7টি primitive type:

1. String
2. Number
3. BigInt
4. Boolean
5. Undefined
6. Null
7. Symbol

### Non-Primitive

মূলত:

8. Object

এর মধ্যে:

* Object
* Array
* Function
* Date
* Map
* Set
* ইত্যাদি object-based values রয়েছে।

---

# 4. Primitive vs Non-Primitive

এটা খুব important concept।

## Primitive

Primitive value হলো JavaScript-এর basic, immutable value type।

উদাহরণ:

```javascript
const name = "Ripon";
const age = 22;
const isStudent = true;
```

## Non-Primitive

Non-primitive values মূলত object/reference-based।

```javascript
const student = {
    name: "Ripon",
    age: 22
};
```

### সহজভাবে:

```text
Primitive
   ↓
Single/basic value

Non-Primitive
   ↓
Collection / structured value
```

---

# 5. String

### English

**A String is a sequence of characters used to represent text.**

### বাংলা

String হলো text বা character-এর sequence।

Example:

```javascript
const name = "Ripon";
```

এখানে:

```text
"Ripon"
```

একটি String।

---

# 6. String লেখার উপায়

JavaScript-এ String তিনভাবে লেখা যায়।

### Double Quotes

```javascript
const name = "Ripon";
```

### Single Quotes

```javascript
const name = 'Ripon';
```

### Backticks

```javascript
const name = `Ripon`;
```

তিনটিই valid।

---

# 7. String Example

```javascript
const firstName = "Shariar";
const lastName = "Ahamed";

console.log(firstName);
console.log(lastName);
```

Output:

```text
Shariar
Ahamed
```

---

# 8. String Concatenation

দুই বা তার বেশি String combine করা যায়।

```javascript
const firstName = "Shariar";
const lastName = "Ahamed";

const fullName = firstName + " " + lastName;

console.log(fullName);
```

Output:

```text
Shariar Ahamed
```

এখানে `+` String concatenate করেছে।

---

# 9. Template Literal

Modern JavaScript-এ String-এর মধ্যে variable বসানোর জন্য template literal খুব useful।

```javascript
const name = "Ripon";
const age = 22;

console.log(`My name is ${name} and I am ${age} years old.`);
```

Output:

```text
My name is Ripon and I am 22 years old.
```

এখানে:

```javascript
${name}
```

এর জায়গায় `name` variable-এর value বসবে।

এটা আমরা পরে **Template Literals** section-এ আরও বিস্তারিত করব।

---

# 10. Number

JavaScript-এর `Number` type integer এবং floating-point number—দুটোই represent করতে পারে।

### Integer

```javascript
const age = 22;
```

### Decimal

```javascript
const cgpa = 3.75;
```

### Negative

```javascript
const temperature = -5;
```

সবগুলোই `number`।

---

# 11. Number Example

```javascript
const age = 22;
const price = 499.99;
const temperature = -10;

console.log(age);
console.log(price);
console.log(temperature);
```

Output:

```text
22
499.99
-10
```

---

# 12. Checking Number Type

```javascript
console.log(typeof 100);
```

Output:

```text
number
```

আর:

```javascript
console.log(typeof 3.14);
```

Output:

```text
number
```

---

# 13. Special Number Values

JavaScript-এর `Number` type-এর মধ্যে কিছু special value রয়েছে।

যেমন:

```text
Infinity
-Infinity
NaN
```

---

# 14. Infinity

```javascript
console.log(10 / 0);
```

Output:

```text
Infinity
```

JavaScript এটাকে error হিসেবে না দেখে `Infinity` value হিসেবে represent করতে পারে।

---

# 15. `NaN`

`NaN` মানে:

> **Not a Number**

Example:

```javascript
console.log("Hello" * 5);
```

Output:

```text
NaN
```

কারণ `"Hello"`-কে meaningful numeric multiplication-এ ব্যবহার করা যায় না।

আর:

```javascript
console.log(Number("abc"));
```

Output:

```text
NaN
```

---

# 16. Important: `NaN` Type

নাম `NaN` হলেও:

```javascript
console.log(typeof NaN);
```

Output:

```text
number
```

এটা beginner-দের কাছে weird মনে হতে পারে।

কারণ JavaScript-এর specification অনুযায়ী `NaN` হলো `Number` type-এর একটি special numeric value।

---

# 17. Boolean

Boolean-এর মাত্র দুটি value:

```text
true
false
```

### Example

```javascript
const isLoggedIn = true;
const isAdmin = false;

console.log(isLoggedIn);
console.log(isAdmin);
```

Output:

```text
true
false
```

Boolean মূলত decision making-এর ক্ষেত্রে খুব গুরুত্বপূর্ণ।

---

# 18. Real-Life Boolean Example

ধরো website-এ user login করেছে কিনা:

```javascript
const isLoggedIn = true;

if (isLoggedIn) {
    console.log("Welcome back!");
}
```

Output:

```text
Welcome back!
```

`if` সম্পর্কে আমরা পরের chapter-গুলোতে বিস্তারিত শিখব।

---

# 19. Undefined

একটি variable declare করা হয়েছে কিন্তু value দেওয়া হয়নি:

```javascript
let name;

console.log(name);
```

Output:

```text
undefined
```

অর্থাৎ variable আছে, কিন্তু এখনো কোনো value assigned হয়নি।

---

# 20. `undefined` Example

```javascript
let result;

console.log(result);
console.log(typeof result);
```

Output:

```text
undefined
undefined
```

কারণ:

```text
value → undefined
type  → undefined
```

---

# 21. Null

`null` মানে সাধারণভাবে:

> **Intentionally empty / no value**

অর্থাৎ programmer ইচ্ছা করে বলছে:

> এখানে এখন কোনো value নেই।

Example:

```javascript
let selectedUser = null;

console.log(selectedUser);
```

Output:

```text
null
```

---

# 22. `undefined` vs `null`

এই difference খুব গুরুত্বপূর্ণ।

### Undefined

Value দেওয়া হয়নি।

```javascript
let user;
```

### Null

ইচ্ছা করে empty value রাখা হয়েছে।

```javascript
let user = null;
```

### সহজ example

```text
undefined
→ "আমি এখনো কিছু পাইনি।"

null
→ "আমি ইচ্ছা করে বলছি এখানে কোনো value নেই।"
```

---

# 23. `typeof null`

এখানে JavaScript-এর একটি historical quirk আছে:

```javascript
console.log(typeof null);
```

Output:

```text
object
```

যদিও `null`-কে সাধারণভাবে object হিসেবে ব্যবহার করা হয় না।

এটা JavaScript-এর পুরোনো behavior, এবং language compatibility-এর কারণে থেকে গেছে।

এটা interview-এও জিজ্ঞেস করা হতে পারে।

---

# 24. BigInt

JavaScript-এর `Number` type সব integer precision-এর জন্য যথেষ্ট নয়।

অনেক বড় integer represent করার জন্য `BigInt` ব্যবহার করা যায়।

Example:

```javascript
const bigNumber = 123456789012345678901234567890n;

console.log(bigNumber);
```

Output:

```text
123456789012345678901234567890n
```

শেষে `n` থাকলে সেটা BigInt literal।

---

# 25. BigInt Type

```javascript
const number = 12345678901234567890n;

console.log(typeof number);
```

Output:

```text
bigint
```

### Important

BigInt এবং Number এক জিনিস নয়।

```javascript
const a = 10n;
const b = 20n;

console.log(a + b);
```

Output:

```text
30n
```

কিন্তু:

```javascript
const a = 10n;
const b = 20;

console.log(a + b);
```

এতে সাধারণভাবে TypeError হবে, কারণ BigInt এবং Number সরাসরি arithmetic-এ mix করা যায় না।

---

# 26. Symbol

`Symbol` হলো JavaScript-এর একটি unique primitive value।

Example:

```javascript
const id = Symbol("id");

console.log(id);
```

Symbol সাধারণত unique identifiers তৈরি করতে useful।

---

# 27. Symbols are Unique

দেখো:

```javascript
const a = Symbol("id");
const b = Symbol("id");

console.log(a === b);
```

Output:

```text
false
```

যদিও description একই:

```text
"id"
```

তবুও দুটো Symbol আলাদা।

### সহজভাবে:

```text
Symbol("id") ≠ Symbol("id")
```

এটা advanced JavaScript-এ বিশেষভাবে কাজে লাগে।

---

# 28. Object

এখন আসি Non-Primitive-এর দিকে।

Object হলো related data এবং functionality organize করার একটি structure।

Example:

```javascript
const student = {
    name: "Ripon",
    age: 22,
    department: "CSE"
};
```

এখানে `student` একটি object।

এর মধ্যে রয়েছে:

```text
name
age
department
```

---

# 29. Object Data Access

```javascript
const student = {
    name: "Ripon",
    age: 22
};

console.log(student.name);
console.log(student.age);
```

Output:

```text
Ripon
22
```

Object নিয়ে আমরা পরে আলাদা বিশাল chapter করব।

---

# 30. Array

Array হলো একাধিক value ordered collection হিসেবে রাখার জন্য ব্যবহৃত structure।

```javascript
const fruits = ["Apple", "Mango", "Banana"];

console.log(fruits);
```

Output:

```text
["Apple", "Mango", "Banana"]
```

Array-এর প্রতিটি element-এর index থাকে।

```text
Apple   → 0
Mango   → 1
Banana  → 2
```

---

# 31. Array is an Object

এটা interesting:

```javascript
const fruits = ["Apple", "Mango"];

console.log(typeof fruits);
```

Output:

```text
object
```

কারণ JavaScript-এ Array হলো object-এর একটি specialized form।

Array আমরা পরে আলাদা chapter-এ অনেক গভীরভাবে শিখব।

---

# 32. Function

Function হলো reusable block of code।

Example:

```javascript
function greet() {
    console.log("Hello!");
}

greet();
```

Output:

```text
Hello!
```

JavaScript-এ function-ও একটি object-এর মতো value হিসেবে ব্যবহার করা যায়।

```javascript
function greet() {
    console.log("Hello");
}

console.log(typeof greet);
```

Output:

```text
function
```

`typeof` এখানে `"function"` return করে।

---

# 33. Primitive Data Types — Full List

এখন 7টি primitive একসাথে:

```javascript
const name = "Ripon";              // String
const age = 22;                    // Number
const huge = 123456789n;           // BigInt
const isStudent = true;            // Boolean
let result;                        // Undefined
const empty = null;                // Null
const id = Symbol("id");           // Symbol
```

---

# 34. `typeof` Cheat Sheet

| Value          | `typeof`      |
| -------------- | ------------- |
| `"Hello"`      | `"string"`    |
| `100`          | `"number"`    |
| `10n`          | `"bigint"`    |
| `true`         | `"boolean"`   |
| `undefined`    | `"undefined"` |
| `null`         | `"object"`    |
| `{}`           | `"object"`    |
| `[]`           | `"object"`    |
| `function(){}` | `"function"`  |

### ⚠️ Important

`typeof null === "object"` — এটা JavaScript-এর historical quirk।

---

# 35. Static vs Dynamic Typing

JavaScript একটি **dynamically typed language**।

এর অর্থ variable-এর type আলাদা করে declare করতে হয় না এবং একই variable-এ পরে অন্য ধরনের value assign করা যায়।

Example:

```javascript
let value = 100;

console.log(typeof value);

value = "Hello";

console.log(typeof value);
```

Output:

```text
number
string
```

একই variable:

```text
value
 ↓
100
 ↓
"Hello"
```

---

# 36. JavaScript-এ Type Declaration

JavaScript-এ সাধারণত এভাবে লিখি না:

```text
int age = 22;
```

বরং:

```javascript
let age = 22;
```

JavaScript নিজেই বুঝে নেয় value-এর type কী।

---

# 37. Dynamic Typing-এর Real-Life Example

ধরো shopping app:

```javascript
let product = 500;

console.log(product);

product = "Out of Stock";

console.log(product);
```

Output:

```text
500
Out of Stock
```

একই variable বিভিন্ন সময়ে different type-এর value রাখতে পারে।

বাস্তব project-এ অবশ্য variable-এর meaning stable রাখা এবং clear naming করা important।

---

# 38. Type Conversion

এখন খুব important concept:

> **Type Conversion**

এক type-এর value-কে অন্য type-এ convert করা।

যেমন:

```text
String → Number
Number → String
String → Boolean
```

---

# 39. String to Number

```javascript
const value = "100";

const number = Number(value);

console.log(number);
console.log(typeof number);
```

Output:

```text
100
number
```

এখানে:

```text
"100"
   ↓
Number()
   ↓
100
```

---

# 40. Number to String

```javascript
const age = 22;

const text = String(age);

console.log(text);
console.log(typeof text);
```

Output:

```text
22
string
```

---

# 41. Boolean Conversion

```javascript
console.log(Boolean(1));
console.log(Boolean(0));
```

Output:

```text
true
false
```

কিছু value Boolean conversion-এ `false` হয়।

এগুলোকে আমরা বলি:

> **Falsy values**

---

# 42. Falsy Values

JavaScript-এর গুরুত্বপূর্ণ falsy values:

```text
false
0
-0
0n
""
null
undefined
NaN
```

এগুলো Boolean context-এ false হিসেবে behave করে।

### Example

```javascript
console.log(Boolean(""));
console.log(Boolean("Hello"));
```

Output:

```text
false
true
```

Truthy/Falsy আমরা **Control Flow** chapter-এ আরও বিস্তারিত দেখব।

---

# 43. Type Coercion

Type conversion এবং coercion-এর মধ্যে subtle difference আছে।

### Type Conversion

আমরা explicitly conversion করি:

```javascript
Number("100");
```

### Type Coercion

JavaScript context অনুযায়ী automatically type convert করে।

Example:

```javascript
console.log("10" + 5);
```

Output:

```text
105
```

কারণ এখানে JavaScript `5`-কে String-এর সাথে concatenate করেছে।

---

# 44. `+` Operator-এর Interesting Behavior

দেখো:

```javascript
console.log("10" + 5);
```

Output:

```text
105
```

কিন্তু:

```javascript
console.log("10" - 5);
```

Output:

```text
5
```

কারণ `-` arithmetic operation হওয়ায় JavaScript `"10"`-কে number হিসেবে coerce করেছে।

এগুলো JavaScript-এর famous type coercion behavior।

---

# 45. More Type Coercion Examples

```javascript
console.log("5" * 2);
console.log("10" / 2);
console.log("10" - 3);
```

Output:

```text
10
5
7
```

কিন্তু:

```javascript
console.log("10" + 3);
```

Output:

```text
103
```

কারণ `+` একই সাথে numeric addition এবং string concatenation—দুটোর কাজ করতে পারে।

---

# 46. Explicit vs Implicit Conversion

### Explicit

Developer নিজে conversion করছে:

```javascript
const age = Number("22");
```

### Implicit

JavaScript নিজে conversion করছে:

```javascript
console.log("22" - 2);
```

---

# 47. Equality-এর Basic Introduction

JavaScript-এ দুই ধরনের equality operator আছে:

```text
==
===
```

এগুলো খুব গুরুত্বপূর্ণ এবং পরের **Operators chapter**-এ detail-এ যাবে।

এখন basic difference:

### Loose Equality `==`

Type coercion করতে পারে।

```javascript
console.log(5 == "5");
```

Output:

```text
true
```

### Strict Equality `===`

Value এবং type—দুটোই compare করে।

```javascript
console.log(5 === "5");
```

Output:

```text
false
```

### Beginner Rule ⭐

Modern JavaScript-এ সাধারণত comparison-এর জন্য:

```javascript
===
```

ব্যবহার করা বেশি predictable।

---

# 48. Primitive Values are Immutable

Primitive values-কে সাধারণভাবে immutable বলা হয়।

এর মানে primitive value-কে সরাসরি modify করা যায় না; নতুন value তৈরি হয়।

Example:

```javascript
let name = "Ripon";

name[0] = "X";

console.log(name);
```

Output:

```text
Ripon
```

String-এর character এভাবে modify হয় না।

যদি নতুন value দিতে চাও:

```javascript
name = "Xipon";
```

এখানে নতুন String value assign হয়েছে।

---

# 49. Primitive vs Reference — Important Introduction

এখন একটি খুব important ধারণার দরজা খুলছি।

Primitive:

```javascript
let a = 10;
let b = a;

b = 20;

console.log(a);
console.log(b);
```

Output:

```text
10
20
```

`b = a` করার সময় value copy হয়েছে।

---

# 50. Object Reference Example

এখন object:

```javascript
const person1 = {
    name: "Ripon"
};

const person2 = person1;

person2.name = "Shariar";

console.log(person1.name);
console.log(person2.name);
```

Output:

```text
Shariar
Shariar
```

কেন?

কারণ object variable-এর ক্ষেত্রে এখানে object-এর reference share হয়েছে।

সহজ mental model:

```text
person1 ──────┐
              ↓
          ┌─────────┐
          │ Object  │
          │ name    │
          │ Shariar │
          └─────────┘
              ↑
person2 ──────┘
```

এটা খুব important concept।

পরে **Reference, Shallow Copy, Deep Copy, Memory & Objects** chapter-এ আমরা এটাকে অনেক গভীরে দেখব।

---

# 51. `const` Object নিয়ে Important বিষয়

অনেকে ভাবে:

> `const` হলে object-এর ভিতরের value change করা যাবে না।

এটা পুরোপুরি ঠিক নয়।

দেখো:

```javascript
const user = {
    name: "Ripon"
};

user.name = "Shariar";

console.log(user.name);
```

Output:

```text
Shariar
```

কাজ করেছে।

কিন্তু:

```javascript
user = {};
```

এটা করা যাবে না।

কারণ `const` binding-কে নতুন object-এ reassign করা যাবে না।

---

# 52. `const` Array-এর ক্ষেত্রেও একই ধারণা

```javascript
const fruits = ["Apple", "Mango"];

fruits.push("Banana");

console.log(fruits);
```

Output:

```text
["Apple", "Mango", "Banana"]
```

কিন্তু:

```javascript
fruits = ["Orange"];
```

করলে error হবে।

কারণ নতুন array-তে reassign করা হচ্ছে।

---

# 53. Memory Concept — Basic Mental Model

এখন exact engine implementation নিয়ে চিন্তা না করে একটি useful mental model রাখো।

Primitive:

```text
a = 10
b = a

a → 10
b → 10
```

Object:

```text
person1 ──→ Object
person2 ──→ Object
```

দুটো variable একই object-এর দিকে reference করতে পারে।

এই ধারণাটা পরের advanced chapter-গুলোর জন্য huge foundation।

---

# 54. A Complete Example

এখন এই chapter-এর অনেক concept একসাথে:

```javascript
const name = "Shariar";
let age = 22;
const cgpa = 3.75;
const isStudent = true;
let university;

const address = null;

const skills = ["HTML", "CSS", "JavaScript"];

const student = {
    name: name,
    age: age,
    cgpa: cgpa
};

console.log(name);
console.log(age);
console.log(cgpa);
console.log(isStudent);
console.log(university);
console.log(address);
console.log(skills);
console.log(student);
```

Output roughly:

```text
Shariar
22
3.75
true
undefined
null
["HTML", "CSS", "JavaScript"]
{
    name: "Shariar",
    age: 22,
    cgpa: 3.75
}
```

---

# 55. Data Types Cheat Sheet

| Data Type | Example           | `typeof`      |
| --------- | ----------------- | ------------- |
| String    | `"Hello"`         | `"string"`    |
| Number    | `100`             | `"number"`    |
| BigInt    | `100n`            | `"bigint"`    |
| Boolean   | `true`            | `"boolean"`   |
| Undefined | `undefined`       | `"undefined"` |
| Null      | `null`            | `"object"`*   |
| Symbol    | `Symbol("id")`    | `"symbol"`    |
| Object    | `{name: "Ripon"}` | `"object"`    |
| Array     | `[1, 2, 3]`       | `"object"`    |
| Function  | `function(){}`    | `"function"`  |

* `typeof null` হলো JavaScript-এর historical behavior।

---

# 🧠 Chapter 2 — Core Concepts You Must Remember

### 1️⃣ Data

Program যে information নিয়ে কাজ করে।

### 2️⃣ Data Type

কোন value কী ধরনের তা নির্দেশ করে।

### 3️⃣ Primitive

Basic immutable values:

```text
String
Number
BigInt
Boolean
Undefined
Null
Symbol
```

### 4️⃣ Non-Primitive

Structured/reference-based values:

```text
Object
Array
Function
...
```

### 5️⃣ Dynamic Typing

JavaScript variable-এর type runtime-এ value অনুযায়ী পরিবর্তিত হতে পারে।

### 6️⃣ Type Conversion

Developer explicitly type পরিবর্তন করে:

```javascript
Number("100");
String(100);
Boolean(1);
```

### 7️⃣ Type Coercion

JavaScript context অনুযায়ী automatically conversion করে।

### 8️⃣ `typeof`

Value-এর type সম্পর্কে জানতে সাহায্য করে।

### 9️⃣ `==` vs `===`

```text
==   → loose equality
===  → strict equality
```

### 🔟 Primitive vs Object

Primitive value এবং object/reference behavior এক নয়।

---

# 🧪 Chapter 2 — Practice Problems

এগুলো **নিজে code করে output predict করার চেষ্টা করবে**।

### Practice 1

```javascript
const name = "Ripon";
const age = 22;
const cgpa = 3.75;
const isStudent = true;

console.log(typeof name);
console.log(typeof age);
console.log(typeof cgpa);
console.log(typeof isStudent);
```

Output কী হবে?

---

### Practice 2

Output আগে predict করো:

```javascript
console.log("10" + 5);
console.log("10" - 5);
console.log("10" * 2);
console.log("10" / 2);
```

---

### Practice 3

```javascript
console.log(Boolean(0));
console.log(Boolean(1));
console.log(Boolean(""));
console.log(Boolean("JavaScript"));
console.log(Boolean(null));
console.log(Boolean(undefined));
```

প্রতিটির output predict করো।

---

### Practice 4

```javascript
let value = 100;

console.log(typeof value);

value = "JavaScript";

console.log(typeof value);

value = true;

console.log(typeof value);
```

Output explain করো।

---

### Practice 5

এই code-এর output কেন এমন হবে?

```javascript
const user1 = {
    name: "Ripon"
};

const user2 = user1;

user2.name = "Shariar";

console.log(user1.name);
```

---

# 🎯 Mini Project — Student Data Profile

আজকের chapter-এর সব গুরুত্বপূর্ণ data type ব্যবহার করে একটি ছোট Student Profile বানাও।

Target:

```text
Name
Age
Student ID
CGPA
Is Student
Skills
Address
```

Example structure:

```javascript
const name = "Shariar";
const age = 22;
const studentId = "231-15-010";
const cgpa = 3.75;
const isStudent = true;

const skills = ["HTML", "CSS", "JavaScript"];

const address = {
    city: "Dhaka",
    country: "Bangladesh"
};

console.log("Name:", name);
console.log("Age:", age);
console.log("Student ID:", studentId);
console.log("CGPA:", cgpa);
console.log("Student:", isStudent);
console.log("Skills:", skills);
console.log("Address:", address);
```

---

## 📌 Chapter 2 Final Mental Map

```text
                    JavaScript Data
                           │
              ┌────────────┴────────────┐
              │                         │
          Primitive                 Non-Primitive
              │                         │
     ┌────────┼────────┐                │
     │        │        │                ↓
  String   Number   Boolean           Object
     │        │        │                │
  BigInt   Undefined  Null          ┌───┼────┐
     │        │        │             │   │    │
  Symbol     │        │           Object Array Function
              │
              └──────→ typeof
                         │
                    Type Conversion
                         │
                    Type Coercion
```

**Chapter 2-এর core foundation এখানেই।**
এর পরের logical step হলো **Chapter 3 — Operators & Expressions**, যেখানে `+`, `-`, `*`, `/`, `%`, `**`, assignment operators, comparison, `==`, `===`, logical operators, ternary operator, nullish coalescing, optional chaining এবং তাদের real-world ব্যবহার একে একে code/output সহ শেখা হবে।
