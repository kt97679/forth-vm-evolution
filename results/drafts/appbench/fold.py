# Upper-case Forth source outside strings and names that must keep their case (Iteration 467, scratch)
import re, sys
KEEP_NEXT = {'INCLUDE', 'REQUIRE', '[CHAR]', 'NEEDS', 'LOAD-PART'}   # CHAR only outside a definition (below)
STR_END = {'S"': '"', '."': '"', 'C"': '"', 'ABORT"': '"', '.(': ')', 'S\\"': '"', 'Z"': '"'}
def fold(text):
    out, i, n, keep, comp = [], 0, len(text), False, False
    while i < n:
        if text[i].isspace(): out.append(text[i]); i += 1; continue
        j = i
        while j < n and not text[j].isspace(): j += 1
        tok = text[i:j]; up = tok.upper()
        if keep: out.append(tok); keep = False; i = j; continue
        if up == '\\':                                   # comment to end of line, as it is
            k = text.find('\n', j); k = n if k < 0 else k; out.append(text[i:k]); i = k; continue
        if up in STR_END:                                 # the string, as it is - unless EVALUATE takes it (and it holds no '/')
            k = text.find(STR_END[up], j + 1); k = n if k < 0 else k + 1; body = text[j:k]
            nxt = text[k:k + 40].split()[:1]
            if up == 'S"' and nxt and nxt[0].upper() == 'EVALUATE' and '/' not in body: body = body.upper()
            out.append(up + body); i = k; continue
        if up in (':', ':NONAME'): comp = True
        elif up == ';': comp = False
        out.append(up); keep = up in KEEP_NEXT or (up == 'CHAR' and not comp); i = j
    return ''.join(out)
if __name__ == '__main__':
    sys.stdout.write(fold(open(sys.argv[1], encoding='latin-1').read()))
