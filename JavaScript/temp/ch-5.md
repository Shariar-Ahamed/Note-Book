# 📘 JavaScript Complete Book — Chapter 5

# Loops & Iteration

### Loops & Iteration — একই কাজ বারবার করার Smart উপায়

JavaScript-এ অনেক সময় আমাদের একই কাজ **বারবার** করতে হয়।

যেমন:

* 1 থেকে 100 পর্যন্ত number print করা
* 100 জন student-এর নাম দেখানো
* একটি shopping cart-এর সব product বের করা
* database/API থেকে পাওয়া সব data process করা
* 1, 2, 3, 4... এভাবে counting করা
* কোনো condition পূরণ না হওয়া পর্যন্ত কাজ চালানো

প্রতিবার আলাদা করে code লিখলে:

```javascript
console.log(1);
console.log(2);
console.log(3);
console.log(4);
console.log(5);
```

এভাবে 100 বার লিখতে হবে। 😵

তার পরিবর্তে **Loop** ব্যবহার করি।

---

# 5.1 What is a Loop?

**Loop** হলো এমন একটি programming structure, যার মাধ্যমে কোনো code নির্দিষ্ট condition অনুযায়ী **বারবার execute** করা যায়।

### সহজভাবে:

```text
একবার code লিখবে
      ↓
বারবার execute হবে
      ↓
Condition false হলে থামবে
```

### Real-Life Example

ধরো teacher বললেন:

> "Class-এর 50 জন student-এর নাম একে একে বলো।"

তুমি যদি প্রতিটি student-এর জন্য আলাদা instruction দাও, অনেক সময় লাগবে।

Programming-এ:

```text
Student 1
Student 2
Student 3
...
Student 50
```

এটা loop দিয়ে করা যায়।

---

# 5.2 JavaScript-এর প্রধান Loop

JavaScript-এ গুরুত্বপূর্ণ loopগুলো হলো:

| Loop         | ব্যবহার                            |
| ------------ | ---------------------------------- |
| `for`        | নির্দিষ্ট সংখ্যক বার কাজ           |
| `while`      | condition true থাকা পর্যন্ত        |
| `do...while` | অন্তত একবার execute করে            |
| `for...of`   | iterable-এর values নিয়ে কাজ        |
| `for...in`   | object-এর keys/properties নিয়ে কাজ |
| Nested loop  | loop-এর ভিতরে loop                 |

এছাড়া:

```javascript
break
continue
```

দিয়ে loop-এর flow control করা যায়।

---

# 5.3 `for` Loop

সবচেয়ে common loop হলো `for` loop।

### Syntax

```javascript
for (initialization; condition; update) {
    // code
}
```

এখানে তিনটি গুরুত্বপূর্ণ অংশ:

```text
initialization
      ↓
condition
      ↓
code
      ↓
update
      ↓
condition
      ↓
...
```

---

# 5.4 Basic `for` Loop

```javascript
for (let i = 1; i <= 5; i++) {
    console.log(i);
}
```

### Output

```text
1
2
3
4
5
```

এখন একদম step-by-step দেখি।

### Step 1

```javascript
let i = 1;
```

`i` এর value = `1`

### Step 2

```javascript
i <= 5
```

```text
1 <= 5 → true
```

তাই:

```javascript
console.log(i);
```

Output:

```text
1
```

### Step 3

```javascript
i++
```

তাই:

```text
i = 2
```

আবার condition check।

```text
2 <= 5 → true
```

তারপর:

```text
2
```

এভাবে চলতে থাকে।

শেষে:

```text
6 <= 5 → false
```

তখন loop বন্ধ হয়ে যায়।

---

# 5.5 `for` Loop-এর তিনটি অংশ

এই code:

```javascript
for (let i = 1; i <= 5; i++) {
    console.log(i);
}
```

এখানে:

### 1. Initialization

```javascript
let i = 1
```

Loop শুরু হওয়ার আগে একবার execute হয়।

### 2. Condition

```javascript
i <= 5
```

প্রতিবার check হয়।

### 3. Update

```javascript
i++
```

প্রতিবার loop body শেষ হওয়ার পর execute হয়।

---

# 5.6 Reverse Loop

শুধু সামনে নয়, পিছন দিকেও loop চালানো যায়।

```javascript
for (let i = 5; i >= 1; i--) {
    console.log(i);
}
```

### Output

```text
5
4
3
2
1
```

এখানে:

```javascript
i--
```

প্রতিবার value 1 করে কমাচ্ছে।

---

# 5.7 Even Numbers

1 থেকে 10 পর্যন্ত even number বের করি।

```javascript
for (let i = 1; i <= 10; i++) {
    if (i % 2 === 0) {
        console.log(i);
    }
}
```

### Output

```text
2
4
6
8
10
```

এখানে:

```javascript
i % 2 === 0
```

মানে number 2 দিয়ে ভাগ করলে remainder `0`।

---

# 5.8 Odd Numbers

```javascript
for (let i = 1; i <= 10; i++) {
    if (i % 2 !== 0) {
        console.log(i);
    }
}
```

### Output

```text
1
3
5
7
9
```

---

# 5.9 Sum of Numbers

1 থেকে 5 পর্যন্ত সব number-এর যোগফল বের করি।

```javascript
let sum = 0;

for (let i = 1; i <= 5; i++) {
    sum = sum + i;
}

console.log(sum);
```

### Output

```text
15
```

কারণ:

```text
0 + 1 = 1
1 + 2 = 3
3 + 3 = 6
6 + 4 = 10
10 + 5 = 15
```

---

# 5.10 `sum += i`

উপরের code আরও short করা যায়:

```javascript
let sum = 0;

for (let i = 1; i <= 5; i++) {
    sum += i;
}

console.log(sum);
```

Output:

```text
15
```

কারণ:

```javascript
sum += i;
```

মানে:

```javascript
sum = sum + i;
```

---

# 5.11 Multiplication Table

ধরো 5-এর নামতা।

```javascript
let number = 5;

for (let i = 1; i <= 10; i++) {
    console.log(number + " x " + i + " = " + number * i);
}
```

### Output

```text
5 x 1 = 5
5 x 2 = 10
5 x 3 = 15
5 x 4 = 20
5 x 5 = 25
5 x 6 = 30
5 x 7 = 35
5 x 8 = 40
5 x 9 = 45
5 x 10 = 50
```

---

# 5.12 Template Literal দিয়ে আরও সুন্দরভাবে

```javascript
let number = 5;

for (let i = 1; i <= 10; i++) {
    console.log(`${number} x ${i} = ${number * i}`);
}
```

Output একই:

```text
5 x 1 = 5
5 x 2 = 10
...
5 x 10 = 50
```

এটা real-world JavaScript-এ অনেক বেশি readable।

---

# 5.13 `while` Loop

`while` loop ব্যবহার করা হয় যখন:

> "Condition true থাকা পর্যন্ত কাজ চালাও।"

### Syntax

```javascript
while (condition) {
    // code
}
```

### Example

```javascript
let i = 1;

while (i <= 5) {
    console.log(i);
    i++;
}
```

### Output

```text
1
2
3
4
5
```

---

# 5.14 `while` Loop কীভাবে কাজ করে?

```javascript
let i = 1;
```

তারপর:

```javascript
while (i <= 5)
```

condition check করে।

```text
1 <= 5 → true
```

তারপর `1` print হয়।

এরপর:

```javascript
i++;
```

এখন:

```text
i = 2
```

আবার condition।

এভাবে:

```text
1 → 2 → 3 → 4 → 5
```

শেষে:

```text
6 <= 5 → false
```

Loop বন্ধ।

---

# 5.15 `for` বনাম `while`

### `for`

যখন কতবার loop চলবে সেটা মোটামুটি জানা থাকে:

```javascript
for (let i = 1; i <= 10; i++) {
    console.log(i);
}
```

### `while`

যখন condition-based repetition বেশি natural:

```javascript
while (userHasNotFinished) {
    // কাজ
}
```

সহজভাবে:

| Situation                    | Loop    |
| ---------------------------- | ------- |
| নির্দিষ্ট counting           | `for`   |
| Known number of iterations   | `for`   |
| Condition-based              | `while` |
| Unknown number of iterations | `while` |

---

# 5.16 `do...while` Loop

`do...while` একটু আলাদা।

এখানে **প্রথমে code execute হবে**, তারপর condition check হবে।

### Syntax

```javascript
do {
    // code
} while (condition);
```

### Example

```javascript
let i = 1;

do {
    console.log(i);
    i++;
} while (i <= 5);
```

### Output

```text
1
2
3
4
5
```

---

# 5.17 `while` বনাম `do...while`

এটা খুব important।

### `while`

```javascript
let i = 10;

while (i <= 5) {
    console.log(i);
}
```

### Output

```text
কিছুই output হবে না
```

কারণ প্রথমেই:

```text
10 <= 5 → false
```

---

### `do...while`

```javascript
let i = 10;

do {
    console.log(i);
} while (i <= 5);
```

### Output

```text
10
```

কারণ `do` block প্রথমে একবার execute হয়েছে।

### মনে রাখবে:

```text
while
→ আগে condition
→ তারপর code

do...while
→ আগে code
→ তারপর condition
```

---

# 5.18 Real-Life Example — Login Attempt

ধরো user-কে অন্তত একবার login attempt করতে হবে।

```javascript
let attempt = 1;

do {
    console.log(`Login attempt: ${attempt}`);
    attempt++;
} while (attempt <= 3);
```

### Output

```text
Login attempt: 1
Login attempt: 2
Login attempt: 3
```

---

# 5.19 Infinite Loop

যে loop কখনো শেষ হয় না তাকে **Infinite Loop** বলে।

### Example

```javascript
let i = 1;

while (i <= 5) {
    console.log(i);
}
```

⚠️ এখানে problem হলো:

```javascript
i++
```

দেওয়া হয়নি।

তাই `i` সবসময় `1` থাকবে।

Condition:

```text
1 <= 5
```

সবসময় true।

ফলে loop চলতেই থাকবে।

---

# 5.20 Infinite `for` Loop

এটাও সম্ভব:

```javascript
for (;;) {
    console.log("Hello");
}
```

এটি infinite loop।

⚠️ Browser/Node.js-এ এমন code accidentalভাবে চালালে সমস্যা হতে পারে।

---

# 5.21 `break`

`break` ব্যবহার করে loop **সম্পূর্ণভাবে বন্ধ** করা যায়।

### Example

```javascript
for (let i = 1; i <= 10; i++) {

    if (i === 5) {
        break;
    }

    console.log(i);
}
```

### Output

```text
1
2
3
4
```

যখন:

```javascript
i === 5
```

তখন:

```javascript
break;
```

loop সম্পূর্ণ stop করে দেয়।

---

# 5.22 Real-Life Example of `break`

ধরো 100 জন student-এর মধ্যে তুমি `"Rahim"`-কে খুঁজছো।

Rahim পাওয়া গেলে আর search করার দরকার নেই।

```javascript
let students = ["Karim", "Sakib", "Rahim", "Hasan", "Nabil"];

for (let i = 0; i < students.length; i++) {

    if (students[i] === "Rahim") {
        console.log("Rahim found!");
        break;
    }

    console.log("Checking:", students[i]);
}
```

### Output

```text
Checking: Karim
Checking: Sakib
Rahim found!
```

Rahim পাওয়ার পর loop stop হয়েছে।

---

# 5.23 `continue`

`continue` loop বন্ধ করে না।

বরং **বর্তমান iteration skip করে next iteration-এ চলে যায়**।

### Example

```javascript
for (let i = 1; i <= 5; i++) {

    if (i === 3) {
        continue;
    }

    console.log(i);
}
```

### Output

```text
1
2
4
5
```

`3` skip হয়েছে।

---

# 5.24 `break` বনাম `continue`

এটা অবশ্যই মনে রাখবে।

### `break`

```text
Loop সম্পূর্ণ বন্ধ
```

### `continue`

```text
Current iteration skip
Loop চলতে থাকে
```

| Keyword    | কাজ                    |
| ---------- | ---------------------- |
| `break`    | পুরো loop stop         |
| `continue` | current iteration skip |

---

# 5.25 `for...of`

এটি modern JavaScript-এর খুব important loop।

এটি iterable-এর **values** নিয়ে কাজ করে।

Array-এর ক্ষেত্রে খুব useful।

### Example

```javascript
let fruits = ["Apple", "Banana", "Mango"];

for (let fruit of fruits) {
    console.log(fruit);
}
```

### Output

```text
Apple
Banana
Mango
```

এখানে:

```javascript
fruit
```

প্রতিবার একটি value পাচ্ছে।

```text
Apple
↓
Banana
↓
Mango
```

---

# 5.26 `for...of` কেন useful?

Traditional `for`:

```javascript
let fruits = ["Apple", "Banana", "Mango"];

for (let i = 0; i < fruits.length; i++) {
    console.log(fruits[i]);
}
```

`for...of`:

```javascript
for (let fruit of fruits) {
    console.log(fruit);
}
```

দ্বিতীয়টা অনেক cleaner।

---

# 5.27 `for...of` with String

String-ও iterable।

```javascript
let name = "Shariar";

for (let character of name) {
    console.log(character);
}
```

### Output

```text
S
h
a
r
i
a
r
```

---

# 5.28 `for...of` with Array

```javascript
let numbers = [10, 20, 30, 40];

for (let number of numbers) {
    console.log(number);
}
```

### Output

```text
10
20
30
40
```

---

# 5.29 `for...in`

`for...in` সাধারণত Object-এর **keys/properties** iterate করতে ব্যবহার করা হয়।

### Example

```javascript
let user = {
    name: "Shariar",
    age: 23,
    country: "Bangladesh"
};

for (let key in user) {
    console.log(key);
}
```

### Output

```text
name
age
country
```

এখানে:

```javascript
key
```

হচ্ছে:

```text
name
age
country
```

---

# 5.30 `for...in` দিয়ে Value পাওয়া

Object-এর value পেতে:

```javascript
let user = {
    name: "Shariar",
    age: 23,
    country: "Bangladesh"
};

for (let key in user) {
    console.log(key, user[key]);
}
```

### Output

```text
name Shariar
age 23
country Bangladesh
```

এখানে:

```javascript
user[key]
```

খুব important।

যদি:

```javascript
key = "name"
```

তাহলে:

```javascript
user["name"]
```

→ `"Shariar"`

---

# 5.31 `for...in` বনাম `for...of`

এটা beginnerদের সবচেয়ে common confusion-এর একটি।

### `for...in`

→ **keys**

```javascript
let user = {
    name: "Shariar",
    age: 23
};

for (let key in user) {
    console.log(key);
}
```

Output:

```text
name
age
```

### `for...of`

→ **values**

```javascript
let fruits = ["Apple", "Mango"];

for (let fruit of fruits) {
    console.log(fruit);
}
```

Output:

```text
Apple
Mango
```

### মনে রাখার trick:

```text
IN  → index/key-এর মধ্যে
OF  → value-এর মধ্যে
```

---

# 5.32 Array-তে `for...in` ব্যবহার করা উচিত?

Technically করা যায়:

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

কিন্তু Array-এর values iterate করার জন্য সাধারণত:

```javascript
for...of
```

বা array methods বেশি appropriate।

এটা পরে **Arrays chapter**-এ বিস্তারিত দেখব।

---

# 5.33 Nested Loop

একটি loop-এর ভিতরে আরেকটি loop থাকলে তাকে **Nested Loop** বলে।

### Example

```javascript
for (let i = 1; i <= 3; i++) {

    for (let j = 1; j <= 3; j++) {
        console.log(i, j);
    }

}
```

### Output

```text
1 1
1 2
1 3
2 1
2 2
2 3
3 1
3 2
3 3
```

### কীভাবে কাজ করছে?

প্রথম outer loop:

```text
i = 1
```

তখন inner loop পুরোটা চলে:

```text
j = 1
j = 2
j = 3
```

তারপর:

```text
i = 2
```

আবার inner loop পুরোটা চলে।

---

# 5.34 Nested Loop — Real-Life Example

ধরো একটি university-তে:

```text
3 Departments
প্রতিটি Department-এ 3 Students
```

তাহলে:

```javascript
for (let department = 1; department <= 3; department++) {

    for (let student = 1; student <= 3; student++) {
        console.log(
            `Department ${department}, Student ${student}`
        );
    }

}
```

### Output

```text
Department 1, Student 1
Department 1, Student 2
Department 1, Student 3
Department 2, Student 1
Department 2, Student 2
Department 2, Student 3
Department 3, Student 1
Department 3, Student 2
Department 3, Student 3
```

---

# 5.35 Pattern Printing

Nested loop বুঝতে pattern printing খুব useful।

### Example

```text
*
**
***
****
*****
```

Code:

```javascript
for (let i = 1; i <= 5; i++) {

    let pattern = "";

    for (let j = 1; j <= i; j++) {
        pattern += "*";
    }

    console.log(pattern);
}
```

### Output

```text
*
**
***
****
*****
```

---

# 5.36 Reverse Pattern

```text
*****
****
***
**
*
```

Code:

```javascript
for (let i = 5; i >= 1; i--) {

    let pattern = "";

    for (let j = 1; j <= i; j++) {
        pattern += "*";
    }

    console.log(pattern);
}
```

### Output

```text
*****
****
***
**
*
```

---

# 5.37 Loop Through Array

এটা web development-এর জন্য অত্যন্ত important।

```javascript
let students = [
    "Shariar",
    "Rahim",
    "Karim",
    "Hasan"
];

for (let student of students) {
    console.log(student);
}
```

### Output

```text
Shariar
Rahim
Karim
Hasan
```

Real-world application:

```text
API
 ↓
Students Array
 ↓
Loop
 ↓
UI-তে Student Cards
```

React-এ পরে তুমি প্রায় একই ধরনের concept ব্যবহার করবে।

---

# 5.38 Array of Objects

বাস্তব application-এ data সাধারণত এমন হয়:

```javascript
let students = [
    {
        name: "Shariar",
        age: 23
    },
    {
        name: "Rahim",
        age: 22
    },
    {
        name: "Karim",
        age: 24
    }
];
```

Loop:

```javascript
for (let student of students) {
    console.log(student.name);
}
```

### Output

```text
Shariar
Rahim
Karim
```

আর:

```javascript
for (let student of students) {
    console.log(
        `${student.name} is ${student.age} years old.`
    );
}
```

### Output

```text
Shariar is 23 years old.
Rahim is 22 years old.
Karim is 24 years old.
```

এটাই পরে API data render করার basic idea।

---

# 5.39 Loop দিয়ে Search

```javascript
let products = [
    "Laptop",
    "Mouse",
    "Keyboard",
    "Monitor"
];

let search = "Keyboard";

for (let product of products) {

    if (product === search) {
        console.log("Product found!");
        break;
    }

}
```

### Output

```text
Product found!
```

---

# 5.40 Loop দিয়ে Maximum Number

```javascript
let numbers = [10, 45, 23, 78, 12];

let max = numbers[0];

for (let number of numbers) {

    if (number > max) {
        max = number;
    }

}

console.log(max);
```

### Output

```text
78
```

### Logic:

```text
max = 10

45 > 10 → max = 45
23 > 45 → No
78 > 45 → max = 78
12 > 78 → No
```

শেষে:

```text
78
```

---

# 5.41 Loop দিয়ে Minimum Number

```javascript
let numbers = [10, 45, 23, 78, 12];

let min = numbers[0];

for (let number of numbers) {

    if (number < min) {
        min = number;
    }

}

console.log(min);
```

### Output

```text
10
```

---

# 5.42 Loop দিয়ে Count

ধরো array-তে কয়টি even number আছে।

```javascript
let numbers = [1, 2, 4, 7, 8, 10, 13];

let count = 0;

for (let number of numbers) {

    if (number % 2 === 0) {
        count++;
    }

}

console.log(count);
```

### Output

```text
4
```

কারণ even numbers:

```text
2, 4, 8, 10
```

মোট:

```text
4
```

---

# 5.43 `break` + `continue` একসাথে

```javascript
for (let i = 1; i <= 10; i++) {

    if (i === 3) {
        continue;
    }

    if (i === 8) {
        break;
    }

    console.log(i);
}
```

### Output

```text
1
2
4
5
6
7
```

### কী হয়েছে?

```text
3 → continue → skip
8 → break → stop
```

---

# 5.44 Loop-এর Scope

`let` দিয়ে loop variable তৈরি করলে সেটি সাধারণত loop block-এর মধ্যে সীমাবদ্ধ থাকে।

```javascript
for (let i = 1; i <= 3; i++) {
    console.log(i);
}
```

এর পরে:

```javascript
console.log(i);
```

করলে error হবে:

```text
ReferenceError
```

কারণ `i` loop-এর বাইরে accessible নয়।

---

# 5.45 `var` এবং Loop

পুরনো JavaScript-এ:

```javascript
for (var i = 1; i <= 3; i++) {
    console.log(i);
}

console.log(i);
```

এখানে output:

```text
1
2
3
4
```

কারণ `var` function-scoped।

এই কারণে modern JavaScript-এ সাধারণত loop variable-এর জন্য:

```javascript
let
```

ব্যবহার করা হয়।

---

# 5.46 Loop-এর `const`

`for...of`-এ `const` খুব common:

```javascript
let fruits = ["Apple", "Mango", "Banana"];

for (const fruit of fruits) {
    console.log(fruit);
}
```

এখানে প্রতিটি iteration-এ নতুন `fruit` binding পাওয়া যায়।

---

# 5.47 Labelled Statement — Advanced Concept

JavaScript-এ loop-কে label দেওয়া যায়।

```javascript
outerLoop:
for (let i = 1; i <= 3; i++) {

    for (let j = 1; j <= 3; j++) {

        if (i === 2 && j === 2) {
            break outerLoop;
        }

        console.log(i, j);
    }
}
```

### Output

```text
1 1
1 2
1 3
2 1
```

এখানে:

```javascript
break outerLoop;
```

শুধু inner loop নয়, পুরো outer loop-ও stop করেছে।

⚠️ এটি valid JavaScript, তবে normal code-এ খুব কম ব্যবহার করা হয়।

---

# 5.48 Which Loop Should You Use?

একটা practical guide:

### নির্দিষ্ট সংখ্যক iteration:

```javascript
for
```

Example:

```javascript
for (let i = 0; i < 10; i++) {}
```

### Condition-based:

```javascript
while
```

Example:

```javascript
while (balance > 0) {}
```

### অন্তত একবার execute করতে হবে:

```javascript
do...while
```

### Array-এর values:

```javascript
for...of
```

### Object-এর keys:

```javascript
for...in
```

---

# 5.49 Loop vs Array Methods

Modern JavaScript-এ শুধু loop নয়, array methods-ও খুব গুরুত্বপূর্ণ।

যেমন:

```javascript
map()
filter()
reduce()
find()
some()
every()
forEach()
```

এগুলো আমরা **Arrays Chapter**-এ বিস্তারিতভাবে শিখব।

উদাহরণ:

```javascript
let numbers = [1, 2, 3];

numbers.forEach(function(number) {
    console.log(number);
});
```

Output:

```text
1
2
3
```

এখন শুধু জানবে:

> `forEach()` একটি array method, traditional loop statement নয়।

---

# 5.50 Mini Project — Student Result System

এবার Chapter 4 + Chapter 5-এর concept একসাথে ব্যবহার করি।

```javascript
let students = [
    {
        name: "Shariar",
        marks: 85
    },
    {
        name: "Rahim",
        marks: 72
    },
    {
        name: "Karim",
        marks: 58
    },
    {
        name: "Hasan",
        marks: 31
    }
];

for (let student of students) {

    let grade;

    if (student.marks >= 80) {
        grade = "A+";
    } else if (student.marks >= 70) {
        grade = "A";
    } else if (student.marks >= 60) {
        grade = "A-";
    } else if (student.marks >= 50) {
        grade = "B";
    } else if (student.marks >= 40) {
        grade = "C";
    } else {
        grade = "F";
    }

    console.log(
        `${student.name} → ${student.marks} → ${grade}`
    );
}
```

### Output

```text
Shariar → 85 → A+
Rahim → 72 → A
Karim → 58 → B
Hasan → 31 → F
```

🔥 এখানে তুমি একসাথে ব্যবহার করেছো:

```text
Array
Object
for...of
if
else if
else
Template Literal
```

পরবর্তী chapter-গুলোতে এগুলো আরও powerful হবে।

---

# 5.51 Mini Project — Shopping Cart Total

```javascript
let cart = [
    {
        name: "Keyboard",
        price: 1500
    },
    {
        name: "Mouse",
        price: 800
    },
    {
        name: "Headphone",
        price: 2000
    }
];

let total = 0;

for (let product of cart) {
    total += product.price;
}

console.log("Total:", total);
```

### Output

```text
Total: 4300
```

### Logic:

```text
1500
+ 800
+ 2000
------
4300
```

এটাই basic shopping cart-এর একটা core logic।

---

# 5.52 Mini Project — Find Product

```javascript
let products = [
    "Laptop",
    "Keyboard",
    "Mouse",
    "Monitor",
    "Headphone"
];

let search = "Monitor";
let found = false;

for (let product of products) {

    if (product === search) {
        found = true;
        break;
    }
}

if (found) {
    console.log("Product found.");
} else {
    console.log("Product not found.");
}
```

### Output

```text
Product found.
```

---

# 🧠 Chapter 5 Cheat Sheet

```text
FOR
→ নির্দিষ্টভাবে loop চালাতে

WHILE
→ condition true থাকা পর্যন্ত

DO...WHILE
→ অন্তত একবার চালাতে

FOR...OF
→ values পেতে

FOR...IN
→ keys পেতে

BREAK
→ পুরো loop stop

CONTINUE
→ current iteration skip

NESTED LOOP
→ loop-এর ভিতরে loop
```

---

# 🔥 সবচেয়ে গুরুত্বপূর্ণ পার্থক্য

### `for`

```javascript
for (let i = 0; i < 5; i++) {
    console.log(i);
}
```

### `while`

```javascript
let i = 0;

while (i < 5) {
    console.log(i);
    i++;
}
```

### `do...while`

```javascript
let i = 0;

do {
    console.log(i);
    i++;
} while (i < 5);
```

### `for...of`

```javascript
for (let value of array) {
    console.log(value);
}
```

### `for...in`

```javascript
for (let key in object) {
    console.log(key);
}
```

---

# 📝 Chapter 5 — Practice Set

### Basic

**1.** Loop কী?

**2.** `for` loop-এর তিনটি অংশ কী?

**3.** `while` এবং `do...while`-এর পার্থক্য কী?

**4.** `break` কী করে?

**5.** `continue` কী করে?

**6.** `for...of` কী return করে?

**7.** `for...in` কী return করে?

**8.** Infinite loop কী?

**9.** Nested loop কী?

**10.** `for...of` এবং `for...in`-এর পার্থক্য কী?

---

## 💻 Coding Practice

### Problem 1 — 1 to 100

1 থেকে 100 পর্যন্ত print করো।

---

### Problem 2 — Even Numbers

1 থেকে 50 পর্যন্ত সব even number print করো।

---

### Problem 3 — Odd Numbers

1 থেকে 50 পর্যন্ত সব odd number print করো।

---

### Problem 4 — Sum

1 থেকে 100 পর্যন্ত সব number-এর sum বের করো।

Expected:

```text
5050
```

---

### Problem 5 — Multiplication Table

যেকোনো একটি number-এর 1 থেকে 10 পর্যন্ত multiplication table তৈরি করো।

---

### Problem 6 — Maximum

```javascript
let numbers = [10, 55, 23, 89, 12, 67];
```

সবচেয়ে বড় number বের করো।

Expected:

```text
89
```

---

### Problem 7 — Minimum

একই array থেকে সবচেয়ে ছোট number বের করো।

Expected:

```text
10
```

---

### Problem 8 — Search

```javascript
let students = [
    "Shariar",
    "Rahim",
    "Karim",
    "Hasan",
    "Nabil"
];
```

`Karim` আছে কিনা check করো।

---

### Problem 9 — Count Even

```javascript
let numbers = [1, 2, 4, 7, 8, 11, 14, 20];
```

কয়টি even number আছে সেটা বের করো।

---

### Problem 10 — Pattern

এই pattern তৈরি করো:

```text
*
**
***
****
*****
```

তারপর:

```text
*****
****
***
**
*
```

দুটোই নিজে code করার চেষ্টা করো।

---

# 🎯 Chapter 5-এর মূল শিক্ষা

এখন তোমার মাথায় এই flow-টা clear থাকা উচিত:

```text
Need to repeat something?
          ↓
      Choose Loop
          ↓
 ┌────────┼──────────┐
 ↓        ↓          ↓
for     while    do...while
          ↓
     Data collection?
          ↓
   ┌──────┴──────┐
   ↓             ↓
for...of      for...in
   ↓             ↓
 values         keys
```

আর সবচেয়ে important:

```text
break
→ Loop শেষ

continue
→ এই iteration বাদ

Nested Loop
→ Loop-এর ভিতরে Loop
```

পরের chapter-এ আমরা যাব **Chapter 6 — Functions**-এ। সেখানে JavaScript-এর সবচেয়ে গুরুত্বপূর্ণ building blocks-এর একটি নিয়ে বিস্তারিত করব: **Function কী, parameter, argument, return, function declaration/expression, arrow function, default parameter, rest parameter, callback function, higher-order function, scope, এবং practical functions**।
