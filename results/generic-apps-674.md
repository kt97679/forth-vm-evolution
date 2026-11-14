# Generic applications: the designs on code they did not see (Iteration 674 - step 1 after relf's report)

relf's report (its Iteration 944) found that the lab's designs do not make relf's shell smaller or faster. The owner
keeps the rule that relf's shell is not an objective of the search (RELF.md, Iteration 365): it is one special
application, and weighing it would bend the designs toward it. This is step 1 of what follows from the report: the
same question asked of generic code, relf's shell left out of it.

The lab scores a design by its engine and its 9 KB kernel image, and its speed on workloads whose hot code is mostly
the kernel's or a few lines long. Any real image is mostly application code compiled at run time, and nothing
scores that. Here seven programs run on the ten designs, on s6 (the lab's hand-made top stage), on relf's CV8 at
vendor/relf's commit e6e7d46 (relf's Iteration 944) and on gforth-fast 0.7.3. relf's CV8 runs three ways: relf64 is
its C engine (cc -O2, as relf builds it), relfasm64 its x86-64 assembler engine, both on its kernel64.img, and
relf32 the C engine at 4-byte cells. Measured per system and program: the code the program lays, the time its
benchmark runs, its load, and the system's start. Also measured: dispatches on the interpreted designs and on CV8,
the bytes each construct costs, and what the JIT leaves of each program.

## What it shows

1. **Application code: the portable designs lay 7-10 % more than CV8, the JIT designs 18-28 % more.** All seven
   programs at 8-byte cells: relf64 47,979 bytes, relfasm64 46,202. Against relf64: the six portable designs
   1.087-1.097 (the knee 52,306), s6 1.135, smallest 1.130, small-jit 1.186, best-all-round 1.267, fastest-x86-32
   1.269 and fastest-x86-64 1.278 (61,296). gforth-fast lays 4.556 (8-byte cell tokens). At 4-byte cells, against
   relf32 (45,076): portable 1.070-1.081, s6 1.102, smallest 1.097, small-jit 1.180, the three others
   1.265-1.274. brainless is 81 % of it.
2. **Where the bytes go** (the constructs table below; brainless counted on the knee: 605 colon definitions, 135
   constants, 87 VALUEs, 45 CREATEs). On brainless at 8-byte cells fastest-x86-64 lays 10,884 bytes more than
   relf64, in three steps:
   - relf64 to the knee, +3,668. The cell-aligned inline strings cost 16 bytes for 8 characters against CV8's 11
     (kernel.4's (S") and (.") step past the string with ALIGNED). A constant is called (3 bytes), where relf lays
     its value (2). A data word's fetch or store is a call and @ or ! (4 bytes), where relf lays one operation with
     a slot (VAR@, VAR!, two fetches as 2VAR@: 2.5-3 bytes). A VALUE is 32 bytes, where relf's is 24: coreext.4
     keeps a kind cell for TO, so 87 VALUEs cost 696 bytes. A defining word is 18 bytes against 13. The other way:
     relf inlines small kernel words (`.` costs it 4 bytes, a call 2) and its DO LOOP is 5 bytes against the
     designs' 4.
   - the knee to small-jit, +3,477: the JIT header, 5 bytes in every colon definition (`: X ;` is 12 bytes, 7
     elsewhere), 605 × 5 = 3,025.
   - small-jit to fastest-x86-64, +3,739: the two-bit tag's wide calls. A call past the first 16 KB is 4 bytes,
     against CV8's 3; brainless lies past them.
3. **The lab's size score does not see any of it.** Across the ten designs, the kernel image's bytes against the
   application code have a Spearman correlation of -0.21 (-0.33 at 4-byte cells). The score's total (engine and
   image) ranks engine plus brainless's code at 0.99, but only because the engine dominates both.
4. **Time: the gap is in the number of dispatches, not in the dispatch.** The benchmarks' geomean against
   relf64's time at 8-byte cells: portable-fastest 1.13, the knee 1.29, portable-arm 1.45, portable-small 1.75,
   least-memory 2.50 and smallest 3.25, with s6 at 2.04, relfasm64 0.94 and gforth-fast 0.56. The same six designs
   run 1.30, 1.45, 1.41, 1.50, 1.67 and 1.88 times relf64's dispatches, so per dispatch the fast ones cost what
   CV8's C engine does or less (portable-fastest about 0.87, the knee 0.89, arm 1.03). At 4-byte cells relf32 is
   slower, and portable-fastest runs 0.72 of its time, arm 0.93 and the knee 1.00.
5. **Where the extra dispatches are**: calls are 14-26 % of the designs' dispatches, DOVAR up to 18 % (scan), and
   DODOES 3-4 % on brainless. These are exactly what relf's run-time compiler takes out, each a mechanism of its
   kernel.4 that the lab's compiler lacks:
   - a constant compiled as its value (681), one dispatch for three;
   - a DOES> `@ ;` word's fetch compiled as one VAR@ (260), one for four;
   - a data word's fetch or store compiled as one operation (940), with a pair as 2VAR@ and VAR@ fused with the
     operation after it;
   - small straight words inlined (683);
   - `LIT n +`, `-` and `=` compiled as one operation (935);
   - the return folded into the last operation (939; the designs have this one).
6. **The JIT gives nothing on brainless.** On the six smaller programs the JIT designs run 0.35-0.36 of relf64's
   time (small-jit 0.63), and on sim16 and scan the JIT leaves 0.0-1.5 % of the dispatches to the interpreter. On
   brainless they take 2.41-3.13 s against relf64's 1.71 and portable-fastest's 2.23, because the JIT leaves 90.4 %
   (fastest-x86-64) and 86.2 % (best-all-round) of its dispatches. The reasons:
   - DODOES has no stencil, so a word that calls a DOES> word is refused, and so are its callers;
   - the VALUE's own DOES> code (coreext.4's `DOES> CELL+ @`) is refused for the return stack's order.

   brainless's 87 VALUEs are DOES> words and are everywhere in it.
7. **Start and load.** Start (BYE alone): the designs 0.8-1.1 ms (1.1-1.3 at 4-byte cells), relf64 1.7 (dynamically
   linked), relfasm64 0.9, gforth-fast 4.5. Loading all seven programs: the designs 21-34 ms (smallest 101), s6 52,
   relf64 50, relfasm64 42, gforth-fast 49.
8. **The whole system** for one application (the engine as the lab packs it, the kernel image, brainless's code).
   The small designs win on the engine: smallest 57,303 bytes, the knee 61,989 and portable-fastest 68,743, against
   relfasm64 65,635. relf64's 98,824 is not comparable, because it is dynamically linked and its C library is not
   counted. The JIT designs come to 75,011-91,330. The knee's lead over relfasm64 lasts up to about 60-70 KB of
   application code; past that, CV8's denser code wins.
9. **The lab's speed score holds.** Against these programs' geomean it ranks the ten designs at 0.99 (speed32 at
   4-byte cells: 0.96). The ranking is right; what it does not show is the absolute gap to CV8 (item 4).

## For step 2 - mechanisms as genes

Step 2 starts from what step 1 found:

- **Count application code in the size score.** Use genapps.py's code bytes for a fixed set of programs. Without
  them the search cannot see most of a real image.
- **The run-time compiler's mechanisms, each a gene priced on that code.** These are generic, none is about relf's
  shell, and every one is relf's (the last its assembler engine's):
  - constants as values;
  - data-word fetch and store as one operation;
  - DOES> `@ ;` fetches;
  - small-word inlining (bytes for dispatches);
  - immediate forms;
  - inline strings not cell-aligned;
  - for 8-byte cells, the dictionary at a low address, so that an address literal (`['] X`, TO's) takes 5 bytes
    rather than 9. relfasm64 has it: TO costs it 5.9 bytes, relf64 9.9.
- **For the JIT designs**: DOES> words (a DODOES stencil, or the fetch rewrite above, which leaves no DODOES to
  translate). Also the 5-byte header per definition and the wide calls, each priced on application code rather
  than on the 9 KB image.
- **A library detail**: VALUE's kind cell (8 bytes per VALUE and a CELL+ per fetch).

relf's shell, and relf's rill3, then serve as held-out checks (step 3), not objectives.

## Method

- **Programs**:
  - sim16, gc16, scan and evo: the selection's own applications, at about 2/5 of appbench.py's calls;
  - wordfreq and minif: held out;
  - brainless: Ertl's chess program, 128 KB of source, held out.

  The lab and relf get their sources folded to upper case (appbench's fold.py; brainless's hex literals as
  decimal). gforth gets them as written. Each full run's result line must be the same on every system.
- **Preludes**: on the lab's systems, brainless loads after appbench's prelude (extend.4, coreext.4, stubs). On relf
  it loads after lab/evolve/genapps/relf-prelude.fth: relf's own extend.4, then the words its kernel lacks, in
  Forth (PARSE-NAME, VALUE as `CREATE , DOES> @`, TO, 2>R and its kind, [IF], SAVE-INPUT, D= and so on). On gforth
  it loads with nothing before it. The other six programs need no prelude anywhere.
- **Code**: the bytes HERE advances over the program's load, less the program's own data (ALLOT , C,). The data is
  counted by a second load with those three words redefined through their old xts, and it is the same on every
  system of a width. The one exception is brainless on relf, 64 bytes more: relf has no DEFER, so brainless
  defines its own, and its 8 DEFERs' cells count as data there and as code elsewhere.
- **Time**: CPU time (user and system, getrusage of the child), pinned to one CPU, with the systems interleaved
  and rotated each round over 5 rounds. A benchmark's time is the median full run less the median load. Start is
  the median of 20 runs of BYE.
- **Dispatches**: the interpreted designs' engines built with -DPROFILE=1, counting per address, with calls as the
  pseudo-operation 256, DOVAR 69 and DODOES 70. relf's count comes from vendor/relf/cv8.c with tools/profile.py's
  patch, which counts every dispatch by its address. Each benchmark's count is the full run less the load.
- **Constructs**: each construct compiled 16 times into one definition, against the same definition empty, and
  each definition word measured whole. Calls go to the kernel, to a word in the image's first 16 KB (NEAR) and to
  a word past it (FAR, after 20,000 bytes allotted).
- **The JIT**: lab/evolve/jitapps.py (Iteration 471), the design built twice, JIT off and on with JITLOG. It
  reports the share of the dispatches left, each refused word traced to the root of its refusal.

## Application code (bytes)

8-byte cells (relf e6e7d46; 5 rounds; 2026-11-14 14:36):

| system | sim16 | gc16 | scan | evo | wordfreq | minif | brainless | all seven | vs relf64 | vs s6 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| s6 | 1,737 | 1,401 | 3,337 | 1,097 | 1,113 | 2,184 | 43,572 | 54,441 | 1.135 | 1.000 |
| smallest | 1,713 | 1,385 | 3,329 | 1,097 | 1,081 | 2,176 | 43,420 | 54,201 | 1.130 | 0.996 |
| least-memory | 1,721 | 1,321 | 3,057 | 953 | 969 | 2,153 | 42,404 | 52,578 | 1.096 | 0.966 |
| portable-small | 1,689 | 1,297 | 3,017 | 945 | 953 | 2,121 | 42,108 | 52,130 | 1.087 | 0.958 |
| portable-knee | 1,713 | 1,305 | 3,025 | 945 | 961 | 2,129 | 42,228 | 52,306 | 1.090 | 0.961 |
| portable-arm | 1,705 | 1,305 | 3,017 | 945 | 953 | 2,129 | 42,140 | 52,194 | 1.088 | 0.959 |
| portable-fastest | 1,729 | 1,313 | 3,025 | 953 | 953 | 2,137 | 42,501 | 52,611 | 1.097 | 0.966 |
| best-all-round | 2,226 | 1,562 | 3,466 | 1,082 | 1,090 | 2,352 | 49,003 | 60,781 | 1.267 | 1.116 |
| small-jit | 2,089 | 1,457 | 3,289 | 1,025 | 1,049 | 2,280 | 45,705 | 56,894 | 1.186 | 1.045 |
| fastest-x86-64 | 2,250 | 1,578 | 3,458 | 1,082 | 1,098 | 2,386 | 49,444 | 61,296 | 1.278 | 1.126 |
| fastest-x86-32 | 2,234 | 1,570 | 3,466 | 1,082 | 1,090 | 2,360 | 49,100 | 60,902 | 1.269 | 1.119 |
| relf64 | 1,663 | 1,330 | 2,725 | 909 | 896 | 1,896 | 38,560 | 47,979 | 1.000 | 0.881 |
| relfasm64 | 1,655 | 1,254 | 2,725 | 909 | 896 | 1,848 | 36,915 | 46,202 | 0.963 | 0.849 |
| gforth-fast | 9,000 | 6,920 | 15,704 | 5,040 | 4,752 | 10,288 | 166,912 | 218,616 | 4.556 | 4.016 |

Their data, bytes: sim16 34,048; gc16 340,544; scan 50,408; evo 9,024; wordfreq 131,104; minif 71,936; brainless
777,016 (relf 777,080).

4-byte cells (5 rounds; 2026-11-14 14:46):

| system | sim16 | gc16 | scan | evo | wordfreq | minif | brainless | all seven | vs relf32 | vs s6 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| s6 | 1,657 | 1,297 | 2,869 | 985 | 977 | 1,988 | 39,912 | 49,685 | 1.102 | 1.000 |
| smallest | 1,637 | 1,281 | 2,861 | 985 | 957 | 1,972 | 39,752 | 49,445 | 1.097 | 0.995 |
| least-memory | 1,645 | 1,249 | 2,713 | 893 | 909 | 1,964 | 39,328 | 48,701 | 1.080 | 0.980 |
| portable-small | 1,617 | 1,233 | 2,685 | 881 | 889 | 1,932 | 39,000 | 48,237 | 1.070 | 0.971 |
| portable-knee | 1,645 | 1,237 | 2,697 | 885 | 901 | 1,948 | 39,140 | 48,453 | 1.075 | 0.975 |
| portable-arm | 1,633 | 1,237 | 2,689 | 885 | 897 | 1,940 | 39,040 | 48,321 | 1.072 | 0.973 |
| portable-fastest | 1,661 | 1,241 | 2,693 | 885 | 889 | 1,944 | 39,393 | 48,706 | 1.081 | 0.980 |
| best-all-round | 2,170 | 1,510 | 3,098 | 1,030 | 1,050 | 2,208 | 45,939 | 57,005 | 1.265 | 1.147 |
| small-jit | 2,029 | 1,397 | 2,985 | 969 | 1,013 | 2,132 | 42,669 | 53,194 | 1.180 | 1.071 |
| fastest-x86-64 | 2,190 | 1,526 | 3,106 | 1,030 | 1,054 | 2,220 | 46,320 | 57,446 | 1.274 | 1.156 |
| fastest-x86-32 | 2,178 | 1,514 | 3,106 | 1,030 | 1,058 | 2,212 | 46,032 | 57,130 | 1.267 | 1.150 |
| relf32 | 1,603 | 1,206 | 2,512 | 853 | 851 | 1,748 | 36,303 | 45,076 | 1.000 | 0.907 |

## What each construct costs (bytes)

8-byte cells; a construct inside a definition is the mean of 16, a definition word is whole:

| construct | s6 | smallest | least-memory | portable-small | portable-knee | portable-arm | portable-fastest | best-all-round | small-jit | fastest-x86-64 | fastest-x86-32 | relf64 | relfasm64 | gforth-fast |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| a primitive (DUP) | 0.9 | 0.9 | 0.9 | 0.9 | 1 | 0.9 | 0.9 | 1 | 1 | 1 | 1 | 1 | 1 | 8 |
| a call: the kernel (.) | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 4 | 4 | 16 |
| a call: NEAR | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 16 |
| a call: FAR | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 4 | 3 | 4 | 4 | 3 | 3 | 16 |
| literal 5 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 16 |
| literal 1000 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 16 |
| literal 100000 | 5 | 5 | 5 | 5 | 5 | 5 | 5 | 5 | 5 | 5 | 5 | 5 | 5 | 16 |
| literal 1000000000 | 5 | 5 | 5 | 5 | 5 | 5 | 5 | 5 | 5 | 5 | 5 | 5 | 5 | 16 |
| a variable | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 4 | 3 | 4 | 4 | 3 | 3 | 16 |
| a variable @ | 3.9 | 3.9 | 3.9 | 3.9 | 4 | 3.9 | 3.9 | 5 | 4 | 5 | 5 | 2.5 | 2.5 | 24 |
| a variable ! | 3.9 | 3.9 | 3.9 | 3.9 | 3.9 | 3.9 | 3.9 | 5 | 4 | 5 | 5 | 2.9 | 2.9 | 24 |
| a constant | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 4 | 3 | 4 | 4 | 2 | 2 | 16 |
| a VALUE | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 4 | 3 | 4 | 4 | 3 | 3 | 16 |
| TO a VALUE | 9.9 | 9.9 | 9.9 | 9.9 | 9.9 | 9.9 | 9.9 | 10 | 10 | 10 | 10 | 9.9 | 5.9 | 24 |
| 5 + | 2.9 | 2.9 | 2.9 | 2.9 | 2 | 2 | 2 | 3 | 3 | 3 | 3 | 2 | 2 | 24 |
| ['] DUP | 9 | 9 | 9 | 9 | 9 | 9 | 9 | 9 | 9 | 9 | 9 | 9 | 5 | 16 |
| IF THEN | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 16 |
| IF ELSE THEN | 6 | 6 | 6 | 6 | 6 | 6 | 6 | 6 | 6 | 6 | 6 | 6 | 6 | 32 |
| BEGIN UNTIL | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 2 | 3 | 3 | 2 | 2 | 2 | 16 |
| BEGIN WHILE REPEAT | 6 | 6 | 6 | 6 | 6 | 6 | 6 | 5 | 6 | 6 | 5 | 5 | 5 | 32 |
| DO LOOP | 16.1 | 15.8 | 4 | 4 | 4 | 4 | 4 | 4 | 4 | 4 | 4 | 5 | 5 | 32 |
| S" ABCDEFGH" | 16.1 | 16.1 | 15.9 | 16 | 15.7 | 15.8 | 15.7 | 15.9 | 15.9 | 15.8 | 15.9 | 11 | 11 | 56 |
| ." ABCDEFGH" | 16.1 | 16.1 | 16.1 | 16.1 | 16.1 | 16.1 | 16.1 | 16 | 16 | 16 | 16 | 11 | 11 | 72 |
| : X ; (a 3-character name) | 7 | 7 | 7 | 7 | 7 | 7 | 7 | 12 | 12 | 12 | 12 | 7 | 7 | 48 |
| a name's character, each (8 more) | 1.1 | 1 | 1.1 | 1 | 1.1 | 1.1 | 1.1 | 1.1 | 1.1 | 1.1 | 1.1 | 1.1 | 1.1 | 1 |
| VARIABLE | 24 | 17 | 24 | 17 | 24 | 24 | 24 | 22 | 22 | 22 | 22 | 17 | 21 | 48 |
| CONSTANT | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 48 |
| CREATE | 16 | 16 | 16 | 16 | 16 | 16 | 16 | 16 | 16 | 16 | 16 | 16 | 16 | 40 |
| a defining word (CREATE , DOES> @) | 18 | 18 | 18 | 18 | 19 | 18 | 18 | 19 | 19 | 19 | 19 | 13 | 13 | 144 |
| its child | 22 | 22 | 22 | 22 | 21 | 22 | 22 | 21 | 21 | 21 | 21 | 19 | 19 | 48 |
| VALUE | 32 | 32 | 32 | 32 | 32 | 32 | 32 | 32 | 32 | 32 | 32 | 24 | 24 | 48 |

At 4-byte cells (build/genapps/constructs-4.md) the calls, literals, branches and JIT headers are the same. The
cell-dependent constructs come out as follows, the designs' figure first and relf32's second:

| construct | designs | relf32 |
|---|---:|---:|
| a string of 8 characters | 12 | 11 |
| ['] and TO's address literal | 5 | 5 |
| VARIABLE | 13-16 | 13 |
| VALUE | 20 | 16 |
| a defining word | 14-19 (19 on the JIT designs) | 13 |
| s6's and smallest's DO LOOP | 8 | 5 |

## Run time (CPU seconds; the benchmark: full run less load)

8-byte cells:

| system | sim16 | gc16 | scan | evo | wordfreq | minif | brainless | geomean vs relf64 | vs s6 | load, all seven (ms) | start (ms) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| s6 | 1.090 | 0.866 | 1.008 | 0.875 | 1.025 | 0.423 | 2.896 | 2.041 | 1.000 | 52 | 0.9 |
| smallest | 1.797 | 1.468 | 1.496 | 1.617 | 1.694 | 0.727 | 3.462 | 3.251 | 1.593 | 101 | 0.8 |
| least-memory | 1.523 | 1.097 | 1.031 | 1.027 | 1.180 | 0.592 | 3.483 | 2.498 | 1.224 | 34 | 0.8 |
| portable-small | 0.854 | 0.780 | 0.740 | 0.773 | 0.838 | 0.389 | 2.817 | 1.746 | 0.855 | 28 | 0.8 |
| portable-knee | 0.812 | 0.585 | 0.585 | 0.443 | 0.458 | 0.293 | 2.536 | 1.289 | 0.631 | 25 | 0.9 |
| portable-arm | 0.793 | 0.648 | 0.638 | 0.565 | 0.593 | 0.343 | 2.567 | 1.452 | 0.712 | 24 | 0.9 |
| portable-fastest | 0.656 | 0.502 | 0.516 | 0.414 | 0.417 | 0.250 | 2.230 | 1.127 | 0.552 | 21 | 0.9 |
| best-all-round | 0.215 | 0.131 | 0.113 | 0.133 | 0.254 | 0.089 | 2.457 | 0.442 | 0.217 | 25 | 0.8 |
| small-jit | 0.633 | 0.323 | 0.142 | 0.137 | 0.274 | 0.228 | 2.913 | 0.722 | 0.354 | 23 | 0.9 |
| fastest-x86-64 | 0.202 | 0.132 | 0.121 | 0.137 | 0.169 | 0.093 | 3.133 | 0.438 | 0.215 | 24 | 1.1 |
| fastest-x86-32 | 0.187 | 0.137 | 0.119 | 0.128 | 0.258 | 0.095 | 2.406 | 0.441 | 0.216 | 21 | 1.0 |
| relf64 | 0.552 | 0.487 | 0.357 | 0.444 | 0.515 | 0.190 | 1.708 | 1.000 | 0.490 | 50 | 1.7 |
| relfasm64 | 0.484 | 0.425 | 0.350 | 0.425 | 0.495 | 0.189 | 1.564 | 0.936 | 0.459 | 42 | 0.9 |
| gforth-fast | 0.342 | 0.247 | 0.239 | 0.183 | 0.211 | 0.140 | 1.161 | 0.562 | 0.276 | 49 | 4.5 |

The six smaller programs alone, against relf64: the JIT designs 0.345-0.364 (small-jit 0.626), portable-fastest
1.099, the knee 1.259. brainless alone: the JIT designs 1.41-1.83, portable-fastest 1.31, the knee 1.49.

4-byte cells:

| system | sim16 | gc16 | scan | evo | wordfreq | minif | brainless | geomean vs relf32 | vs s6 | load, all seven (ms) | start (ms) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| s6 | 0.990 | 0.813 | 0.939 | 0.832 | 0.891 | 0.416 | 2.432 | 1.208 | 1.000 | 56 | 1.3 |
| smallest | 1.873 | 1.506 | 1.577 | 1.701 | 1.711 | 0.748 | 3.238 | 2.143 | 1.774 | 202 | 1.3 |
| least-memory | 1.444 | 1.018 | 1.109 | 0.963 | 1.132 | 0.607 | 3.254 | 1.568 | 1.297 | 131 | 1.3 |
| portable-small | 0.909 | 0.743 | 0.767 | 0.727 | 0.790 | 0.369 | 2.534 | 1.092 | 0.903 | 35 | 1.1 |
| portable-knee | 1.048 | 0.714 | 0.746 | 0.507 | 0.527 | 0.374 | 2.699 | 0.999 | 0.827 | 31 | 1.1 |
| portable-arm | 0.878 | 0.608 | 0.694 | 0.509 | 0.589 | 0.338 | 2.408 | 0.929 | 0.769 | 29 | 1.1 |
| portable-fastest | 0.655 | 0.487 | 0.524 | 0.412 | 0.410 | 0.252 | 2.178 | 0.722 | 0.598 | 26 | 1.1 |
| best-all-round | 0.177 | 0.139 | 0.128 | 0.147 | 0.355 | 0.096 | 3.001 | 0.316 | 0.261 | 33 | 1.1 |
| small-jit | 0.762 | 0.372 | 0.145 | 0.157 | 0.356 | 0.333 | 3.428 | 0.560 | 0.464 | 33 | 1.1 |
| fastest-x86-64 | 0.188 | 0.140 | 0.128 | 0.152 | 0.165 | 0.101 | 3.105 | 0.291 | 0.241 | 31 | 1.1 |
| fastest-x86-32 | 0.177 | 0.140 | 0.122 | 0.146 | 0.313 | 0.096 | 2.752 | 0.305 | 0.252 | 30 | 1.1 |
| relf32 | 0.793 | 0.632 | 0.616 | 0.690 | 0.954 | 0.341 | 2.176 | 1.000 | 0.827 | 71 | 1.7 |

## Dispatches (8-byte cells; the benchmark: full run less load)

| program | relf64 | smallest | least-memory | portable-small | portable-knee | portable-arm | portable-fastest |
|---|---:|---:|---:|---:|---:|---:|---:|
| sim16 | 636,965,163 | 1,110,214,501 (1.74) | 1,086,826,288 (1.71) | 832,401,971 (1.31) | 1,091,698,469 (1.71) | 832,401,623 (1.31) | 846,747,629 (1.33) |
| gc16 | 553,104,692 | 944,156,605 (1.71) | 815,301,767 (1.47) | 722,441,136 (1.31) | 772,338,147 (1.40) | 688,659,339 (1.25) | 683,822,329 (1.24) |
| scan | 434,546,402 | 1,005,511,096 (2.31) | 798,055,178 (1.84) | 719,824,399 (1.66) | 781,447,797 (1.80) | 715,511,574 (1.65) | 709,075,505 (1.63) |
| evo | 576,222,545 | 1,103,909,996 (1.92) | 768,229,695 (1.33) | 741,906,062 (1.29) | 644,194,777 (1.12) | 633,076,099 (1.10) | 628,870,363 (1.09) |
| wordfreq | 660,261,456 | 1,107,935,734 (1.68) | 848,822,213 (1.29) | 803,473,518 (1.22) | 634,026,225 (0.96) | 691,656,986 (1.05) | 606,721,432 (0.92) |
| minif | 244,095,973 | 454,069,281 (1.86) | 424,677,916 (1.74) | 366,851,239 (1.50) | 415,998,537 (1.70) | 359,810,915 (1.47) | 362,780,872 (1.49) |
| brainless | 780,957,231 | 1,568,789,093 (2.01) | 2,036,819,737 (2.61) | 1,972,244,682 (2.53) | 1,345,345,869 (1.72) | 1,891,893,508 (2.42) | 1,239,028,920 (1.59) |
| geomean | | 1.88 | 1.67 | 1.50 | 1.45 | 1.41 | 1.30 |

Calls, DOVAR and DODOES, each a share of the design's dispatches:

| program | smallest | least-memory | portable-small | portable-knee | portable-arm | portable-fastest |
|---|---:|---:|---:|---:|---:|---:|
| sim16 | 22.6 / 10.5 / 0.0 % | 24.0 / 10.7 / 0.0 % | 25.6 / 14.0 / 0.0 % | 22.9 / 10.7 / 0.0 % | 25.6 / 14.0 / 0.0 % | 25.2 / 13.8 / 0.0 % |
| gc16 | 20.7 / 6.2 / 0.0 % | 24.9 / 7.1 / 0.0 % | 24.3 / 8.1 / 0.0 % | 21.9 / 7.5 / 0.0 % | 23.2 / 8.4 / 0.0 % | 23.4 / 8.5 / 0.0 % |
| scan | 21.0 / 12.9 / 0.0 % | 25.4 / 16.3 / 0.0 % | 25.8 / 18.0 / 0.0 % | 24.6 / 16.6 / 0.0 % | 25.8 / 18.1 / 0.0 % | 26.0 / 18.3 / 0.0 % |
| evo | 15.2 / 2.0 / 0.0 % | 19.9 / 2.9 / 0.0 % | 19.2 / 3.0 / 0.0 % | 14.3 / 3.4 / 0.0 % | 14.5 / 3.5 / 0.0 % | 14.6 / 3.5 / 0.0 % |
| wordfreq | 16.0 / 2.0 / 0.0 % | 18.6 / 2.6 / 0.0 % | 18.3 / 2.7 / 0.0 % | 16.4 / 3.4 / 0.0 % | 14.7 / 3.2 / 0.0 % | 16.4 / 3.6 / 0.0 % |
| minif | 21.4 / 7.7 / 0.0 % | 22.6 / 8.2 / 0.0 % | 23.6 / 9.5 / 0.0 % | 22.4 / 8.4 / 0.0 % | 23.9 / 9.7 / 0.0 % | 23.7 / 9.6 / 0.0 % |
| brainless | 20.3 / 0.6 / 3.2 % | 15.5 / 0.5 / 2.5 % | 15.4 / 0.5 / 2.6 % | 21.5 / 0.5 / 3.8 % | 15.2 / 0.4 / 2.7 % | 23.1 / 0.6 / 4.1 % |

A DOVAR is a data word's call returning its address: CV8 runs `var @` as one VAR@ where the designs run three (the
call, DOVAR, @). A DODOES on brainless is mostly a VALUE's fetch, about five dispatches (the call, DODOES, CELL+, @,
the return) where relf's VAR@ is one. Dispatch counts are not times: each design's dispatch costs differently.

## What the JIT leaves (lab/evolve/jitapps.py; the full benchmarks)

| design | program | dispatches, JIT off | left by the JIT | left |
|---|---|---:|---:|---:|
| fastest-x86-64 | sim16 | 2,601,559,329 | 155,604 | 0.0 % |
| fastest-x86-64 | scan | 1,952,193,148 | 28,975,300 | 1.5 % |
| fastest-x86-64 | brainless | 2,039,385,085 | 1,844,184,655 | 90.4 % |
| best-all-round | sim16 | 2,542,629,528 | 156,648 | 0.0 % |
| best-all-round | scan | 1,885,742,970 | 6,511,609 | 0.3 % |
| best-all-round | brainless | 1,359,127,693 | 1,172,124,616 | 86.2 % |

On brainless, the root causes of the dispatches left:

- fastest-x86-64: DODOES without stencils 33.7 %, the return stack's order 11.7 % (VALUE's DOES> code, 10.3 % in
  itself), a stencil not usable 1.3 %, and 52.9 % in words with no refusal of their own (jitapps.py's "translated or
  never reached").
- best-all-round: DODOES 53.1 %, the return stack's order 18.0 % (VALUE's DOES> code 16.2 %), 25.9 % in words with
  no refusal of their own.

The refused words carrying most are brainless's evaluation and move generation (S-DELTA-EVAL, the threat words,
MY-PIECE?, the move generator), each for a DOES> word it calls.

## The whole system for one application (bytes: the engine as packed, the kernel image, brainless's code)

| system | engine | kernel image | brainless's code | together |
|---|---:|---:|---:|---:|
| s6 | 28,680 | 9,265 | 43,572 | 81,517 |
| smallest | 4,912 | 8,971 | 43,420 | 57,303 |
| least-memory | 8,192 | 9,638 | 42,404 | 60,234 |
| portable-small | 9,416 | 9,183 | 42,108 | 60,707 |
| portable-knee | 10,712 | 9,049 | 42,228 | 61,989 |
| portable-arm | 13,320 | 9,202 | 42,140 | 64,662 |
| portable-fastest | 16,536 | 9,706 | 42,501 | 68,743 |
| best-all-round | 29,940 | 8,354 | 49,003 | 87,297 |
| small-jit | 20,588 | 8,718 | 45,705 | 75,011 |
| fastest-x86-64 | 29,332 | 9,774 | 49,444 | 88,550 |
| fastest-x86-32 | 33,428 | 8,802 | 49,100 | 91,330 |
| relf64 (dynamic) | 49,456 | 10,808 | 38,560 | 98,824 |
| relfasm64 | 17,912 | 10,808 | 36,915 | 65,635 |
| gforth-fast (dynamic, its image not counted) | 226,936 | - | 166,912 | 393,848 |

At 4-byte cells: smallest 53,379, the knee 58,509, portable-fastest 64,799, the JIT designs 71,599-86,402, relf32
(dynamic) 81,707.

## Design against design (Spearman, the ten designs)

| | 8-byte | 4-byte |
|---|---:|---:|
| the kernel image's bytes (the size score's image) against application code | -0.21 | -0.33 |
| engine and image (the size score) against engine and brainless's code | 0.99 | 0.99 |
| the speed score (speed, speed32) against these programs' geomean | 0.99 | 0.96 |

## Caveats

- **A shared VM.** Times are medians of 5 interleaved rounds, and a single program's figure moves by a few per
  cent. The geomeans and the dispatch counts are steadier.
- **The preludes differ where the systems do.** relf runs a dozen words in Forth that are primitives or kernel words
  elsewhere (2>R, 2R>, PARSE-NAME and others), which costs it a little on brainless. Its VALUE is
  `CREATE , DOES> @`, which its compiler turns into VAR@, where the lab's coreext.4 VALUE keeps a kind cell. That
  is part of the gap, but in the library rather than the engine.
- **Engines are built as each system builds them**: the designs by their Makefiles, relf64 and relf32 with cc -O2
  and dynamically linked.
- **Seven programs**, four of them the lab's own selection's. brainless is 81 % of the code and the one large
  program; minif and wordfreq are small.
- **Dispatches** are counted only on the interpreted designs: native code dispatches nothing.

## Reproducing

    python3 lab/evolve/genapps.py --cells 8          # about 7 minutes; build/genapps/results-8.json
    python3 lab/evolve/genapps.py --cells 4          # results-4.json (needs the forth32 engines)
    python3 lab/evolve/genapps-report.py build/genapps/results-8.json build/genapps/results-4.json
    python3 lab/evolve/genapps-dispatch.py           # after --cells 8: the dispatch tables
    python3 lab/evolve/genapps-constructs.py --cells 8   # and --cells 4: the construct tables
    python3 lab/evolve/genapps-constructs.py --census portable-knee   # brainless's definitions by kind
    python3 lab/evolve/jitapps.py c7c35f9c97 06b188f45b --db DB --zip ZIP --apps sim16,scan,brainless
      # DB: designs/NAME/record.json's id and genome, a JSON line each
      # ZIP: lab/evolve/apps/brainless's files as x/brainless/NAME

gforth-fast from apt (gforth 0.7.3). Every system's result line is checked to be the same, and genapps.py stops
if one differs.
