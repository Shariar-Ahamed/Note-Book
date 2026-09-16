import os, sys

sys.stdout.reconfigure(encoding='utf-8')

html_path = r"c:\Users\User\Desktop\Note-Book\Code\Chapter-09-Arrays.html"
with open(html_path, "r", encoding="utf-8") as f:
    content = f.read()

print("HTML size:", len(content), "characters")

# Check all sections 9.1 to 9.89
missing_sections = []
for i in range(1, 90):
    sec_num = f"9.{i}"
    if f">{sec_num} " not in content and f">{sec_num}<" not in content and f"{sec_num} " not in content:
        missing_sections.append(sec_num)

if missing_sections:
    print("MISSING SECTIONS:", missing_sections)
else:
    print("ALL 89 SECTIONS (9.1 - 9.89) PRESENT!")

# Check mini projects
print("Project 1 (Shopping Cart):", "Shopping Cart" in content)
print("Project 2 (Student Result):", "Student Result" in content)
print("Project 3 (Search Products):", "Search Products" in content)

# Check practice set 1 to 10
missing_practices = []
for i in range(1, 11):
    if f"Practice {i}" not in content:
        missing_practices.append(i)

if missing_practices:
    print("MISSING PRACTICES:", missing_practices)
else:
    print("ALL 10 PRACTICES PRESENT!")

# Check core concepts & summary
print("Core Concepts present:", "সবচেয়ে গুরুত্বপূর্ণ Concepts" in content)
print("Chapter Summary present:", "Chapter 9 Final Summary" in content)
print("Next Chapter Preview present:", "Chapter 10 Preview" in content)
print("Methods Table present:", "Array Methods — সবচেয়ে গুরুত্বপূর্ণ Table" in content)
