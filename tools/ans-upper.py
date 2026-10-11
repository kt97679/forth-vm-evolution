#!/usr/bin/env python3
"""ans-upper.py SRC DST - the ANS test files (tests/ans, lowercase) in the
upper case this case-sensitive Forth reads: every word upper-cased except
where case is data - the text of S" ." C" ABORT" .( and comments, the word
after CHAR and [CHAR], and 'c' character literals (Iteration 118); and the text
of utilities.fth's $" and $2" (Iteration 124)."""
import sys, re
STR = {'S"': '"', '."': '"', 'C"': '"', 'ABORT"': '"', '.(': ')', 'S\\"': '"', '$"': '"', '$2"': '"'}   # $" $2": utilities.fth's (Iteration 124)
def conv(line):
    out, i, n = [], 0, len(line)
    keep_next = False
    while i < n:
        if line[i] in ' \t': out.append(line[i]); i += 1; continue
        j = i
        while j < n and line[j] not in ' \t': j += 1
        tok = line[i:j]; up = tok.upper()
        if keep_next: out.append(tok); keep_next = False; i = j; continue
        if up == '\\': out.append(line[i:]); break
        if up == '(':
            k = line.find(')', j); k = n if k < 0 else k + 1
            out.append(line[i:k]); i = k; continue
        if up in STR:
            if up == 'S\\"':          # Iteration 183: in S\" a backslash escapes the next character -
                k = j + 1              # an escaped quote does not end it (coreexttest's nested S\")
                while k < n and line[k] != '"': k += 2 if line[k] == '\\' else 1
                k = min(k, n - 1) + 1 if k < n else n
            else:
                k = line.find(STR[up], j + 1); k = n if k < 0 else k + 1
            out.append(up + line[j:k]); i = k; continue
        if re.fullmatch(r"'.'", tok): out.append(tok); i = j; continue
        if up in ('CHAR', '[CHAR]', 'INCLUDE', 'REQUIRE', 'PARSE-NAME'): keep_next = True   # Iteration 181: a file name after INCLUDE, REQUIRE; PARSE-NAME's token, compared with an S" string
        out.append(up); i = j
    return ''.join(out)
src = open(sys.argv[1], encoding='latin-1').read().replace('\r', '')
open(sys.argv[2], 'w', encoding='latin-1').write('\n'.join(conv(l) for l in src.split('\n')))
