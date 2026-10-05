#!/usr/bin/env python3
"""gen-msc.py ENGINE.c - multi-state stack caching (Ertl and Gregg; gforth).

ENGINE.c is the CV8 top-of-stack engine (vm-lab-tos.c, after gen-fold /
gen-super), built with -DDISPATCH256=1; it is rewritten in place. There
the top item is always in a register: state 1. Here there are three
states - nothing, the top, or the top two (`tos`, `nos`) in registers -
and a dispatch table for each. A handler variant knows the state it ends
in, so it dispatches through that state's table: the state needs no
variable.

The hot primitives are generated from stack effects (SPECS): for each
input state, where each input lives, what goes to memory, and an end
state keeping as much in registers as fits - as gforth's vmgen does. DUP
in state 1 ends in state 2 without touching memory; + in state 2 ends in
state 1 without a load.

Every other handler keeps its state-1 body: states 0 and 2 reach it
through one normaliser each, which fills or spills one item and jumps on
the opcode still in t. NOOP, EXIT, BRANCH and the call path touch no data
stack and get a copy per state, so calls and returns keep the cache.

The extra tables are filled at start-up by comparing label addresses with
the state-1 table, so they follow any opcode assignment - folds, the
escape's remap, superinstructions.
"""
import re, sys

# label: (inputs, outputs, C) - bottom to top; the semantics of the
# engine's own handlers (engine/vm-lab.c), letter for letter.
SPECS = {
    'L_dup':     (['a'], ['a', 'a'], ''),
    'L_drop':    (['a'], [], ''),
    'L_swap':    (['a', 'b'], ['b', 'a'], ''),
    'L_over':    (['a', 'b'], ['a', 'b', 'a'], ''),
    'L_rot':     (['a', 'b', 'c'], ['b', 'c', 'a'], ''),
    'L_plus':    (['a', 'b'], ['c'], 'c = a + b;'),
    'L_eq':      (['a', 'b'], ['c'], 'c = -(UNS64)(b == a);'),
    'L_gt':      (['a', 'b'], ['c'], 'c = -(UNS64)((INT64)a < (INT64)b);'),     # <
    'L_ugt':     (['a', 'b'], ['c'], 'c = -(UNS64)(a < b);'),                   # U<
    'L_and':     (['a', 'b'], ['c'], 'c = a & b;'),
    'L_or':      (['a', 'b'], ['c'], 'c = a | b;'),
    'L_xor':     (['a', 'b'], ['c'], 'c = a ^ b;'),
    'L_negate':  (['a'], ['b'], 'b = -a;'),
    'L_lshift':  (['a', 'b'], ['c'], 'c = a << b;'),
    'L_rshift':  (['a', 'b'], ['c'], 'c = a >> b;'),
    'L_fetch':   (['a'], ['x'], 'x = CELL(a);'),
    'L_store':   (['x', 'a'], [], 'CELL(a) = x;'),
    'L_cfetch':  (['a'], ['x'], 'x = BYTE(a);'),
    'L_cstore':  (['x', 'a'], [], 'BYTE(a) = (UNS8)x;'),
    'L_tor':     (['a'], [], 'RPUSH(a);'),
    'L_fromr':   ([], ['a'], 'a = RS; rp += CELL_BYTES;'),
    'L_rfetch':  ([], ['a'], 'a = RS;'),
    'L_lit':     ([], ['n'], 'n = (UNS64)OPND16(ip); ip += 2;'),
    'L_lit8':    ([], ['n'], 'n = (UNS64)BYTE(ip); ip += 1;'),
    'L_0branch': (['f'], [], 'if (f) ip += 2; else ip += BROFF(ip);'),
    # the specialisations (SPEC): tiny words, small literals, immediates, variables
    'L_zeq':     (['a'], ['f'], 'f = -(UNS64)(a == 0);'),
    'L_sub':     (['a', 'b'], ['c'], 'c = a - b;'),
    'L_ne':      (['a', 'b'], ['c'], 'c = -(UNS64)(a != b);'),
    'L_zlt':     (['a'], ['f'], 'f = -(UNS64)((INT64)a < 0);'),
    'L_sgt':     (['a', 'b'], ['c'], 'c = -(UNS64)((INT64)b < (INT64)a);'),      # >
    'L_2dup':    (['a', 'b'], ['a', 'b', 'a', 'b'], ''),
    'L_2drop':   (['a', 'b'], [], ''),
    'L_charp':   (['a'], ['b'], 'b = a + 1;'),
    'L_onep':    (['a'], ['b'], 'b = a + 1;'),
    'L_cellp':   (['a'], ['b'], 'b = a + CELL_BYTES;'),
    'L_cells':   (['a'], ['b'], 'b = a << CELL_SHIFT;'),
    'L_onem':    (['a'], ['b'], 'b = a - 1;'),
    'L_invert':  (['a'], ['b'], 'b = ~a;'),
    'L_count':   (['a'], ['b', 'c'], 'b = a + 1; c = BYTE(a);'),
    'L_aligned': (['a'], ['b'], 'b = (a + CELL_BYTES - 1) & ~(UNS64)(CELL_BYTES - 1);'),
    'L_lit0':    ([], ['n'], 'n = 0;'),
    'L_lit1':    ([], ['n'], 'n = 1;'),
    'L_litm1':   ([], ['n'], 'n = ~(UNS64)0;'),
    'L_vf':      ([], ['x'], 'x = CELL(SLOT());'),
    'L_vs':      (['x'], [], 'CELL(SLOT()) = x;'),
    'L_addi':    (['a'], ['b'], 'b = a + (UNS64)(INT64)(int8_t)BYTE(ip); ip += 1;'),
    'L_eqi':     (['a'], ['b'], 'b = -(UNS64)(a == (UNS64)(INT64)(int8_t)BYTE(ip)); ip += 1;'),
    'L_addix':   (['a'], ['b'], 'b = a + (UNS64)(INT64)(int8_t)BYTE(ip); ip = RS; rp += CELL_BYTES;'),
    'L_eqix':    (['a'], ['b'], 'b = -(UNS64)(a == (UNS64)(INT64)(int8_t)BYTE(ip)); ip = RS; rp += CELL_BYTES;'),
    # relf's format-10 opcodes (OPS10) - ?DUP alone cannot be said this way
    'L_x_i':         ([], ['x'], 'x = RS;'),
    'L_x_j':         ([], ['x'], 'x = CELL(rp + 2 * CELL_BYTES);'),
    'L_x_plusstore': (['x', 'a'], [], 'CELL(a) += x;'),
    'L_x_do':        (['a', 'b'], [], 'RPUSH(a); RPUSH(b);'),
    'L_x_execute':   (['x'], [], 'RPUSH(ip); ip = x;'),
    'L_x_unloop':    ([], [], 'rp += 2 * CELL_BYTES;'),
    'L_x_leave':     ([], [], 'rp += 2 * CELL_BYTES; ip += (int16_t)LD16(ip);'),
    'L_x_loop':      ([], [], '{ UNS64 i_ = RS + 1; if (i_ == CELL(rp + CELL_BYTES)) { rp += 2 * CELL_BYTES; ip += 2; } '
                              'else { CELL(rp) = i_; ip += (int16_t)LD16(ip); } }'),
    'L_x_qdo':       (['a', 'b'], [], 'if (a != b) { RPUSH(a); RPUSH(b); ip += 2; } else ip += (int16_t)LD16(ip);'),
    'L_x_ploop':     (['n'], [], '{ UNS64 i_ = RS, l_ = CELL(rp + CELL_BYTES), j_ = i_ + n; '
                                 'if ((INT64)((i_ - l_) ^ (j_ - l_)) < 0) { rp += 2 * CELL_BYTES; ip += 2; } '
                                 'else { CELL(rp) = j_; ip += (int16_t)LD16(ip); } }'),
    'L_x_br8':       ([], [], 'ip += (int8_t)BYTE(ip);'),
    'L_x_qbr8':      (['f'], [], 'if (f) ip += 1; else ip += (int8_t)BYTE(ip);'),
    'L_x_nqbr':      (['f'], [], 'if (f) ip += (int16_t)LD16(ip); else ip += 2;'),
    'L_x_nqbr8':     (['f'], [], 'if (f) ip += (int8_t)BYTE(ip); else ip += 1;'),
    'L_x_ltbr':      (['a', 'b'], [], 'if ((INT64)a < (INT64)b) ip += 2; else ip += (int16_t)LD16(ip);'),
    'L_x_ltbr8':     (['a', 'b'], [], 'if ((INT64)a < (INT64)b) ip += 1; else ip += (int8_t)BYTE(ip);'),
    'L_x_eqbr':         (['a', 'b'], [], 'if (a == b) ip += 2; else ip += (int16_t)LD16(ip);'),
    'L_x_eqbr8':        (['a', 'b'], [], 'if (a == b) ip += 1; else ip += (int8_t)BYTE(ip);'),
    'L_x_ultbr':        (['a', 'b'], [], 'if (a < b) ip += 2; else ip += (int16_t)LD16(ip);'),
    'L_x_ultbr8':       (['a', 'b'], [], 'if (a < b) ip += 1; else ip += (int8_t)BYTE(ip);'),
    'L_x_nebr':         (['a', 'b'], [], 'if (a != b) ip += 2; else ip += (int16_t)LD16(ip);'),
    'L_x_nebr8':        (['a', 'b'], [], 'if (a != b) ip += 1; else ip += (int8_t)BYTE(ip);'),
    'L_x_sgtbr':        (['a', 'b'], [], 'if ((INT64)a > (INT64)b) ip += 2; else ip += (int16_t)LD16(ip);'),
    'L_x_sgtbr8':       (['a', 'b'], [], 'if ((INT64)a > (INT64)b) ip += 1; else ip += (int8_t)BYTE(ip);'),
    'L_x_zltbr':        (['a'], [], 'if ((INT64)a < 0) ip += 2; else ip += (int16_t)LD16(ip);'),
    'L_x_zltbr8':       (['a'], [], 'if ((INT64)a < 0) ip += 1; else ip += (int8_t)BYTE(ip);'),
    'L_x_eqibr':        (['a'], [], 'UNS64 i_ = (UNS64)(INT64)(int8_t)BYTE(ip); ip += 1; if (a == i_) ip += 2; else ip += (int16_t)LD16(ip);'),
    'L_x_eqibr8':       (['a'], [], 'UNS64 i_ = (UNS64)(INT64)(int8_t)BYTE(ip); ip += 1; if (a == i_) ip += 1; else ip += (int8_t)BYTE(ip);'),
    # Iteration 33: tests that keep their value - what comes in goes out
    'L_x_dupbr':        (['f'], ['f'], 'if (f) ip += 2; else ip += (int16_t)LD16(ip);'),
    'L_x_dupbr8':       (['f'], ['f'], 'if (f) ip += 1; else ip += (int8_t)BYTE(ip);'),
    'L_x_overbr':       (['a', 'b'], ['a', 'b'], 'if (a) ip += 2; else ip += (int16_t)LD16(ip);'),
    'L_x_overbr8':      (['a', 'b'], ['a', 'b'], 'if (a) ip += 1; else ip += (int8_t)BYTE(ip);'),
    # Iteration 34
    'L_x_dupnbr':       (['f'], ['f'], 'if (f) ip += (int16_t)LD16(ip); else ip += 2;'),
    'L_x_dupnbr8':      (['f'], ['f'], 'if (f) ip += (int8_t)BYTE(ip); else ip += 1;'),
    'L_x_swapaddi':     (['a', 'b'], ['b', 'c'], 'c = a + (UNS64)(INT64)(int8_t)BYTE(ip); ip += 1;'),
    # Iteration 50
    'L_x_fill':         (['a', 'u', 'c'], [], '{ UNS64 a_ = a, u_ = u; while (u_) { BYTE(a_) = (UNS8)c; a_++; u_--; } }'),
    'L_x_threadfind':   (['a', 'nb'], ['r'], '{ UNS64 a_ = a, nb_ = nb; UNS8 n_ = BYTE(nb_); while (a_) {     if ((BYTE(a_) & 31) == n_) { UNS64 k_ = 0; while (k_ < n_ && BYTE(a_ + 1 + k_) == BYTE(nb_ + 1 + k_)) k_++; if (k_ == n_) break; }     { UNS8 t_ = BYTE(a_ - 1);       if (t_ < 128) a_ = t_ ? a_ - t_ : 0;       else if (t_ < 192) a_ -= ((UNS64)(t_ & 63) << 8) | BYTE(a_ - 2);       else a_ -= ((UNS64)(t_ & 63) << 16) | ((UNS64)BYTE(a_ - 2) << 8) | BYTE(a_ - 3); } } r = a_; }'),
    'L_x_cmove':        (['s', 'd', 'u'], [], '{ UNS64 s_ = s, d_ = d, u_ = u; while (u_) { BYTE(d_) = BYTE(s_); s_++; d_++; u_--; } }'),
}
STACKFREE = ['L_noop', 'L_exit', 'L_branch', 'L_hcall']   # L_hcall: one-byte calls (Iteration 14)

def rename(code, mp):
    """Whole-word renaming of a spec's declared names - not its C."""
    if not mp or not code: return code
    pat = r'\b(%s)\b' % '|'.join(sorted(map(re.escape, mp), key=len, reverse=True))
    return re.sub(pat, lambda m: mp[m.group(1)], code)

def compose(A, B):
    """A then B as one stack effect: B takes A's outputs first, then
    deeper items; what passes between them becomes a temporary."""
    n = [0]
    def fresh(): n[0] += 1; return 'z%d' % n[0]
    stack, inputs, code = [], [], []
    for ins, outs, c, *_ in (A, B):
        mp = {x: fresh() for x in dict.fromkeys(ins + outs)}
        got = []
        for _ in ins:
            if stack: got.append(stack.pop())
            else: z = fresh(); inputs.insert(0, z); got.append(z)
        for x, z in zip(ins, reversed(got)): mp[x] = z
        code.append(rename(c, mp))
        stack += [mp[x] for x in outs]
    temps = sorted({z for c in code for z in re.findall(r'\bz\d+\b', c)} - set(inputs) - set(stack))
    return (inputs, stack, ' '.join(c for c in code if c), temps)

def variant(label, spec, s):
    ins, outs, code = spec[:3]
    temps = spec[3] if len(spec) > 3 else []
    regs = ['tos', 'nos'][:s]
    v = lambda n: 'v_' + n
    st = []
    for k in range(len(ins)):                      # k = 0 is the top
        src = regs[k] if k < s else 'CELL(dsp + %d * CELL_BYTES)' % (k - s)
        st.append('UNS64 %s = %s;' % (v(ins[len(ins) - 1 - k]), src))
    rem = []                                       # cached items below the inputs, top first
    for k in range(len(ins), s):
        st.append('UNS64 r%d_ = %s;' % (k, regs[k])); rem.append('r%d_' % k)
    st += ['UNS64 %s;' % v(o) for o in dict.fromkeys(list(outs) + list(temps)) if o not in ins]
    if code: st.append(rename(code, {x: v(x) for x in set(ins) | set(outs) | set(temps)}))
    if len(ins) > s: st.append('dsp += %d * CELL_BYTES;' % (len(ins) - s))
    items = [v(o) for o in reversed(outs)] + rem   # the new stack, top first
    so = min(2, len(items))
    for x in reversed(items[so:]): st.append('SPILLX(%s);' % x)   # deepest first
    if so >= 1: st.append('tos = %s;' % items[0])
    if so == 2: st.append('nos = %s;' % items[1])
    st.append('NEXT_S%d();' % so)
    return '%s__s%d: { %s }\n' % (label, s, ' '.join(st))

src = open(sys.argv[1]).read()
import os
labs = set(re.findall(r'^(L_\w+):', src, re.M))

def conditions(text):
    """Each label defined once -> the condition it is defined under, as one
    #if expression (absent: unconditional). Everything generated here for a
    handler - its variants, and the comparison with its address that fills
    the state tables - must exist exactly when the handler does: the
    tables compared with &&L_eqix unconditionally, so multi-state caching
    without specialisations could not compile; nor, once gen-tos.py kept
    the format-10 handlers in their own #if (Iteration 5), without them."""
    frames, where, count = [], {}, {}
    for line in text.splitlines():
        m = re.match(r'\s*#\s*(if|ifdef|ifndef|elif|else|endif)\b\s*(.*)', line)
        if m:
            k, e = m.group(1), m.group(2).split('/*')[0].split('//')[0].strip()
            if k == 'if': frames.append([[], '(%s)' % e])
            elif k == 'ifdef': frames.append([[], 'defined(%s)' % e])
            elif k == 'ifndef': frames.append([[], '!defined(%s)' % e])
            elif k == 'elif': frames[-1][0].append(frames[-1][1]); frames[-1][1] = '(%s)' % e
            elif k == 'else': frames[-1][0].append(frames[-1][1]); frames[-1][1] = None
            else: frames.pop()
            continue
        m = re.match(r'^(L_\w+):', line)
        if m:
            l = m.group(1); count[l] = count.get(l, 0) + 1
            parts = [p for prev, cur in frames for p in ['!' + x for x in prev] + ([cur] if cur else [])]
            where[l] = ' && '.join(parts)
    return {l: c for l, c in where.items() if count[l] == 1 and c}
COND = conditions(src)
def under(l, text):
    """text, compiled exactly when handler l is"""
    return '#if %s\n%s#endif\n' % (COND[l], text) if l in COND else text
specs = {l: sp for l, sp in SPECS.items() if l in labs}
# the folds (gen-fold.py: LX_name, prim then EXIT, in vm-fold-bodies.h): the
# primitive's stack effect, then the return
fb = os.path.join(os.path.dirname(os.path.abspath(sys.argv[1])), 'vm-fold-bodies.h')
if os.path.exists(fb) and '#if FOLD' in src:
    for l in re.findall(r'^(LX_\w+):', open(fb).read(), re.M):
        base = 'L' + l[2:]
        if base in specs:
            ins, outs, code = specs[base][:3]
            specs[l] = (ins, outs, (code + ' ' if code else '') + 'ip = RS; rp += CELL_BYTES;')
# the superinstructions (gen-super.py: LS_k, "/* FIRST SECOND */", in
# vm-super-bodies.h): their two halves' effects, composed
sb = os.path.join(os.path.dirname(os.path.abspath(sys.argv[1])), 'vm-super-bodies.h')
if os.path.exists(sb) and '#if SUPER' in src:
    prims = [l.split()[1] for l in open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'forth', 'kernel.4'))
             if l.startswith('PRIMITIVE')]
    tab = src[src.index('static const void *const dispatch[] = {'):]
    order = re.findall(r'&&(L_\w+)', tab[:tab.index('};')])
    for l, a, b in re.findall(r'^(LS_\d+): /\* (\S+) (\S+) \*/', open(sb).read(), re.M):
        la, lb = order[prims.index(a)], order[prims.index(b)]
        if la in SPECS and lb in SPECS: specs[l] = compose(SPECS[la], SPECS[lb])

# macros, after the cached engine's own
m = src.index('#define FILLNEXT() do { POPT(); NEXT(); } while (0)\n') + len('#define FILLNEXT() do { POPT(); NEXT(); } while (0)\n')
src = src[:m] + '''/* multi-state stack caching (tools/gen-msc.py) */
#define NEXT_S0() do { t = BYTE(ip); ip += 1; goto *dtab256_0[t]; } while (0)
#define NEXT_S1() NEXT()
#define NEXT_S2() do { t = BYTE(ip); ip += 1; goto *dtab256_2[t]; } while (0)
#if GUARD
#define SPILLX(x) do { dsp -= CELL_BYTES; CELL(dsp) = (x); } while (0)
#else
#define SPILLX(x) do { dsp -= CELL_BYTES; if (dsp < dsp_limit) stack_fault(0); CELL(dsp) = (x); } while (0)
#endif
    UNS64 nos = 0;
''' + src[m:]

# the tables for states 0 and 2, after the state-1 table is filled
fill = re.search(r'\n(\s*)dtab256\[i_\] = \(i_ < n_ && i_ < 128\) \? dispatch\[i_\] : (?:&&do_call|HCALL\(i_\));\n(\s*)\}\n', src)
assert fill, 'no 256-entry table to follow (build with DISPATCH256)'
cases = ''.join(under(l, '            if (dtab256[i_] == &&%s) { dtab256_0[i_] = &&%s__s0; dtab256[i_] = &&%s__s1; dtab256_2[i_] = &&%s__s2; }\n'
                % (l, l, l, l)) for l in specs)
cases += ''.join(under(l, '            if (dtab256[i_] == &&%s) { dtab256_0[i_] = &&%s__0; dtab256_2[i_] = &&%s__2; }\n'
                 % (l, l, l)) for l in STACKFREE if l in labs)
src = src[:fill.end()] + '''    static const void *dtab256_0[256], *dtab256_2[256];
    if (!dtab256_0[0]) {
        int i_;
        for (i_ = 0; i_ < 256; i_++) {
%s            if (i_ >= 128) { dtab256_0[i_] = &&do_call__0; dtab256_2[i_] = &&do_call__2; continue; }
            dtab256_0[i_] = &&L_norm0; dtab256_2[i_] = &&L_norm2;
%s        }
    }
''' % (('#if HOTCALLS\n            if (i_ >= 0xE0) { dtab256_0[i_] = &&L_hcall__0; dtab256_2[i_] = &&L_hcall__2; continue; }\n#endif\n'
       if 'L_hcall' in labs else ''), cases) + src[fill.end():]

# the variants, the normalisers and the per-state copies
dc = src.index('\ndo_call:\n') + 1
dce = src.index('    NEXT();\n#endif\n', dc) + len('    NEXT();\n')
call = src[dc:dce]
gen = ['/* ---- multi-state stack caching: generated by tools/gen-msc.py ---- */\n',
       'L_norm0: tos = CELL(dsp); dsp += CELL_BYTES; goto *dtab256[t];       /* 0 -> 1 */\n',
       'L_norm2: SPILLX(nos); goto *dtab256[t];                               /* 2 -> 1 */\n']
for s in (0, 2):
    gen.append(call.replace('do_call:', 'do_call__%d:' % s).replace('NEXT();', 'NEXT_S%d();' % s))
    for l in STACKFREE:
        if l not in labs: continue
        b = re.search(r'^%s:(.*?NEXT\(\);)' % l, src, re.M | re.S).group(1)   # to its own NEXT: L_branch has one per encoding
        gen.append(under(l, '%s__%d:%s\n' % (l, s, b.replace('NEXT();', 'NEXT_S%d();' % s))))
for l, sp in specs.items():
    gen.append(under(l, ''.join(variant(l, sp, s) for s in (0, 1, 2))))
# at the end of the handlers, where every macro they use is defined (SLOT)
i = src.index('#if FOLD\n#define EXITNEXT()')
src = src[:i] + ''.join(gen) + src[i:]
open(sys.argv[1], 'w').write(src)
print('%d primitives in three states, %d stack-free handlers copied' % (len(specs), len([l for l in STACKFREE if l in labs])))
