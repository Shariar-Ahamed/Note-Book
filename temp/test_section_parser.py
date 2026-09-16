import re
import sys
import html

sys.stdout.reconfigure(encoding='utf-8')

with open(r'temp/ch-5.md', 'r', encoding='utf-8') as f:
    raw_md = f.read().replace('\r\n', '\n').replace('\r', '\n')

splits = re.split(r'\n(?=#\s+5\.\d+\s+)', raw_md)
opening_md = splits[0]
numbered_secs_md = splits[1:52]

# Split 52 and the post-sections
sec52_and_after = splits[52]
post_parts = re.split(r'\n(?=#\s+[🧠🔥📝🎯])', sec52_and_after)
sec52_md = post_parts[0]
post_cheat_md = post_parts[1]
post_diff_md = post_parts[2]
post_practice_md = post_parts[3]
post_summary_md = post_parts[4]

all_secs_md = numbered_secs_md + [sec52_md]
print(f"Total numbered sections: {len(all_secs_md)}")
print(f"Post parts: cheat={bool(post_cheat_md)}, diff={bool(post_diff_md)}, practice={bool(post_practice_md)}, summary={bool(post_summary_md)}")
