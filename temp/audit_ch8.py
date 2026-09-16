import os, re

html_path = r"c:\Users\User\Desktop\Note-Book\Code\Chapter-08-Strings.html"
with open(html_path, "r", encoding="utf-8") as f:
    content = f.read()

print("HTML size:", len(content), "characters")

# Check all sections 8.1 to 8.75
missing_sections = []
for i in range(1, 76):
    sec_num = f"8.{i}"
    if f">{sec_num} " not in content and f">{sec_num}<" not in content and f"{sec_num} " not in content:
        missing_sections.append(sec_num)

if missing_sections:
    print("MISSING SECTIONS:", missing_sections)
else:
    print("ALL 75 SECTIONS (8.1 - 8.75) PRESENT!")

# Check practice set 1 to 9
missing_practices = []
for i in range(1, 10):
    if f"Practice {i}" not in content:
        missing_practices.append(i)

if missing_practices:
    print("MISSING PRACTICES:", missing_practices)
else:
    print("ALL 9 PRACTICES PRESENT!")

# Check cheat sheet, tree, summary
print("Architecture tree present:", "String Architecture" in content or "String Ecosystem" in content or "String Methods Reference" in content)
print("Cheat sheet present:", "Cheat Sheet" in content or "String Methods Complete Quick Reference" in content)
print("Chapter Summary present:", "Chapter 8 Summary" in content)
print("Page 1 class present:", "page-1-cover" in content)
