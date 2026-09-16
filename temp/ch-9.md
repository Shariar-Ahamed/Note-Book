# 📘 JavaScript Complete Book — Chapter 9

# Arrays — একসাথে অনেক Data সংরক্ষণ

JavaScript-এর সবচেয়ে গুরুত্বপূর্ণ data structures-এর একটি হলো **Array**।

এতদিন আমরা একটি variable-এ একটি value রাখতাম:

```javascript
let name = "Shariar";
```

কিন্তু ধরো ১০০ জন student-এর নাম রাখতে হবে। আলাদা ১০০টা variable বানানো practical নয়।

তখন আমরা Array ব্যবহার করব:

```javascript
let students = [
    "Shariar",
    "Rahim",
    "Karim",
    "Sakib"
];
```

---

# 9.1 Array কী?

> **Array হলো একটি ordered collection যেখানে একাধিক value একটি variable-এর মধ্যে রাখা যায়।**

### Real-life Example

একটি shopping cart:

```text
🛒 Shopping Cart
│
├── Laptop
├── Mouse
├── Keyboard
└── Headphone
```

JavaScript:

```javascript
let cart = [
    "Laptop",
    "Mouse",
    "Keyboard",
    "Headphone"
];
```

---

# 9.2 Array তৈরি করা

সবচেয়ে common syntax:

```javascript
let fruits = ["Apple", "Banana", "Mango"];
```

Output:

```text
["Apple", "Banana", "Mango"]
```

আরেকভাবে:

```javascript
let fruits = new Array("Apple", "Banana", "Mango");
```

তবে modern JavaScript-এ সাধারণত:

```javascript
[]
```

ব্যবহার করা হয়।

---

# 9.3 Array Index

Array-এর index শুরু হয়:

```text
0
```

থেকে।

```javascript
let fruits = ["Apple", "Banana", "Mango"];
```

এটি:

```text
Index:    0         1         2
          ↓         ↓         ↓
Value:  Apple    Banana     Mango
```

---

# 9.4 Array থেকে Value Access

```javascript
let fruits = ["Apple", "Banana", "Mango"];

console.log(fruits[0]);
console.log(fruits[1]);
console.log(fruits[2]);
```

### Output

```text
Apple
Banana
Mango
```

---

# 9.5 প্রথম Element

```javascript
let skills = ["HTML", "CSS", "JavaScript"];

console.log(skills[0]);
```

Output:

```text
HTML
```

---

# 9.6 শেষ Element

```javascript
let skills = ["HTML", "CSS", "JavaScript"];

console.log(skills[skills.length - 1]);
```

Output:

```text
JavaScript
```

অথবা modern JavaScript:

```javascript
console.log(skills.at(-1));
```

Output:

```text
JavaScript
```

---

# 9.7 Array Length

```javascript
let fruits = ["Apple", "Banana", "Mango"];

console.log(fruits.length);
```

Output:

```text
3
```

`length` হলো মোট element সংখ্যা।

---

# 9.8 Array-তে বিভিন্ন ধরনের Data রাখা যায়

JavaScript Array-তে একই Array-তে বিভিন্ন type রাখা সম্ভব।

```javascript
let data = [
    "Shariar",
    23,
    true,
    null
];

console.log(data);
```

Output:

```text
["Shariar", 23, true, null]
```

এমনকি object/function-ও রাখা যায়।

```javascript
let data = [
    "Ripon",
    23,
    { city: "Dhaka" },
    function () {
        console.log("Hello");
    }
];
```

তবে real-world application-এ একই ধরনের data রাখা সাধারণত বেশি পরিষ্কার।

---

# 9.9 Array Element পরিবর্তন

Array-এর element directly পরিবর্তন করা যায়।

```javascript
let fruits = ["Apple", "Banana", "Mango"];

fruits[1] = "Orange";

console.log(fruits);
```

### Output

```text
["Apple", "Orange", "Mango"]
```

এখানে:

```text
Banana → Orange
```

হয়ে গেছে।

---

# 9.10 নতুন Element যোগ করা

শেষে element যোগ করতে:

```javascript
push()
```

```javascript
let fruits = ["Apple", "Banana"];

fruits.push("Mango");

console.log(fruits);
```

Output:

```text
["Apple", "Banana", "Mango"]
```

---

# 9.11 `push()` একাধিক Element

```javascript
let fruits = ["Apple"];

fruits.push("Banana", "Mango", "Orange");

console.log(fruits);
```

Output:

```text
["Apple", "Banana", "Mango", "Orange"]
```

---

# 9.12 `push()` কী Return করে?

এটা গুরুত্বপূর্ণ।

```javascript
let fruits = ["Apple", "Banana"];

let result = fruits.push("Mango");

console.log(result);
```

Output:

```text
3
```

`push()` নতুন Array length return করে।

---

# 9.13 শেষ Element Remove — `pop()`

```javascript
let fruits = ["Apple", "Banana", "Mango"];

let removed = fruits.pop();

console.log(removed);
console.log(fruits);
```

Output:

```text
Mango
["Apple", "Banana"]
```

---

# 9.14 `pop()` কী Return করে?

`pop()` যে element remove করে, সেটিই return করে।

```javascript
let numbers = [10, 20, 30];

let removed = numbers.pop();

console.log(removed);
```

Output:

```text
30
```

---

# 9.15 প্রথমে Element যোগ — `unshift()`

Array-এর শুরুতে element যোগ করতে:

```javascript
let fruits = ["Banana", "Mango"];

fruits.unshift("Apple");

console.log(fruits);
```

Output:

```text
["Apple", "Banana", "Mango"]
```

---

# 9.16 প্রথম Element Remove — `shift()`

```javascript
let fruits = ["Apple", "Banana", "Mango"];

let removed = fruits.shift();

console.log(removed);
console.log(fruits);
```

Output:

```text
Apple
["Banana", "Mango"]
```

---

# 9.17 Array-এর ৪টি Basic Method

এগুলো খুব ভালোভাবে মনে রাখবে:

| Method      | কাজ              |
| ----------- | ---------------- |
| `push()`    | শেষে যোগ         |
| `pop()`     | শেষ থেকে remove  |
| `unshift()` | শুরুতে যোগ       |
| `shift()`   | শুরু থেকে remove |

Visual:

```text
             push()
               ↓
[ A, B, C ] → [ A, B, C, D ]

             pop()
               ↓
[ A, B, C ] ← [ A, B, C, D ]


          unshift()
             ↓
[ A, B, C ] → [ X, A, B, C ]

           shift()
             ↓
[ A, B, C ] ← [ X, A, B, C ]
```

---

# 9.18 Array Loop — `for`

Array-এর প্রতিটি element নিয়ে কাজ করতে loop খুব গুরুত্বপূর্ণ।

```javascript
let fruits = ["Apple", "Banana", "Mango"];

for (let i = 0; i < fruits.length; i++) {
    console.log(fruits[i]);
}
```

### Output

```text
Apple
Banana
Mango
```

---

# 9.19 `for...of`

Array-এর value সরাসরি পাওয়ার জন্য:

```javascript
let fruits = ["Apple", "Banana", "Mango"];

for (let fruit of fruits) {
    console.log(fruit);
}
```

Output:

```text
Apple
Banana
Mango
```

Beginner-এর জন্য এটি খুব readable।

---

# 9.20 `for...in`

Array-এর index পাওয়ার জন্য:

```javascript
let fruits = ["Apple", "Banana", "Mango"];

for (let index in fruits) {
    console.log(index);
}
```

Output:

```text
0
1
2
```

Array-এর value দরকার হলে সাধারণত `for...of` বেশি appropriate।

---

# 9.21 `for...of` vs `for...in`

| Method     | কী পাওয়া যায় |
| ---------- | ------------ |
| `for...of` | Value        |
| `for...in` | Key/Index    |

```javascript
for (let value of fruits) {
    console.log(value);
}
```

```javascript
for (let index in fruits) {
    console.log(index);
}
```

---

# 9.22 `includes()`

Array-এর মধ্যে কোনো value আছে কিনা:

```javascript
let skills = ["HTML", "CSS", "JavaScript"];

console.log(skills.includes("JavaScript"));
```

Output:

```text
true
```

না থাকলে:

```javascript
console.log(skills.includes("Python"));
```

Output:

```text
false
```

---

# 9.23 `indexOf()`

কোন index-এ value আছে:

```javascript
let skills = ["HTML", "CSS", "JavaScript"];

console.log(skills.indexOf("CSS"));
```

Output:

```text
1
```

না থাকলে:

```javascript
console.log(skills.indexOf("Python"));
```

Output:

```text
-1
```

---

# 9.24 `lastIndexOf()`

একই value একাধিকবার থাকলে শেষ occurrence:

```javascript
let numbers = [10, 20, 10, 30, 10];

console.log(numbers.lastIndexOf(10));
```

Output:

```text
4
```

---

# 9.25 `slice()`

Array-এর একটি অংশ copy করতে:

```javascript
let fruits = [
    "Apple",
    "Banana",
    "Mango",
    "Orange"
];

let result = fruits.slice(1, 3);

console.log(result);
```

Output:

```text
["Banana", "Mango"]
```

মনে রাখবে:

> `end` index include হয় না।

---

# 9.26 `slice()` Original Array পরিবর্তন করে না

```javascript
let fruits = ["Apple", "Banana", "Mango"];

let result = fruits.slice(0, 2);

console.log(result);
console.log(fruits);
```

Output:

```text
["Apple", "Banana"]
["Apple", "Banana", "Mango"]
```

---

# 9.27 Negative `slice()`

```javascript
let fruits = [
    "Apple",
    "Banana",
    "Mango",
    "Orange"
];

console.log(fruits.slice(-2));
```

Output:

```text
["Mango", "Orange"]
```

---

# 9.28 `splice()` — খুব গুরুত্বপূর্ণ 🔥

`splice()` Array-এর মধ্যে:

* add
* remove
* replace

সবই করতে পারে।

Syntax:

```javascript
array.splice(start, deleteCount, item1, item2, ...);
```

---

# 9.29 `splice()` দিয়ে Remove

```javascript
let fruits = ["Apple", "Banana", "Mango"];

fruits.splice(1, 1);

console.log(fruits);
```

Output:

```text
["Apple", "Mango"]
```

এখানে:

```text
start = 1
deleteCount = 1
```

তাই `Banana` remove হয়েছে।

---

# 9.30 `splice()` দিয়ে Add

```javascript
let fruits = ["Apple", "Mango"];

fruits.splice(1, 0, "Banana");

console.log(fruits);
```

Output:

```text
["Apple", "Banana", "Mango"]
```

এখানে:

```text
1 → কোন index থেকে
0 → কিছু remove করব না
"Banana" → নতুন value
```

---

# 9.31 `splice()` দিয়ে Replace

```javascript
let fruits = ["Apple", "Banana", "Mango"];

fruits.splice(1, 1, "Orange");

console.log(fruits);
```

Output:

```text
["Apple", "Orange", "Mango"]
```

---

# 9.32 `splice()` কী Return করে?

যে elements remove হয়েছে, সেগুলো একটি Array হিসেবে return করে।

```javascript
let fruits = ["Apple", "Banana", "Mango"];

let removed = fruits.splice(1, 1);

console.log(removed);
```

Output:

```text
["Banana"]
```

---

# 9.33 `slice()` vs `splice()`

এটা Interview-এ খুব common।

| `slice()`                      | `splice()`                           |
| ------------------------------ | ------------------------------------ |
| Copy/Extract                   | Add/Remove/Replace                   |
| Original Array পরিবর্তন করে না | Original Array পরিবর্তন করে          |
| নতুন Array return করে          | Removed elements-এর Array return করে |
| `slice(start,end)`             | `splice(start,deleteCount,...)`      |

### সহজে মনে রাখো:

> **slice = কেটে copy নেওয়া**

> **splice = মূল Array-তে operation করা**

---

# 9.34 `join()`

Array → String করতে:

```javascript
let skills = ["HTML", "CSS", "JavaScript"];

console.log(skills.join(", "));
```

Output:

```text
HTML, CSS, JavaScript
```

---

# 9.35 `join()` Real-life Example

```javascript
let tags = ["web", "javascript", "frontend"];

let result = tags.join(" #");

console.log("#" + result);
```

Output:

```text
#web #javascript #frontend
```

---

# 9.36 `reverse()`

Array-এর order উল্টে দেয়।

```javascript
let numbers = [1, 2, 3, 4];

numbers.reverse();

console.log(numbers);
```

Output:

```text
[4, 3, 2, 1]
```

⚠️ `reverse()` original Array পরিবর্তন করে।

---

# 9.37 `sort()`

Array sort করতে:

```javascript
let fruits = ["Mango", "Apple", "Banana"];

fruits.sort();

console.log(fruits);
```

Output:

```text
["Apple", "Banana", "Mango"]
```

---

# 9.38 গুরুত্বপূর্ণ — Number Sort

এই জায়গায় beginner-রা অনেক ভুল করে।

```javascript
let numbers = [10, 2, 30, 5];

numbers.sort();

console.log(numbers);
```

Output হতে পারে:

```text
[10, 2, 30, 5]
```

কারণ default `sort()` values-কে String হিসেবে compare করে।

---

# 9.39 Numeric Sort — Ascending

```javascript
let numbers = [10, 2, 30, 5];

numbers.sort((a, b) => a - b);

console.log(numbers);
```

Output:

```text
[2, 5, 10, 30]
```

---

# 9.40 Numeric Sort — Descending

```javascript
let numbers = [10, 2, 30, 5];

numbers.sort((a, b) => b - a);

console.log(numbers);
```

Output:

```text
[30, 10, 5, 2]
```

---

# 9.41 `forEach()`

Array-এর প্রতিটি element-এর উপর function চালাতে:

```javascript
let fruits = ["Apple", "Banana", "Mango"];

fruits.forEach(function (fruit) {
    console.log(fruit);
});
```

Output:

```text
Apple
Banana
Mango
```

---

# 9.42 `forEach()` with Arrow Function

Modern style:

```javascript
let fruits = ["Apple", "Banana", "Mango"];

fruits.forEach(fruit => {
    console.log(fruit);
});
```

---

# 9.43 `forEach()` Index

```javascript
let fruits = ["Apple", "Banana", "Mango"];

fruits.forEach((fruit, index) => {
    console.log(index, fruit);
});
```

Output:

```text
0 Apple
1 Banana
2 Mango
```

---

# 9.44 `map()` 🔥

`map()` একটি Array-এর প্রতিটি element transform করে **নতুন Array** তৈরি করে।

```javascript
let numbers = [1, 2, 3, 4];

let doubled = numbers.map(number => number * 2);

console.log(doubled);
```

Output:

```text
[2, 4, 6, 8]
```

---

# 9.45 `map()` Real-life Example

Product price:

```javascript
let prices = [100, 200, 300];

let discountedPrices = prices.map(price => price * 0.9);

console.log(discountedPrices);
```

Output:

```text
[90, 180, 270]
```

---

# 9.46 `forEach()` vs `map()`

| `forEach()`                     | `map()`                            |
| ------------------------------- | ---------------------------------- |
| প্রতিটি element-এর জন্য কাজ করে | প্রতিটি element transform করে      |
| নতুন Array return করে না        | নতুন Array return করে              |
| Side effects-এর জন্য useful     | Data transformation-এর জন্য useful |

---

# 9.47 `filter()` 🔥

কোনো condition অনুযায়ী elements বেছে নিতে:

```javascript
let numbers = [1, 2, 3, 4, 5, 6];

let evenNumbers = numbers.filter(number => number % 2 === 0);

console.log(evenNumbers);
```

Output:

```text
[2, 4, 6]
```

---

# 9.48 `filter()` Real-life Example

```javascript
let products = [
    { name: "Laptop", price: 70000 },
    { name: "Mouse", price: 1000 },
    { name: "Keyboard", price: 3000 }
];

let expensive = products.filter(product => product.price > 5000);

console.log(expensive);
```

Output:

```text
Laptop
```

বাস্তবে object নিয়ে কাজ করলে পুরো object-ই থাকবে filtered Array-তে।

---

# 9.49 `find()`

Condition অনুযায়ী **প্রথম matching element** বের করতে:

```javascript
let numbers = [10, 20, 30, 40];

let result = numbers.find(number => number > 20);

console.log(result);
```

Output:

```text
30
```

কারণ প্রথম `20`-এর পর `30` condition satisfy করেছে।

---

# 9.50 `find()` না পেলে

```javascript
let numbers = [10, 20, 30];

let result = numbers.find(number => number > 100);

console.log(result);
```

Output:

```text
undefined
```

---

# 9.51 `findIndex()`

Matching element-এর index:

```javascript
let numbers = [10, 20, 30, 40];

let index = numbers.findIndex(number => number > 20);

console.log(index);
```

Output:

```text
2
```

---

# 9.52 `some()`

কমপক্ষে **একটি** element condition satisfy করে কিনা:

```javascript
let numbers = [1, 3, 5, 8];

console.log(numbers.some(number => number % 2 === 0));
```

Output:

```text
true
```

কারণ `8` even।

---

# 9.53 `every()`

**সবগুলো** element condition satisfy করে কিনা:

```javascript
let numbers = [2, 4, 6, 8];

console.log(numbers.every(number => number % 2 === 0));
```

Output:

```text
true
```

কিন্তু:

```javascript
let numbers = [2, 4, 5, 8];

console.log(numbers.every(number => number % 2 === 0));
```

Output:

```text
false
```

---

# 9.54 `reduce()` 🔥🔥

`reduce()` Array-এর অনেকগুলো value থেকে একটি final result তৈরি করতে ব্যবহৃত হয়।

### Example — Sum

```javascript
let numbers = [10, 20, 30, 40];

let total = numbers.reduce((sum, number) => {
    return sum + number;
}, 0);

console.log(total);
```

Output:

```text
100
```

---

# 9.55 `reduce()` কীভাবে কাজ করে?

```text
Initial = 0

0 + 10 = 10
10 + 20 = 30
30 + 30 = 60
60 + 40 = 100
```

শেষে:

```text
100
```

---

# 9.56 `reduce()` Real-life — Shopping Cart

```javascript
let prices = [1000, 2000, 3000];

let total = prices.reduce((sum, price) => {
    return sum + price;
}, 0);

console.log(total);
```

Output:

```text
6000
```

এটি shopping cart-এর total price calculation-এর basic idea।

---

# 9.57 `reduce()` দিয়ে Maximum

```javascript
let numbers = [10, 50, 20, 80, 30];

let max = numbers.reduce((highest, number) => {
    return number > highest ? number : highest;
}, numbers[0]);

console.log(max);
```

Output:

```text
80
```

---

# 9.58 Array Destructuring

Array থেকে সরাসরি variable তৈরি করা যায়।

```javascript
let colors = ["Red", "Green", "Blue"];

let [first, second, third] = colors;

console.log(first);
console.log(second);
console.log(third);
```

Output:

```text
Red
Green
Blue
```

---

# 9.59 Destructuring Skip

```javascript
let colors = ["Red", "Green", "Blue"];

let [first, , third] = colors;

console.log(first);
console.log(third);
```

Output:

```text
Red
Blue
```

---

# 9.60 Destructuring Default Value

```javascript
let colors = ["Red"];

let [first, second = "Blue"] = colors;

console.log(first);
console.log(second);
```

Output:

```text
Red
Blue
```

---

# 9.61 Rest with Array Destructuring

```javascript
let numbers = [1, 2, 3, 4, 5];

let [first, second, ...remaining] = numbers;

console.log(first);
console.log(second);
console.log(remaining);
```

Output:

```text
1
2
[3, 4, 5]
```

---

# 9.62 Spread Operator with Array

Array copy করতে:

```javascript
let fruits = ["Apple", "Banana"];

let newFruits = [...fruits];

console.log(newFruits);
```

Output:

```text
["Apple", "Banana"]
```

---

# 9.63 Array Combine

```javascript
let frontend = ["HTML", "CSS"];
let backend = ["Node.js", "Express"];

let skills = [...frontend, ...backend];

console.log(skills);
```

Output:

```text
["HTML", "CSS", "Node.js", "Express"]
```

---

# 9.64 Array Copy — Important

```javascript
let original = [1, 2, 3];

let copy = [...original];

copy.push(4);

console.log(original);
console.log(copy);
```

Output:

```text
[1, 2, 3]
[1, 2, 3, 4]
```

---

# 9.65 Nested Array

একটি Array-এর ভিতরে আরেকটি Array থাকতে পারে।

```javascript
let matrix = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
];

console.log(matrix);
```

---

# 9.66 Nested Array Access

```javascript
let matrix = [
    [1, 2, 3],
    [4, 5, 6]
];

console.log(matrix[0][1]);
```

Output:

```text
2
```

কারণ:

```text
matrix[0] → [1, 2, 3]

matrix[0][1] → 2
```

---

# 9.67 2D Array Real-life Example

একটি classroom-এর marks:

```javascript
let marks = [
    [80, 75, 90],
    [70, 85, 88],
    [92, 89, 95]
];
```

এখানে প্রতিটি inner Array একজন student-এর marks হতে পারে।

---

# 9.68 Array-এর মধ্যে Object

Real-world JavaScript application-এ এটি খুব common:

```javascript
let students = [
    {
        name: "Shariar",
        age: 23
    },
    {
        name: "Rahim",
        age: 22
    }
];

console.log(students[0].name);
```

Output:

```text
Shariar
```

এই concept React/Node.js-এ অত্যন্ত গুরুত্বপূর্ণ।

---

# 9.69 `Array.isArray()`

কোনো value Array কিনা check করতে:

```javascript
let skills = ["HTML", "CSS"];

console.log(Array.isArray(skills));
```

Output:

```text
true
```

আর:

```javascript
console.log(Array.isArray("Hello"));
```

Output:

```text
false
```

---

# 9.70 Array বনাম Object

| Array               | Object                           |
| ------------------- | -------------------------------- |
| Ordered collection  | Key-value data                   |
| Index ব্যবহার করে   | Key ব্যবহার করে                  |
| `users[0]`          | `user.name`                      |
| List-এর জন্য useful | Entity/data model-এর জন্য useful |

Example:

```javascript
let skills = ["HTML", "CSS", "JS"];
```

Object:

```javascript
let user = {
    name: "Shariar",
    age: 23
};
```

---

# 9.71 Empty Array

```javascript
let items = [];

console.log(items.length);
```

Output:

```text
0
```

তারপর:

```javascript
items.push("Laptop");

console.log(items);
```

Output:

```text
["Laptop"]
```

---

# 9.72 Sparse Array

```javascript
let numbers = [];

numbers[3] = 100;

console.log(numbers);
```

এতে মাঝখানে empty slots তৈরি হতে পারে।

```text
[empty, empty, empty, 100]
```

এভাবে Array তৈরি করা সাধারণত avoid করা ভালো।

---

# 9.73 Array Reference

এটা খুব গুরুত্বপূর্ণ।

```javascript
let a = [1, 2, 3];

let b = a;

b.push(4);

console.log(a);
```

Output:

```text
[1, 2, 3, 4]
```

কেন?

কারণ:

```text
a ──────┐
        ↓
      [1,2,3]
        ↑
        │
b ──────┘
```

`a` এবং `b` একই Array object-কে reference করছে।

---

# 9.74 Array Copy করার সঠিক উপায়

```javascript
let a = [1, 2, 3];

let b = [...a];

b.push(4);

console.log(a);
console.log(b);
```

Output:

```text
[1, 2, 3]
[1, 2, 3, 4]
```

---

# 9.75 `concat()`

দুটি Array combine:

```javascript
let a = [1, 2];
let b = [3, 4];

let result = a.concat(b);

console.log(result);
```

Output:

```text
[1, 2, 3, 4]
```

Spread দিয়েও:

```javascript
let result = [...a, ...b];
```

---

# 9.76 `flat()`

Nested Array flatten করতে:

```javascript
let numbers = [1, 2, [3, 4], [5, 6]];

console.log(numbers.flat());
```

Output:

```text
[1, 2, 3, 4, 5, 6]
```

---

# 9.77 Deep Nested `flat()`

```javascript
let numbers = [
    1,
    [2, [3, [4]]]
];

console.log(numbers.flat(Infinity));
```

Output:

```text
[1, 2, 3, 4]
```

---

# 9.78 `Array.from()`

Array-like বা iterable data থেকে Array তৈরি করতে:

```javascript
let text = "Hello";

let chars = Array.from(text);

console.log(chars);
```

Output:

```text
["H", "e", "l", "l", "o"]
```

---

# 9.79 `Array.of()`

Values দিয়ে Array তৈরি:

```javascript
let numbers = Array.of(10, 20, 30);

console.log(numbers);
```

Output:

```text
[10, 20, 30]
```

---

# 9.80 `Array.from()` দিয়ে Generate

```javascript
let numbers = Array.from(
    { length: 5 },
    (_, index) => index + 1
);

console.log(numbers);
```

Output:

```text
[1, 2, 3, 4, 5]
```

---

# 9.81 Important: `fill()`

Array-এর নির্দিষ্ট জায়গায় একই value বসাতে:

```javascript
let numbers = [1, 2, 3, 4, 5];

numbers.fill(0);

console.log(numbers);
```

Output:

```text
[0, 0, 0, 0, 0]
```

---

# 9.82 `fill()` Partial

```javascript
let numbers = [1, 2, 3, 4, 5];

numbers.fill(0, 1, 3);

console.log(numbers);
```

Output:

```text
[1, 0, 0, 4, 5]
```

---

# 9.83 `copyWithin()`

Array-এর ভিতরের কিছু element অন্য জায়গায় copy করতে:

```javascript
let numbers = [1, 2, 3, 4, 5];

numbers.copyWithin(0, 3);

console.log(numbers);
```

Output:

```text
[4, 5, 3, 4, 5]
```

এটি তুলনামূলকভাবে কম ব্যবহৃত method, কিন্তু JavaScript Array API-এর অংশ হিসেবে জানা ভালো।

---

# 9.84 `flatMap()`

`map()` + `flat()` একসাথে করার মতো।

```javascript
let numbers = [1, 2, 3];

let result = numbers.flatMap(number => [number, number * 2]);

console.log(result);
```

Output:

```text
[1, 2, 2, 4, 3, 6]
```

---

# 9.85 `entries()`

Index এবং value দুটো একসাথে:

```javascript
let fruits = ["Apple", "Banana", "Mango"];

for (let [index, fruit] of fruits.entries()) {
    console.log(index, fruit);
}
```

Output:

```text
0 Apple
1 Banana
2 Mango
```

---

# 9.86 `keys()`

Index পাওয়া যায়:

```javascript
let fruits = ["Apple", "Banana", "Mango"];

for (let key of fruits.keys()) {
    console.log(key);
}
```

Output:

```text
0
1
2
```

---

# 9.87 `values()`

Values:

```javascript
let fruits = ["Apple", "Banana", "Mango"];

for (let value of fruits.values()) {
    console.log(value);
}
```

Output:

```text
Apple
Banana
Mango
```

---

# 9.88 Array Method Categories 🧠

### Add / Remove

```text
push()
pop()
shift()
unshift()
splice()
```

### Search

```text
includes()
indexOf()
lastIndexOf()
find()
findIndex()
```

### Transform

```text
map()
flatMap()
```

### Filter / Check

```text
filter()
some()
every()
```

### Calculation

```text
reduce()
```

### Copy / Extract

```text
slice()
concat()
```

### Ordering

```text
sort()
reverse()
```

### Convert

```text
join()
flat()
```

---

# 9.89 Array Methods — সবচেয়ে গুরুত্বপূর্ণ Table

| Method        | কাজ                  | Original Array পরিবর্তন? |
| ------------- | -------------------- | -----------------------: |
| `push()`      | শেষে যোগ             |                        ✅ |
| `pop()`       | শেষে remove          |                        ✅ |
| `shift()`     | শুরু থেকে remove     |                        ✅ |
| `unshift()`   | শুরুতে যোগ           |                        ✅ |
| `splice()`    | add/remove/replace   |                        ✅ |
| `slice()`     | অংশ copy             |                        ❌ |
| `map()`       | transform            |                        ❌ |
| `filter()`    | filter               |                        ❌ |
| `find()`      | প্রথম match          |                        ❌ |
| `findIndex()` | প্রথম match-এর index |                        ❌ |
| `some()`      | অন্তত একটি match     |                        ❌ |
| `every()`     | সব match             |                        ❌ |
| `reduce()`    | single result        |                        ❌ |
| `includes()`  | value আছে কিনা       |                        ❌ |
| `indexOf()`   | index খোঁজা          |                        ❌ |
| `join()`      | Array → String       |                        ❌ |
| `concat()`    | Array combine        |                        ❌ |
| `reverse()`   | reverse              |                        ✅ |
| `sort()`      | sort                 |                        ✅ |
| `fill()`      | value fill           |                        ✅ |
| `flat()`      | nested flatten       |                        ❌ |

---

# 🔥 Real-life Mini Project — Shopping Cart

এখন Array-এর অনেক concept একসাথে ব্যবহার করি।

```javascript
let cart = [
    {
        name: "Laptop",
        price: 70000
    },
    {
        name: "Mouse",
        price: 1000
    },
    {
        name: "Keyboard",
        price: 3000
    }
];

console.log("Products:");

cart.forEach(product => {
    console.log(product.name);
});

let total = cart.reduce((sum, product) => {
    return sum + product.price;
}, 0);

console.log("Total:", total);
```

### Output

```text
Products:
Laptop
Mouse
Keyboard

Total: 74000
```

এখানে আমরা ব্যবহার করেছি:

```text
Array
Object
forEach()
reduce()
```

এই pattern বাস্তব e-commerce application-এ খুব common।

---

# 🔥 Real-life Mini Project — Student Result

```javascript
let marks = [80, 75, 90, 65, 88];

let total = marks.reduce((sum, mark) => sum + mark, 0);

let average = total / marks.length;

let passed = marks.filter(mark => mark >= 40);

console.log("Total:", total);
console.log("Average:", average);
console.log("Passed:", passed);
```

### Output

```text
Total: 398
Average: 79.6
Passed: [80, 75, 90, 65, 88]
```

---

# 🔥 Real-life Mini Project — Search Products

```javascript
let products = [
    "HP Laptop",
    "Dell Laptop",
    "Logitech Mouse",
    "Mechanical Keyboard"
];

let search = "laptop";

let result = products.filter(product =>
    product.toLowerCase().includes(search.toLowerCase())
);

console.log(result);
```

### Output

```text
[
    "HP Laptop",
    "Dell Laptop"
]
```

এটি basic product search-এর ধারণা।

---

# 🧠 Chapter 9 — সবচেয়ে গুরুত্বপূর্ণ Concepts

তোমাকে এগুলো অবশ্যই ভালোভাবে আয়ত্ত করতে হবে:

```text
1. Array কী
2. Array Index
3. length
4. Accessing elements
5. Updating elements
6. push()
7. pop()
8. shift()
9. unshift()
10. for loop
11. for...of
12. forEach()
13. includes()
14. indexOf()
15. slice()
16. splice()
17. join()
18. reverse()
19. sort()
20. map()
21. filter()
22. find()
23. findIndex()
24. some()
25. every()
26. reduce()
27. Array Destructuring
28. Spread Operator
29. Nested Arrays
30. Array of Objects
31. Array Reference
32. Array Copy
33. concat()
34. flat()
35. flatMap()
36. Array.from()
37. Array.of()
38. fill()
39. entries()
40. keys()
41. values()
42. Array.isArray()
```

---

# 📝 Chapter 9 — Practice Set

## Practice 1 — Basic Array

```javascript
let fruits = ["Apple", "Banana", "Mango"];
```

এগুলো বের করো:

```text
Apple
Mango
3
```

---

## Practice 2 — Add & Remove

```javascript
let skills = ["HTML", "CSS"];
```

`JavaScript` এবং `React` যোগ করো।

তারপর শেষের element remove করো।

---

## Practice 3 — Search

```javascript
let skills = ["HTML", "CSS", "JavaScript", "React"];
```

Check করো:

```text
JavaScript আছে → true
Python আছে → false
```

---

## Practice 4 — Filter

```javascript
let numbers = [10, 15, 20, 25, 30, 35];
```

শুধু even numbers বের করো।

Expected:

```text
[10, 20, 30]
```

---

## Practice 5 — Map

```javascript
let numbers = [1, 2, 3, 4, 5];
```

প্রতিটি number-এর double বের করো।

Expected:

```text
[2, 4, 6, 8, 10]
```

---

## Practice 6 — Reduce

```javascript
let prices = [100, 200, 300, 400];
```

Total বের করো।

Expected:

```text
1000
```

---

## Practice 7 — Find

```javascript
let numbers = [10, 25, 40, 55, 70];
```

`50`-এর বেশি প্রথম number বের করো।

Expected:

```text
55
```

---

## Practice 8 — Sort

```javascript
let numbers = [50, 10, 80, 20, 30];
```

Ascending:

```text
[10, 20, 30, 50, 80]
```

Descending:

```text
[80, 50, 30, 20, 10]
```

---

## Practice 9 — Destructuring

```javascript
let student = ["Shariar", 23, "CSE"];
```

Destructuring করে:

```text
name
age
department
```

আলাদা variable বানাও।

---

## Practice 10 — Mini Project 🛒

```javascript
let cart = [
    { name: "Laptop", price: 70000 },
    { name: "Mouse", price: 1000 },
    { name: "Keyboard", price: 3000 },
    { name: "Monitor", price: 15000 }
];
```

এমন program তৈরি করো যা:

1. সব product-এর নাম দেখাবে
2. সব product-এর total price বের করবে
3. `5000` টাকার বেশি product বের করবে
4. সবচেয়ে বেশি দামের product বের করবে
5. product-এর নামগুলো একটি নতুন Array-তে রাখবে

---

# 🎯 Chapter 9 Final Summary

এক কথায়:

> **Array = এক variable-এর মধ্যে ordered multiple values রাখার ব্যবস্থা।**

সবচেয়ে বেশি মনে রাখবে:

```javascript
let fruits = ["Apple", "Banana", "Mango"];
```

তারপর:

```javascript
fruits.push("Orange");       // Add
fruits.pop();                // Remove last
fruits.unshift("Orange");    // Add first
fruits.shift();              // Remove first
```

Search:

```javascript
fruits.includes("Apple");
fruits.indexOf("Apple");
```

Extract:

```javascript
fruits.slice(0, 2);
```

Modify:

```javascript
fruits.splice(1, 1);
```

Transform:

```javascript
fruits.map(...);
```

Filter:

```javascript
fruits.filter(...);
```

Find:

```javascript
fruits.find(...);
```

Calculate:

```javascript
numbers.reduce(...);
```

Loop:

```javascript
fruits.forEach(...);
```

Combine:

```javascript
[...array1, ...array2];
```

Destructure:

```javascript
let [a, b, c] = array;
```

---

## 🚀 Chapter 9-এর সবচেয়ে গুরুত্বপূর্ণ ৮টি

যদি এখনই সব method মুখস্থ না হয়, অন্তত এগুলো শক্ত করো:

```text
1. push()
2. pop()
3. slice()
4. splice()
5. forEach()
6. map()
7. filter()
8. reduce()
```

এরপর **Chapter 10 — Objects**-এ আমরা JavaScript-এর সবচেয়ে গুরুত্বপূর্ণ data structure-এর আরেকটি অংশ শিখব: **Object, Properties, Methods, Nested Objects, Object Access, Add/Update/Delete, `this`, Object Destructuring, Spread, `Object.keys()`, `Object.values()`, `Object.entries()`, Optional Chaining, Object References, Shallow Copy, এবং Array of Objects**।
