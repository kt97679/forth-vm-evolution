#!/usr/bin/env python3
"""gen-tail.py PREPROCESSED.c OUT.c [--wrap L_a,L_b,...] - tail-call
threading for the CV8 engine.

Input: the top-of-stack engine (vm-lab-tos.c, after gen-fold / gen-super),
preprocessed for one design with -DDISPATCH256=1 (cc -E -P), so every
#if and macro is resolved and every dispatch is the same statement,
`t = BYTE(ip); ip += 1; goto *dtab256[t];`.

Output: the same engine with each handler a function of the machine
state, (ip, dsp, rp, tos, t), all five in argument registers, ending in a
TAIL call through a 256-entry table of functions - opcodes below 0x80,
the call path above. The handler bodies are unchanged: only their jumps
are rewritten. Every handler is small, so the compiler allocates its
registers for it alone, where in the one big function it allocates for
all of them at once (CPython 3.14, Wasm3, WasmKit).

Without musttail (GCC before 15) the tail calls are -O2's sibling calls;
the kernel workload, millions of dispatches, overflows the C stack at
once if one is missed, so the strict check catches it.

--wrap: handlers whose body passes a local's address to the system
(fstat's struct, pipe's two descriptors) keep their frame, so the compiler
will not make their dispatch a jump. Each is split: an inner function runs
the body, saves the state to globals and returns the next function; the
outer one, with no locals, tail-calls it. Which ones need it is read from
the machine code (an indexed indirect CALL in a handler) - see
lab/evolve/evolve.py, build_tail.
"""
import re, sys
WRAP = set(sys.argv[sys.argv.index('--wrap') + 1].split(',')) if '--wrap' in sys.argv else set()

src = open(sys.argv[1]).read()
fs = src.index('static void virtual_machine(void) {')
i = src.index('{', fs); depth, j = 0, i
while True:
    if src[j] == '{': depth += 1
    elif src[j] == '}':
        depth -= 1
        if depth == 0: break
    j += 1
pre, body, post = src[:fs], src[i + 1:j], src[j + 1:]

k = body.index('\nnext:')
preamble, rest = body[:k], body[k + 1:]
labels = [(m.start(), m.group(1)) for m in re.finditer(r'^([A-Za-z_]\w*):(?!:)', rest, re.M)
          if m.group(1) not in ('default',) and not m.group(1).startswith('LSB_')]
names = [n for _, n in labels]
ARGS = 'UNS64 ip, UNS64 dsp, UNS64 rp, UNS64 tos, UNS64 t'
PASS = '(ip, dsp, rp, tos, t)'
STATE = '    const UNS64 dsp_limit = tc_dsp_limit, rp_limit = tc_rp_limit, cbase = tc_cbase;\n' \
        '    (void)dsp_limit; (void)rp_limit; (void)cbase;\n'

def rewrite(b):
    b = b.replace('goto *dtab256[t];', 'return htab[t]%s;' % PASS)
    b = b.replace('goto *esc_tab[t];', 'return esc_ftab[t]%s;' % PASS)
    b = re.sub(r'goto\s+([A-Za-z_]\w*)\s*;',
               lambda m: m.group(0) if m.group(1).startswith('LSB_') else 'return H_%s%s;' % (m.group(1), PASS), b)
    left = re.findall(r'goto\s*\*', b)
    assert not left, 'a computed goto gen-tail.py does not know'
    return b

SAVE = '(tc_ip = ip, tc_dsp = dsp, tc_rp = rp, tc_tos = tos, tc_t = t, %s)'
def inner(b):
    b = rewrite(b).replace('return htab[t]%s;' % PASS, 'return %s;' % (SAVE % 'htab[t]'))
    b = b.replace('return esc_ftab[t]%s;' % PASS, 'return %s;' % (SAVE % 'esc_ftab[t]'))
    b = re.sub(r'return H_(\w+)\(ip, dsp, rp, tos, t\);', lambda m: 'return %s;' % (SAVE % ('H_' + m.group(1))), b)
    return re.sub(r'return\s*;', 'return 0;', b)

funcs = []
for n, ((a, name), nxt) in enumerate(zip(labels, labels[1:] + [(len(rest), None)])):
    blk = rest[a + len(name) + 1:nxt[0]]
    assert blk.count('{') == blk.count('}'), 'handler %s does not end where the next begins' % name
    if name in WRAP:
        tail = ('    return %s;\n' % (SAVE % ('H_' + nxt[1]))) if nxt[1] else '    return 0;\n'
        funcs.append('static __attribute__((noinline)) hfn I_%s(%s) {\n%s%s\n%s}\n' % (name, ARGS, STATE, inner(blk), tail))
        funcs.append('static void H_%s(%s) {\n    hfn f_ = I_%s%s;\n    if (!f_) return;\n'
                     '    return f_(tc_ip, tc_dsp, tc_rp, tc_tos, tc_t);\n}\n' % (name, ARGS, name, PASS))
        continue
    tail = ('    return H_%s%s;\n' % (nxt[1], PASS)) if nxt[1] else ''      # what fell through
    funcs.append('static void H_%s(%s) {\n%s%s\n%s}\n' % (name, ARGS, STATE, rewrite(blk), tail))

# the entry: the old preamble, with label addresses as function names and
# the label tables as tables of functions; then the first dispatch.
p = re.sub(r'&&([A-Za-z_]\w*)', r'H_\1', preamble)
p = p.replace('static const void *const dispatch[] = {', 'static const hfn dispatch[] = {')
ESC_N = re.search(r'const void \*cv8_tab\[128\], \*esc_tab\[(\d+)\];', p)        # 32, or 41 at ESCAPE == 2
ESC_N = int(ESC_N.group(1)) if ESC_N else 0
p = re.sub(r'const void \*cv8_tab\[128\], \*esc_tab\[(\d+)\];', r'hfn cv8_tab[128], esc_tab[\1];', p)
p = p.replace('static const void *dtab256[256];', '')
p = p.replace('dtab256', 'htab')
entry = ('static void virtual_machine(void) {\n%s\n'
         '    tc_dsp_limit = dsp_limit; tc_rp_limit = rp_limit; tc_cbase = cbase;\n'
         '%s'
         '    t = (*(unsigned char*)(ip)); ip += 1;\n'
         '    htab[t]%s;\n}\n') % (p, '    { int e_; for (e_ = 0; e_ < %d; e_++) esc_ftab[e_] = esc_tab[e_]; }\n' % ESC_N
                                  if ESC_N else '', PASS)
head = ('typedef void (*hfn)(%s);\n'
        'static hfn htab[256], esc_ftab[ESC_FTAB_N];\n'
        'static UNS64 tc_dsp_limit, tc_rp_limit, tc_cbase, tc_ip, tc_dsp, tc_rp, tc_tos, tc_t;\n' % ARGS
        + ''.join('static void H_%s(%s);\n' % (n, ARGS) for n in names))
head = head.replace('ESC_FTAB_N', str(max(ESC_N, 32)))   # 32 as ever at level 1; 41 at level 2
open(sys.argv[2], 'w').write(pre + head + ''.join(funcs) + entry + post)
print('%d handlers as functions, %d wrapped' % (len(names), len(WRAP & set(names))))
