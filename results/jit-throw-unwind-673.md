# THROW across the JIT's nested interpreters (Iteration 673 - relf's report, its Iteration 942)

relf, porting relfsh onto the lab's designs, found that on the JIT designs a THROW reached from native code does not
unwind the native frames: the code after the CATCH runs in the wrong interpreter, and the native caller's remaining
code is lost or later returns into the wrong frame. Its reproduction, on a bare design:

    echo ": T2 ABORT ; : T3 ['] T2 CATCH . ; : T5 ['] T3 EXECUTE 5 . ; T5 CR BYE" \
      | designs/fastest-x86-64/forth designs/fastest-x86-64/image.img

Expected `-1 5`. This document: the reproduction on every JIT design, the analysis checked, the fix (in the engine),
the tests, the gates and benchmarks, and relf's two side observations.

## Reproduced

| design (translator's image) | ABORT, 8-byte | `-1 THROW`, 8-byte | ABORT, 4-byte | `-1 THROW`, 4-byte |
|---|---|---|---|---|
| fastest-x86-64 | `-1` | `-1 5` | `-1` | `-1 5` |
| fastest-x86-32 | `-1` | `-1 5` | `-1` | `-1 5` |
| best-all-round | `-1` | `-1 5` | `-1` | `-1` |
| small-jit | `-1 5` | `-1 5` | `-1 5` | `-1 5` |
| portable-knee (no JIT) | `-1 5` | `-1 5` | `-1 5` | `-1 5` |

The three designs with jitexec (EXECUTE and cold words through the helper, jit.c's jit_exec) fail; small-jit has no
jitexec - its native code never calls the interpreter - and is right. On the self-built images of phase 3 both
variants fail on all three: there THROW's cold-list offset is the one every call uses (below), so `: T2 -1 THROW ;`
is translated and calls THROW through the helper too. And an uncaught THROW leaks: 30,000 lines of `T` after
`: T ABORT ;`, then `7 .` - fastest-x86-64 and fastest-x86-32 die (segmentation fault), best-all-round says
"native (C) stack overflow"; small-jit and portable-knee print 7.

## The analysis - confirmed

A JITLOG build of fastest-x86-64 (forth-libc with -DJITLOG=1; offsets decimal, hex in the T and X lines) on the
reproduction: T5 translated (native); CATCH refused (op 34, RP@); T3 refused (its callee CATCH) and run by jit_exec's
nested interpreter (X 0x2a0a); THROW refused (op 35, RP!); T2 translated; THROW run interpreted from ABORT's native code
(X 0x1018 = 4120). So the chain is relf's: the outer interpreter (level 0) runs native T5; T5's EXECUTE runs T3 in a
nested interpreter (level 1: jit_interp, a sentinel pushed, setjmp into jit_jb); CATCH executes native T2 (level 1's
jit_call); T2 calls ABORT through the helper, ABORT is translated, and its THROW, cold, runs in another nested
interpreter (level 2). THROW's RP! puts rp in level 1's CATCH frame; the continuation - THROW's rest, then T3's `.` -
runs on in level 2; T3's EXIT reaches level 1's sentinel, and jit_leave longjmps to jit_jb, level 2's: back in ABORT's
native code after its THROW call, then T2, then level 1's jit_call. One detail more: level 1 then pops the cell
above its sentinel, which is the outer interpreter's return address into INTERPRET, and runs the rest of the input
(`CR BYE`) nested - T5's `5 .` never runs, and nothing crashes in the small case. An uncaught THROW (WARM, QUIT's
`R0 @ RP!`) runs QUIT on in the innermost interpreter, its C frames never freed: the leak. jit_call's return point
(jit_tb: UM/MOD's jit_throw0, (ABORT")'s jit_resume0) covers a throw raised in native code at one level, not an
interpreted THROW whose CATCH is an outer level's.

## The fix (engine/vm-lab.c; the jitexec designs' engines)

An interpreter's level is the part of the return stack below its sentinel, so the RP! itself says whose frame the
CATCH is in - relf's second option, keyed on the return stack:

- Each nested interpreter keeps a record on jit_interp's frame (struct jit_lvl): its sentinel slot, the jit_call
  return point of the interpreter that called into it (jit_tb then), the jit_jb before it and its own; jit_lv is
  the innermost.
- RP! (L_rpstore): when the new rp is past the innermost interpreter's sentinel, jit_unwind finds the interpreter that
  owns rp, hands it the data stack and the RP!'s next operation (jit_tsp, jit_ttos, jit_rip, jit_rp) and longjmps to
  the jit_call it waits in, which resumes it there as after (ABORT")'s jit_resume0 - the native frames and the
  interpreters between dropped. THROW's RP! is that case; WARM's and QUIT's `R0 @ RP!` unwind to the outermost.
- jit_leave: a sentinel leaves to its own interpreter - the one whose slot rp has just passed - not blindly to the
  innermost jit_jb.

Nothing in the kernel or the images changes (relf's first option - CATCH recording the level - would need both, and
new primitives in every design). The cost: none while no nested interpreter runs (jit_lv 0); a compare at RP!; five
stores at each nested entry and a short walk at its leave. The engines: fastest-x86-64 29,124 -> 29,332 bytes at
8-byte cells, 25,500 -> 25,196 at 4; fastest-x86-32 33,188 -> 33,428 and 32,112 -> 32,320; best-all-round 29,748 ->
29,940 and 26,000 -> 26,192. The other seven designs' engines are byte for byte the recorded ones
(results/drafts/designs-sha256-649.txt): the code is under `#if JITEXEC && JITMUL`.

## Tests

designs/test.sh (`make test`), for forth and, where built, forth32: square (as before); throw-abort and throw
(relf's two); throw-outer, the CATCH's continuation returning through an outer EXECUTE (`T4 ['] T3 EXECUTE 4 .`
under T5's: `-1 4 5`); throw-nested, two interpreters between the CATCH and the THROW (T7, refused for its RP@,
between); uncaught, the 30,000 uncaught ABORTs then `7 .`. Before the fix the three jitexec designs fail them at both
widths (best-all-round's forth32 also throw); after, 20 of 20 ok - and every case right on the self-built images
too, on their rebuilt engines. Also right on every design at both widths after the fix: nested CATCHes
(`-1 0 4 5`), a THROW out of a native DO loop, ABORT" and a zero divisor from native code, and a THROW at the bottom
of 50 levels of EXECUTE recursion through a refused word, caught at the top, twice in a row - on the self-built
images, where the recursing word is native (JITLOG), 50 interpreters nested under native code, all unwound.

## Gates and benchmarks

- lab/evolve/export-designs.py, all ten: every engine the lab's bytes at both widths; designs/*/src/vm.c, src32/vm.c
  (and srcarm/vm.c, src32's) taken from it - the only files that change.
- tools/run-tests.sh PASS (the engine generators: 107 paths, each built and its corpus right); evolve.py --validate
  7 of 7; pack-designs.py on the four JIT designs: 9 of 9 workloads right at both widths.
- The self-hosting checks (tools/selfhost-check.sh): all 21 pass again, the JIT designs' engines now with the fix.
- Speed, the old engine against the fixed one on the translator's images: the bench suite best of seven within
  noise; parse best of 25 15.8/15.8 ms (best-all-round) and best of 9 562.7/564.4 ms (fastest-x86-64 at 4-byte
  cells); a million entries of an interpreted word from native code (`: T 0 DO ['] R0 EXECUTE LOOP ;`, R0 refused),
  best of 21: fastest-x86-32 51.0/51.1 and 50.3/56.7 ms, fastest-x86-64 114.5/111.5 and 116.5/113.7 - no cost.

## relf's two observations

Both confirmed with JITLOG, and both an effect of the translator's NOOP padding before a body, which the self-built
images do not have:

- **THROW, 4115 and 4120.** The translator pads THROW's body (five NOOPs) and calls it past them: the kernel's ABORT
  calls 4120, the cold list's offset, so ABORT's THROW is cold-called; a word compiled at run time calls the xt FIND
  gives, 4115, misses the list, and is refused - `: TT 7 THROW ;` stays bytecode. The same for a data word padded
  before its DOVAR: a run-time call of START (xt 451, NOOPs first) is not the JIT's DOVAR literal, and
  `: TV START @ ;` stays bytecode.
- **In the self-built images** the cross compiler aligns inside a body, never before it: `' THROW`, the kernel's
  calls and the cold list are one offset (3731 in fastest-x86-64's), and TT and TV are translated. So the cold list
  needs no change: with the unwind, a THROW cold-called from anywhere is safe, and phase 5 ships the self-built
  images. For the translator's images (designs/ until then) moving the entry to 4115 would trade the kernel's cold
  calls for the run-time ones; what is wrong there is where the calls land, and it goes with those images.
