# 📘 JavaScript Complete Book — Chapter 4

# Control Flow & Decision Making

### Control Flow & Decision Making — Program কোন পথে চলবে তা নিয়ন্ত্রণ করা

JavaScript-এর code সাধারণত **উপরে থেকে নিচে, একটার পর একটা** execute হয়। কিন্তু বাস্তব program-এ সবসময় এমন হয় না।

যেমন:

* বয়স 18 বা তার বেশি হলে → Account তৈরি করবে
* Password ভুল হলে → Error দেখাবে
* User logged in হলে → Dashboard দেখাবে
* Product stock-এ থাকলে → Buy button দেখাবে
* শুক্রবার হলে → বিশেষ message দেখাবে

এই ধরনের **condition অনুযায়ী program-এর execution path পরিবর্তন** করাকে বলা হয় **Control Flow**।

---

# 4.1 What is Control Flow?

**Control Flow** = Program-এর code কোন order-এ এবং কোন condition-এর ভিত্তিতে execute হবে।

### Real-Life Example

ধরো তুমি একটা shopping website-এ login করছো।

```text
Email + Password
       ↓
সঠিক?
 ┌─────┴─────┐
Yes          No
 ↓            ↓
Dashboard   Error
```

JavaScript-এ এই decision নেওয়ার জন্য সবচেয়ে বেশি ব্যবহার হয়:

* `if`
* `else`
* `else if`
* Nested `if`
* `switch`
* `case`
* `default`
* `break`
* `continue`
* Ternary operator
* Truthy / Falsy
* Logical conditions

---

# 4.2 `if` Statement

### `if` কী?

`if` ব্যবহার করে আমরা কোনো condition **true হলে** নির্দিষ্ট code execute করতে পারি।

### Syntax

```javascript
if (condition) {
    // code
}
```

### Example

```javascript
let age = 20;

if (age >= 18) {
    console.log("You are an adult.");
}
```

### Output

```text
You are an adult.
```

### কীভাবে কাজ করছে?

```javascript
age >= 18
```

এখানে:

```text
20 >= 18
```

ফলাফল:

```javascript
true
```

তাই `{ }` এর ভিতরের code execute হয়েছে।

---

# 4.3 `if` Condition False হলে

```javascript
let age = 15;

if (age >= 18) {
    console.log("You are an adult.");
}
```

### Output

```text
কিছুই দেখাবে না
```

কারণ:

```javascript
15 >= 18
```

ফলাফল:

```javascript
false
```

তাই `if` block execute হয়নি।

---

# 4.4 `if...else`

যখন condition **true হলে এক কাজ**, আর **false হলে অন্য কাজ** করতে হবে, তখন `if...else` ব্যবহার করি।

### Syntax

```javascript
if (condition) {
    // true হলে
} else {
    // false হলে
}
```

### Example

```javascript
let age = 16;

if (age >= 18) {
    console.log("You can vote.");
} else {
    console.log("You cannot vote yet.");
}
```

### Output

```text
You cannot vote yet.
```

### Real-Life Example

ATM-এ:

```text
Balance >= Withdraw Amount?
        ↓
      Yes → টাকা দাও
      No  → Insufficient Balance
```

JavaScript:

```javascript
let balance = 5000;
let withdraw = 7000;

if (balance >= withdraw) {
    console.log("Please collect your money.");
} else {
    console.log("Insufficient balance.");
}
```

### Output

```text
Insufficient balance.
```

---

# 4.5 `if...else if...else`

যখন একাধিক condition check করতে হবে তখন `else if` ব্যবহার করি।

### Syntax

```javascript
if (condition1) {

} else if (condition2) {

} else if (condition3) {

} else {

}
```

### Example — Marks

```javascript
let marks = 85;

if (marks >= 80) {
    console.log("Grade A+");
} else if (marks >= 70) {
    console.log("Grade A");
} else if (marks >= 60) {
    console.log("Grade A-");
} else if (marks >= 50) {
    console.log("Grade B");
} else {
    console.log("Fail");
}
```

### Output

```text
Grade A+
```

### Important

JavaScript উপরের condition থেকে check করে।

```text
marks >= 80 ? → Yes → A+

না হলে
marks >= 70 ? → Yes → A

না হলে
marks >= 60 ? → Yes → A-

...
```

একটা matching condition পাওয়ার পর নিচেরগুলো আর check করে না।

---

# 4.6 Multiple Conditions

একটা `if`-এর মধ্যে একাধিক condition দেওয়া যায়।

এখানে আমরা Chapter 3-এর logical operators ব্যবহার করব।

### `&&` — AND

দুটো condition-ই true হতে হবে।

```javascript
let age = 25;
let hasNID = true;

if (age >= 18 && hasNID) {
    console.log("You can open the account.");
}
```

### Output

```text
You can open the account.
```

কারণ:

```text
age >= 18 → true
hasNID → true

true && true → true
```

---

# 4.7 `||` — OR

যেকোনো একটি condition true হলেই হবে।

```javascript
let hasEmail = true;
let hasPhone = false;

if (hasEmail || hasPhone) {
    console.log("You can create an account.");
}
```

### Output

```text
You can create an account.
```

কারণ:

```text
true || false → true
```

---

# 4.8 `!` — NOT

`!` condition-এর result উল্টে দেয়।

```javascript
let isLoggedIn = false;

if (!isLoggedIn) {
    console.log("Please login first.");
}
```

### Output

```text
Please login first.
```

কারণ:

```javascript
isLoggedIn = false
```

তাই:

```javascript
!false
```

হয়ে যায়:

```javascript
true
```

---

# 4.9 Nested `if`

একটি `if`-এর ভিতরে আরেকটি `if` থাকলে তাকে **Nested if** বলে।

### Example

```javascript
let age = 22;
let hasNID = true;

if (age >= 18) {

    if (hasNID) {
        console.log("Account can be created.");
    }

}
```

### Output

```text
Account can be created.
```

### Real-Life Example

Bank account খুলতে:

```text
Age >= 18?
   ↓ Yes
NID আছে?
   ↓ Yes
Account Create
```

Nested `if` দিয়ে:

```javascript
if (age >= 18) {
    if (hasNID) {
        console.log("Account created.");
    }
}
```

---

# 4.10 Nested `if...else`

```javascript
let isLoggedIn = true;
let isAdmin = false;

if (isLoggedIn) {

    if (isAdmin) {
        console.log("Welcome Admin.");
    } else {
        console.log("Welcome User.");
    }

} else {
    console.log("Please login.");
}
```

### Output

```text
Welcome User.
```

---

# 4.11 `switch` Statement

যখন একটি variable-এর **একাধিক নির্দিষ্ট value** check করতে হয়, তখন `switch` অনেক useful।

### Syntax

```javascript
switch (value) {

    case value1:
        // code
        break;

    case value2:
        // code
        break;

    default:
        // code
}
```

### Example

```javascript
let day = 3;

switch (day) {

    case 1:
        console.log("Saturday");
        break;

    case 2:
        console.log("Sunday");
        break;

    case 3:
        console.log("Monday");
        break;

    case 4:
        console.log("Tuesday");
        break;

    default:
        console.log("Invalid day");
}
```

### Output

```text
Monday
```

কারণ:

```javascript
day = 3
```

তাই:

```javascript
case 3
```

match করেছে।

---

# 4.12 `case`

`switch`-এর মধ্যে প্রতিটি possible value-কে `case` বলা হয়।

```javascript
switch (day) {

    case 1:
        console.log("Saturday");
        break;

    case 2:
        console.log("Sunday");
        break;

}
```

এখানে:

```text
case 1
case 2
```

দুটি possible case।

---

# 4.13 `break`

`break` ব্যবহার করে `switch` execution বন্ধ করা হয়।

```javascript
let number = 2;

switch (number) {

    case 1:
        console.log("One");
        break;

    case 2:
        console.log("Two");
        break;

    case 3:
        console.log("Three");
        break;
}
```

### Output

```text
Two
```

`case 2` match করার পর:

```javascript
break;
```

এর কারণে switch শেষ হয়ে যায়।

---

# 4.14 `break` না দিলে কী হয়?

এটা খুব গুরুত্বপূর্ণ।

```javascript
let number = 2;

switch (number) {

    case 1:
        console.log("One");

    case 2:
        console.log("Two");

    case 3:
        console.log("Three");

    default:
        console.log("Other");
}
```

### Output

```text
Two
Three
Other
```

এটাকে বলা হয় **Fall-through**।

অর্থাৎ `case 2` match করার পর `break` না থাকায় পরের case-গুলোর code-ও execute করেছে।

---

# 4.15 Intentional Fall-through

কখনো কখনো আমরা ইচ্ছা করেই একাধিক case একই code-এর জন্য ব্যবহার করি।

### Example

```javascript
let day = "Saturday";

switch (day) {

    case "Saturday":
    case "Sunday":
        console.log("Weekend");
        break;

    default:
        console.log("Working day");
}
```

### Output

```text
Weekend
```

এখানে Saturday এবং Sunday দুটোতেই একই output।

---

# 4.16 `default`

কোনো `case` match না করলে `default` execute হয়।

```javascript
let day = 10;

switch (day) {

    case 1:
        console.log("Saturday");
        break;

    case 2:
        console.log("Sunday");
        break;

    default:
        console.log("Invalid day");
}
```

### Output

```text
Invalid day
```

### Real-Life Example

```text
Payment Method:

1 → bKash
2 → Nagad
3 → Card
অন্য কিছু → Invalid Payment Method
```

---

# 4.17 `switch` বনাম `if...else`

দুটো দিয়েই decision নেওয়া যায়।

### `if...else`

Range বা complex condition-এর জন্য ভালো:

```javascript
let marks = 75;

if (marks >= 80) {
    console.log("A+");
} else if (marks >= 70) {
    console.log("A");
}
```

### `switch`

Specific value-এর জন্য convenient:

```javascript
let role = "admin";

switch (role) {
    case "admin":
        console.log("Admin Panel");
        break;

    case "user":
        console.log("User Dashboard");
        break;
}
```

সহজভাবে:

| Situation                 | সাধারণত     |
| ------------------------- | ----------- |
| Range check               | `if...else` |
| Complex condition         | `if...else` |
| Exact value match         | `switch`    |
| অনেকগুলো নির্দিষ্ট option | `switch`    |

---

# 4.18 Truthy & Falsy

JavaScript-এর অন্যতম গুরুত্বপূর্ণ concept।

`if` condition-এর মধ্যে JavaScript কোনো value-কে automatically **true বা false হিসেবে evaluate** করে।

দুই ধরনের value:

```text
Truthy
Falsy
```

---

# 4.19 Falsy Values

JavaScript-এ প্রধান falsy values:

```javascript
false
0
-0
0n
""
null
undefined
NaN
```

এগুলো condition-এর মধ্যে false হিসেবে behave করে।

### Example

```javascript
let username = "";

if (username) {
    console.log("Username exists.");
} else {
    console.log("Username is empty.");
}
```

### Output

```text
Username is empty.
```

কারণ:

```javascript
""
```

একটি falsy value।

---

# 4.20 Truthy Values

Falsy ছাড়া প্রায় সব value truthy।

উদাহরণ:

```javascript
"hello"
42
-10
[]
{}
true
```

### Example

```javascript
let username = "Shariar";

if (username) {
    console.log("Username exists.");
}
```

### Output

```text
Username exists.
```

---

# 4.21 Empty Array `[]` কি falsy?

না। এটি **truthy**।

```javascript
if ([]) {
    console.log("Array is truthy");
}
```

### Output

```text
Array is truthy
```

---

# 4.22 Empty Object `{}` কি falsy?

না।

```javascript
if ({}) {
    console.log("Object is truthy");
}
```

### Output

```text
Object is truthy
```

এটা beginnerদের জন্য খুব important।

---

# 4.23 Conditional Operator / Ternary Operator

আগের Chapter-এ আমরা Ternary দেখেছি।

এটা `if...else`-এর ছোট version।

### Syntax

```javascript
condition ? valueIfTrue : valueIfFalse;
```

### Example

```javascript
let age = 20;

let result = age >= 18 ? "Adult" : "Minor";

console.log(result);
```

### Output

```text
Adult
```

Equivalent `if...else`:

```javascript
let age = 20;
let result;

if (age >= 18) {
    result = "Adult";
} else {
    result = "Minor";
}

console.log(result);
```

দুটোর output একই।

---

# 4.24 Real-Life Ternary Example

ধরো website-এ login status দেখাতে হবে।

```javascript
let isLoggedIn = true;

let message = isLoggedIn
    ? "Welcome back!"
    : "Please login.";

console.log(message);
```

### Output

```text
Welcome back!
```

---

# 4.25 Nested Ternary

Ternary-এর ভিতরে Ternary দেওয়া যায়।

```javascript
let marks = 85;

let grade =
    marks >= 80 ? "A+"
    : marks >= 70 ? "A"
    : marks >= 60 ? "A-"
    : "Fail";

console.log(grade);
```

### Output

```text
A+
```

### কিন্তু সাবধান ⚠️

অনেক বেশি nested ternary code difficult to read করতে পারে।

তাই complex logic হলে:

```javascript
if...else
```

ব্যবহার করা বেশি readable।

---

# 4.26 Short-Circuit Decision Making

Chapter 3-এ আমরা short-circuit দেখেছি। এখন control flow-এর সঙ্গে এটি ব্যবহার করি।

### `&&`

```javascript
let isLoggedIn = true;

isLoggedIn && console.log("Show Dashboard");
```

### Output

```text
Show Dashboard
```

যদি:

```javascript
let isLoggedIn = false;
```

তাহলে:

```javascript
isLoggedIn && console.log("Show Dashboard");
```

কিছু execute হবে না।

কারণ:

```text
false && anything → false
```

---

# 4.27 `||` দিয়ে Default Value

```javascript
let username = "";

let displayName = username || "Guest";

console.log(displayName);
```

### Output

```text
Guest
```

কারণ:

```javascript
"" || "Guest"
```

→ `"Guest"`

### Real-Life

Website-এ username না থাকলে:

```text
Guest
```

দেখাবে।

---

# 4.28 `??` Nullish Coalescing

`||` এবং `??` এক জিনিস না।

`??` শুধুমাত্র:

```javascript
null
undefined
```

হলে right side value নেয়।

### Example

```javascript
let username = null;

let name = username ?? "Guest";

console.log(name);
```

### Output

```text
Guest
```

কিন্তু:

```javascript
let username = "";

let name = username ?? "Guest";

console.log(name);
```

### Output

```text
```

কারণ `""` null বা undefined নয়।

---

# 4.29 `||` বনাম `??`

```javascript
let value = 0;

console.log(value || 100);
console.log(value ?? 100);
```

### Output

```text
100
0
```

কারণ:

```javascript
0 || 100
```

→ `100`

কিন্তু:

```javascript
0 ?? 100
```

→ `0`

### মনে রাখবে

```text
|| → falsy হলে fallback
?? → null/undefined হলে fallback
```

---

# 4.30 Optional Chaining `?.` দিয়ে Safe Decision

ধরো:

```javascript
let user = {};
```

এখন:

```javascript
console.log(user.profile.name);
```

এতে error হতে পারে, কারণ `profile` নেই।

Optional chaining:

```javascript
console.log(user.profile?.name);
```

### Output

```text
undefined
```

এতে program crash না করে `undefined` পাওয়া যায়।

---

# 4.31 `if` + Optional Chaining

```javascript
let user = {
    profile: {
        name: "Shariar"
    }
};

if (user.profile?.name) {
    console.log("Name:", user.profile.name);
}
```

### Output

```text
Name: Shariar
```

---

# 4.32 Multiple Conditions Example

এবার একটা real-world login system দেখি।

```javascript
let email = "user@gmail.com";
let password = "123456";
let isVerified = true;

if (
    email === "user@gmail.com" &&
    password === "123456" &&
    isVerified
) {
    console.log("Login successful.");
} else {
    console.log("Invalid login information.");
}
```

### Output

```text
Login successful.
```

### এখানে ৩টি condition:

```javascript
email === "user@gmail.com"
```

```javascript
password === "123456"
```

```javascript
isVerified
```

সব true হওয়ায়:

```text
true && true && true
```

→ `true`

---

# 4.33 E-commerce Example

ধরো একটি product:

```javascript
let price = 1500;
let stock = 5;
let isLoggedIn = true;

if (isLoggedIn && stock > 0) {
    console.log("You can buy this product.");
} else {
    console.log("You cannot buy this product.");
}
```

### Output

```text
You can buy this product.
```

---

# 4.34 Discount System

```javascript
let totalAmount = 6000;

if (totalAmount >= 10000) {
    console.log("20% discount");
} else if (totalAmount >= 5000) {
    console.log("10% discount");
} else if (totalAmount >= 2000) {
    console.log("5% discount");
} else {
    console.log("No discount");
}
```

### Output

```text
10% discount
```

### Real-Life Flow

```text
৳10,000+ → 20%
৳5,000+  → 10%
৳2,000+  → 5%
এর কম     → No discount
```

---

# 4.35 Grading System

এটা নিজে খুব ভালোভাবে practice করবে।

```javascript
let marks = 76;

if (marks >= 80) {
    console.log("A+");
} else if (marks >= 70) {
    console.log("A");
} else if (marks >= 60) {
    console.log("A-");
} else if (marks >= 50) {
    console.log("B");
} else if (marks >= 40) {
    console.log("C");
} else if (marks >= 33) {
    console.log("D");
} else {
    console.log("F");
}
```

### Output

```text
A
```

---

# 4.36 Login + Role Based Access

এটা real-world web development-এ খুব common।

```javascript
let isLoggedIn = true;
let role = "admin";

if (isLoggedIn) {

    if (role === "admin") {
        console.log("Welcome to Admin Dashboard.");
    } else if (role === "teacher") {
        console.log("Welcome to Teacher Dashboard.");
    } else {
        console.log("Welcome to User Dashboard.");
    }

} else {
    console.log("Please login first.");
}
```

### Output

```text
Welcome to Admin Dashboard.
```

এই ধরনের logic পরে React, Node.js, Express, authentication system ইত্যাদিতে অনেক কাজে লাগবে।

---

# 4.37 `switch` দিয়ে Role System

একই কাজ `switch` দিয়েও করা যায়।

```javascript
let role = "teacher";

switch (role) {

    case "admin":
        console.log("Admin Dashboard");
        break;

    case "teacher":
        console.log("Teacher Dashboard");
        break;

    case "student":
        console.log("Student Dashboard");
        break;

    default:
        console.log("Unknown Role");
}
```

### Output

```text
Teacher Dashboard
```

---

# 4.38 Important Difference: `==` vs `===`

Control flow-এ এটি অনেক important।

### `==`

Type conversion করতে পারে।

```javascript
let age = "18";

if (age == 18) {
    console.log("Matched");
}
```

### Output

```text
Matched
```

কিন্তু:

```javascript
if (age === 18) {
    console.log("Matched");
}
```

### Output

```text
কিছুই দেখাবে না
```

কারণ:

```text
"18" → String
18   → Number
```

Strict equality:

```javascript
"18" === 18
```

→ `false`

### Best Practice

সাধারণত condition-এ:

```javascript
===
```

ব্যবহার করা ভালো।

---

# 4.39 Common Mistake: `=` এবং `===`

ভুল:

```javascript
if (age = 18) {
    console.log("Adult");
}
```

এখানে `=` assignment operator।

সঠিক:

```javascript
if (age === 18) {
    console.log("Adult");
}
```

---

# 4.40 Common Mistake: Semicolon নিয়ে সমস্যা

JavaScript-এ সাধারণত:

```javascript
if (age >= 18); {
    console.log("Adult");
}
```

এটা ভুল logic।

এই:

```javascript
;
```

এর কারণে `if`-এর সঙ্গে block properly connected থাকে না।

সঠিক:

```javascript
if (age >= 18) {
    console.log("Adult");
}
```

---

# 4.41 Curly Braces ব্যবহার করা

Technically single statement হলে braces ছাড়া লেখা যায়:

```javascript
if (age >= 18)
    console.log("Adult");
```

কিন্তু professional code-এ সাধারণত:

```javascript
if (age >= 18) {
    console.log("Adult");
}
```

ব্যবহার করা হয়।

এতে code readable এবং maintainable হয়।

---

# 4.42 Control Flow-এর Complete Picture

এখন পুরো Chapter-এর concept একসাথে:

```text
                  Program
                     ↓
                 Condition?
                /          \
             true          false
              ↓              ↓
            if            else
              ↓
       Another condition?
          /          \
       true          false
        ↓              ↓
    else if          else
```

আর specific values হলে:

```text
             switch
                ↓
       ┌────────┼────────┐
     case 1   case 2   case 3
       ↓        ↓        ↓
      break    break    break
                ↓
             default
```

---

# 4.43 Real-World Mini Project — ATM Decision System

এবার সব concept ব্যবহার করে ছোট একটা project।

```javascript
let balance = 10000;
let withdrawAmount = 3000;
let pinCorrect = true;

if (pinCorrect) {

    if (withdrawAmount <= balance) {

        balance -= withdrawAmount;

        console.log("Withdrawal successful.");
        console.log("Withdrawn:", withdrawAmount);
        console.log("Remaining balance:", balance);

    } else {

        console.log("Insufficient balance.");

    }

} else {

    console.log("Incorrect PIN.");

}
```

### Output

```text
Withdrawal successful.
Withdrawn: 3000
Remaining balance: 7000
```

### কী হচ্ছে?

প্রথমে:

```javascript
pinCorrect
```

check করছে।

সঠিক হলে:

```javascript
withdrawAmount <= balance
```

check করছে।

তারপর:

```javascript
balance -= withdrawAmount;
```

শেষে balance:

```text
10000 - 3000 = 7000
```

---

# 4.44 Mini Project — Online Shopping Checkout

```javascript
let isLoggedIn = true;
let productInStock = true;
let price = 2500;
let balance = 3000;

if (isLoggedIn) {

    if (productInStock) {

        if (balance >= price) {

            balance -= price;

            console.log("Order placed successfully.");
            console.log("Remaining balance:", balance);

        } else {

            console.log("Insufficient balance.");

        }

    } else {

        console.log("Product is out of stock.");

    }

} else {

    console.log("Please login first.");

}
```

### Output

```text
Order placed successfully.
Remaining balance: 500
```

---

# 4.45 Chapter 4 — Quick Cheat Sheet

| Concept     | কাজ                             |   |                           |
| ----------- | ------------------------------- | - | ------------------------- |
| `if`        | Condition true হলে code চালায়   |   |                           |
| `else`      | Condition false হলে code চালায়  |   |                           |
| `else if`   | Multiple condition check করে    |   |                           |
| Nested `if` | `if`-এর ভিতরে `if`              |   |                           |
| `switch`    | Specific value match করে        |   |                           |
| `case`      | `switch`-এর possible value      |   |                           |
| `break`     | `switch`/loop থেকে বের হয়       |   |                           |
| `default`   | কোনো case match না করলে চলে     |   |                           |
| `&&`        | সব condition true হতে হবে       |   |                           |
| `           |                                 | ` | যেকোনো একটি true হলেই হবে |
| `!`         | Boolean result উল্টায়           |   |                           |
| `?:`        | Short `if...else`               |   |                           |
| `??`        | `null`/`undefined` হলে fallback |   |                           |
| `?.`        | Safe property access            |   |                           |
| Truthy      | `if`-এ true হিসেবে behave করে   |   |                           |
| Falsy       | `if`-এ false হিসেবে behave করে  |   |                           |

---

# 🧠 Chapter 4 — Must Remember

### 1️⃣ `if`

```javascript
if (condition) {
    // code
}
```

### 2️⃣ `if...else`

```javascript
if (condition) {
    // true
} else {
    // false
}
```

### 3️⃣ `else if`

```javascript
if (condition1) {

} else if (condition2) {

} else {

}
```

### 4️⃣ `switch`

```javascript
switch (value) {

    case 1:
        // code
        break;

    case 2:
        // code
        break;

    default:
        // code
}
```

### 5️⃣ Ternary

```javascript
condition ? trueValue : falseValue;
```

### 6️⃣ Truthy/Falsy

```javascript
if (value) {
    // truthy
}
```

### 7️⃣ Default value

```javascript
let name = username ?? "Guest";
```

---

# 📝 Chapter 4 — Practice Questions

### Basic

**1.** `if` statement কী?

**2.** `if` এবং `else`-এর মধ্যে পার্থক্য কী?

**3.** `else if` কখন ব্যবহার করা হয়?

**4.** `switch` কী?

**5.** `break` কেন ব্যবহার করা হয়?

**6.** `default` কী?

**7.** Truthy এবং Falsy কী?

**8.** JavaScript-এর প্রধান falsy values কী কী?

**9.** `&&` এবং `||`-এর মধ্যে পার্থক্য কী?

**10.** Ternary operator কী?

---

### Coding Practice

**Problem 1 — Even/Odd**

```javascript
let number = 25;
```

Check করো number even নাকি odd।

Expected:

```text
Odd
```

---

**Problem 2 — Age Checker**

```javascript
let age = 17;
```

Output:

```text
Adult
```

অথবা:

```text
Minor
```

---

**Problem 3 — Grade System**

```javascript
let marks = 92;
```

Grade বের করো।

---

**Problem 4 — Login System**

এই তিনটা variable ব্যবহার করো:

```javascript
let email = "admin@gmail.com";
let password = "1234";
let isVerified = true;
```

সব ঠিক থাকলে:

```text
Login Successful
```

না হলে:

```text
Login Failed
```

---

**Problem 5 — Shopping**

```javascript
let price = 5000;
let balance = 6000;
let inStock = true;
```

Check করো product কেনা যাবে কি না।

---

# 🚀 Chapter 4 শেষ করার পর তুমি যা বুঝবে

এই Chapter শেষ করলে তুমি JavaScript-এ:

```text
Condition
   ↓
Decision
   ↓
Different Code Path
```

এই পুরো concept বুঝে যাবে।

এগুলোই পরে বাস্তব application-এর:

* Login system
* Signup validation
* Admin/User role
* Shopping cart
* Payment checking
* Attendance system
* Dashboard access
* Form validation
* API response handling

ইত্যাদির basic decision-making logic তৈরি করবে।

---

## 📚 Next Chapter

### **Chapter 5 — Loops & Iteration**

এখানে আমরা একদম বিস্তারিতভাবে শিখব:

* `for` loop
* `while` loop
* `do...while`
* `for...of`
* `for...in`
* Nested loops
* `break`
* `continue`
* Infinite loop
* Loop control
* Arrays-এর সঙ্গে loop
* Objects-এর সঙ্গে loop
* Real-life examples
* Pattern printing
* Practical mini projects

এবং প্রতিটি topic হবে **Concept → Code → Output → সহজ Bangla explanation → Real-life example** এই একই format-এ।
