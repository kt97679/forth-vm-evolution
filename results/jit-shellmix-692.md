# Why the JIT designs run shellmix slowly (Iteration 692)

On 674's six smaller programs the JIT designs ran at 0.35 of relf64's time; on shellmix 1.11-1.49 (results/relf-reply-685.md).
A JITLOG build of fastest-x86-64 (EVOLVE_JITLOG=1 EVOLVE_LIBC=1) running shellmix's benchmark shows why: **nearly all
of shellmix's words are refused** - SHELLMIX, SCRIPT, LINE, RUN, EXPAND-LINE, FIND-VAR, SET-VAR, NEW-VAR, OUT-C, OUT-S,
CHECKSUM-OUT, >NUM and the rest - so it runs interpreted. 18 of the 32 refusals are reason 4 (a callee refused), a
cascade from two roots:

- **DOES> children** (reason 1, operation 70, DODOES): the buffers (BUFFER:) and hooks (HOOK) - this design has no
  jitdoes;
- **the text interpreter's words** (reason 1, operations 36-41, which have no stencil): PARSE (38), WORD (41), FIND
  (36), >NUMBER (37), one after ACCEPT (41). shellmix's >NUM calls >NUMBER: >NUM refused, then RUN, LINE, SCRIPT.

## Two remedies measured (medians; the apps workload of 15, shellmix's benchmark alone of 9)

| change | fastest-x86-64 | best-all-round | fastest-x86-32 |
|---|---|---|---|
| jitdoes on (the gene exists, Iteration 473) | shellmix 0.950, apps 1.009 | shellmix 1.046, apps 1.025 | - |
| PARSE WORD FIND >NUMBER added to the cold words (called through the interpreter's helper, the caller native) | shellmix **1.152**, apps 1.070 | shellmix 1.114, apps 1.044 | shellmix 1.044, apps 0.994 |

(small-jit, which neither touches, moved 4 % between the two builds: the noise.) jitdoes stays a gene for the search
to weigh. The cold words are **rejected** (GOALS.md's register): entering the interpreter from native code at every
call costs more than leaving the chain interpreted. What would help is native code for the parsing operations
themselves - stencils for (PARSE), FIND's and >NUMBER's opcodes - a JIT project of its own, not step 3's.

Also (692): genapps.py --sizes writes its own work directory (build/genapps/sizes-work-N) - run-tests' appsize-check
--quick ran it, and a fresh work-8 lost the full and load drivers mech-dispatch.py, genapps-dispatch.py and
rtconst-check.py read; string-price.py follows it.
