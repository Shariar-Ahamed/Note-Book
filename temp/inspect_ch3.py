with open(r'Code/Chapter-03-Operators-Expressions.html', 'r', encoding='utf-8') as f:
    text = f.read()

print('File length:', len(text))
print('Count of literal \\n:', text.count('\\n'))
print('Count of actual newlines:', text.count('\n'))
print('Count of literal \\":', text.count('\\"'))

# print first 500 characters
print("--- FIRST 500 CHARACTERS ---")
print(repr(text[:500]))
