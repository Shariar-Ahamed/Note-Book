import sys

sys.stdout.reconfigure(encoding='utf-8')

html_path = r"c:\Users\User\Desktop\Note-Book\Code\Chapter-11-Prototypes.html"
with open(html_path, "r", encoding="utf-8") as f:
    content = f.read()

print("HTML size:", len(content), "characters")

# Check all sections 11.1 to 11.54
missing_sections = []
for i in range(1, 55):
    sec_num = f"11.{i}"
    if f">{sec_num} " not in content and f">{sec_num}<" not in content and f"{sec_num} " not in content:
        missing_sections.append(sec_num)

if missing_sections:
    print("MISSING SECTIONS:", missing_sections)
else:
    print("ALL 54 SECTIONS (11.1 - 11.54) PRESENT!")

# Check practice set 1 to 5
missing_practices = []
for i in range(1, 6):
    if f"Practice {i}" not in content:
        missing_practices.append(i)

if missing_practices:
    print("MISSING PRACTICES:", missing_practices)
else:
    print("ALL 5 PRACTICES PRESENT!")

# Check Must Know, Cheat Sheet, Summary, Preview
print("Must Know present:", "Must Know" in content)
print("Quick Cheat Sheet present:", "Quick Cheat Sheet" in content)
print("Chapter Summary present:", "Chapter 11 Final Summary" in content)
print("Next Chapter Preview present:", "Chapter 12 Preview" in content)
