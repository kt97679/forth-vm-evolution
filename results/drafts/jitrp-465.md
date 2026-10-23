# jitrp - the JIT's return-stack pointer in a register: a prototype (Iteration 465)

The owner (464-465): prototype the third idea of the c4 family's second pass (results/drafts/c4-family-459.md) - register
pinning, as Deegen does it and as Ertl and Paysan describe with global register variables. The prototype is the patch
beside this note (results/drafts/jitrp-465.patch, against 2f1f41c); nothing of it is on master.

## What it changes

While native code runs, the return-stack pointer lived in memory - jit.c's jit_rp, its address patched into each
stencil through the IMM_RP hole - so every >R, R>, R@, DO, ?DO, LOOP, +LOOP, I, J, UNLOOP and LEAVE loaded the address,
loaded the pointer and stored it back. With JITRP it lives in a register (r15):

- engine/spn-stencils.c: `register ucell spn_rpr __asm__(JITRP_REG)` and the macros RPDECL, RP and RP_VALUE(); the
  eleven return-stack stencils use RP where they used `*rpp`.
- engine/vm-lab.c: the same register variable, declared before every function (GCC requires it), so the engine's own
  code leaves the register alone; the native call hands the pointer over in it and takes it back (and jit_interp, under
  jitre, reads it there).
- tools/gen-jitk.py: its one return-stack variant (I) through RP_VALUE().
- lab/evolve/evolve.py: a prototype's switch only - EVOLVE_JITRP=1 adds -DJITRP=1 to a JIT design's build.

## What it does

Each return-stack stencil loses three instructions - the address, the load, the store (objdump, -O2):

| stencil | memory | register |
|---|---|---|
| st_tor | 10 | 7 |
| st_fromr | 11 | 8 |
| st_i | 10 | 7 |
| st_do | 13 | 10 |
| st_loop | 14 | 11 |
| st_ploop | 25 | 22 |

Timing on this one-core machine swung 10-20% between repetitions - no verdict there. Instructions executed, counted
exactly by valgrind's cachegrind (--smc-check=all, so the JIT's own code is counted):

| design | loop | bubble | fib | ackermann |
|---|---|---|---|---|
| s6 with the JIT's genes | -0.41% | -0.26% | -0.01% | -0.24% |
| seed 68's fastest GCC JIT design, 6c0c4e6886 (regpin 1, rtloop, rtloopall) | **-19.9%** | **-4.5%** | - | **+2.1%** |

On s6 the return-stack stencils seldom run natively; on an evolved design whose loop genes put its loops in native code,
loop executes a fifth fewer instructions. ackermann's rise is most likely the interpreter's: the register reserved in
the engine's file is one fewer for its own code, and ackermann runs mostly through calls.

## What a gene needs

1. **GCC only** (GCC_ONLY): clang refuses a global register variable there ("register 'r15' unsuitable") - and seed
   68's fastest design is clang's; as regpin is GCC only.
2. **Its register clear of regpin's**: regpin 3 takes r15 (with r14 and rbx); jitrp would take r12 or r13 there -
   JITRP_REG from the build.
3. **With jitk**: gen-jitk.py's template is changed, but the design measured has no jitk; a jitk design built and run.
4. **engines-check**: the JIT variant with jitrp, and with jitrp and jitk, built and their corpus run; batch-checked.
5. **Timing on the laptop** decides, through the evolution: the loop's gain against the interpreter's lost register.

Order: after the after-seed-68 batch (the 32-bit JIT), which touches the same files and has its own run first - one
change at a time; the patch then rebased on it.
