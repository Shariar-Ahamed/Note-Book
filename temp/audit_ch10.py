import sys

sys.stdout.reconfigure(encoding='utf-8')

html_path = r"c:\Users\User\Desktop\Note-Book\Code\Chapter-10-Objects.html"
with open(html_path, "r", encoding="utf-8") as f:
    content = f.read()

print("HTML size:", len(content), "characters")

# Check all sections 10.1 to 10.68
missing_sections = []
for i in range(1, 69):
    sec_num = f"10.{i}"
    if f">{sec_num} " not in content and f">{sec_num}<" not in content and f"{sec_num} " not in content:
        missing_sections.append(sec_num)

if missing_sections:
    print("MISSING SECTIONS:", missing_sections)
else:
    print("ALL 68 SECTIONS (10.1 - 10.68) PRESENT!")

# Check practice set 1 to 10
missing_practices = []
for i in range(1, 11):
    if f"Practice {i}" not in content:
        missing_practices.append(i)

if missing_practices:
    print("MISSING PRACTICES:", missing_practices)
else:
    print("ALL 10 PRACTICES PRESENT!")

# Check mental model, must know, summary, preview
print("Mental Model present:", "Object Mental Model" in content)
print("Must Know present:", "Must Know" in content)
print("Chapter Summary present:", "Chapter 10 Final Summary" in content)
print("Top 10 present:", "সবচেয়ে গুরুত্বপূর্ণ ১০টি" in content)
print("Next Chapter Preview present:", "Chapter 11 Preview" in content)
