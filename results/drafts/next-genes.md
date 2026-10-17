# The next genes - where the dispatches go now (Iteration 323)

Seed 54 runs the after-seed-52 genes; if it is small, the stopping rule ends them until new
genes exist. This is the search for those.

## The interpreted designs - lab/evolve/price.py on seed 53's three fastest

ccf55ad2f5, b926dd6bc8, b38afcd676 (0.343-0.355 of s6's time; the JIT designs 0.13-0.15), their
dispatch streams on the selection workloads, after their own fusions:

| workload | calls | EXIT | calls + EXIT | next 16 pairs (overstated) |
|---|---|---|---|---|
| kernel | 17-19% | 7-10% | 25-29% | 8-11% |
| fib | 11% | 11-12% | 22-24% | 12-21% |
| corpus | 12-14% | 8-9% | 21-23% | 16-19% |
| bubble | 16-19% | 10-16% | 29-32% | 7-8% |
| ackermann | 27-29% | 8% | 35-37% | 0.1% |
| loop | 0% | 0% | 0% | 60-100% |

Triples negligible (the best 0.3%). Calls and returns are the largest share - as missmap found
for mispredictions (15-25%) - but the genes for them exist: folds (prim;EXIT for 23 primitives),
tail, hotinl, factor, opinline, rtempty. Pairs: price.py's own record - nine of the next 16,
given slots, removed 0.2-2.4% in practice; the estimate's overlap overstates it. Two of the
three fastest fuse no pairs at all, the fastest 13: the evolution weighs them already. The
interpreted designs' dispatch-level levers are mostly in the genes now.

## The JIT designs - what the JIT leaves to the interpreter (next)

The speed frontier is the JIT's (0.13-0.15 of s6's time). The JIT translates a word only whole -
an operation without a stencil leaves the word interpreted - and kernel and corpus (compiling,
parsing, FIND) may run much of their time so. No tool counts it: **jitleft.py**, to build - a
JIT design with the profiler (as hotwords.py, the JIT on): the dispatches left are exactly what
the JIT did not translate; by word, and for each hot word the operation that kept it out. New
stencils for those operations are genes. And bfind's effect on the laptop's predictor (missmap,
a design with and without it) can be a chain's first measurement.

## What the JIT leaves to the interpreter (Iteration 339) - lab/evolve/jitleft.py

Seed 55's two fastest JIT designs (c549c0677c, c708e864b7) profiled with the JIT off and on, on this
VM. Both alike:

### c549c0677c

| workload | dispatches, JIT off | left by the JIT | left |
|---|---|---|---|
| kernel | 2,032,355 | 1,136,217 | 55.9% |
| fib | 59,245,391 | 9,767 | 0.0% |
| corpus | 3,714,212 | 3,703,940 | 99.7% |
| loop | 20,033,411 | 9,566 | 0.0% |
| bubble | 7,131,570 | 148,624 | 2.1% |
| ackermann | 17,557,699 | 17,136 | 0.1% |

What is left, by word (the mean share over the workloads), beside the word's share of the JIT-off work:

- (compiled at run time)    21.0% of what is left;  67.3% of the work, JIT off
- INTERPRET                 15.0% of what is left;   5.2% of the work, JIT off
- PARSE-WORD                 8.8% of what is left;   2.7% of the work, JIT off
- COLD                       7.5% of what is left;   0.0% of the work, JIT off
- ?STACK                     3.5% of what is left;   1.5% of the work, JIT off
- REFILL                     3.5% of what is left;   0.7% of the work, JIT off
- C,                         2.3% of what is left;   0.5% of the work, JIT off
- WORD                       2.1% of what is left;   1.1% of the work, JIT off
- HERE                       1.8% of what is left;   0.6% of the work, JIT off
- CMOVE>                     1.8% of what is left;   0.6% of the work, JIT off
- *                          1.8% of what is left;   0.2% of the work, JIT off
- SUPER-OP                   1.7% of what is left;   0.6% of the work, JIT off


**The reading**: fib, loop and ackermann are translated whole (0.0-0.1% left), bubble nearly
(2%); **kernel is 56% interpreted and corpus 99.7%**. The benchmarks' own words are compiled at run
time and translated (fib, loop) - so the corpus's run-time words, run once or a few times each, stay
under whatever makes the JIT translate. What carries the rest: the outer interpreter - INTERPRET
(15% of what is left), PARSE-WORD (8.8%), REFILL, WORD, ?STACK - and compiling words (C, HERE).

**Two genes to look for**: (1) the outer interpreter translatable - which operation in INTERPRET,
PARSE-WORD, WORD, REFILL has no stencil (next: the blockers, word by word); (2) when the JIT
translates code compiled at run time - its threshold, for compile-and-run-once work. With selection
at both widths, (1) counts twice: a JIT design's interpreter is its 32-bit speed.

## Next: why each word is left - a JITLOG build (planned, Iteration 339)

engine/jit.c's jit_body(w, a, end, depth) decodes a word into opl[] with each operation's address in
at[n] and refuses at its first untranslatable point - 17 `return 0`s; the commonest in the decode
loop: `if (L >= JIT_NOPS || !jit_ops[L].ok) return 0;` (an operation with no mapping), the later
ones in loops over i (jit_usable(s) refusals - a stencil read short, a branch it cannot place). The
plan, under -DJITLOG=1 only (a normal build's text the same - no 64-bit change): a static last-address
set to at[n] in the decode loop and at[i] in the later loops, and jit_body's caller writing
"R word address why" to a file named by an environment variable when it refuses; jitleft.py --why
building so, and naming each refused operation from the call map's O lines (address, kind, opcode,
name). Then the counts: which operations keep INTERPRET, PARSE-WORD, WORD, REFILL out - each a
stencil to write, a gene.

## Why each word is left - jitleft.py --why (Iteration 340)

engine/jit.c logs each refusal in a -DJITLOG=1 build only (a normal JIT engine byte-identical: c549c0677c,
112c1292f2df before and after); jitleft.py --why follows each word's refusal through refused callees to
the root. Seed 55's fastest JIT design, c549c0677c:

What is left, by word (the mean share over the workloads), beside the word's share of the JIT-off work:

- (compiled at run time)    21.0% of what is left;  67.3% of the work, JIT off
- INTERPRET                 15.0% of what is left;   5.2% of the work, JIT off; left: never tried
- PARSE-WORD                 8.8% of what is left;   2.7% of the work, JIT off; left: never tried
- COLD                       7.5% of what is left;   0.0% of the work, JIT off; left: never tried
- ?STACK                     3.5% of what is left;   1.5% of the work, JIT off; left: never tried
- REFILL                     3.5% of what is left;   0.7% of the work, JIT off; left: never tried
- C,                         2.3% of what is left;   0.5% of the work, JIT off; left: never tried
- WORD                       2.1% of what is left;   1.1% of the work, JIT off; left: no mapping for vf
- HERE                       1.8% of what is left;   0.6% of the work, JIT off; left: no mapping for vf
- CMOVE>                     1.8% of what is left;   0.6% of the work, JIT off; left: never tried
- *                          1.8% of what is left;   0.2% of the work, JIT off; left: no mapping for UM*
- SUPER-OP                   1.7% of what is left;   0.6% of the work, JIT off; left: never tried

The root operations, by the share of what is left behind them:

-  62.6%  never tried
-   5.1%  no mapping for vf
-   1.8%  no mapping for UM*
-   0.9%  no mapping for @4431
-   0.8%  no mapping for WRITE
-   0.5%  no mapping for vs
-   0.5%  no mapping for 0<?BRANCH8
-   0.3%  no mapping for SP@
-   0.3%  no mapping for DUP?BRANCH8
-   0.2%  no mapping for UM/MOD

**The reading.** 62.6% of what is left was **never tried**: INTERPRET, PARSE-WORD, COLD, ?STACK, REFILL,
C,, CMOVE> - the JIT translates a word on its first call through a JIT header, which the run-time
compiler gives the words it compiles, and a callee when translated code reaches it; the image's own
words have no header, and the outer interpreter is the top-level loop, never called from translated
code. Not a missing stencil: **not a candidate at all**. Then the operations with no mapping: vf (a
fused variable fetch: WORD, HERE - 5.1%), UM* (* - 1.8%), WRITE, vs (a fused variable store),
0<?BRANCH8, SP@, DUP?BRANCH8, UM/MOD.

**The genes**: (1) the image's words JIT candidates - translated on their first call as run-time words
are (or the outer interpreter and its callees at start) - the large lever; (2) stencils for vf, vs,
UM*, UM/MOD and the fused branches - small ones, each.

## The gene jitimg - the image's words as JIT candidates (designed, Iteration 340)

The JIT's protocol (forth/cv8t-jit.4, JIT.md, Iteration 80): a colon word compiled at run time begins
[JIT opcode][4 bytes] - the body's length with bit 31 set until its first call; then the engine
(vm-lab.c: `if (f_ & 0x80000000u) f_ = jit_word(ip - 1, 0);`) translates it and writes back the native
code's offset, or 0 - it stays bytecode, and each call after falls through to the body. The image's
words, converted from the dump, have no such header: never candidates. **The converter can write it**
- the engine needs nothing new.

- **jitimg** (expressed only with jit): 0 none, as now; 1 the outer interpreter - the words jitleft.py
  measured left (INTERPRET, PARSE-WORD, REFILL, WORD, ?STACK, C,, HERE, CMOVE> ...), a fixed list as
  opbody's; 2 every code word. The cost: 5 bytes a word given the header (~2 KB at 2) and, for a word
  the JIT refuses, one more dispatch a call (the header's opcode falls through) - the size objective
  and the speed weigh it: a gene, not a decision.
- **tools/layout.py**: for those words new_body_bytes + 5 on every layout path (HL, byte headers,
  ordinary); the emission of [JIT_CODE][len | 0x80000000, little end first] before the body; mid-word
  targets (tails) and the call map's W and O lines shifted by 5; the body's xt the header's address
  (a call lands on the opcode, as a run-time word's does).
- **Proof**: the JITLOG build's jitleft.py --why with jitimg 1 and 2 - INTERPRET and its callees tried,
  translated or refused for a named operation; the corpus and kernel through alive(); the speed of
  kernel and corpus against jitimg 0; and gene-equiv - a new gene, ids unchanged.
- Then the small ones: stencils for vf, vs, UM*, UM/MOD, 0<?BRANCH8, DUP?BRANCH8, SP@ (jitleft --why's
  list) - each a jit_ops mapping in the converter's JIT tables and a stencil in the SPN set.

## jitimg - first measurements (Iteration 341, results/drafts/jitimg-wip.patch: on top of the pending
## two-width batch)

Built: the converter writes the run-time words' JIT header for the image's plain code words (no
inline aligned data, no tail, nothing landing inside them); jitleft.py --set=gene=value varies a
recorded design. Seed 55's fastest JIT design, c549c0677c:
- jitimg 0: alive, image 9,547 bytes; **jitimg 1: alive, 9,611 bytes** (a dozen headers);
  **jitimg 2: died on the corpus** - some word must not be entered through a header (copied by
  inlining, or compared as an identity): to bisect.
- jitleft --why at jitimg 1: kernel 54.7% left (55.9% before), corpus 99.7%; "never tried" 48.1% of
  what is left (62.6%). PARSE-WORD now tried - and refused: **no mapping for vf**, as WORD and HERE.
  INTERPRET, ?STACK, REFILL still never tried - excluded by the rule (inline aligned data, XT
  literals or strings, most likely).
- **vf** is the engine's getstatic (L_vf: a variable's address from an inline slot, its cell
  pushed - VARIABLE @ fused); **vs** its store. The JIT has no stencil for either - and the outer
  interpreter reads >IN, STATE, BASE so. **Next: stencils for vf and vs** (a jit_ops mapping with
  the slot operand, an SPN stencil each) - jitimg pays only with them; then headers for words with
  aligned data (the token stream's alignment kept: NOP padding the JIT maps, or layout() told the
  stream's start), then jitimg 2's corpus death.

## jitvar - vf and vs given the JIT, and the staircase's next step (Iteration 342; results/drafts/
## jit-genes-wip.patch - jitimg and jitvar, against master and the pending two-width batch)

jitvar: vf (getstatic) and vs (putstatic) as a literal of the slot's address, then @ or ! - the JIT's
tables (O['vf'] = (['LIT', 'FETCH'], 8|9)), and two operand kinds in jit.c's decoder under JITVAR (the
16-bit slot; VARSLOT's 2-3 bytes): jit_cbase + (v << SCALE), as the engine's SLOT(). No new stencil.
c549c0677c with jitvar, and with jitimg 1 and jitvar: both alive. jitleft --why, both on:

- INTERPRET **tried** - refused: no mapping for **PLACE**; PARSE-WORD and WORD: no mapping for
  **(PARSE)**; HERE: no usable stencil for EXIT (to look into); "never tried" 32.9% of what is left
  (62.6% before jitimg, 48.1% with it). The totals unchanged - kernel 54.7%, corpus 99.7% left: the
  words are still refused, one step on.
- **The next blockers are C primitives** - PLACE, (PARSE), and so (FIND), SCAN, SKIP...: the format-10
  words evolution moved into the engine's C for speed. A stencil cannot be a C loop: translating
  INTERPRET needs **helper calls** - native code calling a primitive's C and coming back - which the
  JIT does not have (the handlers are labels of one threaded function, not functions). The large
  step of the staircase; jitimg and jitvar pay in full only after it.

## Helper calls - the design (Iteration 343, approved by the owner: "yes, please proceed")

Two ways: **per-primitive helpers** (a C function a primitive, with the stencils' signature, called
from native code) or **interpreter re-entry** (native code calling back into the interpreter for
whatever it cannot translate - which would also end the cascade: a refused callee refuses its
callers). Re-entry is the more powerful and the riskier (a re-entrant threaded interpreter with a
cached TOS, THROW across native frames, the fault handler); helpers first - bounded, measurable
step by step, and they show whether translating the outer interpreter pays before re-entry is tried.

The machinery is nearly there:
- **The ABI**: every stencil is `spn_st f(cell *sp, cell tos)` returning {sp, tos} (engine/spn-abi.h);
  a helper with that signature is callable from a stencil as it is.
- **Function holes**: spn-stencils.c has IMM_FN() - a 64-bit function-pointer hole, magic
  SPN_FN_VALUE 0x6ea1ed5ea1ed5e66 (used by SPN's st_interp); jit.c patches only the literal's
  (JIT_IMM64 0x5ea1ed5ea1ed5ea1) - it learns the second.
- **One stencil**: `S(st_callc) { spn_st r = ((spn_fn)IMM_FN())(sp, tos); GO(SPN_SP(r), SPN_TOS(r)); }`
  - appended to spn_table[] and jit.c's S_ list at the same place; position-independent (the call
  through a register, the address in the hole - not a relative call the copy would break).
- **The table**: the converter's JIT entries take a symbolic constant - 'PLACE': (['CALLC'],
  '&h_place') - written into vm-jit-ops.h as `(INT64)(uintptr_t)&h_place`, the linker's address.
- **The helpers**, under -DJITHELP (a gene; without it nothing compiled): the C primitives that
  block the outer interpreter, first PLACE - its handler (vm-lab.c L_x_place, ( s n d -- )):

      spn_st h_place(cell *sp, cell tos) {
          unsigned char *d = (unsigned char *)(uintptr_t)tos; ucell n = (ucell)sp[0];
          const unsigned char *s = (const unsigned char *)(uintptr_t)sp[1];
          *d++ = (unsigned char)n; while (n--) *d++ = *s++;
          return SPN_ST(sp + 3, sp[2]);
      }

  then (PARSE), and whatever jitleft --why names next: one helper, one measurement, each step.
  Written by hand from each handler at first; generated from the handlers' source (macro shims, as
  gen-tos.py rewrites them) if there come to be many.

## Helper calls built - and a latent bug in patch 2 found (Iteration 344)

**The latent bug**: jit.c fills a literal hole from the decoded operand only for operand kinds 1-5;
jitvar's slot kinds are 8 and 9, so a translated vf would push k (0) and fetch from address 0. No
test caught it because no word with vf was translated yet (each refused for something else) - it
would have struck exactly when helper calls unblocked them. Fixed: JIT_LITOPND(o) - with JITVAR the
slot kinds too; without, **the original tokens exactly** (a first version with parentheses changed
three of seed 55's JIT designs' engines - `a && b && (c && d)` is another tree than `a && b && c && d`
to GCC; builds proved deterministic, so it was that). results/drafts/jit-genes-fixed.patch is patch 2
corrected: it replaces results/pending/jit-genes-after-seed56.patch once re-verified (identity of the
token-exact form against patch 1 still to run; the parenthesized form passed run-tests, validate 7/7).

**Helper calls** (results/drafts/jithelp-wip.patch - cut against patch 2 with the parenthesized
macro: re-cut against jit-genes-fixed.patch before staging): st_callc (IMM_FN, called through a
register) and jit.c's function hole, jit_op's fn, h_place - all under JITHELP; the converter's rows
carry the helper. c549c0677c with jitimg 1, jitvar, jithelp: built, alive. jitleft --why: **INTERPRET
past PLACE - now stopped at COUNT**; PARSE-WORD at (PARSE). COUNT needs no helper: DUP 1+ SWAP C@ - a
table entry ['DUP', 'ADDI', 'SWAP', 'CFETCH'] with k 1. Then (PARSE)'s helper.

## Helper calls, the next steps (Iteration 345)

Patch 2 corrected and re-verified (results/pending/ORDER.md). The helper-call draft re-cut against it
(results/drafts/jithelp-wip.patch), with h_parse ((PARSE): ( a u c -- s len adv )) and COUNT as the
table entry DUP ADDI(1) SWAP CFETCH. c549c0677c with jitimg 1, jitvar, jithelp: alive. jitleft --why:
**INTERPRET past PLACE and COUNT - now at (FIND)**; **PARSE-WORD past (PARSE) - now at +!**. kernel
still 54.7% left: each word refused one step on. Next: +! - a helper, five lines (( n a -- )); then
(FIND) - the hard one: its handler depends on the design's genes (bfind's walk, the threads) and
reads the engine's internals (the thread table, the header layout) in vm.c, not the JIT's object:
the helper needs those exported to it - or interpreter re-entry instead.


## Interpreter re-entry - built, crashes on its first run (Iteration 346; results/drafts/
## jitre-wip.patch, against the pending batch and jithelp-wip.patch)

As SPN's spn_interp: vm-lab.c's jit_interp(sp, tos, body) spills the stack (the top where dsp points
- gen-tos.py's virtual_machine fills its TOS from there on entry), pushes a sentinel return address,
runs a nested virtual_machine() from the body under __builtin_setjmp (the C library's setjmp cannot
link: an engine has no libc). The sentinel is [the JIT opcode][2]: a "word" whose native code, at
offset 2 of the JIT's memory (offsets below 16 are never native), is a trampoline to jit_leave,
which __builtin_longjmps back with the stack - L_x_jit spills it on the way, no new opcode. The JIT
calls it through SPN's st_interp; the converter adds one row no bytecode maps to, INTERP (operand
kind 4: arg[i] fills the body hole), and a refused callee becomes that operation instead of refusing
its caller - every existing code path handles it as an ordinary operation. The gene jitre (needs
jithelp: its function holes).

**First run**: c549c0677c with jitimg 1, jitvar, jithelp, jitre - built and linked; **died: corpus**,
exit 70 (the fault handler) after the banner, before the first OK. Until jitre, no word holding a
helper call, an interpreted call, or vf was ever run natively - each still refused one step on - so
this is the first execution of all of them: the cause may be any. Likeliest: QUIT, now translatable,
runs right after the banner - it resets the return stack (RP!) and sets up CATCH, and a CATCH frame
in native code cannot be returned to by a THROW in the nested interpreter. **Next**: bisect - (1)
CALLC, h_place, h_parse, COUNT and vf each on a small word compiled at run time, run natively; (2) a
JITLOG run naming the word translated last before the fault; (3) the JIT refusing words with RP!,
CATCH or a return-stack trick (as JITX refuses unbalanced >R) - then jitre again.

## The bisection (Iteration 347)

A snippet of run-time words, each variant's output against the same design with the JIT off
(c549c0677c; T2 calls PLACE, T3 COUNT, T4 (PARSE), T6 a callee the JIT refuses):
- **jitvar + jithelp (run-time words only): identical** - PLACE's and (PARSE)'s helpers and COUNT's
  entry run natively and right. The helper calls are proven.
- **jitimg 1 + jitvar + jithelp: broken** - one header at a time over the outer interpreter's 18
  words, exactly one breaks it: **(PARSE)**. A one-operation word, which the compiler inlines by
  copying the operation at its body's start - with the header there, it copies the JIT opcode. Fix
  (to make): the converter gives no header to a word whose body is one operation and EXIT.
- **+ jitre: T6 faults** ("relf: segmentation fault", status 70) even in the simplest case, startup
  fine (so not QUIT). One hazard fixed on the way: entered at its header, an interpreted callee runs
  L_x_jit, which for a word left bytecode repoints its caller's call - found from the return address,
  here the sentinel: patching the bytes before it. The callee is now entered past the header (in the
  draft) - not sufficient: T6 still faults. gdb could not run the engine (status 1, no output, with
  or without address randomisation). **Next**: the fault handler (guard_trap) made to print the
  faulting rip and address (the signal's ucontext), in a scratch build - then the trampoline, the
  stencil, or the nested interpreter.

## The re-entry fault, located (Iteration 348)

gdb cannot run an engine (status 1, no output); the engine's own fault handler can say where. In a
scratch build (never for a design): engines link the lab's runtime (-DRTLIB=1), whose rt_fault
installs a one-argument handler without SA_SIGINFO; with 0x04000004 (SA_SIGINFO) and a three-
argument wrapper, the handler printed the rip (ucontext + 40, gregs[16]), the fault address, the
landmarks, and the native code's bytes - disassembled with
`objdump -D -b binary -mi386:x86-64 --adjust-vma=16`. The minimal case
(`: S1 S" hello world" ; : U1 S1 TYPE ; : T6 U1 ;  T6`):

- rip = fault address = jit_mem + 0x10295a: execution jumped there - the dictionary, mapped right
  after the JIT's 1 MB: **U1's bytecode, called as machine code**.
- The sentinel [0c 02 00 00 00] and the trampoline (movabs rax, jit_leave; jmp rax) are right.
- The native code: at 0x10 `push rax; call 0x10295a; mov rax,rdi; mov rdx,rsi; pop rax; jmp ...`,
  then EXIT - **the ordinary S_CALL stencil**, not st_interp (x86-64's IMM_FN is a movabs of
  0x6ea1ed5ea1ed5e66: an st_interp would show the movabs and a call through the register); at 0x30
  T6: a tail jump to 0x10, then EXIT. So U1 was translated as a native call to a bytecode address,
  bypassing the `f < 2 -> INTERP` rewrite - some path sends a refused callee to S_CALL: jit_inl1's
  one-operation inlining, or the JITK emission loop's own treatment of calls. **Next**: read those
  paths; JITLOG the translation of U1 and T6. Also: whether the bisection's helper words were
  translated at all - "identical" proves nothing if they ran as bytecode; check with JITLOG before
  calling the helpers proven.
- A change kept in the scratch work (to carry into the draft): st_interp known by its holes (a
  function and a literal), not by index - JITK's stencil variants have other indices.

## Interpreter re-entry works (Iteration 349)

The located fault had a one-line cause: **JIT_L_INTERP was 65534 - 0xFFFE, the translator's own
marker for "a call resolved"**. The converter took max(t2_names()) + 1, and t2_names holds a special
key at 65533 beside the operations (0-130); so every interpreted call was emitted as an ordinary
native call to its argument - a bytecode address (the disassembly: st_call's exact bytes, its call
aimed at S1 + 5, its tail jump at TYPE). Now the first index above the operations, asserted below
the markers (and jit_ops no longer 65,535 entries).

With re-entry a refused callee no longer stops its caller's translation - so the decoder read on
past a call to (S") into its inline string, the bytes taken for calls. jit_rtouch: a callee that reads
or pops the return stack below its own entry (R> or R@ with no >R before - its caller's return
address) refuses its caller, as before. And st_interp is known by its holes (a function and a
literal), not by index.

- The minimal program (S1 with a string, U1 calling S1 and TYPE, T6 calling U1): S1 refused for
  (S") (why 4), U1 translated with two interpreted calls, T6 calling U1 natively - **output identical
  to the JIT off**, status 0; with T2 (PLACE's helper), T3 (COUNT), T4 ((PARSE)'s helper) - identical.
- **The helper words translated, verified**: the log shows T2, T3, T4 given native code (0x10, 0x70,
  0x80) - last turn's "proven" now is.
- **Next**: (PARSE)'s image header (jitimg 1 + jithelp) - to re-check now; the corpus and the kernel
  with re-entry; the engine paths, the forced gate; then jitleft --why: does the outer interpreter
  translate, and do kernel and corpus get faster.

## All four JIT genes run correctly - and do not yet move the numbers (Iteration 350)

The kernel workload faulted with all four on (jitimg 1, jitvar, jithelp, jitre); a scratch fault report
for the build that crashes (the lab's runtime given SA_SIGINFO; the instruction pointer mapped by `nm`
on engine.full - engines are not position-independent) put it **in jit_body**: the translator itself.
With refused callees no longer ending a translation, the callees loop went on to the calls the decoder
had made of the data after a call to (.") and its kind - garbage targets; one unmapped. jit_rtouch had
called "safe" any callee with an operation it did not know. Now: unknown before EXIT, or no EXIT in 64
operations - refused (to be safe); and a callee address outside the image refuses its caller. Variants:
jitvar+jithelp+jitre, the same + jitimg 1, and jitimg 1 without jitre - **all alive** (the corpus, the
kernel). (PARSE)'s header no longer breaks anything (Iteration 347's failure is gone).

**jitleft --why, all four on (c549c0677c)**: kernel 54.6% left to the interpreter (55.9% with none of
them), corpus 99.6% (99.7%); fib, loop, ackermann 0.0-0.1% as before. INTERPRET refused for **(FIND)**,
PARSE-WORD and WORD for **+!** - operations without a mapping, which re-entry (for callees) cannot help.
"Never tried" 29.8% of what is left (62.6% before jitimg). Every mechanism correct; the outer
interpreter still interpreted. Left: +! (a helper, five lines), (FIND) (the engine's internals), or op
thunks - any unmapped operation run by the interpreter (needs every operation's length from the
converter). Whether it pays is unmeasured: INTERPRET is 5.2% of the JIT-off work.
