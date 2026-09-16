import re
import html

def highlight_js(code_str):
    # Tokens to extract: comment, string, keyword, builtin, boolean, number
    token_spec = [
        ('COMMENT_MULTI', r'/\*[\s\S]*?\*/'),
        ('COMMENT_LINE', r'//.*$'),
        ('STRING_TMPL', r'`(?:\\.|[^`\\])*`'),
        ('STRING_DBL', r'"(?:\\.|[^"\\])*"'),
        ('STRING_SGL', r"'(?:\\.|[^'\\])*'"),
        ('KEYWORD', r'\b(?:for|while|do|break|continue|if|else|let|const|var|function|return|switch|case|default|of|in|new|typeof|try|catch|finally|throw|class|extends|await|async|yield)\b'),
        ('BOOL_NULL', r'\b(?:true|false|null|undefined|NaN)\b'),
        ('BUILTIN', r'\b(?:console|Math|Array|Object|String|Number|Boolean|parseInt|parseFloat|prompt|alert)\b'),
        ('NUMBER', r'\b\d+(?:\.\d+)?\b'),
        ('OTHER', r'[^\s\w]+|\w+|\s+'),
    ]
    tok_regex = '|'.join(f'(?P<{name}>{pattern})' for name, pattern in token_spec)
    
    out = []
    for mo in re.finditer(tok_regex, code_str, flags=re.MULTILINE):
        kind = mo.lastgroup
        val = mo.group()
        esc = html.escape(val)
        if kind in ('COMMENT_MULTI', 'COMMENT_LINE'):
            out.append(f'<span class="syn-com">{esc}</span>')
        elif kind in ('STRING_TMPL', 'STRING_DBL', 'STRING_SGL'):
            out.append(f'<span class="syn-str">{esc}</span>')
        elif kind == 'KEYWORD':
            out.append(f'<span class="syn-kw">{esc}</span>')
        elif kind == 'BOOL_NULL':
            out.append(f'<span class="syn-bool">{esc}</span>')
        elif kind == 'BUILTIN':
            out.append(f'<span class="syn-fn">{esc}</span>')
        elif kind == 'NUMBER':
            out.append(f'<span class="syn-num">{esc}</span>')
        else:
            out.append(esc)
    return ''.join(out)

test_code = """// Sample test
for (let i = 0; i < 5; i++) {
    console.log(`Val: ${i}`, true, 100);
}"""
print(highlight_js(test_code))
