#!/usr/bin/env python3
"""
tools/layout.py - the layout pass: place every word, then re-encode.

Iteration 173, on branch token16. Reads the addressed dictionary dump,
lays the whole image out again with token bodies instead of cell
bodies, recomputes every reference that the new spacing invalidates,
and CHECKS the result rather than asserting it.

WHAT THE LAYOUT PASS ACTUALLY HAS TO DO

tools/sod16.py translates one word body in isolation. That is enough to
measure size and to prove the encoding reversible, and not enough to
boot: a token body is a different size from a cell body, so every
address in the image moves. This tool does the whole image.

The image is a strict ascending sequence, confirmed in Iteration 171:

    [prologue: 2 code cells, then filler, then the first link cell]
    [link][name field, aligned][body]      per word, oldest first
    ...                                    ending at HERE

The older word's body ends exactly where the newer word's link cell
begins - checked here on every consecutive pair, not assumed.

WHAT MOVES, AND WHAT DOES NOT

  link fields    relative, so the VALUE changes when spacing does.
  call offsets   become word numbers, which do not move at all. This
                 is the category that vanishes, and it is why
                 Iteration 167 could say re-layout is a list rather
                 than a search.
  branch offsets token units, converted in sod16.py.
  (LOOP) operand a byte offset in a cell, recomputed for the new
                 spacing.
  DEFER xts      stored START-relative; become word numbers.

CODE IS NOT TOLD FROM DATA BY WHETHER IT DECODES

26 CONSTANTs decode cleanly as code and ARE code, because CONSTANT
compiles `LIT-TOK , , EXIT-TOK ,`. Meanwhile 404 DOVAR words and 93
DOES> words are data sitting behind a call. The classifier is the first
cell of the body, not the success of a decoder - getting this backwards
translates constants correctly and silently corrupts every variable.

A data body keeps its cells. Its first cell is a call to a runtime that
does `R>` to get the parameter field address, so the parameter field
must stay CELL aligned - which is arranged by padding with NOOPs BEFORE
the call token, exactly as (LOOP) is. Padding after the token would be
what the parameter field pointed at.

THE DOES> TAILS

A DOES>-created word's body[0] calls a MID-WORD address: (;CODE) points
it just past the DOES> in the defining word. A SOD16 call token is a
word number and a word number can only name a word start, so these have
no representation - see SOD16.md.

Measured, there are exactly TWO such targets in this image, inside
BUFFER: and inside DEFER, shared by 81 and 12 words. So they are given
word numbers past the end of the chain, and the image carries a small
side table of (word number, byte offset) pairs so the loader can
rebuild those entries after it has rebuilt the chain ones. Two entries.
The word table itself stays derived and unsaved; this table describes
how to finish deriving it.
"""
import re, sys, collections, json   # json: Iteration 77 - the tag's ranking used it unimported

ARGV = list(sys.argv)          # sod16.py's argv is faked below; keep ours
DUMP = sys.argv[1] if len(sys.argv) > 1 else '/tmp/dump64.txt'
CELL = int(sys.argv[2]) if len(sys.argv) > 2 else 8

sys.argv = ['sod16.py', DUMP, str(CELL)]
_src = open(__file__.replace('layout.py', 'sod16.py')).read()
_lib = _src[:_src.index("# ---- optional emission")]
G = {'__name__': 'sod16lib'}
exec(compile(_lib, 'sod16lib', 'exec'), G)

# Encoding options, parsed BEFORE any body is classified, because they
# change what read_ops() returns and so the size of every body.
def _opt(name, default=None):
    return ARGV[ARGV.index(name) + 1] if name in ARGV else default
CPT = int(_opt('--cpt')) if '--cpt' in ARGV else None   # scale shift S
DATAPRIMS = '--dataprims' in ARGV
if '--fold' in ARGV: G['FOLD'] = True
if '--fold-set' in ARGV: G['FOLDSET'] = set(_opt('--fold-set').split(','))
if CPT is not None and CPT > 1: G['ALIGN_TAILS'] = 1 << CPT
V8 = '--v8' in ARGV
if V8:
    G['V8'] = True
    G['V8_FOLDLIST'] = _opt('--fold-set', '').split(',')
    if '--ops10-file' in ARGV:      # colon words as opcodes: [[name, opcode], ...]
        import json
        G['X_OPS10'].update({n: op for n, op in json.load(open(_opt('--ops10-file')))})
    if '--supers-file' in ARGV:     # superinstructions: [[first, second, opcode], ...]
        import json
        G['SUPERS'] = {(a, b): op for a, b, op in json.load(open(_opt('--supers-file')))}
    if '--hotcalls-file' in ARGV:   # one-byte calls: [[old target address, opcode, name], ...]
        import json                 # (Iteration 13: the image side, for pricing; no engine runs them yet)
        G['HOTCALLS'].update({a: op for a, op, _ in json.load(open(_opt('--hotcalls-file')))})

# --bytehdr: byte-granular dictionary headers. The link is 1-3 bytes with
# its tag byte LAST (read backward from the nfa), names are not padded,
# code bodies are not padded at the end, and the call scale is 0. Only
# bodies that hold cell-sized things - data words, and code with inline
# cell operands or a builtin tail - get their START aligned. This needs
# the cv8b.4 overlay in the image, since the kernel's own SEARCH-WORDLIST
# and NAME> assume a cell link and an aligned name.
BYTEHDR = '--bytehdr' in ARGV
if BYTEHDR and not (V8 and CPT == 0):
    sys.exit("--bytehdr requires --v8 --cpt 0")


# ---- the two-bit tag (Iteration 66, FORMAT-TAG2.md): --tag2 -----------
TAG2_ON = '--tag2' in ARGV
if TAG2_ON and not (V8 and CPT == 0):
    sys.exit("--tag2 requires --v8 --cpt 0")
if TAG2_ON and CELL != 8:
    sys.exit("--tag2: 64-bit cells for now - a DOES> body's 4-byte call must fit its first cell")


def linklen(d):
    if TAG2_ON: return 1 if d < 64 else 2 if d < (1 << 14) else 3 if d < (1 << 22) else 4
    return 1 if d < 128 else (2 if d < 16384 else 3)


def linkbytes(d, n):
    if TAG2_ON:
        # tag 2: low byte first, the tag in the top two bits of the LAST byte -
        # the one before the name, read first (vm-lab.c PREVNFA)
        assert 0 <= d < (1 << (8 * n - 2)), "link %d out of %d bits" % (d, 8 * n - 2)
        return bytes([(d >> (8 * i)) & 0xFF for i in range(n - 1)] + [((n - 1) << 6) | (d >> (8 * (n - 1)))])
    if n == 1: return bytes([d])
    if n == 2: return bytes([d & 0xFF, 0x80 | (d >> 8)])
    return bytes([d & 0xFF, (d >> 8) & 0xFF, 0xC0 | (d >> 16)])
if '--spec' in ARGV: G['SPEC'].update(_opt('--spec').split(','))
if '--escape' in ARGV:
    G['ESCAPE'] = True
    G['ESC_PRIMS'].update(G['ESC_PRIMS_ALL'])
    if '--escape2' in ARGV: G['ESC_PRIMS'].update(G['ESC2_PRIMS'])
if '--no-varcall' in ARGV: G['VARCALL'] = False
if '--no-varslot' in ARGV: G['VARSLOT'] = False
UB = 1 if V8 else 2                # bytes per stream unit
DOVARP = len(G['prims']) + 1       # after LIT32
DODOES = len(G['prims']) + 2

# --- phase 3: swap the CV8 compiler words in (cv8.4) -----------------
# cv8.4 defines its words as `;8`, `IF8`, ... because redefining `;` in
# the CELL image would break the cell compiler on the very next
# definition. Here the body of each `X8` becomes the body of `X`, so the
# emitted image's compiler emits CV8. The `X8` names stay, harmlessly.
# The suffix is a parameter, not a constant: every stage that emits its
# own encoding ships an overlay using the same trick with a different
# suffix (cv8.4 uses '8', cpt16.4 uses '16').
if '--compiler-overlay' in ARGV:
    OVERLAY_SUFFIX = ARGV[ARGV.index('--compiler-overlay') + 1]
elif '--cv8-compiler' in ARGV:
    OVERLAY_SUFFIX = '8'
else:
    OVERLAY_SUFFIX = None
CV8_COMPILER = OVERLAY_SUFFIX is not None
SRC_OF = {}          # destination word start -> source word start
SWAPPED = {}         # an X8 word whose body went into X: its start -> X's start (Iteration 38)

words, cells, tokn = G['words'], G['cells'], G['tokn']
read_ops, to_tokens, layout = G['read_ops'], G['to_tokens'], G['layout']
retag = G['retag']
idx_of, prims, stub_ops = G['idx_of'], G['prims'], G['stub_ops']
align_up, LOOPS, STR = G['align_up'], G['LOOPS'], G['STR']
code_end = G['code_end']

# ---- the anchor -----------------------------------------------------
START = None
for l in open(DUMP, errors='replace'):
    m = re.match(r'^S (\d+) (\d+)', l)
    if m: START, HERE = int(m.group(1)), int(m.group(2)); break
if START is None:
    sys.exit("no S anchor line in %s - regenerate the dump with the "
             "current tools/dict-dump-addr.4" % DUMP)

# ---- the dictionary, oldest first ----------------------------------
order = list(reversed(words))          # definition order, as sod16.py numbers
for w in order:
    w['nfa']  = w['s'] - align_up(len(w['n']) + 1, CELL)
    w['link'] = w['nfa'] - CELL
starts = {w['s']: w for w in order}
num = {w['s']: i for i, w in enumerate(order)}

# The structure is checked, not assumed.
gaps = sum(1 for i in range(len(order) - 1)
           if order[i]['e'] != order[i + 1]['link'])
PROLOGUE = order[0]['link'] - START    # bytes before the first link cell

# ---- classify every body -------------------------------------------
# body[0] is a call to a runtime => the body is DATA behind that call.
DOVAR = {w['s'] for w in order if w['n'] == 'DOVAR'}
tails = collections.Counter()
for w in order:
    v = cells.get(w['s'])
    if v is not None and not (v & 1):
        t = w['s'] + CELL + v
        if t not in starts: tails[t] += 1
TAILS = sorted(tails)                  # deterministic: ascending address
tailnum = {t: len(order) + i for i, t in enumerate(TAILS)}

def classify(w):
    """('code', ops) or ('data', first-cell-target or None)."""
    v = cells.get(w['s'])
    if v is not None and not (v & 1):
        t = w['s'] + CELL + v
        if t in DOVAR or t in TAILS:
            return 'data', t
    ops = read_ops(w)
    if ops is not None and to_tokens(ops) is not None:
        return 'code', ops
    return 'data', None

# ---- inlining at the hottest call sites (Iteration 92): --hot-inline FILE K
# The list (lab/evolve/hotsites.py): [[caller, callee, k, share], ...], the
# hottest first. The first K this design can inline safely (sod16.py,
# inline_body) are spliced in as the bodies are read, just below.
import os as _os
# the words whose bodies this file rewrites after reading them - the run-time
# compiler's opcode constants under the tag (checked against that section)
T2_CONSTS = ('EXIT-OP', 'LIT16-OP', 'BRANCH-OP', '0BRANCH-OP', 'LIT32-OP', 'DOVAR-OP', 'DODOES-OP', 'LIT8-OP', 'LIT64-OP',
             'BRANCH8-OP', '?BRANCH8-OP', 'JIT-OP')
G['HOT_PATCHED'].update(T2_CONSTS)
if '--hot-inline' in ARGV and not _os.environ.get('SOD16_NO_HOTINL'):
    _want, _sel = int(ARGV[ARGV.index('--hot-inline') + 2]), []
    if CV8_COMPILER:                                 # the swap below, foreseen (sod16.py, final_word)
        _by8 = collections.defaultdict(list)
        for _w in order: _by8[_w['n']].append(_w)
        for _n, _ws in _by8.items():
            if len(_n) > len(OVERLAY_SUFFIX) and _n.endswith(OVERLAY_SUFFIX) and _n[:-len(OVERLAY_SUFFIX)] in _by8 and G['raw_read'](_ws[-1]):
                _dst = _by8[_n[:-len(OVERLAY_SUFFIX)]][-1]
                G['HOT_FINAL'][_ws[-1]['s']] = _dst['n']; G['HOT_BODY'][_dst['s']] = _ws[-1]['s']
                G['HOT_SKIP'].add(_dst['s']); G['HOT_SKIP'].update(x['s'] for x in _ws[:-1])
    for _c, _t, _k, _ in json.load(open(_opt('--hot-inline'))):
        if len(_sel) >= _want: break
        for _w in [x for x in order if G['HOT_FINAL'].get(x['s'], x['n']) == _c and x['s'] not in G['HOT_SKIP']]:
            _ops = G['raw_read'](_w) or []
            _at = [j for j, v in G['hot_sites'](_w, _ops).items() if v == (_t, _k)]
            if _at and G['inline_body'](_ops[_at[0]][1]) is not None and not any(_w['s'] < e < _w['e'] for e in G['ENTRIES']):
                _sel.append((_c, _t, _k)); break
            if _os.environ.get('SOD16_HOTINL_WHY'): print('hot-inline: not %s>%s#%d - %s' % (_c, _t, _k, G['HOT_WHY'][0] if _at else 'no such call'))
    G['HOTINL'].update(_sel)
    print('hot-inline: %d sites - %s' % (len(_sel), ', '.join('%s>%s#%d' % x for x in _sel)))

kind, info, tok = {}, {}, {}
for w in order:
    k, i = classify(w)
    kind[w['s']], info[w['s']] = k, i

if CV8_COMPILER:
    # `X8` body becomes `X`'s body, so the image's compiler emits CV8.
    _by = {}
    for w in order:
        _by.setdefault(w['n'], []).append(w)
    _n, _miss, _unmatched = 0, [], []
    for w in order:
        if (len(w['n']) <= len(OVERLAY_SUFFIX)
                or not w['n'].endswith(OVERLAY_SUFFIX)): continue
        tgt = w['n'][:-len(OVERLAY_SUFFIX)]
        if tgt not in _by:
            _unmatched.append(w['n']); continue
        dst = _by[tgt][-1]
        if kind[w['s']] != 'code' or info[w['s']] is None:
            _miss.append(w['n']); continue
        kind[dst['s']], info[dst['s']] = 'code', list(info[w['s']])
        # A swapped body's operand offsets are relative to the SOURCE
        # word's old address, so anything that resolves an inline
        # address must use that base, not the destination's.
        SRC_OF[dst['s']] = w['s']
        SWAPPED[w['s']] = dst['s']
        _n += 1
    print("compiler overlay '%s': %d word bodies swapped in%s%s"
          % (OVERLAY_SUFFIX, _n, "; NOT translatable: %s" % _miss if _miss else "",
             "; no such target: %s" % _unmatched if _unmatched else ""))

# ---- the X8 copies dropped (Iteration 38): --drop-x8 -----------------
# After the swap every X8 word is a second copy of its X's code, kept only
# because something reaches it: copied bodies call X8 words (VARIABLE,
# with VARIABLE8's body, calls CREATE8) and POSTPONE them. Each such call
# goes to X - the same code - and (POSTPONE) operands resolve to X through
# body_at below; then the X8 words leave the image: 8.1% of seed 6's
# smallest design, 7.7% of its fastest (lab/evolve, Iteration 38).
#
# Every call or (POSTPONE) of any X8 goes to its X - the latest code under
# that name: cv8.4's WHILE8 calls IF8, and with run-time fusion IF is
# cv8-fuse.4's, as seed 7's designs were built. One exception (Iteration
# 41): a later X8 that defers to the one it replaces (cv8-fuse-loop.4)
# calls an EARLIER X8 OF ITS OWN NAME - from X too, whose code it is - and
# that call stays, keeping the earlier one; sent to X it would call itself.
def _refs(ws, skip=(), chain=None):       # every call target and (POSTPONE) target in these words' code
    r = set()
    for _w in ws:
        if kind[_w['s']] != 'code' or not info[_w['s']]: continue
        _, _cs, _, _, _ = layout(info[_w['s']])
        for _j, (_k, _pl) in enumerate(info[_w['s']]):
            if _k == 'C': r.add(_pl)
            elif _k == 'XT':
                # a (POSTPONE) of a swapped X8 resolves to its X (body_at) -
                # unless it is a deferral to an earlier one of its own name:
                # POSTPONE of an IMMEDIATE word compiles (POSTPONE), not a
                # call, so cv8-fuse-loop.4's ?DO8 reaches the old ?DO8 so
                _t = SRC_OF.get(_w['s'], _w['s']) + _cs[_j] + _pl
                if _t not in skip or (chain and chain(_w['s'], _t)): r.add(_t)
    return r
DROPPED = {}
import os as _os
_NO_LEAN = _os.environ.get('SOD16_NO_LEAN')      # both parts of the gene lean off, to measure (Iteration 39)
if CV8_COMPILER and '--drop-x8' in ARGV and SWAPPED and not _os.environ.get('SOD16_NO_DROPX8') and not _NO_LEAN:   # the switch: to measure
    _nm = {w['s']: w['n'] for w in order}
    def _chain(caller, t):                # a later X8 (or its X) deferring to an earlier one of its name
        src = SRC_OF.get(caller, caller)
        return src in SWAPPED and _nm.get(src) == _nm.get(t) and t < src
    for _w in order:
        if kind[_w['s']] == 'code' and info[_w['s']]:
            info[_w['s']] = [('C', SWAPPED[_pl]) if _k == 'C' and _pl in SWAPPED and not _chain(_w['s'], _pl) else (_k, _pl)
                             for _k, _pl in info[_w['s']]]
    _cand = set(SWAPPED)                                        # every X8: out unless a deferral still calls it
    while True:
        _r = _refs([w for w in order if w['s'] not in _cand], skip=SWAPPED, chain=_chain)
        _back = {s for s in _cand if s in _r}
        if not _back: break
        _cand -= _back
    DROPPED = {s: SWAPPED[s] for s in _cand}
    _out = set(DROPPED)
    _gone = [w for w in order if w['s'] in _out]
    order = [w for w in order if w['s'] not in _out]
    print('drop-x8: %d copies out, %d bytes of the old image' % (len(_gone), sum(w['e'] - w['link'] for w in _gone)))

# ---- the dump tool and dead shadowed words left out (Iteration 39) ---
# tools/dict-dump-addr.4 is loaded LAST, to write this very dump: its
# words (NFA ... DUMP) came into every image, 490-688 bytes of seed 6's
# front, and nothing in the running system uses them. And a word defined
# again under the same name is reachable by name no more; if nothing calls
# it or (POSTPONE)s it either (cv8.4's FOLD-OP under cv8-fuse.4's), it is
# reachable not at all. Both leave `order` only where nothing refers to
# them - checked, not assumed.
DUMPTOOL = ('NFA', 'BP', 'BE', 'NFATAB', '#NFA', 'TA', 'CELLB', 'INIT-NFATAB', 'COLLECT', 'SWAPC', 'SORTNFA', 'DUMP', 'PROLOGUE-DUMP')
if '--drop-dumptool' in ARGV and not _os.environ.get('SOD16_NO_DROPTOOL') and not _NO_LEAN:
    _names = [w['n'] for w in order]
    _k = len(_names) - 1 - _names[::-1].index('NFA') if 'NFA' in _names else None
    _tool = order[_k:] if _k is not None and all(w['n'] in DUMPTOOL for w in order[_k:]) else []
    _keep = order[:_k] if _tool else order
    _r = _refs(_keep)
    if any(w['s'] in _r for w in _tool):
        print('drop-dumptool: a word refers to the dump tool - kept'); _tool = []
    _seen, _shadow = set(), []
    for w in reversed(_keep):
        if w['n'] in _seen and kind[w['s']] == 'code' and w['s'] not in _r: _shadow.append(w)
        _seen.add(w['n'])
    _out = set(w['s'] for w in _tool + _shadow)
    order = [w for w in order if w['s'] not in _out]
    print('drop-dumptool: %d dump-tool words, %d dead shadowed (%s) out, %d bytes of the old image'
          % (len(_tool), len(_shadow), ' '.join(w['n'] for w in _shadow) or '-', sum(w['e'] - w['link'] for w in _tool + _shadow)))

# ---- scratch buffers out of the file (Iteration 44): --bss ----------
# TIB, POCKET and INCLUDE-BUFFER are VARIABLEs with an ALLOT: 1,040 bytes
# of every image that are only ever written before they are read. Each
# becomes a word that pushes START + an offset past the image's end - a
# LITOFF patched once the layout is known - and its parameter field moves
# there: v8pfa and remap_pfa_off send references to it, DP starts past
# them, and the engine's memory there is zero (a static array). NAMEBUF
# stays: FIND reads it for every candidate, and a call would cost more
# than a variable.
BSS_WORDS = ('TIB', 'POCKET', 'INCLUDE-BUFFER')
BSS, BSS_OFF, BSS_END = {}, {}, None
if V8 and CV8_COMPILER and '--bss' in ARGV and not _os.environ.get('SOD16_NO_BSS'):
    _start = [w for w in order if w['n'] == 'START']
    for _n in BSS_WORDS:
        _ws = [w for w in order if w['n'] == _n]
        if not _ws or not _start: continue
        _w = _ws[-1]
        if kind[_w['s']] != 'data' or not G['is_var'](_w['s']): continue    # only a VARIABLE and its ALLOT
        BSS[_w['s']] = (_w['s'] - START + CELL, _w['e'] - (_w['s'] + CELL))  # old parameter field, its bytes
        kind[_w['s']], info[_w['s']] = 'code', [('LITOFF', 0), ('C', _start[-1]['s']), ('P', '@'), ('P', '+'), ('P', 'EXIT')]
    print('bss: %s out of the file, %d bytes' % (' '.join(w['n'] for w in order if w['s'] in BSS), sum(n for _, n in BSS.values())))

# ---- FILL and CMOVE: their own bodies the opcode too (Iteration 50) --
# With FILL or CMOVE a format-10 opcode, calls in the image's code become it
# (ops10_rewrite); code compiled at RUN time still calls the colon word -
# the sieve's FILL. So its body becomes the opcode and EXIT: the same work -
# the body was checked against the definition the opcode does (ops10_at) -
# for a call and two dispatches instead of 12-14 a byte, and its loop gone.
# Only these two, which never look at their caller's return address (I J
# UNLOOP (DO) do), and only where the design has them: no recorded design.
_OPB = ('FILL', 'CMOVE', 'SCAN', 'SKIP', 'TABS>BL', '(PARSE)', 'HASH', 'PLACE')     # Iteration 54: the input side's too
if '--op-bodies' in ARGV: _OPB += ('(FIND)', '(>NUMBER)', 'THREAD-FIND', '+!', '?DUP')   # Iteration 92: the gene opbody
for _n in _OPB:
    if _n not in G['X_OPS10']: continue
    _at = {a: n for a, n in G['ops10_at']().items() if n == _n}
    _w = [w for w in order if w['s'] in _at]
    if _w: kind[_w[-1]['s']], info[_w[-1]['s']] = 'code', [('P', _n), ('P', 'EXIT')]

# ---- one-byte calls (Iteration 14): --hotcalls N --------------------
# The targets with the most call sites in the image's code take the bytes
# 0xE0-0xFF, through a table in the header (2 bytes an entry). Chosen here,
# from the design's own code, before anything is sized: a site before an
# inline operand counts last (its operand stays aligned, so what it saves
# depends on where it lands), and a target must have three sites - two
# would only pay for its entry. lab/evolve/callsites.py priced it.
import os as _os
HOT = []
if V8 and '--hotcalls' in ARGV and not TAG2_ON and not _os.environ.get('SOD16_NO_HOTCALLS'):
    _free, _all = collections.Counter(), collections.Counter()
    for w in order:
        if kind[w['s']] != 'code': continue
        _ops = info[w['s']]
        for _j, (_k, _pl) in enumerate(_ops):
            if _k != 'C': continue
            _all[_pl] += 1
            if not G['before_operand'](_ops, _j): _free[_pl] += 1
    _rank = sorted(_all, key=lambda a: (-_free[a], -_all[a], a))
    HOT = [a for a in _rank if _free[a] >= 3][:min(32, int(_opt('--hotcalls')))]
    G['HOTCALLS'].update({a: 0xE0 + i for i, a in enumerate(HOT)})
    print('one-byte calls: %d targets, %d sites' % (len(HOT), sum(_all[a] for a in HOT)))

# ---- the two-bit tag: the design's operations ranked ------------------
# Every operation this design's engine has (sod16 t2_names) gets a code: the
# pinned ones - NOOP at 0 (padding is NOOPs), what the run-time compiler
# writes by constant - then the rest by the reference profile's weight
# (--tag2-rank FILE: name -> weight, each selected workload equal), then by
# how often the image's code uses it. 63 one-byte codes, the escape at 0x3F,
# the rest escaped. Exact counts, so the numbering - and the image - are
# reproducible. Before anything is sized: sizes depend on it.
T2MAP = None
G['JIT_ON'] = '--jit' in ARGV           # Iteration 81: the JIT's opcode among the tag's operations (sod16 t2_names)
if V8 and _os.environ.get('SOD16_T2NAMES'):        # the names behind the reference ranking (lab/evolve/tag2-rank.py)
    json.dump({str(k): v for k, v in G['t2_names']().items()}, open(_os.environ['SOD16_T2NAMES'], 'w'))
if TAG2_ON:
    _names = G['t2_names']()
    _static = collections.Counter()
    for w in order:
        if kind[w['s']] != 'code': continue
        _ops = info[w['s']]
        for _j in range(len(_ops)):
            _L = G['opcode_L'](_ops, _j)
            if _L is not None: _static[_L] += 1
    _ref = json.load(open(_opt('--tag2-rank'))) if '--tag2-rank' in ARGV else {}
    _pin = [idx_of[n] for n in ('NOOP', 'EXIT', 'LIT', 'BRANCH', '?BRANCH')]
    _pin += [G['V8_LIT8'], G['V8_LIT32'], G['V8_LIT64'], G['V8_DOVAR'], G['V8_DODOES']]
    _pin += [G['X_OPS10'][n] for n in ('BRANCH8', '?BRANCH8') if n in G['X_OPS10']]
    _pin += [G['T2_JIT']] if '--jit' in ARGV else []   # Iterations 80-81: every run-time word's first byte - no slot
    # the run-time loop compilers (cv8-fuse-loop.4, cv8-fuse-loopall.4): their
    # loop opcodes, pinned - loopall has no fallback, and an escaped loop
    # opcode in loop's tables falls back to calling the colon word
    if any(x['n'] in ('LOOPTAB', 'LOOP-OPS') for x in order):
        _pin += [G['X_OPS10'][n] for n in ('(DO)', '(LOOP)', '(+LOOP)', '(?DO)', '(LEAVE)', 'I', 'J', 'UNLOOP')
                 if n in G['X_OPS10'] and G['X_OPS10'][n] not in _pin]
    assert all(p in _names for p in _pin), [p for p in _pin if p not in _names]
    # --tag2-hot W: an operation weighing at least W in the reference is hot -
    # ranked first, by weight; the rest by how often the image uses it. 0:
    # every weighed operation hot (speed first); large: none (size first).
    _hot = float(_opt('--tag2-hot')) if '--tag2-hot' in ARGV else 0.0
    def _key(x):
        wt = _ref.get(_names[x], 0)
        return (0, -wt, -_static[x], x) if wt > 0 and wt >= _hot else (1, -_static[x], -wt, x)
    _rest = sorted((x for x in _names if x not in _pin), key=_key)
    _all = _pin + _rest
    assert len(_all) <= 63 + 256, "%d operations: more than 63 one-byte codes and 256 escaped" % len(_all)
    T2MAP = {'one': {x: c for c, x in enumerate(_all[:63])}, 'esc': {x: s for s, x in enumerate(_all[63:])}, 'escc': 0x3F}
    G['TAG2'][0] = T2MAP
    print('tag 2: %d operations, %d one-byte, %d escaped; %d escaped uses in the image (a byte each)'
          % (len(_all), len(T2MAP['one']), len(T2MAP['esc']), sum(_static[x] for x in T2MAP['esc'])))
    # the run-time compiler's opcode constants (forth/cv8t.4) - each a body
    # [LIT n][EXIT] - rewritten to this design's codes; the short branches'
    # to their codes, or 0 where the design has none
    _cn = {'EXIT-OP': 1, 'LIT16-OP': 2, 'BRANCH-OP': 3, '0BRANCH-OP': 4, 'LIT32-OP': 68,
           'DOVAR-OP': 69, 'DODOES-OP': 70, 'LIT8-OP': 71, 'LIT64-OP': 124}
    _cx = {'BRANCH8-OP': 'BRANCH8', '?BRANCH8-OP': '?BRANCH8', 'JIT-OP': None}   # JIT-OP: forth/cv8t-jit.4
    assert set(_cn) | set(_cx) <= set(T2_CONSTS), 'tag 2: an opcode constant --hot-inline does not know (T2_CONSTS)'
    _done = set()
    for w in order:
        if w['n'] not in _cn and w['n'] not in _cx: continue
        _ops = info[w['s']]
        _lj = [j for j, (k, _p) in enumerate(_ops) if k in ('LIT', 'LITX')]
        assert kind[w['s']] == 'code' and len(_lj) == 1, ('tag 2: an opcode constant not [LIT n][EXIT]', w['n'], _ops)
        _k, _p = _ops[_lj[0]]
        if w['n'] in _cn:
            assert _p == _cn[w['n']], ('tag 2: unexpected value', w['n'], _p)
            _ops[_lj[0]] = (_k, T2MAP['one'][_p])
        else:
            _x = G['X_OPS10'].get(_cx[w['n']]) if _cx[w['n']] else (G['T2_JIT'] if '--jit' in ARGV else None)
            _ops[_lj[0]] = (_k, T2MAP['one'][_x] if _x is not None else 0)
        _done.add(w['n'])
    print('tag 2: %d opcode constants rewritten' % len(_done))

for w in order:
    if kind[w['s']] == 'code': tok[w['s']] = to_tokens(info[w['s']])

# ---- new sizes ------------------------------------------------------
def tail_bytes(w):
    """Unheadered data compiled after this word's code - see code_end.

    A PRIMITIVE stub is read by shape, not by walking, so code_end does
    not apply to it and would report its second cell as a tail."""
    if kind[w['s']] != 'code' or stub_ops(w) is not None: return 0
    return w['e'] - code_end(w)

def body_needs_align(w):
    """In bytehdr mode only these bodies start on a cell boundary."""
    if kind[w['s']] != 'code': return True
    if tail_bytes(w): return True
    return any(k in ('OPD', 'XT', 'STR', 'ALN') for k, _ in (info[w['s']] or []))


def new_body_bytes(w):
    if kind[w['s']] == 'code':
        if BYTEHDR:
            return len(tok[w['s']]) * UB + tail_bytes(w)
        return align_up(len(tok[w['s']]) * UB, CELL) + tail_bytes(w)
    if info[w['s']] is not None:
        # [pad][call token][parameter field, CELL aligned]
        # The pad goes BEFORE the token so the parameter field, which is
        # the address just past it, stays CELL aligned for `@`.
        return CELL + (w['e'] - w['s'] - CELL)
    return w['e'] - w['s']             # opaque: copied verbatim

# The thread each word belongs to, needed BEFORE placement in bytehdr
# mode: a link's length depends on its distance, and its distance is to
# the previous word in the same thread. Hashing needs only the name and
# the thread count, both known now.
_FW = [w for w in order if w['n'] == 'FORTH-WORDLIST']
if not _FW:
    sys.exit("no FORTH-WORDLIST in the dump")
_NTH = cells.get(_FW[0]['s'] + CELL, 0)
if not (1 <= _NTH <= 4096):
    sys.exit("FORTH-WORDLIST declares %r threads" % _NTH)


def _wl_hash(name):
    b = name.encode('latin-1')
    v = len(b) ^ (b[0] << 1)
    if len(b) > 1:
        v ^= b[1] << 2
    return v & (_NTH - 1)


_prev_in_thread, _last = {}, {}
for w in order:
    h = _wl_hash(w['n'])
    _prev_in_thread[w['s']] = _last.get(h)
    _last[h] = w['s']

new_off, off = {}, PROLOGUE
LINKLEN = {}
for w in order:
    if BYTEHDR:
        pv = _prev_in_thread[w['s']]
        # Bound from above: the nfa lands at most 3 bytes past `off`, so
        # a link sized for that distance always fits the real one.
        ll = 1 if pv is None else linklen(off + 3 - new_off[pv]['nfa'])
        LINKLEN[w['s']] = ll
        new_off[w['s']] = {'link': off}; off += ll
        new_off[w['s']]['nfa'] = off;   off += len(w['n']) + 1
        if body_needs_align(w): off = align_up(off, CELL)
        new_off[w['s']]['body'] = off;  off += new_body_bytes(w)
    else:
        new_off[w['s']] = {'link': off}
        off += CELL
        new_off[w['s']]['nfa']  = off; off += align_up(len(w['n']) + 1, CELL)
        new_off[w['s']]['body'] = off; off += new_body_bytes(w)
NEW_HERE = off
if BSS:                                              # Iteration 44: the buffers' place past the image
    _o = align_up(NEW_HERE, CELL)
    for _s, (_opfa, _n) in BSS.items(): BSS_OFF[_s] = _o; _o += align_up(_n, CELL)
    BSS_END = _o
# SYMMAP=file: write each word's body range in the NEW image, one line
# per word - start, end, name. tools/attribute.py joins it with an
# engine profile (-DPROFILE=1, VMPROF=file) to charge every dispatched
# VM instruction to the Forth word it executed in.
import os as _os
if _os.environ.get('SYMMAP'):
    with open(_os.environ['SYMMAP'], 'w') as _f:
        for _w in order:
            _b = new_off[_w['s']]['body']
            _f.write('%d %d %s\n' % (_b, _b + new_body_bytes(_w), _w['n']))
OLD_HERE = order[-1]['e'] - START

# ---- recompute the link chains, and re-walk them to prove it --------
# The word list is HASHED: as many chains as there are threads, each
# linked newest to oldest. The thread count is read out of the image
# being translated rather than assumed, so this file has no opinion
# about it and cannot disagree with kernel.4.
FW = [w for w in order if w['n'] == 'FORTH-WORDLIST']
if not FW:
    sys.exit("no FORTH-WORDLIST in the dump")
FW = FW[0]
FW_PF = FW['s'] + CELL                       # parameter field: [n][heads]
NTHREADS = cells.get(FW_PF, 0)
if not (1 <= NTHREADS <= 4096):
    sys.exit("FORTH-WORDLIST declares %r threads" % NTHREADS)


def wl_hash(name):
    """kernel.4's HASH, and cross.4's THASH. All three must agree."""
    b = name.encode('latin-1')
    v = len(b) ^ (b[0] << 1)
    if len(b) > 1:
        v ^= b[1] << 2
    return v & (NTHREADS - 1)


# Definition order within each thread; `order` is already oldest first.
threads = [[] for _ in range(NTHREADS)]
for w in order:
    threads[wl_hash(w['n'])].append(w)

linkval = {}
for t in threads:
    for i, w in enumerate(t):
        if i == 0:
            linkval[w['s']] = 0                          # end of chain
        elif BYTEHDR:
            # a DISTANCE backward from this nfa, always positive
            linkval[w['s']] = (new_off[w['s']]['nfa']
                               - new_off[t[i - 1]['s']]['nfa'])
            assert linkval[w['s']] < ((1 << (8 * LINKLEN[w['s']] - 2)) if TAG2_ON else
                                      (1 << LINKLEN[w['s']] * 7 + (1 if LINKLEN[w['s']] > 1 else 0))), \
                "link does not fit at %s" % w['n']
        else:
            linkval[w['s']] = (new_off[t[i - 1]['s']]['nfa']
                               - new_off[w['s']]['link'])

# The heads, as offsets from START, which is how the image stores them
# and what COLD relocates. An empty thread stays 0.
HEADS = [new_off[t[-1]['s']]['nfa'] if t else 0 for t in threads]

# Walk every chain back and check the union is exactly the dictionary.
by_nfa = {new_off[w['s']]['nfa']: w for w in order}
seen_names, broken = [], False
for t, head in zip(threads, HEADS):
    if not head:
        continue
    cur, n = by_nfa[head], 0
    while True:
        seen_names.append(cur['n'])
        lv = linkval[cur['s']]
        if lv == 0:
            break
        nxt = by_nfa.get(new_off[cur['s']]['nfa'] - lv if BYTEHDR
                         else new_off[cur['s']]['link'] + lv)
        if nxt is None:
            broken = True
            break
        cur = nxt
        n += 1
        if n > len(order) + 2:
            broken = True
            break
chain_ok = (not broken
            and sorted(seen_names) == sorted(w['n'] for w in order))

# The heads live in FORTH-WORDLIST's own parameter field, which is DATA
# and would otherwise be copied out of the dump verbatim - with the
# addresses of the image we were translating FROM. Overwrite them.
for i, h in enumerate(HEADS):
    cells[FW_PF + (i + 1) * CELL] = h

# ---- xts are ADDRESSES, and get relocated --------------------------
# Iteration 176. `: EXECUTE ( xt --- ) >R ;` is pure Forth, not a
# primitive: it makes the xt the return address, and EXIT jumps to it.
# So an xt has to be an executable address in either engine. A CALL
# TOKEN is a word number; an XT is an address. Iteration 165 conflated
# them, and 175 refused (POSTPONE) on the strength of that.
#
# Nothing here converts an xt to a word number. Everything here moves
# an offset to where its target landed.
body_at = {w['s'] - START: w for w in order}
for _a, _b in DROPPED.items():                     # a (POSTPONE) of a dropped X8 lands on its X
    body_at[_a - START] = next(w for w in order if w['s'] == _b)

def remap_body_off(off):
    w = body_at.get(off)
    return new_off[w['s']]['body'] if w else None

# (POSTPONE)'s inline operand: a relative address from the operand cell
# to another word's body. sod16.py passes it through because a per-word
# translator cannot see where other words land.
xt_ok, xt_bad, xt_new = 0, [], {}
for w in order:
    if kind[w['s']] != 'code': continue
    ops = info[w['s']]
    _, cs, ts, _, _ = layout(ops)
    for j, (k, pl) in enumerate(ops):
        if k != 'XT': continue
        tgt = (SRC_OF.get(w['s'], w['s']) + cs[j]) + pl - START
        n2 = remap_body_off(tgt)
        if n2 is None: xt_bad.append((w['n'], tgt))
        else:
            xt_ok += 1
            # RELOCATE it, do not merely count it: the operand is a byte
            # offset from its own cell to the target's body, and both
            # move. Until Iteration 196 the old value was passed through
            # and only checked, which no translated image ever noticed -
            # nothing in one COMPILES, so (POSTPONE) never ran. It runs
            # as soon as the image has its own compiler (cv8.4).
            xt_new[(w['s'], j)] = n2 - (new_off[w['s']]['body'] + ts[j])

# ---- DEFER xts -----------------------------------------------------
# A DEFER cell holds its xt as a START-relative offset (shell.4's
# !XT/@XT), which is what makes it survive a save. Under SOD16 an xt is
# a word number instead - Iteration 165 - so these convert, and the
# conversion is checked: every one must land on a word start.
#
# The BUFFER: words are NOT this. Their second cell is a live malloc'd
# pointer in this dump, and RESET-BUFFERS zeroes it before SAVE-SYSTEM,
# so in a saved image it carries nothing. That is the difference
# Iteration 167 was pointing at when it said the handful of
# image-range values come from a live-process dump.
DEFER_TAIL = None
for t in TAILS:
    h = [w for w in order if w['s'] < t < w['e']][0]
    if h['n'] == 'DEFER': DEFER_TAIL = t

# A DEFER cell holds a START-relative offset to a word body (shell.4's
# !XT/@XT). It stays an offset; it just points somewhere else now.
defers, defer_bad = {}, []
for w in order:
    if info.get(w['s']) != DEFER_TAIL or DEFER_TAIL is None: continue
    xt = cells.get(w['s'] + CELL)
    new = remap_body_off(xt) if xt is not None else None
    if new is not None: defers[w['s']] = new
    else: defer_bad.append((w['n'], xt))

# ---- BUFFER: parameter fields --------------------------------------
# pool.4: [+0 ptr][+1 size][+2 link]. The ptr is a live malloc'd address
# in this dump and RESET-BUFFERS zeroes it before a save, so it is
# written as 0 - the "not yet allocated" state ALLOC-BUFFERS expects.
# The link is a START-relative offset to the PREVIOUS buffer's body,
# and bodies move, so it is remapped. That is a relocation category the
# layout list in SOD16.md did not have.
BUF_TAIL = None
for t in TAILS:
    h = [w for w in order if w['s'] < t < w['e']][0]
    if h['n'] == 'BUFFER:': BUF_TAIL = t

# BUF-BODY is HERE at the moment CREATE has laid down the header and
# the leading call cell, so a buffer link points at the PARAMETER
# FIELD - one cell past the body start - not at the body start. In the
# new layout the parameter field is also one cell in, because the
# padding plus the call token come to exactly one cell.
pfa_at = {w['s'] - START + CELL: w for w in order}
buf_bad = []
def remap_pfa_off(off):
    """old START-relative parameter-field offset -> new one, or None."""
    w = pfa_at.get(off)
    if w and w['s'] in BSS_OFF: return BSS_OFF[w['s']]              # Iteration 44: past the image
    return new_off[w['s']]['body'] + CELL if w else None

bufs = 0
for w in order:
    if BUF_TAIL is None or info.get(w['s']) != BUF_TAIL: continue
    bufs += 1
    lnk = cells.get(w['s'] + 3 * CELL)
    if lnk: 
        if remap_pfa_off(lnk) is None: buf_bad.append((w['n'], lnk))

# ---- the BUILTIN table ---------------------------------------------
# shell.4 compiles its builtin table at HERE between definitions, so
# the entries have no headers and land inside the previous word's tail
# (see code_end). Each is [link][xt][len][name], and BOTH the link and
# the xt are START-relative offsets into an image whose bodies have all
# moved. BUILTIN-LIST holds the head, also as an offset.
#
# The entries move as a block with the tail that contains them, so a
# new offset is the tail's new position plus the same distance in.
tail_start = {}          # old address of a code word's tail
for w in order:
    if tail_bytes(w):
        tail_start[w['s']] = code_end(w)

def remap_tail_addr(addr):
    """old absolute address inside some tail -> new image offset."""
    for s0, ts_ in tail_start.items():
        w = starts[s0]
        if ts_ <= addr < w['e']:
            head = align_up(len(tok[s0]) * UB, CELL)
            return new_off[s0]['body'] + head + (addr - ts_)
    return None

BL = [w for w in order if w['n'] == 'BUILTIN-LIST']
builtins, bi_bad = 0, []
if BL:
    head = cells.get(BL[0]['s'] + CELL)          # parameter field
    o = head
    seen = set()
    while o and o not in seen:
        seen.add(o)
        a = START + o
        if remap_tail_addr(a) is None: bi_bad.append(('entry', o)); break
        xt = cells.get(a + CELL)
        if remap_body_off(xt) is None: bi_bad.append(('xt', o, xt))
        builtins += 1
        o = cells.get(a)                          # link to previous
    if remap_tail_addr(START + head) is None: bi_bad.append(('head', head))

# ---- the four remaining offset cells --------------------------------
# save-system.4 enumerates these, so they do not have to be guessed.
# SS-UNRELOCATE: "COLD is the authority on which cells these are, and
# there are exactly two: DP and FORTH-WORDLIST." SET-BOOT adds BOOT,
# and pool.4 adds BUF-LIST. Everything else that holds an offset is
# either scrubbed by SS-SCRUB or is one of the categories above.
#
# DP and FORTH-WORDLIST are ABSOLUTE in a live dump, because COLD added
# START to them at boot, and are written back as offsets. BOOT and
# BUF-LIST are offsets at rest.
def pfa_of(name):
    w = [x for x in order if x['n'] == name]
    return w[0]['s'] + CELL if w else None

fixed, fixed_bad = {}, []
_dp = pfa_of('DP')
if _dp: fixed['DP'] = BSS_END if BSS_END is not None else NEW_HERE   # past the buffers (Iteration 44)
_fw = pfa_of('FORTH-WORDLIST')
# The first cell of the word list is the THREAD COUNT, not a chain head.
# It used to be the head, and this line still forced it to the newest
# word's nfa - so a translated image began its boot relocation loop with
# `<address> 1 DO`, which counts up to 2^64. The image hung before it
# printed its banner. The heads themselves are patched into `cells`
# where the threads are computed.
if _fw: fixed['FORTH-WORDLIST'] = NTHREADS
_bt = pfa_of('BOOT')
if _bt:
    v = cells.get(_bt)
    # The dump session never runs SET-BOOT, so BOOT is 0 and the image
    # comes up at the Forth interpreter. Point it at MAIN so the image
    # is turnkey, which is what relfsh's image is: otherwise the only
    # way in is to type MAIN, and that eats the stdin a shell script
    # needs.
    _main = [x for x in order if x['n'] == 'MAIN']
    if not v and _main: fixed['BOOT'] = new_off[_main[0]['s']]['body']
    elif not v: fixed['BOOT'] = 0
    elif remap_body_off(v) is not None: fixed['BOOT'] = remap_body_off(v)
    else: fixed_bad.append(('BOOT', v))
# ---- live-session scratch -------------------------------------------
# The dump is of a LIVE session, and nothing scrubs it: these hold the
# build session's absolute addresses, so two builds of the same sources
# differed in exactly these cells. save-system.4's SS-SCRUB blanks the
# kernel's ones in a saved image - COLD, WARM, QUIT or the shell's MAIN
# set each again before it is read - and the last five are the dump
# tool's own variables (tools/dict-dump-addr.4). LAST matters beyond
# reproducibility: it is not reset at boot, so until the first
# definition it pointed into the build session's address space, and an
# IMMEDIATE typed straight after boot wrote to an arbitrary address.
# Zeroed, as in a saved image, it is at least the same every time.
# pool.4's, locals.4's and the saver's own scratch are SS-SCRUB's too;
# BUF-BODY and BUF-PTR held heap addresses in the full self image.
SCRUB = {'START', 'S0', 'R0', 'HLD', 'SRC', '#SRC', '>IN', 'SID', '#TIB',
         'SPAN', 'LAST', 'CURRENT', 'CSP', "'LEAVE", 'INCLUDE-POINTER',
         'CONTEXT', 'BUF-BODY', 'BUF-SIZE', 'BUF-PTR', 'LSAVE-SP',
         'SS-FID', 'SS-LEN', 'SS-BUF',
         'NFA', 'BP', 'BE', 'NFATAB', 'TA'}
_bl = pfa_of('BUF-LIST')
if _bl:
    v = cells.get(_bl)
    if not v: fixed['BUF-LIST'] = 0
    elif remap_pfa_off(v) is not None: fixed['BUF-LIST'] = remap_pfa_off(v)
    else: fixed_bad.append(('BUF-LIST', v))
if BL:
    h = cells.get(BL[0]['s'] + CELL)
    if h: fixed['BUILTIN-LIST'] = remap_tail_addr(START + h)

def tk(v): return (v & 0xFFFF).to_bytes(2, 'little')

# ---- CPT16: call tokens are scaled image offsets, not word numbers ---
SKIPPAD = '--skip-pad' in ARGV
def new_target_off(target):
    """old absolute call-target address -> new image offset."""
    if target in new_off:
        # A data body is [NOOP pad][call token][parameter field]. The pad
        # exists only to align the parameter field; a call may land on
        # the token itself and skip executing the NOOPs.
        if (SKIPPAD and not DATAPRIMS and kind[target] == 'data'
                and info[target] is not None):
            return new_off[target]['body'] + CELL - 2
        return new_off[target]['body']
    h = [x for x in order if x['s'] < target < x['e']][0]
    c2t_, _, _, _, _ = layout(info[h['s']])
    return new_off[h['s']]['body'] + c2t_[target - h['s']]
def calltok_addr(target):
    if CPT is None:
        return 256 + (num[target] if target in num else tailnum[target])
    off = new_target_off(target)
    assert off % (1 << CPT) == 0, "call target %d not %d-aligned" % (off, 1 << CPT)
    v = 256 + (off >> CPT)
    assert v <= 0xFFFF, "call target offset %d beyond CPT16 reach" % off
    return v
if CPT is not None:
    G['G_CALLTOK'][0] = lambda target, n: calltok_addr(target)
def v8val(target):
    off = new_target_off(target)
    assert off % (1 << CPT) == 0, "v8 call target %d not aligned" % off
    return off >> CPT
if V8: G['V8_CALLTOK'][0] = v8val
def v8pfa(target):
    off = BSS_OFF[target] if target in BSS_OFF else new_off[target]['body'] + CELL   # [DOVAR][pad] is one cell
    assert off % (1 << CPT) == 0 and (off >> CPT) < (1 << 23)
    return off >> CPT
def v8loc(old):
    n2 = remap_pfa_off(old)
    if n2 is None: n2 = remap_body_off(old)
    assert n2 is not None and n2 % (1 << CPT) == 0, old
    assert (n2 >> CPT) < (1 << 23), "locals slot %d beyond 23-bit reach" % n2
    return n2 >> CPT
G['V8_PFA'][0] = v8pfa
G['V8_LOC'][0] = v8loc
def callbytes(target):
    if V8 and TAG2_ON:
        v = v8val(target); return G['t2call'](v, G['t2calllen'](v))
    if V8:
        v = v8val(target)
        if G['VARCALL']:
            if v < (1 << 14): return bytes([0x80 | (v >> 8), v & 0xFF])
            return bytes([0xC0 | (v >> 16), (v >> 8) & 0xFF, v & 0xFF])
        return bytes([0x80 | (v >> 8), v & 0xFF])
    return tk(calltok_addr(target))

# ---- emit the token image -------------------------------------------
def emit(path):
    """Write the token image. Layout and values all come from above."""
    # Name flag bytes and prologue cells come from the dump's H and P
    # lines; DUMP itself masks the flags off and never walks the
    # prologue, so both were added in Iteration 174.
    flag, pro = {}, {}
    for l in open(DUMP, errors='replace'):
        m = re.match(r'^H (\d+) (\d+)', l)
        if m: flag[int(m.group(1))] = int(m.group(2)) & 0xFF
        m = re.match(r'^P (\d+) (-?\d+)', l)
        if m: pro[int(m.group(1))] = int(m.group(2))

    M = (1 << (8 * CELL)) - 1
    def cel(v): return (v & M).to_bytes(CELL, 'little')
    def tk(v):  return (v & 0xFFFF).to_bytes(2, 'little')

    img = bytearray()
    # CALLMAP=file (Iteration 13): every call site and every operation's
    # first byte in the code bodies, for lab/evolve/callsites.py:
    #   H header-bytes image-bytes scale
    #   C offset length target-offset old-target forced caller target
    #   O offset kind first-byte name
    #   T offset                        a branch target (Iteration 88)
    #   W body-start body-end code|data name      every word (Iteration 88)
    #   M 1 code name / M 2 selector name / M E code   the tag's codes (88)
    # Offsets from the image's start - the engine's base, as SYMMAP's.
    # forced: a call before an inline operand, always the long form. name:
    # the operation's design-independent name (sod16 t2_names, the tag's).
    _cm = [] if (V8 and _os.environ.get('CALLMAP')) else None
    _NM = G['t2_names']() if _cm is not None else {}
    def _tname(a):
        if a in starts: return starts[a]['n']
        h = [x for x in order if x['s'] < a < x['e']]
        return '%s+%d' % (h[0]['n'], a - h[0]['s']) if h else '?%d' % a
    # Prologue. The first two cells are calls - ip = base starts here -
    # and become call tokens. The remaining cells are kept at their own
    # cell positions, so the region keeps its size and the first link
    # cell stays where the layout expects it.
    for i in (0, 1):
        v = pro[START + i * CELL]
        if _cm is not None:
            _t = START + i * CELL + CELL + v
            _cm.append('C %d %d %d %d 1 (prologue) %s' % (len(img), len(callbytes(_t)), new_target_off(_t), _t, _tname(_t)))
        img += callbytes(START + i * CELL + CELL + v)
    while len(img) < PROLOGUE - 3 * CELL: img += b'\x00'
    for i in (2, 3, 4): img += cel(pro[START + i * CELL])
    assert len(img) == PROLOGUE, "prologue emitted %d, expected %d" % (len(img), PROLOGUE)

    # Builtin entries: old address -> new image offset, for the links.
    bi_new = {START + o: remap_tail_addr(START + o) for o in seen} if BL else {}

    for w in order:
        s0 = w['s']
        assert len(img) == new_off[s0]['link'], "link drift at %s" % w['n']
        if BYTEHDR: img += linkbytes(linkval[s0], LINKLEN[s0])
        else:       img += cel(linkval[s0])
        nm = w['n'].encode('latin-1')
        img += bytes([flag.get(w['nfa'], 0x80 | len(nm))]) + nm
        # pad to the body: a cell boundary in the classic layout, or only
        # as far as body_needs_align() asked for in the byte layout
        while len(img) < new_off[s0]['body']: img += b'\x00'
        assert len(img) == new_off[s0]['body'], "body drift at %s" % w['n']

        if kind[s0] == 'code':
            # Re-encode with the relocated locals-slot literals. Safe to
            # do after the layout was computed because a LITOFF is
            # always the 32-bit form, so its size does not depend on its
            # value; the assertion below is what proves that held.
            ops2 = list(info[s0])
            for (ws, j), nv in lit_new.items():
                if ws == s0: ops2[j] = ('LITOFF', nv)
            for (ws, j), nv in xt_new.items():
                if ws == s0: ops2[j] = ('XT', nv)
            if V8: img += bytes(to_tokens(ops2))
            else:
                for t_ in to_tokens(ops2): img += tk(t_)
            if _cm is not None:
                _c2t, _, _ts, _, _ = layout(ops2)
                for _j, (_k, _pl) in enumerate(ops2):
                    if _k in ('ALN', 'XT', 'OPD', 'STR', 'EQIT', 'EQITS'): continue    # data, not operations
                    _at = new_off[s0]['body'] + _ts[_j]
                    if _k == 'C':      # tag 2: 01, 10, 11 in the top bits - 2, 3, 4 bytes (Iteration 88)
                        _cm.append('C %d %d %d %d %d %s %s' % (_at, (img[_at] >> 6) + 1 if TAG2_ON else 1 if _pl in G['HOTCALLS'] else 3 if img[_at] >= 0xC0 else 2,
                                   new_target_off(_pl), _pl, 1 if G['before_operand'](ops2, _j) else 0, w['n'], _tname(_pl)))
                    else:              # Iteration 88: and the operation's name, design-independent (sod16 t2_names)
                        _cm.append('O %d %s %d %s' % (_at, _k, img[_at], _NM.get(G['opcode_L'](ops2, _j), _k)))
                for _c in sorted(G['branch_targets'](ops2)[1]):      # Iteration 88: where branches land
                    if _c in _c2t: _cm.append('T %d' % (new_off[s0]['body'] + _c2t[_c]))
            if not BYTEHDR:
                while len(img) % CELL: img += b'\x00'
            # Unheadered tail, with its builtin entries relocated.
            # Derived from tail_bytes, not from code_end directly, so a
            # PRIMITIVE stub - which code_end does not apply to - cannot
            # grow a spurious tail here while the layout says it has none.
            a = w['e'] - tail_bytes(w)
            while a < w['e']:
                v = cells.get(a, 0)
                if a in bi_new:                      # [link][xt][len][name]
                    lk = cells.get(a, 0)
                    img += cel(bi_new.get(START + lk, 0) if lk else 0)
                    img += cel(remap_body_off(cells.get(a + CELL, 0)) or 0)
                    img += cel(cells.get(a + 2 * CELL, 0))
                    a += 3 * CELL
                    continue
                img += cel(v); a += CELL
        else:
            n = info[s0]
            if n is None:                            # opaque, copied whole
                a = s0
                while a < w['e']: img += cel(cells.get(a, 0)); a += CELL
            else:
                if DATAPRIMS and n in DOVAR:
                    # [DOVAR][pad][PFA]: the primitive pushes ALIGNED(ip)
                    img += (bytes([T2MAP['one'][G['V8_DOVAR']]]) + b'\x00' * (CELL - 1)) if TAG2_ON \
                        else (bytes([69]) + b'\x00' * (CELL - 1)) if V8 else (tk(DOVARP) + b'\x00' * (CELL - 2))
                elif DATAPRIMS:
                    # [DODOES][tail][pad][PFA]: pushes ALIGNED(ip) as the
                    # return address the tail's R> expects, jumps to tail
                    # tag 2: always the 4-byte call - DODOES finds the parameter
                    # field at align(body + 5), as CREATE reserves (FORMAT-TAG2.md)
                    img += (bytes([T2MAP['one'][G['V8_DODOES']]]) + G['t2call'](v8val(n), 4) + b'\x00' * (CELL - 5)) if TAG2_ON \
                        else (bytes([70]) + callbytes(n) + b'\x00' * (CELL - 3)) if V8 else (tk(DODOES) + tk(calltok_addr(n)) + b'\x00' * (CELL - 4))
                else:
                    img += b'\x00' * (CELL - 2)     # pad BEFORE the token
                    img += tk(calltok_addr(n))
                vals = [cells.get(s0 + k * CELL, 0)
                        for k in range(1, (w['e'] - s0) // CELL)]
                if s0 in defers: vals[0] = defers[s0]
                elif n == BUF_TAIL:
                    vals[0] = 0                      # ptr, as RESET-BUFFERS
                    if len(vals) > 2 and vals[2]:
                        vals[2] = remap_pfa_off(vals[2])
                elif w['n'] in fixed: vals[0] = fixed[w['n']]
                elif w['n'] in SCRUB: vals = [0] * len(vals)
                for v in vals: img += cel(v)
        if _cm is not None:    # Iteration 88: every word's body - start, end, code or data, name
            _cm.append('W %d %d %s %s' % (new_off[s0]['body'], new_off[s0]['body'] + new_body_bytes(w), kind[s0], w['n']))
        assert len(img) == new_off[s0]['body'] + new_body_bytes(w), \
            "body size drift at %s" % w['n']

    assert len(img) == NEW_HERE, "image %d, layout said %d" % (len(img), NEW_HERE)
    # The compiler's own tables (forth/cv8-fuse.4), when this dump has
    # them: its fold list and, with --rtfuse, the superinstruction pairs,
    # so that code compiled at RUN time uses the opcodes this image's
    # engine gives them. FOLD-TABLE always gets this design's folds.
    # cv8.4's own FOLD-OPS gets this design's folds too, in fold-opcode
    # order, padded with 255 (no opcode): its compiler scans all 23, and
    # the default list writes back exactly the bytes it already had.
    # --set-compiler-vars: the compiler's call shift and DOES> form, which
    # cv8.4 and cv8b.4 set as a PAIR - shift 3, near DOES> calls, 2 bytes
    # reserved; or shift 0, far calls, 3 bytes - but which a design chooses
    # independently: scale is --cpt, the DOES> form --does-far. Without
    # this, code compiled at run time encodes calls the engine misreads.
    CVARS = {}
    if '--set-compiler-vars' in ARGV:
        far = '--does-far' in ARGV
        CVARS = {'CV8-SHIFT-V': CPT or 0, 'CV8-DOES-FAR?': -1 if far else 0, 'CV8-DOES-RESERVE': 3 if far else 2}
        if TAG2_ON: CVARS = {'CV8-SHIFT-V': 0, 'CV8-DOES-FAR?': -1, 'CV8-DOES-RESERVE': 4}   # the 4-byte call
    for w in order:
        if not V8 or w['n'] not in ('FOLD-OPS', 'FOLD-TABLE', 'SUPER-TABLE', 'IMM-OPS', 'LOOP-OPS', 'X10-XTS', 'X10-OPS', 'LOOPTAB') + tuple(CVARS): continue
        at, op = new_off[w['s']]['body'] + CELL, G['cv8_op']   # [DOVAR][pad], then the data
        if w['n'] in CVARS:
            data = (CVARS[w['n']] & ((1 << (8 * CELL)) - 1)).to_bytes(CELL, 'little')
        elif w['n'] == 'FOLD-OPS':
            ops = [op(x)[0] for x in G['V8_FOLDLIST'] if x]
            assert len(ops) <= 23, "more folds than FOLD-OPS holds"
            data = bytes(ops + [255] * (23 - len(ops)))
        elif w['n'] == 'LOOPTAB':
            # Iteration 43: the compact run-time loop compiler
            # (forth/cv8-fuse-loopall.4) - the eight loop opcodes, I's image
            # offset in 16 bits, J's and UNLOOP's distance past it in a byte
            # each. Only for a design with all eight: there is no fallback.
            _lw = ['(DO)', '(LOOP)', '(+LOOP)', '(?DO)', '(LEAVE)', 'I', 'J', 'UNLOOP']
            assert all(n in G['X_OPS10'] for n in _lw), 'LOOPTAB: rtloopall needs all eight loop opcodes'
            _byn = {x['n']: x for x in order}
            _o = [new_off[_byn[n]['s']]['body'] for n in ('I', 'J', 'UNLOOP')]
            assert _o[0] < 65536 and 0 < _o[1] - _o[0] < 256 and 0 < _o[2] - _o[0] < 256, 'LOOPTAB: I J UNLOOP not neighbours %r' % _o
            data = bytes([G['X_OPS10'][n] for n in _lw] + [_o[0] & 255, _o[0] >> 8, _o[1] - _o[0], _o[2] - _o[0]])
        elif w['n'] in ('LOOP-OPS', 'X10-XTS', 'X10-OPS'):
            # Iteration 41: the loop opcodes for code compiled at run time
            # (forth/cv8-fuse-loop.4) - each the design has, 0 for the rest -
            # and I J UNLOOP with their image offsets, the lowest and highest
            # first. SOD16_NO_RTLOOP=1 writes zeros, to measure.
            _lw = ['(DO)', '(LOOP)', '(+LOOP)', '(?DO)', '(LEAVE)']
            _ok = not _os.environ.get('SOD16_NO_RTLOOP')
            _byn = {x['n']: x for x in order}
            _x = [(new_off[_byn[n]['s']]['body'], G['X_OPS10'][n]) for n in ('I', 'J', 'UNLOOP')
                  if _ok and n in G['X_OPS10'] and n in _byn]
            if w['n'] == 'LOOP-OPS': data = bytes([G['X_OPS10'].get(n, 0) if _ok else 0 for n in _lw])
            elif w['n'] == 'X10-XTS':
                _o = [o for o, _ in _x]
                data = b''.join(cel(v) for v in ([min(_o), max(_o)] + _o + [0] * (3 - len(_o)) if _o else [0] * 5))
            else: data = bytes([op for _, op in _x] + [0] * (3 - len(_x)))
        elif w['n'] == 'IMM-OPS':
            # Iteration 37: ADDI and SWAP+I for code compiled at run time
            # (forth/cv8-fuse.4, IMM+) - with --rtfuse, where this design has
            # them; zeros otherwise. SOD16_NO_RTIMM=1 writes zeros, to measure.
            rt = '--rtfuse' in ARGV and not _os.environ.get('SOD16_NO_RTIMM') and 'imm' in G['SPEC']
            data = bytes([G['X_IMM']['ADDI'] if rt else 0, G['X_OPS10'].get('SWAP+I', 0) if rt else 0,
                          op('+')[0], op('SWAP')[0]])     # the overlay compares against these
        elif w['n'] == 'FOLD-TABLE':
            ops = [op(x)[0] for x in G['V8_FOLDLIST'] if x]
            data = bytes([len(ops)] + ops); assert len(data) <= 24, "fold table overflows"
        else:
            pairs = sorted(G['SUPERS'].items(), key=lambda kv: kv[1]) if '--rtfuse' in ARGV else []
            # A test then ?BRANCH, fused as the compiler compiles IF, UNTIL and
            # WHILE (forth/cv8-fuse.4, ?BRANCH,; Iteration 9) - first in the
            # table: code compiled at run time has no other way to them. A
            # test the compiler does not emit as one opcode is left out.
            tests = []
            if '--rtfuse' in ARGV and not _os.environ.get('SOD16_NO_TESTBR'):
                for t, v in G['TESTBR'].items():
                    if v[2] not in G['X_OPS10']: continue
                    try: tests.append((op(t)[0], op('?BRANCH')[0], G['X_OPS10'][v[2]]))
                    except Exception: pass
            # Iteration 60: I then + as I+ (forth/cv8-fuse-iplus.4 points LAST-OP
            # at I's byte; the fuser finds this entry) - first, never cut.
            if '--rtfuse' in ARGV and 'I+' in G['X_OPS10'] and 'I' in G['X_OPS10']:
                tests = [(G['X_OPS10']['I'], op('+')[0], G['X_OPS10']['I+'])] + tests
            pairs = pairs[:24 - len(tests)]      # the table's room (forth/cv8-fuse.4); the rest fused in the image only
            data = bytes([len(tests) + len(pairs)] + [x for e in tests for x in e]
                         + [x for (a, b), f in pairs for x in (op(a)[0], op(b)[0], f)])
            assert len(data) <= 73, "superinstruction table overflows"
        if TAG2_ON and w['n'] in ('FOLD-OPS', 'FOLD-TABLE', 'SUPER-TABLE', 'IMM-OPS', 'LOOP-OPS', 'X10-OPS', 'LOOPTAB'):
            # tag 2: the tables in this design's one-byte codes. An escaped
            # operation cannot sit in a byte: its entry goes (0 means none, as
            # the overlays read it). Folds at run time go entirely - their
            # opcode was the fold base plus a position, which ranking undoes.
            _c = lambda x: T2MAP['one'].get(x, 0) if x else 0
            if w['n'] == 'FOLD-OPS': data = bytes([255] * 23)
            elif w['n'] == 'FOLD-TABLE': data = bytes([0])
            elif w['n'] == 'SUPER-TABLE':
                _t = [tuple(data[1 + 3 * i:4 + 3 * i]) for i in range(data[0])]
                _t = [tuple(T2MAP['one'][x] for x in e) for e in _t if all(x in T2MAP['one'] for x in e)]
                data = bytes([len(_t)] + [x for e in _t for x in e])
            elif w['n'] == 'LOOPTAB':
                assert all(x in T2MAP['one'] for x in data[:8]), 'tag 2: LOOPTAB opcodes not pinned'
                data = bytes([T2MAP['one'][x] for x in data[:8]]) + data[8:]
            else: data = bytes(_c(x) for x in data)
        img[at:at + len(data)] = data

    _flags = ((1 if G['VARCALL'] else 0) | (2 if G['VARSLOT'] else 0)
              | (4 if G['SPEC'] else 0) | 8 | (16 if BYTEHDR else 0) | (32 if HOT else 0)
              | (64 if TAG2_ON else 0)) if V8 else 0
    hdr = (b'SOD1' if CPT is None else (b'CV8' if V8 else b'CPT') + bytes([48 + CPT]))
    hdr += bytes([CELL, ord('L') if G['SPEC'] else 0, 1 if V8 else 0, _flags])
    # The engine cannot derive the word table from one chain any more,
    # so the header carries every thread head: a count, then that many
    # START-relative offsets. SOD16 needs them to number its calls; the
    # other encodings name a call by address and ignore this entirely.
    # Iteration 58: --thin-header. Only SOD16 reads the heads (the loader
    # returns before its word table for every other encoding); the loader
    # wants a count of at least 1, so a CV8 image can carry one, zero: 16
    # bytes where 32 heads took 264.
    if V8 and '--thin-header' in ARGV:
        hdr += cel(1) + cel(0)
    else:
        hdr += cel(NTHREADS)
        for h in HEADS:
            hdr += cel(h)
    hdr += cel(len(TAILS))
    for t in TAILS:
        h = [x for x in order if x['s'] < t < x['e']][0]
        c2t_, _, _, _, _ = layout(info[h['s']])
        hdr += cel(num[h['s']]) + cel(c2t_[t - h['s']])
    # SPEC images always carry the 5-cell locals header, so the format
    # does not depend on what was loaded. A bare kernel has no save
    # stack: the header is zeroed, and no LOC opcode is ever emitted
    # (there are no calls to a locals runtime to rewrite).
    if G['SPEC'] and not [w for w in order if w['n'] == 'LSAVE-MAX']:
        hdr += cel(0) * 5
    if G['SPEC'] and [w for w in order if w['n'] == 'LSAVE-MAX']:
        # CV8 locals opcodes: where the save stack lives, its limit, and the
        # Forth words to fall back to. Offsets from base, one cell each.
        def body_of(n): return new_off[[w for w in order if w['n'] == n][-1]['s']]['body']
        lmax = [w for w in order if w['n'] == 'LSAVE-MAX'][-1]
        lmax_v = [pl for k, pl in info[lmax['s']] if k in ('LIT', 'LITX')][0]
        hdr += cel(body_of('LSAVE-SP') + CELL) + cel(body_of('LSAVE-STACK') + CELL)
        hdr += cel(lmax_v) + cel(body_of('LSAVE')) + cel(body_of('LRESTORE'))
    if HOT:            # last in the header: one-byte calls' targets, as image offsets
        assert G['VARCALL'], "one-byte calls take far-call prefixes: they need --varcall"
        _o = [new_target_off(a) for a in HOT]
        assert all(0 <= x < 1 << 16 for x in _o), "a one-byte call's target beyond 64 KB"
        hdr += bytes([len(_o)]) + b''.join(x.to_bytes(2, 'little') for x in _o)
    open(path, 'wb').write(hdr + bytes(img))
    if _cm is not None:
        with open(_os.environ['CALLMAP'], 'w') as _f:
            _f.write('H %d %d %d\n' % (len(hdr), len(img), CPT or 0))
            if TAG2_ON:          # Iteration 88: the tag's codes - one byte, or the escape and a selector
                _f.write('M E %d\n' % T2MAP['escc'])
                _f.write(''.join('M 1 %d %s\n' % (c, _NM[x]) for x, c in sorted(T2MAP['one'].items(), key=lambda kv: kv[1])))
                _f.write(''.join('M 2 %d %s\n' % (c, _NM[x]) for x, c in sorted(T2MAP['esc'].items(), key=lambda kv: kv[1])))
            _f.write(''.join(x + '\n' for x in _cm))
    return len(hdr), len(img)

# ---- literals that hold offsets -------------------------------------
# locals.4's L-EMIT: "Two cells: the offset as a literal, then a
# relative call to the runtime word, which does the + START itself."
#
# So a locals-using word's body carries LIT <offset from START to a
# slot word's body>. That is position-INDEPENDENT, which is why it
# survives a save, and it is not layout-INDEPENDENT, which is why SOD16
# has to move it: the bodies are all somewhere else now.
#
# The four runtime words are found through the variables that hold
# their xts, not by name, so renaming them cannot silently break this.
# The signature is positional, like every other operand in this file:
# a LIT is an offset only when a call to one of those four follows it.
LOCALS_RT = set()
for _n in ('L-LSAVE-XT', 'L-L!-XT', 'L-LZERO-XT', 'L-LRESTORE-XT'):
    _p = pfa_of(_n)
    if _p:
        _v = cells.get(_p)
        if _v: LOCALS_RT.add(START + _v)

lit_ok, lit_bad, lit_new = 0, [], {}
for w in order:
    if kind[w['s']] != 'code': continue
    ops = info[w['s']]
    for j in range(len(ops) - 1):
        if ops[j][0] not in ('LIT', 'LITOFF'): continue
        if ops[j + 1][0] != 'C': continue
        if ops[j + 1][1] not in LOCALS_RT: continue
        v = ops[j][1]
        n2 = remap_pfa_off(v)
        if n2 is None: n2 = remap_body_off(v)
        if n2 is None: lit_bad.append((w['n'], v))
        else: lit_ok += 1; lit_new[(w['s'], j)] = n2
for _s, _o in BSS_OFF.items(): lit_new[(_s, 0)] = _o        # Iteration 44: each buffer word's LITOFF

# ---- report ---------------------------------------------------------
c = collections.Counter(kind.values())
codeb = sum(w['e'] - w['s'] for w in order if kind[w['s']] == 'code')
datab = sum(w['e'] - w['s'] for w in order if kind[w['s']] == 'data')
newcode = sum(new_body_bytes(w) for w in order if kind[w['s']] == 'code')
tails_kept = [(w['n'], tail_bytes(w)) for w in order if tail_bytes(w)]
newdata = sum(new_body_bytes(w) for w in order if kind[w['s']] == 'data')
heads = sum(CELL + align_up(len(w['n']) + 1, CELL) for w in order)
heads_new = (sum(LINKLEN[w['s']] + len(w['n']) + 1 for w in order)
             if BYTEHDR else heads)

EMIT = None
for i, a in enumerate(ARGV):
    if a == '--emit-image': EMIT = ARGV[i + 1]

print("dump %s   cell %d" % (DUMP, CELL))
print("structure: %d words, prologue %d B, %d header-adjacency gaps"
      % (len(order), PROLOGUE, gaps))
print("DOES> tails: %d distinct, %d words behind them"
      % (len(TAILS), sum(tails.values())))
for t in TAILS:
    h = [w for w in order if w['s'] < t < w['e']][0]
    print("   word number %d = %s +%d   (%d words)"
          % (tailnum[t], h['n'], t - h['s'], tails[t]))
print()
print("%-22s %12s %12s %8s" % ("", "cell image", "token image", "ratio"))
print("%-22s %12d %12d %8.3f" % ("code bodies", codeb, newcode, newcode/codeb))
print("%-22s %12d %12d %8.3f" % ("data bodies", datab, newdata, newdata/datab))
print("%-22s %12d %12d %8.3f" % ("headers + names", heads, heads_new,
                                     heads_new / heads))
print("%-22s %12d %12d %8.3f"
      % ("whole image", OLD_HERE, NEW_HERE, NEW_HERE/OLD_HERE))
print()
untranslated = [w for w in order
                if kind[w['s']] == 'data' and info[w['s']] is None
                and cells.get(w['s']) is not None]
print("code words %d, data words %d" % (c['code'], c['data']))
print("UNTRANSLATED code bodies: %d  (copied verbatim would be wrong)"
      % len(untranslated))
print("unheadered tails carried after code: %s" % (tails_kept or "none"))
if tails_kept:
    print("BUILTIN table: %d entries relocated, %d unresolved %s"
          % (builtins, len(bi_bad), bi_bad[:3] if bi_bad else ""))
for w in untranslated:
    print("   %s" % w['n'])
print("link chain re-walks to the same %d words in the same order: %s"
      % (len(order), "yes" if chain_ok else "NO"))
print("(POSTPONE) operands relocated: %d resolved, %d unresolved %s"
      % (xt_ok, len(xt_bad), xt_bad[:3] if xt_bad else ""))
print("DEFER xts relocated: %d resolved, %d unresolved %s"
      % (len(defers), len(defer_bad), defer_bad if defer_bad else ""))
print("BUFFER: fields: %d words, ptr zeroed, %d links unremappable %s"
      % (bufs, len(buf_bad), buf_bad[:3] if buf_bad else ""))
print("locals slot literals relocated: %d resolved, %d unresolved %s"
      % (lit_ok, len(lit_bad), lit_bad[:3] if lit_bad else ""))
print("named offset cells: %d set, %d unresolved %s"
      % (len(fixed), len(fixed_bad), fixed_bad if fixed_bad else ""))
for k in sorted(fixed): print("   %-16s -> %d" % (k, fixed[k]))
for i, a in enumerate(ARGV):
    if a == '--symbols':
        with open(ARGV[i + 1], 'w') as f:
            for w in order:
                f.write("%d %d %s %s\n" % (new_off[w['s']]['body'],
                        new_body_bytes(w), kind[w['s']], w['n']))
if EMIT:
    h, b = emit(EMIT)
    print("wrote %s: %d B header + %d B image" % (EMIT, h, b))
    if TAG2_ON:
        # the engine's map (vm-lab.c TAG2): each code's logical operation
        _one = ['T2_NONE'] * 64; _one[0x3F] = 'T2_ESC'
        for _x, _c in T2MAP['one'].items(): _one[_c] = str(_x)
        _esc = ['T2_NONE'] * 256
        for _x, _s in T2MAP['esc'].items(): _esc[_s] = str(_x)
        _d = _os.path.dirname(_os.path.abspath(EMIT))
        open(_os.path.join(_d, 'vm-tag2-one.h'), 'w').write(', '.join(_one) + '\n')
        open(_os.path.join(_d, 'vm-tag2-esc.h'), 'w').write(', '.join(_esc) + '\n')
        print("wrote the tag-2 map: vm-tag2-one.h, vm-tag2-esc.h")
        if '--jit' in ARGV:
            # Iteration 80 (JIT.md): each logical operation as SPN stencils,
            # for engine/jit.c - the stencils, the operand's kind (0 none,
            # 1 u8, 2 u16, 3 s32, 4 s64, 5 s8, 6 an 8-bit branch, 7 a
            # 16-bit one) and a constant for the literal holes the operand
            # does not fill. What is not here stays bytecode.
            S1 = {'DUP': ['DUP'], 'DROP': ['DROP'], 'SWAP': ['SWAP'], 'OVER': ['OVER'], 'ROT': ['ROT'],
                  '+': ['PLUS'], '-': ['NEGATE', 'PLUS'], 'AND': ['AND'], 'OR': ['OR'], 'XOR': ['XOR'],
                  'NEGATE': ['NEGATE'], '=': ['EQ'], '<': ['LT'], '>': ['GT'], 'U<': ['ULT'],
                  'LSHIFT': ['LSHIFT'], 'RSHIFT': ['RSHIFT'], '@': ['FETCH'], '!': ['STORE'],
                  'C@': ['CFETCH'], 'C!': ['CSTORE'], 'I': ['I'], 'J': ['J'], 'UNLOOP': ['UNLOOP'],
                  'I+': ['I', 'PLUS'], '(DO)': ['DO'], 'EXIT': ['EXIT'], '2DUP': ['OVER', 'OVER'],
                  '2DROP': ['DROP', 'DROP'], 'NOOP': []}
            K = {'lit0': (['LIT'], 0), 'lit1': (['LIT'], 1), 'litm1': (['LIT'], -1), '0=': (['LIT', 'EQ'], 0),
                 '0<': (['LIT', 'LT'], 0), 'INVERT': (['LIT', 'XOR'], -1), '<>': (['EQ', 'LIT', 'XOR'], -1),
                 '1+': (['ADDI'], 1), '1-': (['ADDI'], -1), 'CELL+': (['ADDI'], 8), 'CHAR+': (['ADDI'], 1),
                 'CELLS': (['LIT', 'LSHIFT'], 3)}
            O = {'LIT8': (['LIT'], 1), 'LIT': (['LIT'], 2), 'LIT32': (['LIT'], 3), 'LIT64': (['LIT'], 4),
                 'ADDI': (['ADDI'], 5), 'EQI': (['LIT', 'EQ'], 5), 'SWAP+I': (['SWAP', 'ADDI'], 5),
                 'BRANCH': (['BRANCH'], 7), 'BRANCH8': (['BRANCH'], 6), '?BRANCH': (['0BRANCH'], 7),
                 '?BRANCH8': (['0BRANCH'], 6), '(LOOP)': (['LOOP'], 7), '(LEAVE)': (['LEAVE'], 7),
                 '<?BRANCH': (['LT', '0BRANCH'], 7), '<?BRANCH8': (['LT', '0BRANCH'], 6),
                 '=?BRANCH': (['EQ', '0BRANCH'], 7), '=?BRANCH8': (['EQ', '0BRANCH'], 6),
                 'U<?BRANCH': (['ULT', '0BRANCH'], 7), 'U<?BRANCH8': (['ULT', '0BRANCH'], 6),
                 '>?BRANCH': (['GT', '0BRANCH'], 7), '>?BRANCH8': (['GT', '0BRANCH'], 6),
                 '?NBRANCH': (['LIT', 'EQ', '0BRANCH'], 7), '?NBRANCH8': (['LIT', 'EQ', '0BRANCH'], 6),
                 '<>?BRANCH': (['EQ', 'LIT', 'EQ', '0BRANCH'], 7), '<>?BRANCH8': (['EQ', 'LIT', 'EQ', '0BRANCH'], 6)}
            def _jd(nm):
                if nm in ('LIT8X', 'ADDIX', 'EQIX') or nm.endswith(';EXIT'):
                    d = _jd(nm[:-1] if nm in ('LIT8X', 'ADDIX', 'EQIX') else nm[:-5])
                    return d and (d[0] + ['EXIT'], d[1], d[2])
                if nm in S1: return (S1[nm], 0, 0)
                if nm in K: return (K[nm][0], 0, K[nm][1])
                if nm in O: return (O[nm][0], O[nm][1], 0)
                if ' ' in nm:      # a pair: both parts without operands, at most one constant
                    a_, b_ = nm.split(' ', 1); da, db = _jd(a_), _jd(b_)
                    if da and db and not da[1] and not db[1] and not (da[2] and db[2]):
                        return (da[0] + db[0], 0, da[2] or db[2])
                return None
            _jl, _rows = 0, []
            for _x, _nm in sorted(G['t2_names']().items()):
                _dj = _jd(_nm)        # (not _d: that is the directory the headers go to)
                if _dj and len(_dj[0]) <= 5:
                    _rows.append('[%d] = {1, %d, %d, %d, {%s}},  /* %s */' % (_x, len(_dj[0]), _dj[1], _dj[2],
                                 ', '.join('S_' + s for s in _dj[0]) or '0', _nm.replace('*/', '* /')))
            _jc = T2MAP['one'][G['T2_JIT']]
            open(_os.path.join(_d, 'vm-jit-ops.h'), 'w').write(
                '/* vm-jit-ops.h - this design\'s operations as SPN stencils (layout.py --jit, JIT.md) */\n'
                '#define JIT_CODE %d\nstatic const struct jit_op jit_ops[] = {\n%s\n};\n' % (_jc, '\n'.join(_rows)))
            print("wrote vm-jit-ops.h: %d of %d operations translatable; JIT is code %d" % (len(_rows), len(G['t2_names']()), _jc))

sys.exit(0 if chain_ok and gaps == 0 and not defer_bad and not xt_bad
         and not buf_bad and not untranslated and not bi_bad and not fixed_bad
         and not lit_bad else 1)
