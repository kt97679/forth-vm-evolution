#!/usr/bin/env python3
"""gen-tos.py vm.c > vm-tos.c - top-of-stack caching, mechanically.
Hot primitives get hand-written TOS bodies; every other primitive is
wrapped SPILL / unchanged body / FILL, so its memory-stack view (and
SP@, DEPTH, the syscalls) is exactly what it was."""
import re, sys
s = open(sys.argv[1]).read()
HOT = {
 'L_lit':    'PUSHT(OPND16(ip)); ip += 2; NEXT();',
 'L_lit8':   'PUSHT(BYTE(ip)); ip += 1; NEXT();',
 'L_lit8x':  'PUSHT(BYTE(ip)); ip = RS; rp += CELL_BYTES; NEXT();',
 'L_drop':   'POPT(); NEXT();',
 'L_dup':    'PUSHT(tos); NEXT();',
 'L_swap':   't = NOS; NOS = tos; tos = t; NEXT();',
 'L_rot':    't = CELL(dsp + CELL_BYTES); CELL(dsp + CELL_BYTES) = NOS; NOS = tos; tos = t; NEXT();',
 'L_over':   't = NOS; PUSHT(t); NEXT();',
 'L_cfetch': 'tos = BYTE(tos); NEXT();',
 'L_fetch':  'tos = CELL(tos); NEXT();',
 'L_cstore': 'BYTE(tos) = (UNS8)NOS; tos = CELL(dsp + CELL_BYTES); dsp += 2 * CELL_BYTES; NEXT();',
 'L_store':  'CELL(tos) = NOS; tos = CELL(dsp + CELL_BYTES); dsp += 2 * CELL_BYTES; NEXT();',
 'L_and':    'tos &= NOS; dsp += CELL_BYTES; NEXT();',
 'L_or':     'tos |= NOS; dsp += CELL_BYTES; NEXT();',
 'L_xor':    'tos ^= NOS; dsp += CELL_BYTES; NEXT();',
 'L_fromr':  'PUSHT(RS); rp += CELL_BYTES; NEXT();',
 'L_tor':    'RPUSH(tos); POPT(); NEXT();',
 'L_rfetch': 'PUSHT(RS); NEXT();',
 'L_eq':     'tos = -(UNS64)(NOS == tos); dsp += CELL_BYTES; NEXT();',
 'L_ugt':    'tos = -(UNS64)(NOS < tos); dsp += CELL_BYTES; NEXT();',
 'L_gt':     'tos = -(UNS64)((INT64)NOS < (INT64)tos); dsp += CELL_BYTES; NEXT();',
 'L_plus':   'tos += NOS; dsp += CELL_BYTES; NEXT();',
 'L_negate': 'tos = -tos; NEXT();',
 'L_lshift': 'tos = NOS << tos; dsp += CELL_BYTES; NEXT();',
 'L_rshift': 'tos = NOS >> tos; dsp += CELL_BYTES; NEXT();',
 # PFA = align(body+3), matching vm-lab.c's ENC=3 L_dovar and the DODOES
 # path. This table OVERRIDES the source; when the source changed and this
 # did not, the first CREATE after boot pushed the wrong address on the
 # 32-bit build and the right one on 64-bit, by alignment luck.
 'L_dovar':  'PUSHT((ip + (DOESFAR ? 3 : 2) + CELL_BYTES - 1) & ~(UNS64)(CELL_BYTES - 1)); ip = RS; rp += CELL_BYTES; NEXT();',
 'L_lit0':   'PUSHT(0); NEXT();',
 'L_lit1':   'PUSHT(1); NEXT();',
 'L_litm1':  'PUSHT(~(UNS64)0); NEXT();',
 'L_vf':     '{ UNS64 a = SLOT(); PUSHT(CELL(a)); } NEXT();',
 'L_vs':     '{ UNS64 a = SLOT(); CELL(a) = tos; POPT(); } NEXT();',
 'L_lstore': '{ UNS64 a = SLOT(); CELL(a) = tos; POPT(); } NEXT();',
 'L_zeq':    'tos = -(UNS64)(tos == 0); NEXT();',
 'L_sub':    'tos = NOS - tos; dsp += CELL_BYTES; NEXT();',
 'L_ne':     'tos = -(UNS64)(NOS != tos); dsp += CELL_BYTES; NEXT();',
 'L_zlt':    'tos = -(UNS64)((INT64)tos < 0); NEXT();',
 'L_sgt':    'tos = -(UNS64)((INT64)tos < (INT64)NOS); dsp += CELL_BYTES; NEXT();',
 'L_2dup':   '{ UNS64 a_ = NOS, b_ = tos; PUSHT(a_); PUSHT(b_); } NEXT();',
 'L_2drop':  'tos = CELL(dsp + CELL_BYTES); dsp += 2 * CELL_BYTES; NEXT();',
 'L_charp':  'tos += 1; NEXT();',
 'L_onep':   'tos += 1; NEXT();',
 'L_cellp':  'tos += CELL_BYTES; NEXT();',
 'L_cells':  'tos <<= CELL_SHIFT; NEXT();',
 'L_onem':   'tos -= 1; NEXT();',
 'L_invert': 'tos = ~tos; NEXT();',
 'L_count':  '{ UNS64 a_ = tos; tos = a_ + 1; PUSHT(BYTE(a_)); } NEXT();',
 'L_aligned':'tos = (tos + CELL_BYTES - 1) & ~(UNS64)(CELL_BYTES - 1); NEXT();',
 'L_addi':   'tos += (UNS64)(INT64)(int8_t)BYTE(ip); ip += 1; NEXT();',
 'L_addix':  'tos += (UNS64)(INT64)(int8_t)BYTE(ip); ip = RS; rp += CELL_BYTES; NEXT();',
 'L_eqi':    'tos = -(UNS64)(tos == (UNS64)(INT64)(int8_t)BYTE(ip)); ip += 1; NEXT();',
 'L_eqix':   'tos = -(UNS64)(tos == (UNS64)(INT64)(int8_t)BYTE(ip)); ip = RS; rp += CELL_BYTES; NEXT();',
 'L_0branch':'t = tos; POPT(); if (t) ip += 2; else ip += BROFF(ip); NEXT();',
 # relf's format-10 opcodes (OPS10): written for the cached top, not wrapped
 'L_x_qbr8':  't = tos; POPT(); if (t) ip += 1; else ip += (int8_t)BYTE(ip); NEXT();',
 'L_x_nqbr':  't = tos; POPT(); if (t) ip += (int16_t)LD16(ip); else ip += 2; NEXT();',
 'L_x_nqbr8': 't = tos; POPT(); if (t) ip += (int8_t)BYTE(ip); else ip += 1; NEXT();',
 'L_x_ltbr':  't = (INT64)NOS < (INT64)tos; dsp += CELL_BYTES; POPT(); if (t) ip += 2; else ip += (int16_t)LD16(ip); NEXT();',
 'L_x_ltbr8': 't = (INT64)NOS < (INT64)tos; dsp += CELL_BYTES; POPT(); if (t) ip += 1; else ip += (int8_t)BYTE(ip); NEXT();',
 'L_x_eqbr': 't = NOS == tos; dsp += CELL_BYTES; POPT(); if (t) ip += 2; else ip += (int16_t)LD16(ip); NEXT();',
 'L_x_eqbr8': 't = NOS == tos; dsp += CELL_BYTES; POPT(); if (t) ip += 1; else ip += (int8_t)BYTE(ip); NEXT();',
 'L_x_ultbr': 't = NOS < tos; dsp += CELL_BYTES; POPT(); if (t) ip += 2; else ip += (int16_t)LD16(ip); NEXT();',
 'L_x_ultbr8': 't = NOS < tos; dsp += CELL_BYTES; POPT(); if (t) ip += 1; else ip += (int8_t)BYTE(ip); NEXT();',
 'L_x_nebr':       't = NOS != tos; dsp += CELL_BYTES; POPT(); if (t) ip += 2; else ip += (int16_t)LD16(ip); NEXT();',
 'L_x_nebr8':      't = NOS != tos; dsp += CELL_BYTES; POPT(); if (t) ip += 1; else ip += (int8_t)BYTE(ip); NEXT();',
 'L_x_sgtbr':      't = (INT64)NOS > (INT64)tos; dsp += CELL_BYTES; POPT(); if (t) ip += 2; else ip += (int16_t)LD16(ip); NEXT();',
 'L_x_sgtbr8':     't = (INT64)NOS > (INT64)tos; dsp += CELL_BYTES; POPT(); if (t) ip += 1; else ip += (int8_t)BYTE(ip); NEXT();',
 'L_x_zltbr':      't = (INT64)tos < 0; POPT(); if (t) ip += 2; else ip += (int16_t)LD16(ip); NEXT();',
 'L_x_zltbr8':     't = (INT64)tos < 0; POPT(); if (t) ip += 1; else ip += (int8_t)BYTE(ip); NEXT();',
 'L_x_eqibr':      't = tos == (UNS64)(INT64)(int8_t)BYTE(ip); ip += 1; POPT(); if (t) ip += 2; else ip += (int16_t)LD16(ip); NEXT();',
 'L_x_eqibr8':     't = tos == (UNS64)(INT64)(int8_t)BYTE(ip); ip += 1; POPT(); if (t) ip += 1; else ip += (int8_t)BYTE(ip); NEXT();',
 # Iteration 33: the tests that keep their value - nothing popped
 'L_x_dupbr':      'if (tos) ip += 2; else ip += (int16_t)LD16(ip); NEXT();',
 'L_x_dupbr8':     'if (tos) ip += 1; else ip += (int8_t)BYTE(ip); NEXT();',
 'L_x_overbr':     'if (NOS) ip += 2; else ip += (int16_t)LD16(ip); NEXT();',
 'L_x_overbr8':    'if (NOS) ip += 1; else ip += (int8_t)BYTE(ip); NEXT();',
 # Iteration 34
 'L_x_dupnbr':     'if (tos) ip += (int16_t)LD16(ip); else ip += 2; NEXT();',
 'L_x_dupnbr8':    'if (tos) ip += (int8_t)BYTE(ip); else ip += 1; NEXT();',
 'L_x_swapaddi':   't = NOS; NOS = tos; tos = t + (UNS64)(INT64)(int8_t)BYTE(ip); ip += 1; NEXT();',
 # Iteration 50: the byte loops as opcodes - three popped, the fourth the top
 'L_x_fill':       '{ UNS64 c_ = tos, u_ = NOS, a_ = CELL(dsp + CELL_BYTES); tos = CELL(dsp + 2 * CELL_BYTES); dsp += 3 * CELL_BYTES; while (u_) { BYTE(a_) = (UNS8)c_; a_++; u_--; } } NEXT();',
 'L_x_threadfind': '{ UNS64 nb_ = tos, a_ = NOS; dsp += CELL_BYTES; UNS8 n_ = BYTE(nb_); while (a_) {     if ((BYTE(a_) & 31) == n_) { UNS64 k_ = 0; while (k_ < n_ && BYTE(a_ + 1 + k_) == BYTE(nb_ + 1 + k_)) k_++; if (k_ == n_) break; }     { UNS8 t_ = BYTE(a_ - 1);       if (t_ < 128) a_ = t_ ? a_ - t_ : 0;       else if (t_ < 192) a_ -= ((UNS64)(t_ & 63) << 8) | BYTE(a_ - 2);       else a_ -= ((UNS64)(t_ & 63) << 16) | ((UNS64)BYTE(a_ - 2) << 8) | BYTE(a_ - 3); } } tos = a_; } NEXT();',
 # Iteration 54: the input side - SCAN, SKIP: three in, two out; TABS>BL: two in
 'L_x_scan':       '{ UNS64 c_ = tos, u_ = NOS, a_ = CELL(dsp + CELL_BYTES); dsp += CELL_BYTES; while (u_ && (UNS64)BYTE(a_) != c_) { a_++; u_--; } NOS = a_; tos = u_; } NEXT();',
 'L_x_skip':       '{ UNS64 c_ = tos, u_ = NOS, a_ = CELL(dsp + CELL_BYTES); dsp += CELL_BYTES; while (u_ && (UNS64)BYTE(a_) == c_) { a_++; u_--; } NOS = a_; tos = u_; } NEXT();',
 'L_x_tabsbl':     '{ UNS64 u_ = tos, a_ = NOS; tos = CELL(dsp + CELL_BYTES); dsp += 2 * CELL_BYTES; while (u_) { if (BYTE(a_) == 9) BYTE(a_) = 32; a_++; u_--; } } NEXT();',
 'L_x_parse':      '{ UNS64 c_ = tos, u_ = NOS, a_ = CELL(dsp + CELL_BYTES), p_ = a_, s_; while (u_ && (UNS64)BYTE(p_) == c_) { p_++; u_--; } s_ = p_; while (u_ && (UNS64)BYTE(p_) != c_) { p_++; u_--; } CELL(dsp + CELL_BYTES) = s_; NOS = p_ - s_; tos = (p_ - a_) + (u_ ? 1 : 0); } NEXT();',
 'L_x_hash':       '{ UNS64 t_ = tos, u_ = NOS, a_ = CELL(dsp + CELL_BYTES), h_; dsp += 2 * CELL_BYTES; h_ = (UNS64)BYTE(a_) << 1; if ((INT64)u_ > 1) h_ ^= (UNS64)BYTE(a_ + 1) << 2; tos = (h_ ^ u_) & (t_ - 1); } NEXT();',
 'L_x_place':      '{ UNS64 d_ = tos, n_ = NOS, s_ = CELL(dsp + CELL_BYTES); tos = CELL(dsp + 2 * CELL_BYTES); dsp += 3 * CELL_BYTES; BYTE(d_) = (UNS8)n_; d_++; while (n_) { BYTE(d_) = BYTE(s_); d_++; s_++; n_--; } } NEXT();',
 'L_x_cmove':      '{ UNS64 u_ = tos, d_ = NOS, s_ = CELL(dsp + CELL_BYTES); tos = CELL(dsp + 2 * CELL_BYTES); dsp += 3 * CELL_BYTES; while (u_) { BYTE(d_) = BYTE(s_); s_++; d_++; u_--; } } NEXT();',
 'L_x_execute': '{ UNS64 x_ = tos; POPT(); RPUSH(ip); ip = x_; } NEXT();',
 'L_x_i':     'PUSHT(RS); NEXT();',
 'L_x_j':     'PUSHT(CELL(rp + 2 * CELL_BYTES)); NEXT();',
 'L_x_qdup':  'if (tos) PUSHT(tos); NEXT();',
 'L_x_plusstore': '{ UNS64 a_ = tos; CELL(a_) += NOS; tos = CELL(dsp + CELL_BYTES); dsp += 2 * CELL_BYTES; } NEXT();',
 'L_x_do':    '{ RPUSH(NOS); RPUSH(tos); tos = CELL(dsp + CELL_BYTES); dsp += 2 * CELL_BYTES; } NEXT();',
 'L_x_qdo':   '{ UNS64 n2_ = tos, n1_ = NOS; tos = CELL(dsp + CELL_BYTES); dsp += 2 * CELL_BYTES; '
              'if (n1_ != n2_) { RPUSH(n1_); RPUSH(n2_); ip += 2; } else ip += BROFF(ip); } NEXT();',
 'L_x_ploop': '{ UNS64 n_ = tos, i_ = RS, l_ = CELL(rp + CELL_BYTES), j_ = i_ + n_; POPT(); '
              'if ((INT64)((i_ - l_) ^ (j_ - l_)) < 0) { rp += 2 * CELL_BYTES; ip += 2; } '
              'else { CELL(rp) = j_; ip += BROFF(ip); } } NEXT();',
}
NOSTACK = {'L_noop', 'L_exit', 'L_branch', 'L_dodoes', 'L_lsave', 'L_lrest', 'L_lzero',
           # The escape only reads its selector and jumps: wrapped, it SPILLed the
           # cached top into memory and the escaped primitive found the stack one
           # cell deep - the converter's "BUF-ALLOC fault", in every cached engine.
           'L_esc', 'L_hcall', 'L_x_unloop', 'L_x_loop', 'L_x_leave', 'L_x_br8'}   # never touch the data stack
fend = s.index("\n#if FOLD\n#define EXITNEXT")
start = s.index("L_noop:")
sec = s[start:fend]
out, labs = [], [(m.start(), m.group(1)) for m in re.finditer(r'^(L_\w+):', sec, re.M)]
pos0 = 0; res = sec[:labs[0][0]]
def _pp(x): return [l.strip() for l in x.splitlines() if l.lstrip().startswith('#')]
_expect = _pp(res)
for i, (pos, lab) in enumerate(labs):
    nxt = labs[i + 1][0] if i + 1 < len(labs) else len(sec)
    blk = sec[pos:nxt]
    # Keep what lies between this handler and the next - preprocessor lines,
    # comments, blank lines - out of the handler's block: a hand-written
    # cached body (HOT) replaces the whole block. Only trailing '#' lines were
    # kept, so a comment after them lost them too: the "#endif" closing SPEC
    # and the "#if ENC == 3 && OPS10" after it, which a comment follows - the
    # format-10 handlers fell inside SPEC, and a design with format-10 words
    # and no specialisations could not compile (Iteration 5, the uniform sample).
    lines = blk.splitlines(True)
    tail = []
    while lines:
        t = lines[-1].strip()
        if t == '' or t.startswith('#') or (t.startswith('/*') and t.endswith('*/')):
            tail.insert(0, lines.pop()); continue
        if t.endswith('*/') and t.startswith('*'):          # a block comment's last line
            taken = []
            while lines and lines[-1].strip().startswith(('*', '/*')):
                taken.insert(0, lines.pop())
                if taken[0].strip().startswith('/*'): break
            if taken and taken[0].strip().startswith('/*'):
                tail[:0] = taken; continue
            lines += taken                                   # a comment begun on a code line: code
        break
    tail = ''.join(tail)
    blk = ''.join(lines)
    _expect += _pp(tail) if lab in HOT else _pp(blk) + _pp(tail)
    if lab in HOT:
        blk = '%s: %s\n' % (lab, HOT[lab])
    elif lab not in NOSTACK:
        blk = blk.replace(lab + ':', lab + ': SPILL();', 1).replace('NEXT();', 'FILLNEXT();')
    res += blk + tail
# Every preprocessor line outside the bodies that HOT replaces must survive,
# in order: one lost moves handlers into another condition without a word -
# the format-10 handlers fell inside SPEC that way (Iteration 5). The HOT
# bodies' own conditionals go with them: they are CV8's bodies, and the file
# refuses any other encoding (the #error below).
_it, _first = iter(_pp(res)), None
for _n, _l in enumerate(_expect):
    if not any(_l == _o for _o in _it): _first = (_n, _l); break
if _first: sys.exit('gen-tos.py: preprocessor line %d of the handlers lost: %s' % _first)
s = s[:start] + res + s[fend:]
s = s.replace("#define FOLDBASE 128", """#define FOLDBASE 128
#define TOSCACHE 1
#if ENC != 3
#error "vm-lab-tos.c: its hand-written cached bodies are CV8's - compile it with -DENC=3"
#endif""", 1)
# tos register, fill on entry
s = s.replace("static void virtual_machine(void) {\n    VMREGS", """static void virtual_machine(void) {
    VMREGS
    UNS64 tos = CELL(dsp); dsp += CELL_BYTES;       /* fill */
#define NOS CELL(dsp)
#if GUARD
#define PUSHT(x) do { UNS64 v_ = (x); dsp -= CELL_BYTES; \\
        CELL(dsp) = tos; tos = v_; } while (0)
#else
#define PUSHT(x) do { UNS64 v_ = (x); dsp -= CELL_BYTES; \\
        if (dsp < dsp_limit) stack_fault(0); CELL(dsp) = tos; tos = v_; } while (0)
#endif
#define POPT() do { tos = CELL(dsp); dsp += CELL_BYTES; } while (0)
#undef VMPUSH
#define VMPUSH PUSHT
#define SPILL() do { dsp -= CELL_BYTES; CELL(dsp) = tos; } while (0)
#define FILLNEXT() do { POPT(); NEXT(); } while (0)
#if ENC == 3
#define BROFF(a) ((int16_t)LD16(a))
#else
#define BROFF(a) (2 * (int16_t)TOK(a))
#endif""", 1)
sys.stdout.write(s)
