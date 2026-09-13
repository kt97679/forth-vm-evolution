#!/usr/bin/env python3
"""make-corpus.py SRC DST - normalise a Forth test file into a form every
stage can read.

Three things are fixed, all of them accidents of how the file was edited
in the RelF tree rather than anything about the tests themselves:

  CRLF                    -> LF
  CP1251 bytes            -> ASCII ('?' for anything unrepresentable)
  multi-line `(` comments -> one comment per line

Only the last has any semantic weight. ANSI Forth's `(` skips to the next
`)` *in the current parse area*, so a comment that opens on one line and
closes on another relies on an extension. RelF provides it; SOD32 does
not. A corpus shared between them must not depend on it.

The rewrite closes such a comment at the end of its first line and turns
each continuation line into a `\\` line comment, dropping the stray `)`.
No test case is touched: the transformation only ever runs inside a
region that was already a comment.
"""
import sys


def word_at(line, i, ch):
    """True if line[i] == ch and it stands alone as a Forth word."""
    if line[i] != ch:
        return False
    before = (i == 0) or line[i - 1] in ' \t'
    after = (i + 1 >= len(line)) or line[i + 1] in ' \t'
    return before and after


def scan(line):
    """Walk a line that starts OUTSIDE a comment. Return (text, open?)."""
    i = 0
    while i < len(line):
        if word_at(line, i, '\\'):
            return line, False          # rest of line already a comment
        if word_at(line, i, '('):
            j = line.find(')', i)
            if j < 0:
                return line, True       # comment runs past end of line
            i = j + 1
            continue
        i += 1
    return line, False


def normalise(text):
    out, inside = [], False
    for line in text.split('\n'):
        if inside:
            j = line.find(')')
            if j < 0:
                out.append('\\ ' + line)
                continue
            head, tail = line[:j], line[j + 1:]
            body, inside = scan(tail)
            out.append('\\ ' + head + (' ' + body if body.strip() else ''))
            if inside:
                out[-1] += ' )'
                inside = True
            continue
        body, inside = scan(line)
        out.append(body + ' )' if inside else body)
    return '\n'.join(out) + '\n'


def main():
    src, dst = sys.argv[1], sys.argv[2]
    raw = open(src, 'rb').read()
    try:
        text = raw.decode('utf-8')
    except UnicodeDecodeError:
        text = raw.decode('cp1251', errors='replace')
    text = text.replace('\r\n', '\n').replace('\r', '\n')
    text = text.encode('ascii', errors='replace').decode('ascii')
    open(dst, 'w').write(normalise(text))
    print(f"{src} -> {dst}")


if __name__ == '__main__':
    main()
