#!/usr/bin/env python3
"""The tracer (Iteration 162, the owner): what ran, and why.

A trace engine is vm-lab.c built with -DPROFILE=2 (the evolver's
PROFILING[0] = 2): a shadow call stack, and the first time each instruction
runs a record - its call path, the top three data-stack cells, the input line
being interpreted. This tool builds one for a design, runs inputs through it,
and reads the records back through the converter's map (CALLMAP: W lines, a
word's bytes; O lines, its instructions).

    vmtrace.py [--design s6|ID] [--word NAME]... [--folded FILE] [--uncovered]
               [--self-test] INPUT...

INPUT: a file of Forth text, run as the engine's input (relative INCLUDEs run
from its directory). Native code is not traced: the JIT is off in a trace
build, as tail calls and the compiler's own optimisations are.
"""
import bisect, json, os, re, shutil, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, 'lab', 'evolve'))


def evolve():
    argv, sys.argv = sys.argv, ['vmtrace']
    import evolve as E
    sys.argv = argv
    E.setup()
    return E


def genome(E, design):
    if design in E.HUMAN: return E.canon(E.HUMAN[design])
    for f in sorted(os.listdir(os.path.join(ROOT, 'results'))):
        if f.startswith('evolve-') and f.endswith('.md'):
            for l in open(os.path.join(ROOT, 'results', f), errors='replace'):
                if l.startswith('{"bin"') and '"id": "%s"' % design in l:
                    return E.canon(json.loads(l)['genome'])
    sys.exit('vmtrace: no design %s' % design)


def build(E, design):
    """A trace engine for the design: (engine, image, map, work directory)."""
    g = dict(genome(E, design), tail=0, msc=0, jit=0, jitx=0, jitloop=0, jitinl=0)
    d = os.path.join(E.EV, 'trace-' + design); shutil.rmtree(d, ignore_errors=True)
    cm = d + '.map'; os.environ['CALLMAP'] = cm; E.PROFILING[0] = 2
    try: eng, img = E.build(E.canon(g), d)
    finally: E.PROFILING[0] = False; del os.environ['CALLMAP']
    return eng, img, cm, E.private_work(d)


def probes(eng, img, pw):
    """SRC, #SRC and >IN as offsets from the image base - asked of the design."""
    r = subprocess.run([eng, img], cwd=pw, input=b'SRC START @ - . #SRC START @ - . >IN START @ - . CR BYE\n',
                       capture_output=True, timeout=30)
    n = re.findall(rb'(-?\d+) (-?\d+) (-?\d+)', r.stdout)
    return ','.join(x.decode() for x in n[-1]) if n else None


def run(eng, img, pw, text, out, cwd=None, probe=None):
    env = dict(os.environ, VMTRACE=out)
    if probe: env['VMTRACE_PROBES'] = probe
    return subprocess.run([eng, img], cwd=cwd or pw, input=text, capture_output=True, timeout=600, env=env)


class Map:
    def __init__(self, path):
        L = [l.split() for l in open(path)]
        self.words = sorted((int(x[1]), int(x[2]), x[4] if len(x) > 4 else x[3]) for x in L if x[0] == 'W')
        self.starts = [w[0] for w in self.words]
        self.ops = {int(x[1]): ' '.join(x[2:]) for x in L if x[0] == 'O'}
        self.rt, self.rts = {}, []        # words compiled at run time: start -> name (named by the design)

    def runtime(self, names):
        self.rt.update(names); self.rts = sorted(self.rt)

    def word(self, a):
        k = bisect.bisect_right(self.starts, a) - 1
        if k >= 0 and a < self.words[k][1]: return self.words[k]
        k = bisect.bisect_right(self.rts, a) - 1
        return (self.rts[k], None, self.rt[self.rts[k]]) if k >= 0 and a >= self.words[-1][1] else None

    def name(self, a):
        w = self.word(a)
        return '%s+%d' % (w[2], a - w[0]) if w else '@%d' % a


def named_run(M, eng, img, pw, text, out, cwd=None, probe=None):
    """Run, and name what the run compiled: a second, identical run ends by
    asking the design's own >NAME for every call target the map lacks."""
    run(eng, img, pw, text, out, cwd, probe)
    first, _ = records([out])
    unknown = sorted({t for r in first.values() for t, _ in r['path'] if M.word(t) is None})
    if not unknown: return
    body = re.sub(rb'\n\s*BYE\s*$', b'\n', text.rstrip() + b'\n')
    epi = b''   # Iteration 244: no >NAME in the kernel - the walk below names every word compiled past the image
    # and every word compiled past the image, walking each thread with the
    # design's own NEXT-NFA8 and NAME>8 (byte headers - the front and s6):
    # what EXECUTE ran is never a call target, but its name is here
    nm8 = b'NAME>8' if any(w[2] == 'NAME>8' for w in M.words) else b'NAME>'   # a lean --cv8-compiler image: NAME> holds its code
    epi += (b': TRWALK ( lim --- ) FORTH-WORDLIST @ 1+ 1 DO FORTH-WORDLIST I CELLS + @ BEGIN DUP WHILE DUP ' + nm8 + b' START @ -'
            b' DUP 3 PICK < IF DROP ELSE CR 777002 . . DUP COUNT 31 AND TYPE SPACE THEN NEXT-NFA8 REPEAT DROP LOOP DROP ;\n'
            b'%d TRWALK\n' % M.words[-1][1])
    r = run(eng, img, pw, body + b'\n' + epi + b'CR BYE\n', out, cwd, probe)
    M.runtime({int(a): n.decode(errors='replace') for a, n in re.findall(rb'77700[12] (\d+) (\S+)', r.stdout)})


def records(files):
    """First records across runs (the earliest file wins), and folded stacks."""
    first, folded = {}, {}
    for f in files:
        for l in open(f, errors='replace'):
            if l.startswith('F '):
                m = re.match(r'F (\d+) d=(\d+) p=(\S*) s=(\S+)(?: in=(\d+) l=(.*))?$', l.rstrip('\n'))
                if m and int(m.group(1)) not in first:
                    path = [tuple(int(v) for v in x.split('/')) for x in m.group(3).split(',') if x]
                    first[int(m.group(1))] = dict(depth=int(m.group(2)), path=path, stack=m.group(4),
                                                  inp=m.group(5), line=m.group(6))
            elif l.startswith('P '):
                n, _, p = l[2:].rstrip('\n').partition(' ')
                folded[p] = folded.get(p, 0) + int(n)
    return first, folded


def context(M, r):
    path = ' <- '.join('%s (from %s)' % (M.name(t), M.name(ret - 1) if ret else '?') for t, ret in reversed(r['path'][-6:]))
    s = 'stack %s' % r['stack'].replace(',', ' ')
    if r.get('line') is not None: s += ', at >IN %s of: %s' % (r['inp'], r['line'])
    return '%s | %s' % (path or '(top level)', s)


def report(M, first, folded, words=(), uncovered=False, folded_out=None):
    ins = {}
    for a in M.ops:
        w = M.word(a)
        if w: ins.setdefault(w[2], []).append(a)
    ran = sum(1 for w in ins for a in ins[w] if a in first)
    total = sum(len(v) for v in ins.values())
    never = [w for w in ins if not any(a in first for a in ins[w])]
    part = sorted(((sum(1 for a in ins[w] if a not in first), len(ins[w]), w) for w in ins
                   if any(a in first for a in ins[w]) and not all(a in first for a in ins[w])), reverse=True)
    print('instructions run %d of %d (%.1f%%); words never entered %d; partly run %d'
          % (ran, total, 100.0 * ran / max(1, total), len(never), len(part)))
    if uncovered:
        print('never entered:', ' '.join(never))
        for n, t, w in part: print('  %-18s %d of %d not run: %s' % (w, n, t, ' '.join(
            '+%d %s' % (a - M.word(a)[0], M.ops[a]) for a in sorted(ins[w]) if a not in first)))
    for w in words:
        for a in sorted(ins.get(w, [])):
            r = first.get(a)
            print('%-20s %-24s %s' % (M.name(a), M.ops[a][:24], context(M, r) if r else 'NEVER RUN'))
    if folded_out:
        with open(folded_out, 'w') as f:
            for p, n in sorted(folded.items(), key=lambda kv: -kv[1]):
                f.write('%s %d\n' % (';'.join(M.name(int(t)).split('+')[0] for t in p.split(';') if t), n))
        print('folded stacks: %s (%d paths)' % (folded_out, len(folded)))


def self_test(E):
    """The first record in SQ: called from TWICE, 3 on the stack, this line."""
    eng, img, cm, pw = build(E, 's6-cv8b'); M = Map(cm); pr = probes(eng, img, pw)
    out = os.path.join(pw, 'self.trace')
    named_run(M, eng, img, pw, b': SQ DUP * ;\n: TWICE SQ SQ ;\n3 TWICE . CR\nBYE\n', out, probe=pr)
    first, folded = records([out])
    sq = [s_ for s_, n in M.rt.items() if n == 'SQ']
    r = first.get(sq[0]) if sq else None
    nm = lambda a: (M.word(a) or (0, 0, '?'))[2]
    ok = bool(r and r['path'] and nm(r['path'][-1][0]) == 'SQ' and nm(r['path'][-1][1] - 1) == 'TWICE'
              and r['stack'].split(',')[0] == '3' and '3 TWICE' in (r['line'] or ''))
    ok = ok and any(nm(int(p.split(';')[-1])) == 'SQ' for p in folded)
    print('self-test %s: %s' % ('ok' if ok else 'FAIL', context(M, r) if r else 'no record in SQ'))
    return ok


def main(a):
    E = evolve()
    if '--self-test' in a: sys.exit(0 if self_test(E) else 1)
    design = a[a.index('--design') + 1] if '--design' in a else 's6-cv8b'
    words = [a[i + 1] for i, x in enumerate(a) if x == '--word']
    fo = a[a.index('--folded') + 1] if '--folded' in a else None
    skip = {i + 1 for i, x in enumerate(a) if x in ('--design', '--word', '--folded')}
    inputs = [x for i, x in enumerate(a) if not x.startswith('--') and i not in skip]
    eng, img, cm, pw = build(E, design); M = Map(cm); pr = probes(eng, img, pw); files = []
    for i, f in enumerate(inputs):
        out = os.path.join(pw, 'run%d.trace' % i); files.append(out)
        named_run(M, eng, img, pw, open(f, 'rb').read(), out, cwd=os.path.dirname(os.path.abspath(f)), probe=pr)
    first, folded = records(files)
    report(M, first, folded, words, '--uncovered' in a, fo)


if __name__ == '__main__':
    main(sys.argv[1:])
