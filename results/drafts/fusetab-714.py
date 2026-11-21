#!/usr/bin/env python3
"""results/drafts/fusetab-714.py NAME ENG IMG ENGA IMGA [W] - the self-hosting gate's deterministic half (Iteration 714;
results/drafts/premortem-roles-707.md: a role ships its self-built image only if its speed is the translator's): the
translator-built image IMG on its engine ENG against the self-built A (IMGA) on ENGA (a JIT design's engine rebuilt with
A's layout; else ENG). Each image prints the run-time compiler's tables from inside itself - VAR-OPS (12 bytes, the gene
rtvar's) and INL-OPS (152, rtinline's), "absent" where its overlay is not in the design - and lays the five selection
programs (evolve.app_size: the code bytes each lays, deterministic), and compiles two probes - a call of a one-operation
word (rtinline copies its body) and a variable's @ and ! (rtvar's vf and vs) - reading each definition's bytes (HERE's
advance). PASS when both tables and both probes are equal, and at the byte header the five sizes too - or each zeroed
table leaving the same difference (A is laid out smaller, so a call can be near rather than far, a slot 2 bytes rather
than 3: an address's effect, the fusion's on and off alike). Under the two-bit tag a call's length follows its distance
(2-4 bytes), and with no table at all nothing tells the two apart: there the sizes are reported only.
W: 4 for the 4-byte-cell build (default 8). From the repository's top, in a built tree."""
import contextlib, json, os, re, shutil, sys, tempfile
name, eng, img, enga, imga = sys.argv[1:6]; w = int(sys.argv[6]) if len(sys.argv) > 6 else 8
eng, img, enga, imga = (os.path.abspath(x) for x in (eng, img, enga, imga))
sys.argv = ['x']; sys.path.insert(0, 'lab/evolve'); import evolve as E
if w == 4: E.TWO_WIDTHS[0] = True; E.setup_widths(); E.TWO_WIDTHS[0] = False
else: E.setup()
TABS = (('VAR-OPS', 12), ('INL-OPS', 152))
PROBES = ((': FT-INC 1+ ;', ': FT-T FT-INC FT-INC ;'), ('VARIABLE FT-V', ': FT-W FT-V @ FT-V ! ;'))
def probes(e, i, pw):
    out = []
    for pre, d in PROBES:
        src = '%s HERE %s HERE SWAP - 777001 . . 777002 . CR BYE\n' % (pre, d)
        o = E.sh([e, i], cwd=pw, inp=src.encode(), timeout=60, cpu=5).stdout.decode('latin-1')
        m = re.search(r'777001 (-?\d+) 777002', o)
        out.append(int(m.group(1)) if m else None)
    return out
import appsize
def app_size(e, i, pw, pre=b''):
    """evolve.app_size, PRE run first (a table zeroed: the fusion off in the same image)."""
    out = []
    for app in appsize.SELECTION:
        o = [E.sh([e, i], cwd=pw, inp=pre + appsize.stdin(app, m), timeout=60, cpu=5).stdout.decode('latin-1') for m in ('size', 'count')]
        v = appsize.parse(*o); out.append(None if v is None else v[0] - v[1])
    return out
def tables(e, i, pw):
    out = {}
    for t, n in TABS:
        src = ': FT-%s %s %d 0 DO DUP I + C@ . LOOP DROP ; 777001 . FT-%s 777002 . CR BYE\n' % (t, t, n, t)
        o = E.sh([e, i], cwd=pw, inp=src.encode(), timeout=60, cpu=5).stdout.decode('latin-1')
        m = re.search(r'777001 ((?:\d+ )+)777002', o)
        out[t] = [int(x) for x in m.group(1).split()] if m else 'absent'
    return out
with (E.at_width(E.WIDTH4) if w == 4 else contextlib.nullcontext()):
    pw = tempfile.mkdtemp(dir=E.EV)
    for f in os.listdir(E.W):
        if f != 'kernel.img': os.symlink(os.path.join(E.W, f), os.path.join(pw, f))
    T, A = tables(eng, img, pw), tables(enga, imga, pw)
    sT, sA = E.app_size(eng, img, pw), E.app_size(enga, imga, pw)
    pT, pA = probes(eng, img, pw), probes(enga, imga, pw)
    off = {t: app_size(eng, img, pw, ('%s %d 0 FILL\n' % (t, n)).encode()) for t, n in TABS if T[t] != 'absent'}
    offA = {t: app_size(enga, imga, pw, ('%s %d 0 FILL\n' % (t, n)).encode()) for t, n in TABS if A[t] != 'absent'}
    tag2 = bool(E.express(E.canon(json.load(open(os.path.join(os.path.dirname(img), 'record.json')))['genome'])).get('tag2'))
    shutil.rmtree(pw, ignore_errors=True)
ok = True
for t, n in TABS:
    same = T[t] == A[t]; ok &= same
    nz = lambda v: 'absent' if v == 'absent' else '%d of %d bytes nonzero' % (sum(1 for x in v if x), n)
    print('fusetab: %s %s - the translator\'s %s, A\'s %s: %s' % (name, t, nz(T[t]), nz(A[t]), 'the same' if same else 'DIFFER'))
    if not same and T[t] != 'absent' and A[t] != 'absent':
        d = [k for k in range(n) if T[t][k] != A[t][k]]
        print('    differ at %s: the translator %s, A %s' % (d[:12], [T[t][k] for k in d[:12]], [A[t][k] for k in d[:12]]))
same = pT == pA; ok &= same
print('fusetab: %s the probes (inline, var) - the translator\'s %s B, A\'s %s B: %s' % (name, pT, pA, 'the same' if same else 'DIFFER'))
same = sT == sA
# 714: A is laid out smaller, so the programs' code can sit nearer the kernel - a call near rather than far (the byte
# header's reach), a slot of 2 bytes rather than 3 (VARSLOT): A's code then differs with the fusion on and off alike.
# At the byte header that is a pass when every zeroed table leaves the same difference, program by program.
dif = [a - t for a, t in zip(sA, sT)]
addr = bool(off) and all([(a or 0) - (t or 0) for a, t in zip(offA.get(k) or [], v)] == dif for k, v in off.items())
if not tag2 and off: ok &= same or addr      # no table: the code is A's own layout's (a8d35bdccc: shellmix -30 B) - reported
print('fusetab: %s the five programs\' code - the translator\'s %s (%d B), A\'s %s (%d B): %s' % (
      name, sT, sum(sT), sA, sum(sA), 'the same' if same else 'DIFFER' + (' (the two-bit tag: calls by distance - reported only)' if tag2 else
      ' - by the address alone: the same difference with each table zeroed' if addr else
      ' (no fusion table: A\'s own layout - reported only)' if not off else '')))
for t, v in off.items():
    print('fusetab: %s the five programs\' code in the translator\'s with %s zeroed (the fusion off): %s (%d B) - the table %s the code;'
          ' A\'s with it zeroed %s (%d B)%s' % (name, t, v, sum(x or 0 for x in v), 'changes' if v != sT else 'does not change',
          offA.get(t), sum(x or 0 for x in offA.get(t) or []), ' - the same as the translator\'s' if offA.get(t) == v else ''))
print('fusetab: %s %s' % (name, 'PASS' if ok else 'FAIL'))
sys.exit(0 if ok else 1)
