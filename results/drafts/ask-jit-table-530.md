# A review of a converter's JIT table: does every row mean what the interpreter does? (the code is included below)

A Forth system is built from a cross-compiler (Python) that emits, besides the image, a C header the engine's
copy-and-patch JIT reads: **vm-jit-ops.h**, one row per bytecode operation - the stencils (machine-code templates) that
together do what the interpreter does for that operation, the operand's kind, and a constant for literal holes the
operand does not fill. Operations without a row stay bytecode. Please find rows or numbers that are wrong - a row whose
stencils compute something other than the interpreter's operation, at either cell width, or an index or offset that
does not match what the JIT reads. Every finding will become a test (the JIT's code is run against the interpreter on
the same programs at both widths), so a specific claim with the input that shows it is worth far more than a worry.

## What must hold

- **Same effect at both widths.** Designs are built with 8-byte cells (64-bit) and with 4-byte cells (32-bit). A row's
  stencils must compute exactly what the interpreter computes at that width - address arithmetic in cells, sign and
  overflow at the cell's width, the order of the two cells of a double.
- **Operand kinds match the encoding.** The operand kind (0 none, 1 u8, 2 u16, 3 s32, 4 s64, 5 s8, 6 an 8-bit branch,
  7 a 16-bit one; with jitvar 8 and 9, a variable's slot) must describe the bytes that follow the operation in the image
  exactly as the interpreter reads them - their width, signedness and what the value means.
- **The table's indices.** Rows are indexed by the operation's logical number (the one-byte codes; an escaped primitive
  128 + its selector). Extra rows (EXECUTE, a cold call, ABORT") go right after the last real operation - not past the
  JIT's own opcode (0xFE00) - and their #defines must name the same indices the rows sit at.
- **Word offsets** (#define JIT_W_*) are a word's body offset in this design's image.

## Bugs found here before - the kind I mean

1. CELL+ was ADDI 8 and CELLS LSHIFT 3 at both widths: every 32-bit JIT design computed wrong addresses (906 failures in
   one run). Fixed: the cell's width (the K map below).
2. 2@ and 2! were translated assuming 8-byte cells (the JIT's stencil sequence for them). Fixed.
3. The extra rows' index came from the highest name the converter knew - the JIT's own opcode at 0xFE00 - so the table
   ran to 65,029 rows: 585 KB in every engine with the gene jitexec, and no search kept the gene. Fixed.

## The answer I'd like

For each suspected bug: the row or line, the mechanism, a minimal Forth program that shows it (and at which width), the
expected and actual result, and your confidence. Then risky rows you believe correct, and invariants worth a check
(for example: every row of the table run against the interpreter at both widths on edge values). No style comments.

---

## tools/layout.py: the tag-2 map and the JIT table (lines 1600-1742)

```python
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
print("link chain re-walks to the same %d words in the same order: %s%s"
      % (len(order) - len(HL), "yes" if chain_ok else "NO", ' (%d headerless, on no chain)' % len(HL) if HL else ''))
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
        _one = ['T2_NONE'] * (128 if T2WIDE_ON else 64); _one[0x3F] = 'T2_ESC'
        for _x, _c in T2MAP['one'].items(): _one[_c if _c < 64 else _c - 64] = str(_x)   # wide: 0x80-0xBF the second half
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
            if '--jitx' in ARGV:   # Iteration 108, the gene jitx: the return stack, in words that balance it (engine/jit.c)
                S1.update({'>R': ['TOR'], 'R>': ['FROMR'], 'R@': ['RFETCH'], 'FILL': ['FILL']})
            K = {'lit0': (['LIT'], 0), 'lit1': (['LIT'], 1), 'litm1': (['LIT'], -1), '0=': (['LIT', 'EQ'], 0),
                 '0<': (['LIT', 'LT'], 0), 'INVERT': (['LIT', 'XOR'], -1), '<>': (['EQ', 'LIT', 'XOR'], -1),
                 '1+': (['ADDI'], 1), '1-': (['ADDI'], -1), 'CELL+': (['ADDI'], CELL), 'CHAR+': (['ADDI'], 1),
                 'CELLS': (['LIT', 'LSHIFT'], 3 if CELL == 8 else 2),   # 493: the cell's width - 4-byte cells at 32 bits
                 # Iteration 290: 2@ and 2! as opcodes - five stencils each, CELL+'s ADDI the one constant;
                 # without them a JIT design that takes the opcodes leaves every word holding one to the
                 # interpreter (jit.c: all or nothing), 2@ and 2! themselves among them
                 '2@': (['DUP', 'ADDI', 'FETCH', 'SWAP', 'FETCH'], CELL), '2!': (['SWAP', 'OVER', 'STORE', 'ADDI', 'STORE'], CELL)}   # 507/509: the cell, as CELL+ (493)
            O = {'LIT8': (['LIT'], 1), 'LIT': (['LIT'], 2), 'LIT32': (['LIT'], 3), 'LIT64': (['LIT'], 4),
                 'ADDI': (['ADDI'], 5), 'EQI': (['LIT', 'EQ'], 5), 'SWAP+I': (['SWAP', 'ADDI'], 5), 'DUP+I': (['DUP', 'ADDI'], 5), 'DUP<I': (['DUP', 'LIT', 'LT'], 5),
                 'BRANCH': (['BRANCH'], 7), 'BRANCH8': (['BRANCH'], 6), '?BRANCH': (['0BRANCH'], 7),
                 '?BRANCH8': (['0BRANCH'], 6), '(LOOP)': (['LOOP'], 7), '(LEAVE)': (['LEAVE'], 7),
                 '<?BRANCH': (['LT', '0BRANCH'], 7), '<?BRANCH8': (['LT', '0BRANCH'], 6),
                 '=?BRANCH': (['EQ', '0BRANCH'], 7), '=?BRANCH8': (['EQ', '0BRANCH'], 6),
                 'U<?BRANCH': (['ULT', '0BRANCH'], 7), 'U<?BRANCH8': (['ULT', '0BRANCH'], 6),
                 '>?BRANCH': (['GT', '0BRANCH'], 7), '>?BRANCH8': (['GT', '0BRANCH'], 6),
                 '?NBRANCH': (['LIT', 'EQ', '0BRANCH'], 7), '?NBRANCH8': (['LIT', 'EQ', '0BRANCH'], 6),
                 '<>?BRANCH': (['EQ', 'LIT', 'EQ', '0BRANCH'], 7), '<>?BRANCH8': (['EQ', 'LIT', 'EQ', '0BRANCH'], 6)}
            if '--jitloop' in ARGV:   # Iteration 129, the gene jitloop: SPN's (+LOOP) and (?DO) stencils, a branch operand as (LOOP)'s
                O.update({'(+LOOP)': (['PLOOP'], 7), '(?DO)': (['QDO'], 7)})
            # Iteration 504: jithelp retired (frozen since 455) - its C helpers and the rows' function field gone
            if '--jitvar' in ARGV:    # Iteration 342, the gene jitvar: vf and vs - a literal of the slot's address, then @ or !
                O['vf'] = (['LIT', 'FETCH'], 9 if G['VARSLOT'] else 8); O['vs'] = (['LIT', 'STORE'], 9 if G['VARSLOT'] else 8)
            if '--jitmul' in ARGV:    # Iteration 472, the gene jitmul: UM* and UM/MOD (spn-stencils.c, JITMUL); COUNT from stencils there are
                # 475: UM/MOD too - a zero divisor leaves native code as -10 THROW (jit.c's jit_throw0)
                S1.update({'UM*': ['UMSTAR'], 'UM/MOD': ['UMMOD'], 'SP@': ['SPFETCH'], 'ALIGNED': ['ALIGNED']})   # 484: SP@, ALIGNED
                K.setdefault('COUNT', (['DUP', 'ADDI', 'SWAP', 'CFETCH'], 1))
            if '--jitinl' in ARGV:    # Iteration 137, the gene jitinl: D+'s stencil (spn-stencils.c, JITINL)
                S1.update({'D+': ['DPLUS']})
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
            _jl, _rows, _miss = 0, [], []
            for _x, _nm in sorted(G['t2_names']().items()):
                _dj = _jd(_nm)        # (not _d: that is the directory the headers go to)
                if _dj and len(_dj[0]) <= 5:
                    _rows.append('[%d] = {1, %d, %d, %d, {%s}%s},  /* %s */' % (_x, len(_dj[0]), _dj[1], _dj[2],
                                 ', '.join('S_' + s for s in _dj[0]) or '0', '', _nm.replace('*/', '* /')))
                else: _miss.append('/* [%d] %s - no stencils */' % (_x, _nm.replace('*/', '* /')))   # 472: named, for jitapps.py
            if '--jitexec' in ARGV:    # Iteration 476, the gene jitexec: EXECUTE - a row no bytecode maps to, and the primitive if any
                _le = max(k for k in G['t2_names']().keys() if k < 0xFE00) + 2   # 517: not past T2_JIT (0xFE00) - the rows
                # there made jit_ops 65,029 rows, 585 KB of every jitexec engine: why no search ever kept jitexec
                _rows.append('[%d] = {1, 1, 4, 0, {S_EXECUTE}%s},  /* EXECUTE (jitexec) - its operand the site\'s cache (481) */' % (_le, ''))
                _rows.append('[%d] = {1, 1, 4, 0, {S_CALLX}%s},  /* a cold call through the helper (486) */' % (_le + 1, ''))
                _rows.append('[%d] = {1, 1, 4, 0, {S_ABORTQ}%s},  /* (ABORT") - the flag here, the interpreter on a true one (488) */' % (_le + 2, ''))
            _lint = ''                  # Iteration 504: jitre retired (frozen since 455) - its interpreted-call row gone
            _jc = T2MAP['one'][G['T2_JIT']]
            def _wends():              # Iteration 489: every image word's body, start and end - the decoder's end for a word reached
                rows_ = sorted((new_off[w_['s']]['body'], new_off[w_['s']]['body'] + new_body_bytes(w_)) for w_ in order
                               if w_['s'] in new_off and kind.get(w_['s']) == 'code')
                return ('#define JIT_NWENDS %d\nstatic const unsigned int jit_wends[][2] = {%s};\n'
                        % (len(rows_), ', '.join('{%d, %d}' % r_ for r_ in rows_) or '{0, 0}'))
            def _woff(nm):             # Iteration 485: a word's offset in the image (its body, as the call map's W lines), -1 if none
                ws_ = [w_ for w_ in order if w_['n'] == nm]
                return new_off[ws_[0]['s']]['body'] if ws_ else -1
            def _one(nm):              # Iteration 473, the gene jitdoes: an operation's one-byte code, -1 if it has none
                xs = [x for x, n_ in G['t2_names']().items() if n_ == nm]
                return T2MAP['one'].get(xs[0], -1) if xs and isinstance(T2MAP['one'], dict) else (T2MAP['one'][xs[0]] if xs and xs[0] < len(T2MAP['one']) else -1)
            open(_os.path.join(_d, 'vm-jit-ops.h'), 'w').write(
                '/* vm-jit-ops.h - this design\'s operations as SPN stencils (layout.py --jit, JIT.md) */\n'
                '#define JIT_CODE %d\n#define JIT_DOVAR %d\n#define JIT_DODOES %d\n#define JIT_FROMR %d\n%s%sstatic const struct jit_op jit_ops[] = {\n%s\n};\n'
                % (_jc, T2MAP['one'][[x for x, nm in G['t2_names']().items() if nm == 'DOVAR'][0]],
                   _one('DODOES'), _one('R>'), _lint + _wends(), (('#define JIT_L_EXECUTE %d\n' % _le) + ''.join('#define JIT_W_%s %d\n' % (k_, _woff(n_))
                   for k_, n_ in (('SQ', '(S")'), ('DQ', '(.")'), ('TYPE', 'TYPE')))
                   + '#define JIT_L_ABORTQ %d\n#define JIT_W_AQ %d\n' % (_le + 2, _woff('(ABORT")'))
                   + '#define JIT_L_CALLX %d\n#define JIT_W_COLD %s\n' % (_le + 1, ', '.join(str(_woff(n_)) for n_ in
                   ('EMIT', 'TYPE', 'CR', 'SPACE', 'SPACES', '.', 'U.', '.R', 'ABORT', 'THROW', 'KEY', 'ACCEPT')))) if '--jitexec' in ARGV else '', '\n'.join(_rows))   # not (ABORT"): it reads its caller's bytecode
                + '/* the operations without stencils (Iteration 472) */\n' + '\n'.join(_miss) + '\n')
            print("wrote vm-jit-ops.h: %d of %d operations translatable; JIT is code %d" % (len(_rows), len(G['t2_names']()), _jc))

_short_fails_out()
sys.exit(0 if chain_ok and gaps == 0 and not defer_bad and not xt_bad
         and not buf_bad and not untranslated and not bi_bad and not fixed_bad
         and not lit_bad else 1)
```

## engine/jit.c: the row's type, and how the translator decodes an operand (lines 219 and 872-898)

```c
struct jit_op { unsigned char ok, n, opnd; signed char k; unsigned char st[5]; };
/* ... */
            a++;
            if (L == T2_ESC) { L = jit_esc[BYTE(a)]; a++; }
#if JITLOG
            jitlog_op = (int)L;
#endif
            if (L >= (unsigned)JIT_NOPS || !jit_ops[L].ok) return 0;
            opl[n] = (unsigned short)L;
            switch (jit_ops[L].opnd) {
            case 0: arg[n] = (UNS64)(INT64)jit_ops[L].k; break;
            case 1: arg[n] = BYTE(a); a += 1; break;
            case 2: arg[n] = LD16(a); a += 2; break;
            case 3: arg[n] = (UNS64)(INT64)(int32_t)jit_ld32(a); a += 4; break;
            case 4: arg[n] = (UNS64)jit_ld32(a) | (UNS64)jit_ld32(a + 4) << 32; a += 8; break;
            case 5: arg[n] = (UNS64)(INT64)(int8_t)BYTE(a); a += 1; break;
            case 6: arg[n] = a + (UNS64)(INT64)(int8_t)BYTE(a); a += 1; break;
            case 7: arg[n] = a + (UNS64)(INT64)(int16_t)LD16(a); a += 2; break;
#if JITVAR
            /* Iteration 342, the gene jitvar: a variable's slot - vf and vs (getstatic, putstatic) as
               a literal of the address, then @ or ! - the address the engine's SLOT() makes */
            case 8: arg[n] = jit_cbase + ((UNS64)LD16(a) << SCALE); a += 2; break;
            case 9: { UNS64 t_ = BYTE(a);       /* VARSLOT: two bytes, or three with the top bit */
                if (t_ & 0x80) { t_ = ((t_ & 0x7F) << 16) | ((UNS64)BYTE(a + 1) << 8) | BYTE(a + 2); a += 3; }
                else { t_ = (t_ << 8) | BYTE(a + 1); a += 2; }
                arg[n] = jit_cbase + (t_ << SCALE); } break;
#endif
            default: return 0;
            }
```

*From forth-vm-evolution at cf1551a. Names used and not shown (G['t2_names'], T2MAP, CELL, the stencil names in the
lists) are what their names say: the operation numbering, the tag-2 one-byte and escape maps, the cell's width in bytes,
and the SPN stencils of engine/spn-stencils.c.*
