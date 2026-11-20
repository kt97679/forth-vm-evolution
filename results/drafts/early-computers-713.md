# What the early computers lend the search (Iteration 713, the owner's idea)

The owner: "another deep dive into best practices on the early computers ... they used a lot of tricks to improve
performance and fit into limited resources, maybe you can find something we can reuse." The early games' dive
(`results/drafts/early-games-713.md`) had found nearly everything already here, so this one went past the
instruction-set tricks to the period's other discipline: **memory as the pages a program touches** - Denning's
working set (1968), program restructuring for paging (Hatfield and Gerald, IBM Systems Journal 1971), the overlay
linkers and the 8051's data overlaying (locals of functions never active together share one area), VAX/VMS's
demand-zero pages. Our memory objective is exactly that count (cputime's MINFLT, a page each), so each idea was
priced by reading which pages a run's mappings hold (`/proc/PID/smaps`, polled until exit) and then counting
faults with the idea tried.

## 1. Found and built: the JIT translator's frame - 10-19 pages of every JIT design (`jitfew`, queued)

Polling smaps at a workload's end showed the JIT designs' C stack at 52-108 KB on the kernel workload (start-up:
4-8 KB) - c7c35f9c97 60 KB, 9b15ba26f7 108 KB. The cause is `jit_body` (engine/jit.c): its arrays `at`, `arg`
(1,025 and 1,024 cells), `nat` (1,025 x 4 bytes), `opl` (1,024 x 2), `tl` (1,024) - a 23,752-byte frame (objdump:
`sub $0x5cc8,%rsp`) - and it recurses into each untranslated callee (`depth + 1`, up to 16) with the caller's
frame still live. A word of 40 operations writes only the first 40 entries of each array, but each array's head
is on a page of its own, so every depth costs ~5 pages and the stack keeps them. The arrays are the early linkers'
problem in reverse: storage sized for the worst case at every level, where they shared one area sized for the
need.

How the cost was confirmed: JIT_MAXOPS 1024 -> 128 in a scratch engine (every array 8x shorter): c7c35f9c97's
corpus 71 -> 54 pages, c6f1c1331b's 59 -> 44, the outputs alike; 782f3ad7ff (no JIT) unchanged.

**The gene jitfew** (results/queued-genes/jitfew-after-seed96.patch, after jitdead and fixenv): jit_body keeps
arrays of JIT_FEWOPS = 128 operations in its own frame (3 KB) and calls the body (`jit_body_`, the arrays now its
parameters); a word with more operations - the decoding is the only place that can run out, before anything is
emitted or a callee translated - answers JIT_ROOM, and `jit_body_big` (cold) translates it again from its start in
1,024-entry arrays. The translation is the same word for word; only where its scratch lives changes. Off, the
engine is the one before (the old declarations under `#else`).

Tested on top of the queue (both patches applied), eight JIT designs from chain B's list, gene off and on, five
interleaved rounds, medians (`results/drafts/jitfew-test-713.py ROOT IDS 5 LIST`):

| design | memory, pages (max over the selection but apps) | apps, pages | engine, bytes | outputs |
|---|---|---|---|---|
| c7c35f9c97 (fast64) | 72 -> 56 (-22 %) | 173 -> 146 | 27,492 -> 27,860 (+368) | alike |
| c6f1c1331b (smalljit) | 60 -> 46 (-23 %) | 161 -> 136 | 18,740 -> 19,204 (+464) | alike |
| 9b15ba26f7 | 79 -> 63 (-20 %) | 183 -> 156 | 33,256 -> 33,624 (+368) | alike |
| 3dd824e8ae | 59 -> 45 (-24 %) | 160 -> 136 | 18,996 -> 19,540 (+544) | alike |
| d8f72aa60f | 49 -> 39 (-20 %) | 140 -> 125 | 14,276 -> 14,500 (+224) | alike |
| bfc83686a9 | 44 -> 39 (-11 %) | 134 -> 127 | 19,060 -> 19,364 (+304) | alike |
| 4b6ca4aaf8 | 43 -> 38 (-12 %) | 132 -> 125 | 16,244 -> 16,660 (+416) | alike |
| ec331aea6e | 43 -> 38 (-12 %) | 132 -> 125 | 16,244 -> 16,660 (+416) | alike |

Memory -20 to -64 KB, the engine +224 to +544 bytes (0.5-1.2 % of these designs' totals): a trade between two
objectives, so a gene (GOALS.md: a mechanism goes behind a gene), the search to weigh it. Time: every workload
within the noise of five rounds (-7.7 to +6.6 %, medians near 0; the kernel workload -0.4 to -3.7 % on six of
eight - fewer faults). engines-check.py's three new variants (jitfew; without jitx; with jitdead, jitexec,
jitmul, jitcfa) - see the result line in PROGRESS.md.

Priced on the way and not kept:
- **A lower cap** (JIT_MAXOPS 256 or 128, nothing else): memory -9 to -17 pages, the engine 0 or -64 bytes, but a
  word past the cap stays bytecode - Iteration 488 raised the cap from 256 to 1,024 for cd16sim's PROCESS and
  fcp's long words. The same pages without that cost is what jitfew is.
- **Variable-length arrays** sized by a run-time cap in one inlined body: +256 to +336 bytes on five designs, but
  +4.3 KB on 9b15ba26f7 (GCC stopped inlining jit_init and jit_fuse) and its pages unmoved.
- **-fno-stack-clash-protection** (Ubuntu's GCC has the protection on): no probe loop in these engines' code -
  Iteration 228's load_image was the only one, and that frame went static then - pages within 2, bytes 0 to -32.

## 2. Priced, not proposed: FILL 0 by demand-zero pages

VAX/VMS added a page "zeroed on demand": nothing is written until the program writes. Linux does the same for
private anonymous memory, and madvise(MADV_DONTNEED) returns a range to that state. The kernel workload's
cross.4 does `CREATE IMAGE 40000 ALLOT  IMAGE 40000 0 FILL` over fresh dictionary memory - ten pages written with
zeros. Removing the FILL entirely (the most a demand-zero FILL could save) moved fb0d57c8a2's kernel workload 27 ->
25 pages and c7c35f9c97's 58 -> 55: the metacompile writes most of IMAGE anyway. Time: FILL is an opcode (memset)
in these designs, the difference in the noise (-1.9 to +2.6 %). A system call in the engine, and a check that the
range is the dictionary's own anonymous mapping (on the engine's .data a DONTNEED would bring back the file's
bytes), for 8-12 KB on one workload - not worth a mechanism.

## 3. Priced by estimate, not built: the image mapped from its file

Multics' shared procedure segments, and every modern loader: map the code, copy a page only when it is written.
The engine reads the image into its dictionary mapping (vm-lab.c: mmap, then read), so each image page is
written once at start-up. The images are 9.6-9.7 KB - three pages; mapped privately from the file, the read-only
ones would come in at one fault and only the pages written would be copied. At most 1-2 pages a design, and a
page-aligned image format to make it possible. Not worth it at this image size.

## 4. Checked against the register: already here

- **Mesa's statistically-built byte code** (Sweet and Sandman, ASPLOS 1982 - push immediate the commonest
  instruction, about half of the immediates zero, most of the rest small): CV8's lit0, lit1, litm1, lit8; the
  tag's one-byte codes for the most used words (layout.py, by the reference counts).
- **Smalltalk-80's operand-in-opcode groups and 32 special selectors** (push temp 0-15 in one byte; + - < > ...
  sent without a literal): CV8's one-byte primitives; one-byte calls in the pairs' slots (register row); Forth's
  kernel has no locals to number.
- **The Transputer's prefix bytes** (pfix/nfix building an operand four bits at a time): CV8's literal and call
  widths; short branches priced this iteration (`early-games-713.md`).
- **BCPL's INTCODE and Cintcode** (compact interpretive code, about half the size of machine code): the byte
  code itself.
- **The B5000's A and B registers** (the top of the stack in two registers, spilled only when both are full):
  the tos gene, multi-state caching, the JIT's stack cache (jitk).
- **The IBM 650's SOAP** (each instruction placed where the drum would be when the last one finished): alignhot,
  the handler order, the profile-guided build (register row).
- **The AGC's interpreter** (interpretive code: more function in the same core, at a cost in time): the whole
  design space - the smallest designs are that trade.
- **Overlays and program restructuring** (code needed together on one page): engine text is file-backed, and the
  kernel maps a fault's neighbouring cached pages with it (fault-around), so code order moves little of a run's
  fault count; the writable data's layout (fixed data layout, register row, proposed) is where order counts.

## A trap met on the way

A scratch clone whose build/ is a link to the sandbox's build writes through it: evolve.setup copies forth/'s
overlays into build/work, where each is a link to the sandbox's forth/ file (`shutil.copy` follows it). At the same
commit the bytes are equal and only the mtimes change - and then the sandbox's evolve.py refuses ("build/ is older
than its sources"); with a changed overlay in the clone it would write that change into the sandbox. Here: the
files touched back after each run (`git status` clean throughout); a clone with its own build would avoid it.

## Sources

- P. J. Denning, The working set model for program behavior (SOSP 1967; CACM 1968):
  https://cs.uwaterloo.ca/~brecht/courses/epfl/Possible-Readings/vm-and-gc/working-set-model-denning-sosp-1967.pdf
- D. J. Hatfield and J. Gerald, Program restructuring for virtual memory, IBM Systems Journal 10(3), 1971:
  https://doi.org/10.1147/sj.103.0168
- The 8051's L51 linker, data RAM overlaying: https://courses.cs.washington.edu/courses/cse477/00sp/docs/c51primer/c08.htm
- Overlay (programming): https://en.wikipedia.com/wiki/.OVR
- VAX/VMS demand zeroing (OSTEP): https://www.educative.io/courses/operating-systems-virtualization-concurrency-persistence/N825WAxyyj8
- Bensoussan, Clingen, Daley, The Multics virtual memory: https://courses.cs.washington.edu/courses/cse451/20wi/readings/MulticsVM.pdf
- Sweet and Sandman, Empirical analysis of the Mesa instruction set (ASPLOS 1982):
  https://xeroxparcarchive.computerhistory.org/ivy/sweet/papers/sasplos/.Analysis.bravo!1.html;
  notes: https://homepage.cs.uiowa.edu/~jones/arch/spring03/notes/18alto.html
- Smalltalk-80 (the Blue Book), chapter 26: https://archive.esug.org/HistoricalDocuments/Smalltalk80/BlueBookImplementation/bluebook_chapter26.html
- The Transputer's prefix functions (INMOS technical note 21): https://transputer.net/tn/21/tn21.html
- M. Richards, INTCODE (1975): https://www.softwarepreservation.org/projects/BCPL/cambridge/Richards-Intcode_for_BCPL-1975.pdf;
  the Cintcode design: https://www.cl.cam.ac.uk/~mr10/bcplman.pdf
- The Burroughs stack architectures: https://homepage.cs.uiowa.edu/~jones/arch/notes/11burroughs.html
- SOAP for the IBM 650: https://en.wikipedia.org/wiki/Symbolic_Optimal_Assembly_Program
- The AGC's interpreter (yaYUL's manual): https://www.ibiblio.org/apollo/assembly_language_manual.html

## The measuring scripts

`results/drafts/jitfew-test-713.py` (the gene off and on, interleaved: time, pages, outputs, bytes) and
`results/drafts/stack-pages-713.py` (pages per workload, the outputs hashed - run from a root, so a clone's engine
sources are measured). Both take the root first and a list file last. The gene's patch was made with a script on a
clone with the queue applied; the other pricing runs (the FILL, the caps, smaps at a workload's end) were one-off
scratch scripts, their numbers above.
