# 📘 JavaScript Complete Book

# Chapter 3 — Operators & Expressions

### Operators, Expressions এবং JavaScript-এ Data নিয়ে কাজ করা

Chapter 1-এ আমরা JavaScript-এর foundation এবং Chapter 2-এ **Variables, Data Types, Type Conversion & Type Coercion** শিখেছি।

এখন আমরা শিখব কীভাবে JavaScript-এ stored data নিয়ে **calculation, comparison, decision-making এবং logical operations** করা হয়।

এই chapter-এর মূল বিষয়:

```text
Operators
   ↓
Expressions
   ↓
Calculations
   ↓
Comparisons
   ↓
Logical Decisions
```

---

# 1. What is an Operator?

### English

An **operator** is a symbol or keyword that tells JavaScript to perform an operation.

### বাংলা

Operator হলো এমন একটি symbol বা keyword যা JavaScript-কে কোনো নির্দিষ্ট operation করতে বলে।

Example:

```javascript
10 + 5
```

এখানে:

```text
10 → Operand
+  → Operator
5  → Operand
```

Result:

```text
15
```

### সহজভাবে

```text
Operand + Operator + Operand
   10        +         5
              ↓
             15
```

---

# 2. What is an Operand?

Operator যে value-এর উপর কাজ করে, তাকে **operand** বলে।

Example:

```javascript
20 - 8
```

এখানে:

```text
20 → Operand
-  → Operator
8  → Operand
```

আর:

```javascript
x * 10
```

এখানে:

```text
x  → Operand
*  → Operator
10 → Operand
```

---

# 3. What is an Expression?

### English

An **expression** is a piece of code that produces a value.

### বাংলা

Expression হলো এমন code যা একটি value produce করে।

Example:

```javascript
10 + 20
```

Result:

```text
30
```

আর:

```javascript
age >= 18
```

Result হতে পারে:

```text
true
```

### আরও Example

```javascript
5 * 10
```

```javascript
"Hello" + " World"
```

```javascript
20 > 10
```

সবগুলো expression।

---

# 4. Types of Operators

JavaScript-এ অনেক ধরনের operator রয়েছে।

আমরা এই chapter-এ শিখব:

1. Arithmetic Operators
2. Assignment Operators
3. Comparison Operators
4. Equality Operators
5. Logical Operators
6. Unary Operators
7. Increment/Decrement
8. Ternary Operator
9. Nullish Coalescing Operator
10. Optional Chaining
11. Bitwise Operators
12. `typeof`
13. `in`
14. `instanceof`
15. Operator Precedence

---

# 5. Arithmetic Operators

Arithmetic operators mathematical calculation করার জন্য ব্যবহার হয়।

প্রধান arithmetic operators:

```text
+    Addition
-    Subtraction
*    Multiplication
/    Division
%    Modulus
**   Exponentiation
```

---

# 6. Addition `+`

```javascript
const a = 10;
const b = 20;

console.log(a + b);
```

Output:

```text
30
```

### Real-life Example

ধরো:

```text
Product = ৳500
Delivery = ৳100
```

```javascript
const productPrice = 500;
const deliveryCharge = 100;

const total = productPrice + deliveryCharge;

console.log(total);
```

Output:

```text
600
```

---

# 7. String Concatenation with `+`

`+` শুধু number যোগ করে না। String combine-ও করতে পারে।

```javascript
const firstName = "Shariar";
const lastName = "Ripon";

console.log(firstName + " " + lastName);
```

Output:

```text
Shariar Ripon
```

---

# 8. Subtraction `-`

```javascript
const a = 50;
const b = 20;

console.log(a - b);
```

Output:

```text
30
```

### Real-life

```javascript
const balance = 1000;
const expense = 250;

const remaining = balance - expense;

console.log(remaining);
```

Output:

```text
750
```

---

# 9. Multiplication `*`

```javascript
const price = 500;
const quantity = 3;

console.log(price * quantity);
```

Output:

```text
1500
```

### Real-life

একটি product-এর price ৳500 এবং quantity 3 হলে total:

```text
500 × 3 = 1500
```

---

# 10. Division `/`

```javascript
const totalMarks = 400;
const subjects = 4;

console.log(totalMarks / subjects);
```

Output:

```text
100
```

---

# 11. Modulus `%`

এটা খুব important।

`%` remainder বা ভাগশেষ বের করে।

```javascript
console.log(10 % 3);
```

Output:

```text
1
```

কারণ:

```text
10 ÷ 3

3 × 3 = 9

10 - 9 = 1
```

তাই:

```text
10 % 3 = 1
```

---

# 12. Modulus-এর Real-Life Use

একটি number even না odd সেটা বের করতে `%` ব্যবহার করা যায়।

```javascript
const number = 10;

console.log(number % 2);
```

Output:

```text
0
```

কারণ 10 সম্পূর্ণভাবে 2 দিয়ে divisible।

আর:

```javascript
const number = 7;

console.log(number % 2);
```

Output:

```text
1
```

---

# 13. Even / Odd Concept

```javascript
const number = 15;

if (number % 2 === 0) {
    console.log("Even");
} else {
    console.log("Odd");
}
```

Output:

```text
Odd
```

এখানে আমরা ব্যবহার করেছি:

* `%`
* `===`
* `if`
* `else`

`if/else` আমরা পরের chapter-এ বিস্তারিত শিখব।

---

# 14. Exponentiation `**`

Power বা exponent বের করার জন্য:

```javascript
console.log(2 ** 3);
```

Output:

```text
8
```

কারণ:

```text
2 × 2 × 2 = 8
```

আর:

```javascript
console.log(5 ** 2);
```

Output:

```text
25
```

---

# 15. Arithmetic Operators Summary

| Operator | কাজ            |  Example | Result |
| -------- | -------------- | -------: | -----: |
| `+`      | Addition       | `10 + 5` |   `15` |
| `-`      | Subtraction    | `10 - 5` |    `5` |
| `*`      | Multiplication | `10 * 5` |   `50` |
| `/`      | Division       | `10 / 5` |    `2` |
| `%`      | Remainder      | `10 % 3` |    `1` |
| `**`     | Power          | `2 ** 3` |    `8` |

---

# 16. Assignment Operator `=`

`=` হলো assignment operator।

এটি comparison করে না।

```javascript
let age = 22;
```

এর অর্থ:

> `age` variable-এর মধ্যে `22` value assign করো।

---

# 17. Reassignment

```javascript
let score = 50;

score = 80;

console.log(score);
```

Output:

```text
80
```

প্রথমে:

```text
score → 50
```

পরে:

```text
score → 80
```

---

# 18. Compound Assignment Operators

JavaScript-এ shortcut assignment operator আছে।

```text
+=
-=
*=
/=
%=
**=
```

---

# 19. `+=`

```javascript
let score = 50;

score += 10;

console.log(score);
```

Output:

```text
60
```

এটা essentially:

```javascript
score = score + 10;
```

এর shortcut।

---

# 20. `-=`

```javascript
let balance = 1000;

balance -= 250;

console.log(balance);
```

Output:

```text
750
```

Equivalent:

```javascript
balance = balance - 250;
```

---

# 21. `*=`

```javascript
let price = 100;

price *= 5;

console.log(price);
```

Output:

```text
500
```

Equivalent:

```javascript
price = price * 5;
```

---

# 22. `/=`

```javascript
let amount = 1000;

amount /= 4;

console.log(amount);
```

Output:

```text
250
```

---

# 23. `%=`

```javascript
let number = 17;

number %= 5;

console.log(number);
```

Output:

```text
2
```

কারণ:

```text
17 % 5 = 2
```

---

# 24. `**=`

```javascript
let number = 2;

number **= 3;

console.log(number);
```

Output:

```text
8
```

Equivalent:

```javascript
number = number ** 3;
```

---

# 25. Comparison Operators

Comparison operator দুইটি value compare করে এবং সাধারণত Boolean result দেয়:

```text
true
false
```

প্রধান operators:

```text
>
<
>=
<=
==
===
!=
!==
```

---

# 26. Greater Than `>`

```javascript
console.log(10 > 5);
```

Output:

```text
true
```

কারণ 10 বড় 5 থেকে।

---

# 27. Less Than `<`

```javascript
console.log(5 < 10);
```

Output:

```text
true
```

---

# 28. Greater Than or Equal `>=`

```javascript
console.log(10 >= 10);
```

Output:

```text
true
```

কারণ 10, 10-এর সমান।

আর:

```javascript
console.log(15 >= 10);
```

Output:

```text
true
```

---

# 29. Less Than or Equal `<=`

```javascript
console.log(10 <= 10);
```

Output:

```text
true
```

---

# 30. Loose Equality `==`

`==` value compare করার সময় type coercion করতে পারে।

```javascript
console.log(5 == "5");
```

Output:

```text
true
```

কারণ JavaScript এখানে type conversion করে comparison করতে পারে।

---

# 31. Strict Equality `===`

`===` value এবং type—দুটোই compare করে।

```javascript
console.log(5 === "5");
```

Output:

```text
false
```

কারণ:

```text
5   → number
"5" → string
```

Value দেখতে একই হলেও type আলাদা।

---

# 32. `==` vs `===`

এটা খুব ভালোভাবে মনে রাখবে।

```javascript
console.log(10 == "10");
```

Output:

```text
true
```

কিন্তু:

```javascript
console.log(10 === "10");
```

Output:

```text
false
```

### Beginner/Modern JS Rule ⭐

সাধারণত comparison করার সময়:

```javascript
===
```

এবং:

```javascript
!==
```

ব্যবহার করা বেশি predictable।

---

# 33. Loose Inequality `!=`

`!=` value equal নয় কিনা check করে এবং type coercion করতে পারে।

```javascript
console.log(5 != "5");
```

Output:

```text
false
```

কারণ loose comparison অনুযায়ী তারা equal।

---

# 34. Strict Inequality `!==`

`!==` value অথবা type—যেকোনো একটি আলাদা হলে `true` দেয়।

```javascript
console.log(5 !== "5");
```

Output:

```text
true
```

কারণ type আলাদা।

---

# 35. Comparison Summary

| Operator | Meaning               |
| -------- | --------------------- |
| `>`      | Greater than          |
| `<`      | Less than             |
| `>=`     | Greater than or equal |
| `<=`     | Less than or equal    |
| `==`     | Loose equality        |
| `===`    | Strict equality       |
| `!=`     | Loose inequality      |
| `!==`    | Strict inequality     |

---

# 36. Logical Operators

Logical operators একাধিক condition/value নিয়ে কাজ করতে পারে।

প্রধান তিনটি:

```text
&&   AND
||   OR
!    NOT
```

---

# 37. AND `&&`

`&&` তখন `true` হয় যখন **দুই পাশের condition-ই truthy/true** হয়।

```javascript
console.log(true && true);
```

Output:

```text
true
```

কিন্তু:

```javascript
console.log(true && false);
```

Output:

```text
false
```

### Truth Table

| A     | B     | `A && B` |
| ----- | ----- | -------- |
| true  | true  | true     |
| true  | false | false    |
| false | true  | false    |
| false | false | false    |

---

# 38. Real-Life AND Example

ধরো কোনো website-এ checkout করার জন্য:

```text
User logged in
AND
Cart is not empty
```

দুটোই true হতে হবে।

```javascript
const isLoggedIn = true;
const hasItems = true;

console.log(isLoggedIn && hasItems);
```

Output:

```text
true
```

---

# 39. OR `||`

`||`-এর ক্ষেত্রে অন্তত একটি operand truthy হলে result truthy হতে পারে।

```javascript
console.log(true || false);
```

Output:

```text
true
```

### Truth Table

| A | B | `A || B` |
|---|---|---|
| true | true | true |
| true | false | true |
| false | true | true |
| false | false | false |

---

# 40. Real-Life OR Example

ধরো login করা যাবে:

```text
Google account
OR
Email/password
```

যেকোনো একটি থাকলেই চলবে।

```javascript
const hasGoogleLogin = false;
const hasEmailLogin = true;

console.log(hasGoogleLogin || hasEmailLogin);
```

Output:

```text
true
```

---

# 41. NOT `!`

`!` Boolean value উল্টে দেয়।

```javascript
console.log(!true);
```

Output:

```text
false
```

আর:

```javascript
console.log(!false);
```

Output:

```text
true
```

---

# 42. Real-Life NOT Example

```javascript
const isLoggedIn = false;

console.log(!isLoggedIn);
```

Output:

```text
true
```

কারণ:

```text
isLoggedIn = false
!false = true
```

---

# 43. Double NOT `!!`

`!!` কোনো value-কে Boolean-এ convert করার একটি common technique।

```javascript
console.log(!!"Hello");
```

Output:

```text
true
```

আর:

```javascript
console.log(!!0);
```

Output:

```text
false
```

কারণ প্রথম `!` এবং দ্বিতীয় `!` মিলিয়ে Boolean conversion-এর মতো behavior দেয়।

---

# 44. Logical Operators শুধু Boolean Return করে?

এখানে JavaScript-এর একটি **খুব important** behavior আছে।

`&&` এবং `||` সবসময় `true` বা `false` return করে না।

তারা operand-এর actual value return করতে পারে।

Example:

```javascript
console.log("Hello" && "World");
```

Output:

```text
World
```

কারণ `"Hello"` truthy, তাই `&&` পরের operand evaluate করে এবং `"World"` return করে।

---

# 45. `&&` Short-Circuit

```javascript
console.log(false && "Hello");
```

Output:

```text
false
```

কারণ প্রথম value-ই falsy।

JavaScript দ্বিতীয় operand-এর দিকে যেতে হয় না।

এটাকে বলে:

> **Short-circuit evaluation**

---

# 46. `||` Short-Circuit

```javascript
console.log("Hello" || "World");
```

Output:

```text
Hello
```

কারণ `"Hello"` truthy।

JavaScript প্রথম truthy value পেয়ে থেমে গেছে।

---

# 47. Practical Default Value Pattern

পুরোনো/common pattern:

```javascript
const username = userInput || "Guest";

console.log(username);
```

যদি `userInput` falsy হয়, `"Guest"` ব্যবহার হবে।

তবে মনে রাখবে—`||` সব falsy value-কে fallback হিসেবে treat করে।

এজন্য modern JavaScript-এ অনেক ক্ষেত্রে `??` বেশি precise।

---

# 48. Nullish Coalescing `??`

`??` হলো modern JavaScript-এর খুব useful operator।

এটি fallback দেয় যখন left side:

```text
null
```

অথবা:

```text
undefined
```

হয়।

Example:

```javascript
const username = null;

console.log(username ?? "Guest");
```

Output:

```text
Guest
```

---

# 49. `??` vs `||`

এটা খুব important।

```javascript
console.log(0 || 100);
```

Output:

```text
100
```

কারণ `0` falsy।

কিন্তু:

```javascript
console.log(0 ?? 100);
```

Output:

```text
0
```

কারণ `0` null বা undefined নয়।

### তাই:

```text
|| → সব falsy value-এর ক্ষেত্রে fallback হতে পারে

?? → শুধু null বা undefined-এর ক্ষেত্রে fallback
```

---

# 50. Practical Example of `??`

ধরো user's age `0` valid value হতে পারে।

```javascript
const age = 0;

console.log(age ?? 18);
```

Output:

```text
0
```

কিন্তু:

```javascript
console.log(age || 18);
```

Output:

```text
18
```

তাই context অনুযায়ী operator নির্বাচন করতে হবে।

---

# 51. Optional Chaining `?.`

ধরো একটি nested object:

```javascript
const user = {
    profile: {
        name: "Ripon"
    }
};
```

তুমি লিখতে পারো:

```javascript
console.log(user.profile.name);
```

Output:

```text
Ripon
```

কিন্তু যদি `profile` না থাকে?

```javascript
const user = {};

console.log(user.profile.name);
```

এতে error হবে।

---

# 52. Optional Chaining দিয়ে

```javascript
const user = {};

console.log(user.profile?.name);
```

Output:

```text
undefined
```

`?.` বলে:

> যদি এই property/object null বা undefined হয়, তাহলে error না দিয়ে undefined return করো।

---

# 53. Optional Chaining Example

```javascript
const user = {
    profile: {
        address: {
            city: "Dhaka"
        }
    }
};

console.log(user.profile?.address?.city);
```

Output:

```text
Dhaka
```

আর:

```javascript
const user = {};

console.log(user.profile?.address?.city);
```

Output:

```text
undefined
```

---

# 54. Optional Chaining with Functions

`?.()` দিয়ে optional function call করা যায়।

```javascript
const user = {
    greet() {
        console.log("Hello!");
    }
};

user.greet?.();
```

Output:

```text
Hello!
```

যদি function না থাকে:

```javascript
const user = {};

user.greet?.();
```

তাহলে error না দিয়ে call skip করতে পারে।

---

# 55. Increment Operator `++`

Variable-এর value 1 বাড়াতে:

```javascript
let count = 5;

count++;

console.log(count);
```

Output:

```text
6
```

Equivalent:

```javascript
count = count + 1;
```

---

# 56. Decrement Operator `--`

Value 1 কমাতে:

```javascript
let count = 5;

count--;

console.log(count);
```

Output:

```text
4
```

Equivalent:

```javascript
count = count - 1;
```

---

# 57. Prefix vs Postfix

এটা একটু tricky।

### Postfix

```javascript
let x = 5;

console.log(x++);
```

Output:

```text
5
```

কিন্তু পরে:

```javascript
console.log(x);
```

Output:

```text
6
```

### Prefix

```javascript
let x = 5;

console.log(++x);
```

Output:

```text
6
```

### Difference

```text
x++ → আগে old value use, পরে increment

++x → আগে increment, পরে new value use
```

---

# 58. Prefix/ Postfix Example

```javascript
let a = 10;

let b = a++;

console.log(a);
console.log(b);
```

Output:

```text
11
10
```

কারণ `a++` প্রথমে `10` return করেছে, তারপর `a` হয়েছে `11`।

---

এখন:

```javascript
let a = 10;

let b = ++a;

console.log(a);
console.log(b);
```

Output:

```text
11
11
```

কারণ `++a` আগে increment করেছে।

---

# 59. Unary Operators

যে operator একটি operand-এর উপর কাজ করে তাকে unary operator বলা হয়।

Examples:

```javascript
typeof value
```

```javascript
!value
```

```javascript
++value
```

```javascript
--value
```

এখানে এক operand নিয়ে operation হচ্ছে।

---

# 60. Unary Plus `+`

String number-কে number-এ convert করার জন্য unary `+` ব্যবহার করা যায়।

```javascript
const value = "100";

console.log(+value);
```

Output:

```text
100
```

Type:

```javascript
console.log(typeof +value);
```

Output:

```text
number
```

তবে beginner হিসেবে explicit:

```javascript
Number(value)
```

অনেক সময় বেশি readable।

---

# 61. Unary Minus `-`

```javascript
const value = "10";

console.log(-value);
```

Output:

```text
-10
```

এখানে string `"10"` numeric conversion-এর মধ্য দিয়ে গেছে।

---

# 62. Ternary Operator `? :`

Ternary operator হলো ছোট `if/else` condition লেখার concise way।

Syntax:

```javascript
condition ? valueIfTrue : valueIfFalse
```

Example:

```javascript
const age = 20;

const result = age >= 18 ? "Adult" : "Minor";

console.log(result);
```

Output:

```text
Adult
```

---

# 63. Ternary Operator Breakdown

এই code:

```javascript
const result = age >= 18 ? "Adult" : "Minor";
```

মানে:

```text
যদি age >= 18
      ↓
    Adult
নাহলে
      ↓
    Minor
```

---

# 64. Real-Life Ternary Example

```javascript
const isLoggedIn = true;

const message = isLoggedIn
    ? "Welcome back!"
    : "Please login";

console.log(message);
```

Output:

```text
Welcome back!
```

### কখন ব্যবহার করবে?

Simple condition-এর জন্য।

খুব complex condition হলে normal `if/else` বেশি readable।

---

# 65. Bitwise Operators

এগুলো comparatively advanced।

Bitwise operators number-এর binary representation-এর bit নিয়ে কাজ করে।

প্রধান operators:

```text
&
|
^
~
<<
>>
>>>
```

এগুলো web development-এর daily beginner work-এ খুব বেশি লাগে না, কিন্তু JavaScript language-এর অংশ হিসেবে জানা উচিত।

---

# 66. Bitwise AND `&`

```javascript
console.log(5 & 3);
```

Binary:

```text
5 → 101
3 → 011
```

AND:

```text
101
011
---
001
```

`001` = `1`

Output:

```text
1
```

---

# 67. Bitwise OR `|`

```javascript
console.log(5 | 3);
```

Binary:

```text
101
011
---
111
```

`111` = `7`

Output:

```text
7
```

---

# 68. Bitwise XOR `^`

```javascript
console.log(5 ^ 3);
```

Binary:

```text
101
011
---
110
```

`110` = `6`

Output:

```text
6
```

---

# 69. Bitwise NOT `~`

```javascript
console.log(~5);
```

Output:

```text
-6
```

এটা two's complement representation-এর কারণে হয়।

Bitwise concepts low-level programming, flags, certain algorithms ইত্যাদিতে useful হতে পারে।

---

# 70. Left Shift `<<`

```javascript
console.log(5 << 1);
```

Output:

```text
10
```

Binary:

```text
5 = 101

101 << 1
= 1010
= 10
```

---

# 71. Right Shift `>>`

```javascript
console.log(10 >> 1);
```

Output:

```text
5
```

---

# 72. Zero-fill Right Shift `>>>`

```javascript
console.log(10 >>> 1);
```

Output:

```text
5
```

`>>` এবং `>>>` negative number-এর ক্ষেত্রে গুরুত্বপূর্ণভাবে আলাদা behave করতে পারে।

---

# 73. `typeof` Operator

Chapter 2-এ আমরা এটা দেখেছি।

```javascript
const name = "Ripon";

console.log(typeof name);
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

---

# 74. `in` Operator

`in` দিয়ে object-এর মধ্যে কোনো property আছে কিনা check করা যায়।

```javascript
const user = {
    name: "Ripon",
    age: 22
};

console.log("name" in user);
```

Output:

```text
true
```

আর:

```javascript
console.log("email" in user);
```

Output:

```text
false
```

---

# 75. `instanceof`

`instanceof` দিয়ে কোনো object কোনো constructor/class-এর instance কিনা check করা যায়।

```javascript
const fruits = [];

console.log(fruits instanceof Array);
```

Output:

```text
true
```

আর:

```javascript
const date = new Date();

console.log(date instanceof Date);
```

Output:

```text
true
```

OOP এবং prototypes শেখার সময় `instanceof` আরও পরিষ্কার হবে।

---

# 76. Operator Precedence

একটি expression-এ একাধিক operator থাকলে কোনটা আগে execute হবে?

এটা নির্ধারণ করে **operator precedence**।

Example:

```javascript
console.log(10 + 5 * 2);
```

অনেকে ভাবতে পারে:

```text
10 + 5 = 15
15 × 2 = 30
```

কিন্তু output:

```text
20
```

কারণ multiplication আগে:

```text
5 × 2 = 10

10 + 10 = 20
```

---

# 77. Parentheses `()` দিয়ে Priority Control

যদি তুমি addition আগে করতে চাও:

```javascript
console.log((10 + 5) * 2);
```

Output:

```text
30
```

কারণ:

```text
10 + 5 = 15
15 × 2 = 30
```

### Golden Rule ⭐

যদি precedence নিয়ে confusion হয়, parentheses ব্যবহার করো।

---

# 78. Common Precedence Idea

সাধারণভাবে:

```text
()
↓
**
↓
*, /, %
↓
+, -
↓
>, <, >=, <=
↓
==, ===, !=, !==
↓
&&
↓
||
↓
??
↓
? :
↓
assignment
```

এটা পুরো specification-এর সম্পূর্ণ table নয়; বরং practical mental model।

---

# 79. A Big Example

এখন অনেক operator একসাথে:

```javascript
const price = 500;
const quantity = 3;
const discount = 100;

const total = price * quantity - discount;

console.log(total);
```

Calculation:

```text
500 × 3 = 1500
1500 - 100 = 1400
```

Output:

```text
1400
```

---

# 80. Real-World Shopping Example

```javascript
const productPrice = 1200;
const quantity = 2;
const discount = 300;
const deliveryCharge = 100;

const subtotal = productPrice * quantity;
const total = subtotal - discount + deliveryCharge;

console.log("Subtotal:", subtotal);
console.log("Total:", total);
```

Output:

```text
Subtotal: 2400
Total: 2200
```

---

# 81. Logical + Comparison Example

```javascript
const age = 22;
const hasId = true;

const canEnter = age >= 18 && hasId;

console.log(canEnter);
```

Output:

```text
true
```

এখানে:

```text
age >= 18
    ↓
  true

hasId
  ↓
 true

true && true
    ↓
  true
```

---

# 82. `||` + `??` Example

```javascript
const username = "";

console.log(username || "Guest");
```

Output:

```text
Guest
```

কারণ empty string falsy।

কিন্তু:

```javascript
const username = "";

console.log(username ?? "Guest");
```

Output:

```text
```

এখানে empty string `null` বা `undefined` নয়, তাই fallback হয়নি।

---

# 83. Optional Chaining + Nullish Coalescing

এই combination real-world frontend development-এ অনেক useful।

```javascript
const user = {};

const city = user.profile?.address?.city ?? "Unknown";

console.log(city);
```

Output:

```text
Unknown
```

এখানে:

```text
user.profile
      ↓
undefined
      ↓
?. prevents error
      ↓
undefined
      ↓
?? "Unknown"
      ↓
"Unknown"
```

---

# 84. Common Mistake — `=` vs `===`

❌ ভুল ধারণা:

```javascript
if (age = 18)
```

এখানে `=` assignment operator।

Comparison করতে সাধারণত:

```javascript
if (age === 18)
```

ব্যবহার করবে।

---

# 85. Common Mistake — `==` vs `===`

```javascript
console.log(0 == false);
```

Output:

```text
true
```

কিন্তু:

```javascript
console.log(0 === false);
```

Output:

```text
false
```

কারণ:

```text
0     → number
false → boolean
```

Modern JS-এ strict equality সাধারণত safer/predictable choice।

---

# 86. Common Mistake — String + Number

```javascript
console.log("Price: " + 100 + 50);
```

Output:

```text
Price: 10050
```

কারণ প্রথম `+`-এর পর String concatenation শুরু হয়েছে।

যদি 100 + 50 করতে চাও:

```javascript
console.log("Price: " + (100 + 50));
```

Output:

```text
Price: 150
```

---

# 87. Common Mistake — Floating Point

JavaScript-এর floating-point arithmetic-এ কিছু surprising result হতে পারে।

```javascript
console.log(0.1 + 0.2);
```

Output:

```text
0.30000000000000004
```

কেন?

কারণ computer সাধারণত decimal fraction-কে binary floating-point representation-এ store করে, এবং কিছু decimal value exactভাবে represent করা যায় না।

এটা JavaScript-এর একার সমস্যা নয়; IEEE 754 floating-point systems-এর সাধারণ limitation।

---

# 88. Financial Calculation-এর ক্ষেত্রে সতর্কতা

যেমন:

```javascript
console.log(0.1 + 0.2);
```

Expected:

```text
0.3
```

কিন্তু actual:

```text
0.30000000000000004
```

Real-world financial systems-এ floating-point-এর বদলে integer smallest unit (যেমন cents/paisa) বা appropriate decimal/money handling ব্যবহার করা হয়।

এটা advanced application development-এ খুব important।

---

# 89. Chapter 3 — Operator Cheat Sheet

### Arithmetic

```text
+    -    *    /    %    **
```

### Assignment

```text
=    +=    -=    *=    /=    %=    **=
```

### Comparison

```text
>    <    >=    <=
```

### Equality

```text
==   ===   !=   !==
```

### Logical

```text
&&   ||   !
```

### Increment/Decrement

```text
++   --
```

### Conditional

```text
? :
```

### Modern Operators

```text
??
?.
```

### Other

```text
typeof
in
instanceof
```

### Bitwise

```text
&
|
^
~
<<
>>
>>>
```

---

# 🧠 Chapter 3 — Quick Revision

এক লাইনে মনে রাখো:

> **Operator data-এর উপর operation করে, আর expression সেই operation-এর মাধ্যমে একটি value produce করতে পারে।**

```text
10 + 20
```

এখানে:

```text
10  → Operand
+   → Operator
20  → Operand
30  → Result
```

আর operators-এর বড় picture:

```text
                    Operators
                        │
       ┌────────────────┼────────────────┐
       │                │                │
   Arithmetic       Comparison       Logical
       │                │                │
   + - * / % **     > < === !==     && || !
       │                │                │
       └────────────────┼────────────────┘
                        │
                Assignment
                        │
              = += -= *= /= %=
                        │
                  Modern JS
                        │
                ??   ?.   ?:
```

---

# 🧪 Chapter 3 — Practice Set

এগুলো আগে **নিজে output predict করবে**, তারপর browser console-এ run করবে।

### Practice 1

```javascript
console.log(20 + 10);
console.log(20 - 10);
console.log(20 * 10);
console.log(20 / 10);
console.log(20 % 3);
console.log(2 ** 5);
```

---

### Practice 2

```javascript
let score = 100;

score += 20;
score -= 10;
score *= 2;
score /= 2;

console.log(score);
```

Final output কী?

---

### Practice 3

```javascript
console.log(10 > 5);
console.log(10 < 5);
console.log(10 >= 10);
console.log(10 <= 9);
console.log(10 == "10");
console.log(10 === "10");
```

প্রতিটির output explain করো।

---

### Practice 4

```javascript
console.log(true && false);
console.log(true || false);
console.log(!true);
console.log(!false);
```

---

### Practice 5

```javascript
console.log("5" + 2);
console.log("5" - 2);
console.log("5" * 2);
console.log("5" / 2);
```

**কেন প্রথমটার behavior অন্যগুলোর থেকে আলাদা—নিজে explain করার চেষ্টা করো।**

---

### Practice 6

```javascript
const age = 17;

const result = age >= 18 ? "Adult" : "Minor";

console.log(result);
```

---

### Practice 7

```javascript
const user = {
    profile: {
        name: "Ripon"
    }
};

console.log(user.profile?.name);
console.log(user.address?.city);
```

---

### Practice 8 — Real Project Logic

ধরো:

```text
Product Price = 1500
Quantity = 3
Discount = 500
Delivery = 100
```

JavaScript দিয়ে বের করো:

```text
Subtotal
Final Total
```

---

# 🎯 Chapter 3 Mini Project — Shopping Cart Calculator

নিজে এই logic তৈরি করার চেষ্টা করো:

```text
Product Price
Quantity
Discount
Delivery Charge
----------------
Subtotal
Final Total
```

Example:

```text
Product Price: 800
Quantity: 2
Discount: 100
Delivery: 60
```

Expected:

```text
Subtotal: 1600
Final Total: 1560
```

এখানে তোমাকে ব্যবহার করতে হবে:

* Variables
* Arithmetic operators
* Assignment
* `console.log()`

---

## ⭐ Chapter 3-এর Must-Know Concepts

এই chapter থেকে বিশেষভাবে এগুলো strong করবে:

```text
+  -  *  /  %  **
=  += -= *= /=
>  <  >= <=
== === != !==
&& || !
++ --
? :
??
?.
typeof
```

এর মধ্যে **`===`, `&&`, `||`, `??`, `?.`, `%`, `++/--`, ternary এবং operator precedence** বিশেষভাবে ভালোভাবে practice করবে।

---

## 📌 পরের Chapter

# Chapter 4 — Control Flow & Decision Making

এখানে JavaScript কীভাবে **decision নেয়** সেটা শুরু হবে:

```text
if
else
else if
nested if
switch
case
default
break
fall-through
truthy
falsy
logical conditions
ternary
```

এরপর আমরা ধীরে ধীরে **Loops → Functions → Strings → Arrays → Objects → Scope → DOM → Events → Async JavaScript → APIs → OOP → Advanced JavaScript → JavaScript Internals**-এর দিকে এগোব।
