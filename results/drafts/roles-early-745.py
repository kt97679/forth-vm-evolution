#!/usr/bin/env python3
"""results/drafts/roles-early-745.py DB REMEASURE REMEASURE32 RECORDS (Iteration 745) - an early look at the roles after
seed 97 alone: which holders the new series already presses, by each role's rule (lab/evolve/followup-roles.py: speed
2 %, binary + image 1 %, memory 8 KB) read loosely on one machine's in-run numbers - a forecast of the roles' chains'
size, not a decision (the chains measure on three machines, paired by session).

DB: the run's database (pack/db.jsonl); REMEASURE, REMEASURE32: the pack's re-measures (6 rounds, the fast end - an
in-run reading at the fast end runs 6-8 % optimistic, the curse; a re-measured one does not); RECORDS: the roles'
records (results/relf-designs-718.md, for the holders seed 97 did not carry). The holders: designs/NAME/record.json.
A holder carried into seed 97 is read in generation 0 (3 rounds, unselected); a challenger by its re-measure when it
has one, else in-run (marked ~). Speeds are time / s6's in the same round; lower is faster. Reads only. python3 -I -B."""
import glob, json, os, sys

db, rm64, rm32, records = sys.argv[1:5]
sys.argv = ['x']; sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'lab', 'evolve'))
import evolve as E
R = {}
for line in open(db, errors='replace'):
    try: r = json.loads(line)
    except Exception: continue
    if r.get('status') == 'ok' and r.get('speed'): R[r['id']] = r          # the newest alive record of an id
RM = json.load(open(rm64)); RM32 = json.load(open(rm32))
OLD = {}
for l in open(records, errors='replace'):
    if l.startswith('{'):
        r = json.loads(l); OLD[r['id']] = r
H = {}
for f in sorted(glob.glob('designs/*/record.json')):
    H[os.path.basename(os.path.dirname(f))] = json.load(open(f))['id']
JIT = {i for i, r in R.items() if E.jit_on(E.canon(E.require(dict(r['genome']))))}   # the JIT expressed, as the screen
jit = lambda i: i in JIT


def s64(i):
    return (RM[i]['speed'], '') if i in RM else (R[i]['speed'], '~')


def s32(i):
    return (RM32[i]['speed32'], '') if i in RM32 else (R[i].get('speed32') or 9, '~')


def show(i, h):
    a, m = s64(i); b, n = s32(i); r = R[i]
    new = ','.join(g for g in ('hashk', 'numfirst', 'chainorder', 'jitdead', 'jitfew') if r['genome'].get(g)) or '-'
    return '%s %s%.4f (%+.1f %%) %s%.4f (%+.1f %%) %s B (%+.2f %%) %d KB (%+d) [%s]' % (
        i, m, a, 100 * (a / s64(h)[0] - 1), n, b, 100 * (b / s32(h)[0] - 1), format(r['total'], ','),
        100 * (r['total'] / R[h]['total'] - 1), r['rss'], r['rss'] - R[h]['rss'], new)


def report(role, h, pool, beats, key):
    print('\n%s - holder %s: %s' % (role, h, show(h, h).split(' ', 1)[1]))
    c = sorted((i for i in pool if i != h and beats(i, h)), key=key)
    print('  beating it by the rule here: %d%s' % (len(c), '' if c else ' - none'))
    for i in c[:5]: print('    ' + show(i, h))


ALL = list(R)
FREE = [i for i in ALL if not jit(i)]
JITS = [i for i in ALL if jit(i)]
sp, sp32 = (lambda i: s64(i)[0]), (lambda i: s32(i)[0])
mem_ok = lambda i, h: R[i]['rss'] <= R[h]['rss'] + 8
print('seed 97: %d alive (%d JIT-free); re-measured %d at 64 bits, %d at 32' % (len(ALL), len(FREE), len(RM), len(RM32)))
print('holders carried into seed 97: %s; not carried: %s' % (
    ', '.join('%s %s' % (n, i) for n, i in H.items() if i in R), ', '.join('%s %s' % (n, i) for n, i in H.items() if i not in R)))

g = H['fastest-x86-64']
if g in R: report('fastest-x86-64 (2 % faster at 64 bits)', g, ALL, lambda i, h: sp(i) <= 0.98 * sp(h), sp)
g = H['portable-fastest']      # its rule: the mean of x86-64, x86-32 and ARMv7 - here the two x86 widths
if g in R: report('portable-fastest (JIT-free; 2 % faster over both widths, here no ARMv7)', g, FREE,
                  lambda i, h: (sp(i) * sp32(i)) ** .5 <= 0.98 * (sp(h) * sp32(h)) ** .5, lambda i: sp(i) * sp32(i))
g = H['portable-knee']         # faster on a width or 1 % smaller; no width 2 % slower, not 1 % larger
if g in R: report('portable-knee (JIT-free; 2 % faster on a width or 1 % smaller, no width 2 % slower, not 1 % larger)', g, FREE,
                  lambda i, h: (sp(i) <= 0.98 * sp(h) or sp32(i) <= 0.98 * sp32(h) or R[i]['total'] <= 0.99 * R[h]['total'])
                  and sp(i) <= 1.02 * sp(h) and sp32(i) <= 1.02 * sp32(h) and R[i]['total'] <= 1.01 * R[h]['total'] and mem_ok(i, h),
                  lambda i: R[i]['total'])
g = H['smallest']              # 1 % smaller, no width 2 % slower; and every smaller design shown (649's precedent)
if g in R:
    report('smallest (1 % smaller, no width 2 % slower)', g, ALL, lambda i, h: R[i]['total'] <= 0.99 * R[h]['total']
           and sp(i) <= 1.02 * sp(h) and sp32(i) <= 1.02 * sp32(h) and mem_ok(i, h), lambda i: R[i]['total'])
    sm = sorted((i for i in ALL if R[i]['total'] < R[g]['total']), key=lambda i: (R[i]['total'], sp(i)))
    ok = [i for i in sm if sp(i) <= 1.02 * sp(g) and sp32(i) <= 1.02 * sp32(g) and mem_ok(i, g)]
    print('  smaller at all: %d designs (%s-%s B), %d of them no width 2 %% slower and memory within 8 KB:' % (
        len(sm), format(R[sm[0]]['total'], ',') if sm else '-', format(R[sm[-1]]['total'], ',') if sm else '-', len(ok)))
    for i in ok[:5]: print('    ' + show(i, g))
g = H['small-jit']             # the smallest JIT design: 1 % smaller and no width 2 % slower
if g in R:
    report('small-jit (JIT; 1 % smaller, no width 2 % slower)', g, JITS, lambda i, h: R[i]['total'] <= 0.99 * R[h]['total']
           and sp(i) <= 1.02 * sp(h) and sp32(i) <= 1.02 * sp32(h) and mem_ok(i, h), lambda i: R[i]['total'])
    near = sorted((i for i in JITS if R[i]['total'] <= 0.99 * R[g]['total']), key=lambda i: sp(i))
    print('  1 %% smaller JIT designs: %d; the fastest of them:' % len(near))
    for i in near[:3]: print('    ' + show(i, g))

print('\nnot carried - their records the old scale (718; memory before the layout), shown beside seed 97\'s best:')
for n in ('fastest-x86-32', 'best-all-round', 'least-memory', 'portable-small', 'portable-arm'):
    i = H[n]
    if i in R: continue
    o = OLD.get(i, {})
    print('  %s %s: 718 record %.4f / %.4f, %s B, %s KB' % (n, i, o.get('speed', 0), o.get('speed32', 0), format(o.get('total', 0), ','), o.get('rss')))
best32 = min(ALL, key=sp32)
lean = sorted(ALL, key=lambda i: (R[i]['rss'], R[i]['total']))[:3]
print('  seed 97: the fastest at 32 bits %s %s%.4f; the leanest %s' % (best32, s32(best32)[1], sp32(best32), ', '.join(
    '%s %d KB %s B %.3f' % (i, R[i]['rss'], format(R[i]['total'], ','), sp(i)) for i in lean)))
o = OLD[H['least-memory']]
for kb in (96, 100, 104):
    c = [i for i in ALL if R[i]['rss'] <= kb]
    f = min(c, key=sp) if c else None
    print('  at most %d KB: %d designs, the fastest %s %.3f / %.3f (the holder\'s 718 record %.3f / %.3f at %d KB)' % (
        kb, len(c), f, sp(f), sp32(f), o['speed'], o['speed32'], o['rss']) if f else '  at most %d KB: none' % kb)
