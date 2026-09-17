# 📘 JavaScript Complete Book — Chapter 8

# Strings — String / টেক্সট নিয়ে কাজ

JavaScript-এ **String** হলো text বা character-এর sequence।

যেমন:

```javascript
let name = "Shariar";
let university = "Daffodil International University";
let message = "Hello JavaScript!";
```

এগুলো সবই **String**।

---

# 8.1 String কী?

সহজভাবে:

> **String = এক বা একাধিক character-এর collection যা text represent করে।**

### Real-life Example

একটি website-এ:

```text
Name: Shariar Ahamed Ripon
Email: ripon@example.com
Address: Dhaka, Bangladesh
```

এখানে `Name`, `Email`, `Address`-এর value—সবই String।

---

# 8.2 String তৈরি করার ৩টি উপায়

JavaScript-এ String সাধারণত তিনভাবে লেখা যায়:

### 1. Double Quotes

```javascript
let name = "Shariar";
```

### 2. Single Quotes

```javascript
let name = 'Shariar';
```

### 3. Backticks

```javascript
let name = `Shariar`;
```

তিনটিই valid।

---

# 8.3 Single Quote vs Double Quote

```javascript
let name1 = "Shariar";
let name2 = 'Shariar';

console.log(name1);
console.log(name2);
```

### Output

```text
Shariar
Shariar
```

কাজের দিক থেকে দুটোই প্রায় একই।

---

# 8.4 Backticks

Backtick:

```text
`
```

এটি বিশেষভাবে গুরুত্বপূর্ণ কারণ এর মাধ্যমে **Template Literal** ব্যবহার করা যায়।

```javascript
let name = `Shariar`;

console.log(name);
```

Output:

```text
Shariar
```

Template Literal আমরা পরে বিস্তারিত দেখব।

---

# 8.5 String-এর মধ্যে Quote ব্যবহার

ধরো text-এর মধ্যে quotation mark লাগবে।

```javascript
let message = 'He said "Hello"';

console.log(message);
```

### Output

```text
He said "Hello"
```

অথবা:

```javascript
let message = "It's a beautiful day";

console.log(message);
```

Output:

```text
It's a beautiful day
```

---

# 8.6 Escape Character

String-এর মধ্যে একই ধরনের quote ব্যবহার করতে হলে `\` ব্যবহার করা যায়।

```javascript
let message = "He said \"Hello\"";

console.log(message);
```

### Output

```text
He said "Hello"
```

এখানে:

```text
\"
```

মানে quote-টিকে String-এর শেষ হিসেবে না ধরে character হিসেবে ব্যবহার করো।

---

# 8.7 Common Escape Characters

| Escape | অর্থ            |
| ------ | --------------- |
| `\"`   | Double quote    |
| `\'`   | Single quote    |
| `\\`   | Backslash       |
| `\n`   | New line        |
| `\t`   | Tab             |
| `\r`   | Carriage return |
| `\b`   | Backspace       |
| `\f`   | Form feed       |

---

# 8.8 New Line — `\n`

```javascript
let message = "Hello\nJavaScript";

console.log(message);
```

### Output

```text
Hello
JavaScript
```

Real-life example:

```javascript
let address = "Dhaka\nBangladesh";

console.log(address);
```

Output:

```text
Dhaka
Bangladesh
```

---

# 8.9 Tab — `\t`

```javascript
console.log("Name:\tShariar");
```

Output:

```text
Name:   Shariar
```

---

# 8.10 String Length

String-এর character সংখ্যা জানতে:

```javascript
.length
```

ব্যবহার করা হয়।

```javascript
let name = "Shariar";

console.log(name.length);
```

### Output

```text
7
```

কারণ:

```text
S h a r i a r
1 2 3 4 5 6 7
```

---

# 8.11 Space-ও Character

```javascript
let name = "Shariar Ahamed";

console.log(name.length);
```

Space-ও count হবে।

---

# 8.12 String Index

JavaScript-এ String-এর প্রতিটি character-এর একটি index থাকে।

Index শুরু হয়:

```text
0
```

থেকে।

```javascript
let name = "Ripon";
```

এটা:

```text
R i p o n
0 1 2 3 4
```

---

# 8.13 Character Access — `[]`

```javascript
let name = "Ripon";

console.log(name[0]);
console.log(name[1]);
console.log(name[4]);
```

### Output

```text
R
i
n
```

---

# 8.14 প্রথম Character

```javascript
let name = "JavaScript";

console.log(name[0]);
```

Output:

```text
J
```

---

# 8.15 শেষ Character

শেষ character বের করতে:

```javascript
let name = "JavaScript";

console.log(name[name.length - 1]);
```

Output:

```text
t
```

কারণ length:

```text
10
```

শেষ index:

```text
10 - 1 = 9
```

---

# 8.16 `.at()` Method

শেষ character আরও সহজে:

```javascript
let name = "JavaScript";

console.log(name.at(-1));
```

Output:

```text
t
```

`at()` negative index support করে।

```javascript
console.log(name.at(-2));
```

Output:

```text
p
```

---

# 8.17 `charAt()`

```javascript
let name = "Ripon";

console.log(name.charAt(0));
console.log(name.charAt(2));
```

Output:

```text
R
p
```

### `[]` বনাম `charAt()`

```javascript
let name = "Ripon";

console.log(name[10]);
console.log(name.charAt(10));
```

Output:

```text
undefined

```

`charAt()` invalid index-এ empty string (`""`) দেয়, আর `[]` সাধারণত `undefined` দেয়।

---

# 8.18 String Concatenation

দুই বা তার বেশি String একসাথে যুক্ত করাকে **Concatenation** বলে।

```javascript
let firstName = "Shariar";
let lastName = "Ripon";

let fullName = firstName + " " + lastName;

console.log(fullName);
```

### Output

```text
Shariar Ripon
```

---

# 8.19 String + Number

```javascript
let age = 23;

console.log("Age: " + age);
```

Output:

```text
Age: 23
```

JavaScript এখানে number-কে String-এর সাথে concatenate করেছে।

---

# 8.20 `+=` দিয়ে String যোগ

```javascript
let message = "Hello";

message += " ";
message += "JavaScript";

console.log(message);
```

Output:

```text
Hello JavaScript
```

---

# 8.21 Template Literals

Modern JavaScript-এ String তৈরি করার সবচেয়ে useful featureগুলোর একটি হলো:

> **Template Literal**

Backtick ব্যবহার করতে হয়:

```javascript
` `
```

### Example

```javascript
let name = "Shariar";
let age = 23;

let message = `My name is ${name} and I am ${age} years old.`;

console.log(message);
```

### Output

```text
My name is Shariar and I am 23 years old.
```

---

# 8.22 `${}` কী?

Template Literal-এর মধ্যে:

```javascript
${variable}
```

ব্যবহার করে variable-এর value বসানো যায়।

```javascript
let product = "Laptop";
let price = 75000;

console.log(`Product: ${product}`);
console.log(`Price: ${price} BDT`);
```

Output:

```text
Product: Laptop
Price: 75000 BDT
```

---

# 8.23 Expression-এর ব্যবহার

শুধু variable নয়, expression-ও দেওয়া যায়।

```javascript
let a = 10;
let b = 20;

console.log(`Total = ${a + b}`);
```

Output:

```text
Total = 30
```

---

# 8.24 Function-এর Result

```javascript
function getName() {
    return "Shariar";
}

console.log(`Hello ${getName()}`);
```

Output:

```text
Hello Shariar
```

---

# 8.25 Multiline String

Normal quote-এ:

```javascript
let message = "Hello
JavaScript";
```

এভাবে সরাসরি লিখলে error হবে।

কিন্তু Template Literal:

```javascript
let message = `Hello
JavaScript
World`;

console.log(message);
```

Output:

```text
Hello
JavaScript
World
```

---

# 8.26 `toUpperCase()`

String-এর সব letter uppercase করতে:

```javascript
let name = "shariar";

console.log(name.toUpperCase());
```

Output:

```text
SHARIAR
```

---

# 8.27 `toLowerCase()`

```javascript
let name = "SHARIAR";

console.log(name.toLowerCase());
```

Output:

```text
shariar
```

---

# 8.28 Real-life Example — Login

User email:

```javascript
let email = "USER@GMAIL.COM";

console.log(email.toLowerCase());
```

Output:

```text
user@gmail.com
```

Login system-এ case normalization-এর মতো কাজে এটি useful হতে পারে।

---

# 8.29 `trim()`

User input-এর শুরু বা শেষে extra space থাকলে:

```javascript
let username = "   Shariar   ";

console.log(username.trim());
```

Output:

```text
Shariar
```

এটি:

```text
"   Shariar   "
```

কে:

```text
"Shariar"
```

করে।

---

# 8.30 `trimStart()`

শুধু শুরু থেকে whitespace remove:

```javascript
let text = "   Hello";

console.log(text.trimStart());
```

Output:

```text
Hello
```

---

# 8.31 `trimEnd()`

শুধু শেষ থেকে:

```javascript
let text = "Hello   ";

console.log(text.trimEnd());
```

Output:

```text
Hello
```

---

# 8.32 `includes()`

কোনো String-এর মধ্যে নির্দিষ্ট text আছে কিনা check করতে:

```javascript
let message = "I love JavaScript";

console.log(message.includes("JavaScript"));
```

Output:

```text
true
```

না থাকলে:

```javascript
console.log(message.includes("Python"));
```

Output:

```text
false
```

---

# 8.33 Real-life Example — Search

```javascript
let title = "JavaScript Complete Course";

let search = "JavaScript";

if (title.includes(search)) {
    console.log("Match found");
}
```

Output:

```text
Match found
```

---

# 8.34 `startsWith()`

String কোনো নির্দিষ্ট text দিয়ে শুরু হয়েছে কিনা:

```javascript
let url = "https://example.com";

console.log(url.startsWith("https"));
```

Output:

```text
true
```

---

# 8.35 `endsWith()`

```javascript
let file = "profile.jpg";

console.log(file.endsWith(".jpg"));
```

Output:

```text
true
```

Real-life:

```javascript
let file = "document.pdf";

if (file.endsWith(".pdf")) {
    console.log("PDF file");
}
```

---

# 8.36 `indexOf()`

কোনো text কোথায় আছে তা বের করতে:

```javascript
let text = "I love JavaScript";

console.log(text.indexOf("JavaScript"));
```

Output:

```text
7
```

কারণ `"JavaScript"` শুরু হয়েছে index `7` থেকে।

---

# 8.37 `indexOf()` না পেলে

```javascript
let text = "I love JavaScript";

console.log(text.indexOf("Python"));
```

Output:

```text
-1
```

অর্থাৎ:

```text
-1 = পাওয়া যায়নি
```

---

# 8.38 `lastIndexOf()`

একই text একাধিকবার থাকলে শেষ occurrence-এর index পাওয়া যায়।

```javascript
let text = "JavaScript is great. JavaScript is powerful.";

console.log(text.lastIndexOf("JavaScript"));
```

Output:

```text
21
```

---

# 8.39 `search()`

```javascript
let text = "I love JavaScript";

console.log(text.search("JavaScript"));
```

Output:

```text
7
```

`search()` পরে Regex-এর সাথে আরও useful হবে।

---

# 8.40 `slice()`

String-এর একটি অংশ বের করতে:

```javascript
slice(start, end)
```

### Example

```javascript
let text = "JavaScript";

console.log(text.slice(0, 4));
```

Output:

```text
Java
```

মনে রাখবে:

> `end` index include হয় না।

---

# 8.41 `slice()` Example

```javascript
let text = "JavaScript";

console.log(text.slice(4, 10));
```

Output:

```text
Script
```

Index:

```text
J a v a S c r i p t
0 1 2 3 4 5 6 7 8 9
```

---

# 8.42 Negative `slice()`

```javascript
let text = "JavaScript";

console.log(text.slice(-6));
```

Output:

```text
Script
```

শেষ ৬টি character।

---

# 8.43 `substring()`

```javascript
let text = "JavaScript";

console.log(text.substring(0, 4));
```

Output:

```text
Java
```

`substring()` negative index-কে `0` হিসেবে treat করে।

---

# 8.44 `slice()` vs `substring()`

| Feature        | `slice()` | `substring()` |
| -------------- | --------- | ------------- |
| Negative index | ✅         | ❌             |
| End excluded   | ✅         | ✅             |
| সাধারণ ব্যবহার | বেশি      | কম            |

Modern code-এ অনেক ক্ষেত্রে `slice()` বেশি convenient।

---

# 8.45 `substr()` — পুরোনো Method

```javascript
text.substr(start, length)
```

এটি পুরোনো/deprecated API।

নতুন code-এ সাধারণত ব্যবহার না করে:

```javascript
slice()
```

ব্যবহার করা ভালো।

---

# 8.46 `replace()`

String-এর একটি অংশ replace করতে:

```javascript
let text = "I love JavaScript";

let result = text.replace("JavaScript", "Python");

console.log(result);
```

Output:

```text
I love Python
```

---

# 8.47 Important — `replace()` Original String পরিবর্তন করে না

```javascript
let text = "Hello World";

let result = text.replace("World", "JavaScript");

console.log(text);
console.log(result);
```

Output:

```text
Hello World
Hello JavaScript
```

কারণ String **immutable**।

---

# 8.48 String Immutability

এটি খুব গুরুত্বপূর্ণ।

String তৈরি হওয়ার পর তার character সরাসরি পরিবর্তন করা যায় না।

```javascript
let name = "Ripon";

name[0] = "S";

console.log(name);
```

Output:

```text
Ripon
```

`R` → `S` হয়নি।

---

# 8.49 তাহলে String পরিবর্তন কীভাবে হয়?

নতুন String তৈরি হয়।

```javascript
let name = "Ripon";

name = "Shariar";

console.log(name);
```

এখানে পুরোনো String পরিবর্তন না হয়ে নতুন value assign হয়েছে।

---

# 8.50 `replaceAll()`

সব occurrence replace করতে:

```javascript
let text = "apple apple apple";

console.log(text.replaceAll("apple", "banana"));
```

Output:

```text
banana banana banana
```

---

# 8.51 `concat()`

দুটি String যুক্ত করতে:

```javascript
let first = "Hello";
let second = "World";

console.log(first.concat(" ", second));
```

Output:

```text
Hello World
```

তবে modern JavaScript-এ সাধারণত:

```javascript
first + " " + second
```

অথবা template literal বেশি readable।

---

# 8.52 `split()`

String-কে Array-তে ভাগ করতে:

```javascript
let text = "HTML CSS JavaScript";

let result = text.split(" ");

console.log(result);
```

Output:

```text
["HTML", "CSS", "JavaScript"]
```

---

# 8.53 `split()` with Comma

```javascript
let skills = "HTML,CSS,JavaScript,React";

console.log(skills.split(","));
```

Output:

```text
["HTML", "CSS", "JavaScript", "React"]
```

এটি real-world data processing-এ খুব useful।

---

# 8.54 String → Array → String

```javascript
let skills = "HTML,CSS,JavaScript";

let arr = skills.split(",");

console.log(arr);

let result = arr.join(" | ");

console.log(result);
```

Output:

```text
["HTML", "CSS", "JavaScript"]

HTML | CSS | JavaScript
```

---

# 8.55 `repeat()`

একটি String নির্দিষ্ট সংখ্যকবার repeat করতে:

```javascript
let text = "Hi ";

console.log(text.repeat(3));
```

Output:

```text
Hi Hi Hi
```

---

# 8.56 `padStart()`

String-এর শুরুতে character যোগ করে নির্দিষ্ট length করা যায়।

```javascript
let number = "5";

console.log(number.padStart(3, "0"));
```

Output:

```text
005
```

---

# 8.57 `padEnd()`

```javascript
let number = "5";

console.log(number.padEnd(3, "0"));
```

Output:

```text
500
```

---

# 8.58 Real-life Example — Invoice Number

```javascript
let invoiceNumber = "25";

let formatted = invoiceNumber.padStart(5, "0");

console.log(formatted);
```

Output:

```text
00025
```

---

# 8.59 `charCodeAt()`

Character-এর UTF-16 code unit value পাওয়া যায়।

```javascript
let letter = "A";

console.log(letter.charCodeAt(0));
```

Output:

```text
65
```

আর:

```javascript
console.log("a".charCodeAt(0));
```

Output:

```text
97
```

---

# 8.60 `String.fromCharCode()`

Code value থেকে String character তৈরি করা যায়।

```javascript
console.log(String.fromCharCode(65));
```

Output:

```text
A
```

---

# 8.61 Unicode

JavaScript String Unicode text handle করতে পারে।

```javascript
let text = "বাংলাদেশ";

console.log(text);
```

Output:

```text
বাংলাদেশ
```

আর:

```javascript
let text = "Hello 👋";

console.log(text);
```

Output:

```text
Hello 👋
```

---

# 8.62 `localeCompare()`

দুটি String compare করতে:

```javascript
console.log("apple".localeCompare("banana"));
```

সাধারণত negative result পাওয়া যাবে, কারণ `"apple"` আগে।

```javascript
console.log("banana".localeCompare("apple"));
```

সাধারণত positive result।

```javascript
console.log("apple".localeCompare("apple"));
```

Output:

```text
0
```

Sorting-এর সময় এটি useful।

---

# 8.63 Case-sensitive Comparison

```javascript
console.log("hello" === "Hello");
```

Output:

```text
false
```

কারণ:

```text
h ≠ H
```

---

# 8.64 Case-insensitive Comparison

দুটিকে একই case-এ convert করে compare করতে পারো:

```javascript
let a = "Hello";
let b = "HELLO";

console.log(a.toLowerCase() === b.toLowerCase());
```

Output:

```text
true
```

---

# 8.65 String Object বনাম Primitive String

সাধারণভাবে:

```javascript
let name = "Ripon";
```

এটি primitive String।

আর:

```javascript
let name = new String("Ripon");
```

এটি String object।

### Important

সাধারণ application code-এ:

```javascript
new String()
```

ব্যবহার না করাই ভালো।

Primitive String ব্যবহার করো:

```javascript
let name = "Ripon";
```

---

# 8.66 `typeof String`

```javascript
let name = "Ripon";

console.log(typeof name);
```

Output:

```text
string
```

কিন্তু:

```javascript
let name = new String("Ripon");

console.log(typeof name);
```

Output:

```text
object
```

---

# 8.67 String Conversion

Number → String:

```javascript
let age = 23;

console.log(String(age));
```

Output:

```text
"23"
```

অথবা:

```javascript
console.log(age.toString());
```

Output:

```text
"23"
```

---

# 8.68 Real-life Example — User Input

Browser-এর form input সাধারণত String হিসেবে আসে।

```javascript
let age = "23";

console.log(typeof age);
```

Output:

```text
string
```

Number হিসেবে দরকার হলে:

```javascript
let numericAge = Number(age);

console.log(numericAge);
console.log(typeof numericAge);
```

Output:

```text
23
number
```

---

# 8.69 String Methods একসাথে

একটি String:

```javascript
let text = "  JavaScript is Awesome  ";
```

এর উপর:

```javascript
console.log(text.trim());
console.log(text.toUpperCase());
console.log(text.toLowerCase());
console.log(text.includes("JavaScript"));
console.log(text.startsWith("  Java"));
console.log(text.endsWith("  "));
```

এভাবে বিভিন্ন operation করা যায়।

---

# 8.70 Real-life Project Example — Username Formatter

ধরো user লিখেছে:

```text
   SHARIAR AHAMED RIPON
```

আমরা চাই:

```text
shariar ahamed ripon
```

Code:

```javascript
let username = "   SHARIAR AHAMED RIPON   ";

let formattedUsername = username
    .trim()
    .toLowerCase();

console.log(formattedUsername);
```

Output:

```text
shariar ahamed ripon
```

---

# 8.71 Real-life Example — Email Normalization

```javascript
let email = "   USER@GMAIL.COM   ";

email = email.trim().toLowerCase();

console.log(email);
```

Output:

```text
user@gmail.com
```

---

# 8.72 Real-life Example — File Extension

```javascript
let fileName = "profile.png";

if (fileName.endsWith(".png")) {
    console.log("PNG image detected");
}
```

Output:

```text
PNG image detected
```

---

# 8.73 Real-life Example — Search Box

```javascript
let product = "HP Laptop Core i5";

let search = "laptop";

if (product.toLowerCase().includes(search.toLowerCase())) {
    console.log("Product found");
}
```

Output:

```text
Product found
```

এটি e-commerce search functionality-এর basic concept।

---

# 8.74 Real-life Example — Generate Profile Message

```javascript
let name = "Shariar";
let skill = "Full Stack Development";
let experience = 1;

let message = `
Hello, I am ${name}.
I am learning ${skill}.
Experience: ${experience} year.
`;

console.log(message);
```

Output:

```text
Hello, I am Shariar.
I am learning Full Stack Development.
Experience: 1 year.
```

---

# 8.75 String Methods Cheat Sheet 🧠

| Method                  | কাজ                         |
| ----------------------- | --------------------------- |
| `.length`               | String-এর length            |
| `[index]`               | Character access            |
| `.at()`                 | Character access            |
| `.charAt()`             | Character access            |
| `.toUpperCase()`        | Uppercase                   |
| `.toLowerCase()`        | Lowercase                   |
| `.trim()`               | দুই পাশের whitespace remove |
| `.trimStart()`          | শুরু থেকে whitespace remove |
| `.trimEnd()`            | শেষ থেকে whitespace remove  |
| `.includes()`           | text আছে কিনা               |
| `.startsWith()`         | শুরু check                  |
| `.endsWith()`           | শেষ check                   |
| `.indexOf()`            | প্রথম occurrence-এর index   |
| `.lastIndexOf()`        | শেষ occurrence-এর index     |
| `.search()`             | Search                      |
| `.slice()`              | অংশ বের করা                 |
| `.substring()`          | অংশ বের করা                 |
| `.replace()`            | একটি occurrence replace     |
| `.replaceAll()`         | সব occurrence replace       |
| `.concat()`             | String যোগ                  |
| `.split()`              | String → Array              |
| `.repeat()`             | Repeat                      |
| `.padStart()`           | শুরুতে padding              |
| `.padEnd()`             | শেষে padding                |
| `.charCodeAt()`         | Character code              |
| `String.fromCharCode()` | Code → Character            |
| `.localeCompare()`      | String comparison           |

---

# 🔥 String-এর সবচেয়ে গুরুত্বপূর্ণ বিষয়

এই flow-টা মনে রাখো:

```text
String
 │
 ├── Create
 │    ├── "Hello"
 │    ├── 'Hello'
 │    └── `Hello`
 │
 ├── Access
 │    ├── [index]
 │    ├── at()
 │    └── charAt()
 │
 ├── Information
 │    └── length
 │
 ├── Transform
 │    ├── toUpperCase()
 │    ├── toLowerCase()
 │    ├── trim()
 │    └── replace()
 │
 ├── Search
 │    ├── includes()
 │    ├── indexOf()
 │    ├── startsWith()
 │    └── endsWith()
 │
 ├── Extract
 │    ├── slice()
 │    └── substring()
 │
 ├── Convert
 │    └── split()
 │
 └── Template
      └── `${}`
```

---

# 🧠 খুব গুরুত্বপূর্ণ Concept

### String Immutable

```javascript
let text = "Hello";

text[0] = "Y";

console.log(text);
```

Output:

```text
Hello
```

String-এর character সরাসরি পরিবর্তন করা যায় না।

---

### `slice()` end index include করে না

```javascript
let text = "JavaScript";

console.log(text.slice(0, 4));
```

Output:

```text
Java
```

---

### `includes()` Boolean দেয়

```javascript
"JavaScript".includes("Script");
```

Result:

```text
true
```

---

### `indexOf()` না পেলে `-1`

```javascript
"Hello".indexOf("x");
```

Result:

```text
-1
```

---

### `split()` String-কে Array বানায়

```javascript
"HTML,CSS,JS".split(",");
```

Result:

```javascript
["HTML", "CSS", "JS"]
```

---

# 📝 Practice Set — Chapter 8

### Practice 1

Output কী হবে?

```javascript
let name = "JavaScript";

console.log(name.length);
console.log(name[0]);
console.log(name[name.length - 1]);
```

---

### Practice 2

Output কী হবে?

```javascript
let text = "Hello JavaScript";

console.log(text.toUpperCase());
console.log(text.toLowerCase());
```

---

### Practice 3

User input:

```javascript
let username = "   SHARIAR   ";
```

এমন code লেখো যাতে output হয়:

```text
shariar
```

---

### Practice 4

Check করো:

```javascript
let email = "user@gmail.com";
```

Email-এর মধ্যে `@` আছে কিনা।

---

### Practice 5

Check করো:

```javascript
let file = "profile.jpg";
```

এটি `.jpg` file কিনা।

---

### Practice 6

এই String থেকে:

```javascript
let text = "JavaScript";
```

শুধু:

```text
Script
```

বের করো।

---

### Practice 7

```javascript
let skills = "HTML,CSS,JavaScript,React";
```

এটিকে Array বানাও।

Expected:

```javascript
["HTML", "CSS", "JavaScript", "React"]
```

---

### Practice 8

নিচের output তৈরি করো:

```text
My name is Shariar.
I am 23 years old.
I am learning JavaScript.
```

**Template Literal** ব্যবহার করে।

---

### Practice 9 — Mini Project 💻

একটি product data:

```javascript
let productName = "  HP LAPTOP  ";
let price = 75000;
let category = "electronics";
```

Output:

```text
Product: HP LAPTOP
Price: 75000 BDT
Category: ELECTRONICS
```

এখানে ব্যবহার করবে:

* `trim()`
* `toUpperCase()`
* Template Literal

---

# 🎯 Chapter 8 Final Summary

এই chapter-এ আমরা শিখলাম:

```text
✅ String কী
✅ Single / Double / Backtick
✅ Escape Characters
✅ String Length
✅ Indexing
✅ at()
✅ charAt()
✅ Concatenation
✅ Template Literals
✅ ${expression}
✅ Multiline Strings
✅ toUpperCase()
✅ toLowerCase()
✅ trim()
✅ includes()
✅ startsWith()
✅ endsWith()
✅ indexOf()
✅ lastIndexOf()
✅ search()
✅ slice()
✅ substring()
✅ replace()
✅ replaceAll()
✅ concat()
✅ split()
✅ repeat()
✅ padStart()
✅ padEnd()
✅ charCodeAt()
✅ Unicode
✅ localeCompare()
✅ String Conversion
✅ String Immutability
```

### ⭐ সবচেয়ে বেশি ব্যবহার হবে

```javascript
length
[]
at()
toUpperCase()
toLowerCase()
trim()
includes()
startsWith()
endsWith()
indexOf()
slice()
replace()
split()
```

পরবর্তী অধ্যায় হবে **📘 Chapter 9 — Arrays**, যেখানে আমরা Array তৈরি, indexing, `push()`, `pop()`, `shift()`, `unshift()`, `slice()`, `splice()`, `find()`, `filter()`, `map()`, `reduce()`, `sort()`, `forEach()`, nested arrays, array destructuring এবং real-life projectsসহ বিস্তারিত শিখব।
