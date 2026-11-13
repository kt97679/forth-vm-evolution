#!/usr/bin/env python3
"""tools/article-check.py [--self-test] - the article's figures, checked before a review (Iteration 659; the arithmetic
check of prompts/04). Two checks, on both drafts as they stand:

1. The same numbers in English and Russian (article/article-en-draft.md, article/article-ru-draft.md), section by section
   - the headings pair in order, and the counts must match. Every number outside the code blocks: thousands written 26,242
   or 26 242, a range 3-7 or 3–7 as two numbers, a sign dropped, a possessive's 's dropped, the number of 4-byte or
   4-байтной kept, a ratio's x dropped (0.31x). Numbers written as words are not seen. A section whose
   numbers differ is named with the difference, each side's numbers the other lacks.
2. Every distinctive figure of the English draft - three significant digits or more, outside the code blocks, years
   aside - looked up as written (the same digits, thousands marks aside) in the records: results/ (the chains' raw
   sessions aside), PROGRESS.md, README.md, FINDINGS-*.md, designs/README.md. Those not found are listed, each a figure
   to trace by hand: rounded, derived, or read off a build. Found is not traced: the same digits can be another quantity
   (the introduction's 24,320 is also a design's bytes in results/evolve-amd-ryzen-7-pro-8840hs-seed58.md).

--self-test first plants a changed digit and a dropped number in a copy of the Russian draft, and fails unless check 1
names exactly those. Exit 1 when check 1 or the self-test fails; check 2 lists, it does not fail. The report on stdout.
From the repository's top, as the build user."""
import collections, os, re, sys

EN, RU = 'article/article-en-draft.md', 'article/article-ru-draft.md'
STRIP = '()[]{}*_`"\'«»„“”.,;:!?|'
NUM = re.compile(r'\d+(?:\.\d+)?')


def sections(text, sep):
    """[(heading, [numbers])] in order - the top before the first heading included; code blocks skipped; sep, the
    language's thousands mark, removed between digit groups"""
    out, head, nums, code = [], '(top)', [], False
    for line in text.split('\n'):
        if line.startswith('```'):
            code = not code
            continue
        if code:
            continue
        if line.startswith('#'):
            out.append((head, nums))
            head, nums = line.strip(), []
            continue
        line = re.sub(r'(?<![\d.,])(\d{1,3})((?:%s\d{3})+)(?![\d.,])' % re.escape(sep),
                      lambda m: m.group(1) + m.group(2).replace(sep, ''), line)
        for tok in line.split():
            tok = re.sub(r"(?<=\d)[x×]$", '', re.sub(r"['’]s$", '', tok.strip(STRIP)).strip(STRIP))
            if tok and not any(c.isalpha() for c in tok):
                nums += NUM.findall(tok)
            elif re.match(r'\d+(?:\.\d+)?[-–][^\W\d_]', tok):
                nums.append(NUM.match(tok).group())
    out.append((head, nums))
    return out


def parity(en_text, ru_text):
    """{section number: (heading, the English numbers the Russian lacks, the Russian numbers the English lacks)} - or
    exits when the headings do not pair"""
    en, ru = sections(en_text, ','), sections(ru_text, ' ')
    if len(en) != len(ru):
        sys.exit('article-check: %d sections in English, %d in Russian - the headings do not pair' % (len(en), len(ru)))
    diff = {}
    for k, ((h, a), (_, b)) in enumerate(zip(en, ru)):
        ca, cb = collections.Counter(a), collections.Counter(b)
        if ca != cb:
            diff[k] = (h, ca - cb, cb - ca)
    return diff


def show(c):
    return ', '.join('%s%s' % (n, ' x%d' % k if k > 1 else '') for n, k in sorted(c.items())) or '-'


en_text, ru_text = open(EN).read(), open(RU).read()
report, failed = [], False
p = report.append

if '--self-test' in sys.argv:
    base = parity(en_text, ru_text)
    mut = ru_text.replace('26 242', '26 224', 1).replace('13 883', '', 1)
    got = parity(en_text, mut)
    planted = {}
    for k in set(base) | set(got):
        b = base.get(k, ('', collections.Counter(), collections.Counter()))
        g = got.get(k, ('', collections.Counter(), collections.Counter()))
        d = (g[1] - b[1], g[2] - b[2])
        if d[0] or d[1]:
            planted[k] = d
    want = [(collections.Counter({'26242': 1, '13883': 1}), collections.Counter({'26224': 1}))]
    ok = list(planted.values()) == want
    p('self-test: a digit changed (26 242 -> 26 224) and a number dropped (13 883) in a copy of the Russian draft - %s'
      % ('named, and nothing else' if ok else 'NOT as planted: %s' % planted))
    failed |= not ok

diff = parity(en_text, ru_text)
p('1. English and Russian: %d sections, %d with different numbers' % (len(sections(en_text, ',')), len(diff)))
for k, (h, a, b) in sorted(diff.items()):
    p('   %s - English only: %s; Russian only: %s' % (h[:60], show(a), show(b)))
failed |= bool(diff)

records = set()
for top, dirs, files in os.walk('results'):
    dirs[:] = [d for d in dirs if not d.startswith('chain-')]
    for f in files:
        if f.endswith(('.md', '.txt', '.json', '.csv', '.tsv')):
            records.update(NUM.findall(re.sub(r'(?<=\d),(?=\d{3}(?!\d))', '', open(os.path.join(top, f), errors='replace').read())))
for f in ['PROGRESS.md', 'README.md', 'designs/README.md'] + sorted(g for g in os.listdir('.') if g.startswith('FINDINGS-')):
    records.update(NUM.findall(re.sub(r'(?<=\d),(?=\d{3}(?!\d))', '', open(f).read())))
figs, missing = 0, []
for h, nums in sections(en_text, ','):
    for n in nums:
        sig = len(n.replace('.', '').lstrip('0'))
        if sig < 3 or ('.' not in n and 1900 <= int(n) <= 2099):
            continue
        figs += 1
        if n not in records:
            missing.append('%s (%s)' % (n, h[:40]))
p('2. distinctive figures of the English draft: %d, %d of them in the records as written (%d numbers in the records;'
  ' found is not traced - the same digits can be another quantity)' % (figs, figs - len(missing), len(records)))
for m in missing:
    p('   not found: ' + m)
print('\n'.join(report))
sys.exit(1 if failed else 0)
