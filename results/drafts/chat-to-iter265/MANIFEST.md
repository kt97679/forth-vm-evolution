# Files from the chat that ended at Iteration 265 - MANIFEST

Packed 2026-10-13 21:45 UTC on that chat's machine. Everything here is **as found**: copied, not rewritten; nothing reconstructed from memory. Where a figure came from a file that was later changed in place, that is said below.

## 1. Scripts that produced figures recorded in PROGRESS.md, Iterations 244-265 (`scripts/`)

| original path | iteration | figure | status | in the archive |
|---|---|---|---|---|
| `/tmp/disp.py` | 241-244 | dispatch counts of the smallest design (add5ec8937): corpus, kernel, parse, fib and NEXT-NFA8 - Iteration 242's corpus 58.90M (seed 45's code 58.95M, master 63.43M); Iteration 244's kernel 9.14M (all-thread walk) -> 8.66M (one thread), option B corpus 58.75M, kernel 8.53M | as found | `scripts/disp.py` |
| `/tmp/sz2.py` | 244 | engine + image sizes of six designs: primitives-first alone, bit-7 option A (+32 bytes on byte-header designs) and option B (-64 to -136) | as found | `scripts/sz2.py` |
| `/tmp/t6.py` | 244 | coreext.4's >NAME on two designs: DUP, a UTF-8 name, :NONAME found as (NONAMEn) | as found | `scripts/t6.py` |
| `/tmp/bis.py` | 244 | debugging, no recorded figure: bisected cross32.4 to its first failing line (83, REPEAT) under the new POSTPONE | as found | `scripts/bis.py` |
| `/tmp/rs4.sh` | 244 | debugging, no recorded figure: built the 32-bit kernel from the old and the new seed by hand | as found | `scripts/rs4.sh` |
| `/tmp/gate46c.py` | 244 | the gate over seed 45's front and the joint front for the bit-7 patch (128 of 128) | as found | `scripts/gate46c.py` |
| `/tmp/jitdis.py` | 245 | built 28677d13b1's engine to disassemble st_call and st_exit (eight instructions a call and return) | as found | `scripts/jitdis.py` |
| `/tmp/tt.py` | 246 | jittail first trial: ackermann and fib output and wall time; a 3-million-deep tail recursion (overflow without the gene, 0 with it) | as found | `scripts/tt.py` |
| `/tmp/tt2.py` | 246 | jittail CPU times, not alternated (ackermann x600 241.5 -> 229.0 ms, a later run 95.0 vs 98.1) - the '-5%, then +3%' of Iteration 246 | as found | `scripts/tt2.py` |
| `/tmp/tt3.py` | 246 | ackermann x2000 alternated over 15 rounds: medians 379.6 -> 310.2 ms (-18%), minima 315.3 -> 266.6 ms (-15%) | as found | `scripts/tt3.py` |
| `/tmp/tt4.py` | 246 | six selection workloads alternated over 9 rounds (corpus 0.923, fib 1.133, loop 1.023, bubble 1.010, ackermann 0.840; its kernel run was broken) | as found | `scripts/tt4.py` |
| `/tmp/tt5.py` | 246 | fib and corpus over 25 alternated rounds (ratios 1.007 and 0.994) | as found | `scripts/tt5.py` |
| `/tmp/tt6.py` | 246 | jittail built without jitx, without jitloop and with jitos; ackermann and the deep recursion on each | as found | `scripts/tt6.py` |
| `/tmp/mkjt.py` | 246 | two jittail genomes written to a temporary results file for ans-check (14 of 14 each) | as found | `scripts/mkjt.py` |
| `/tmp/ansjt.py` | 246 | a first ans-check wrapper with injected genomes - found 0 designs (ans-check reads results files); superseded by mkjt.py, no figure | as found | `scripts/ansjt.py` |
| `/tmp/dz.py` | 247 | engines with and without DIV0_CHECK (add5ec8937 +160; cc6d168e0a, 28677d13b1, f20de05a64 +96) | as found | `scripts/dz.py` |
| `/tmp/facts46.py` | 248 | seed 46's facts (statuses, children by how made, the attic, the front by thirds, genes on the front, repeat rates) | as found | `scripts/facts46.py` |
| `/tmp/died46.py` | 248 | the 222 'engine did not compile' deaths against the living, by gene | as found | `scripts/died46.py` |
| `/tmp/died46b.py` | 248 | all 222 had tail=1; no living design had tail | as found | `scripts/died46b.py` |
| `/tmp/tailfail.py` | 248 | reproduced cb0545f94f's compile failure (the dispatch offsets in the tail engine) | as found | `scripts/tailfail.py` |
| `/tmp/tailfail2.py` | 248 | cb0545f94f with the fix: built (engine 10,632, image 8,433) and ran the corpus | as found | `scripts/tailfail2.py` |
| `/tmp/gate47.py` | 248, 252 | the gate over seed 46's front and the joint front (148 of 148) | as found | `scripts/gate47.py` |
| `/tmp/hist.py` | between 248 and 253 | the progress charts: per seed, the fastest speed and the smallest sizes from the results files | as found | `scripts/hist.py` |
| `/tmp/epi.py` | 250 | gene interactions from seed 46's mutations (rtloop -0.40 / -0.98 log speed without / with the JIT; ipaclone t 6-8); copied into the repository as lab/evolve/gene-interactions.py | as found | `scripts/epi.py` |
| `/tmp/gd.py` | 251-252 | guard 0/1 sizes and `0 @` with output to a pipe on 3456ac1e5e, fe3c9c3940, 3bb2087f9d (guard +448 / +256 / -32; the handler +384, then +192 / +160 / +128, then +160 / +128 / +128) | as found | `scripts/gd.py` |
| `/tmp/gd2.py` | 257 | the same on the scratch tree with lean-open (7,168 / 16,828 / 21,276) | as found | `scripts/gd2.py` |
| `/tmp/cm.py` | 254 | built 3456ac1e5e with the converter's call map (build/evolve/cm.map) that factor.py, nib.py and lz2.py read | as found | `scripts/cm.py` |
| `/tmp/factor.py` | 254 | greedy factoring into helper words. AS FOUND it is the exact-bytes version - the 12-byte figure (4 helpers); the 146-byte figure came from its opcode-name version, which this file replaced in place (not preserved) | as found | `scripts/factor.py` |
| `/tmp/kprof.py` | 255 | the fastest design's kernel and corpus workloads by word, without the JIT (1,732,919 dispatches, 56.2% in run-time words) | as found | `scripts/kprof.py` |
| `/tmp/kprof2.py` | 255 | the same on /tmp/ansall with cross.4's fast path (1,091,259, -37%) | as found | `scripts/kprof2.py` |
| `/tmp/kt.py` | 255 | the kernel workload on 3bb2087f9d with the JIT, master against the fast path, alternated over 15 rounds (2.8 -> 2.5 ms) | as found | `scripts/kt.py` |
| `/tmp/sz3.py` | 256 | the smallest engine's largest symbols (virtual_machine 3,448, main 791, the tables 512 each, ...) | as found | `scripts/sz3.py` |
| `/tmp/lto.py` | 258 | -flto on three designs (7,112 -> 7,040; 16,828 -> 16,476; 21,276 -> 20,764) | as found | `scripts/lto.py` |
| `/tmp/lto2.py` | 258 | LTO timed: the JIT stopped translating (fib 2.5x, loop 3.9x slower); interpreted within noise | as found | `scripts/lto2.py` |
| `/tmp/nib.py` | 258 | runs of the 15 commonest one-byte operations packed two to a byte: 27 bytes | as found | `scripts/nib.py` |
| `/tmp/march.py` | 258 | -march=x86-64-v3: engines +32, -32, +224 | as found | `scripts/march.py` |
| `/tmp/jk1.py` | 259 | jitk 0/2/3 builds of 3bb2087f9d: 21,244 / 23,516 / 24,028 bytes; corpus and hand tests | as found | `scripts/jk1.py` |
| `/tmp/jk2.py` | 259 | jitk timed over 11 rotating rounds (fib 1.163 / 1.002, loop 0.907 / 0.971, bubble 0.954 / 0.955, ackermann 0.986 / 1.014, corpus 0.956 / 0.967) | as found | `scripts/jk2.py` |
| `/tmp/lz.py` | 260 | a byte-level LZ77 parse of the smallest design's code (714 bytes at a 3-byte echo, 886 at 2) | as found | `scripts/lz.py` |
| `/tmp/lz2.py` | 260 | the echo on whole instructions, no branch, target or return-stack word (283 / 427 bytes) | as found | `scripts/lz2.py` |
| `/tmp/gd3.py` | 260 | max-goto-duplication-insns at its default, 0, 32, 128 (3456ac1e5e 7,112 / 7,304 / 7,816 / 7,880) | as found | `scripts/gd3.py` |
| `/tmp/lt.py` | 260 | lto with the stencils outside it: -32 / -160 bytes; fib and loop on 3bb2087f9d | as found | `scripts/lt.py` |
| `/tmp/cl.py` | 261 | five designs with gcc and with clang 18 through a cc symlink (interpreted 9,408-9,440; the JIT designs failed on -fipa-cp-clone) | as found | `scripts/cl.py` |
| `/tmp/cl2.py` | 261 | clang with the GCC-only flags left out (10,256 / 17,868 / 25,788, the JIT translating) and at -Oz (the link failed) | as found | `scripts/cl2.py` |
| `/tmp/cl3.py` | 261 | found -Oz's link error (undefined bcmp) | as found | `scripts/cl3.py` |
| `/tmp/cl4.py` | 261 | clang -Oz on the scratch tree with lean-open (8,624 / 17,772 / 20,396) | as found | `scripts/cl4.py` |
| `/tmp/os.py` | 262 | GCC -O2 against -Os for the smallest design - stopped by the 120 s timeout: no figure | as found | `scripts/os.py` |
| `/tmp/factor0.py` | 263 | headerless factoring with 2-byte calls: 154 bytes (40 helpers) | as found | `scripts/factor0.py` |
| `/tmp/factor1.py` | 263 | headerless factoring with 1-byte calls: 359 bytes | as found | `scripts/factor1.py` |
| `/tmp/dz2.py` | 263 | the zero-divisor trim: 7,200 / 16,796 / 21,212 / 7,232 bytes; -10 still caught | as found | `scripts/dz2.py` |
| `/tmp/tokfill.txt` | 264 | data: an excerpt of tools/layout.py (lines 280-300) read for the factor plan | as found | `scripts/tokfill.txt` |

The scripts import the repository's evolver from `/home/claude/forth-vm-evolution/lab/evolve` (or a scratch tree's, `/tmp/mo`, `/tmp/b46b`...) and read build outputs such as `build/evolve/cm.map`; they were run as the user claude. `factor0.py` and `factor1.py` are `factor.py` with its `HDR, CALL` line changed (0, 2 and 0, 1).

## 2. The check jobs and their logs, Iterations 244-262 (`jobs/`, `logs/`)

`job53.sh`-`job77.sh` ran the checks in the background (run-tests, validate, the gate, ans-check, outbuf, readline); `jNN*.log` is what each wrote. As found - some jobs died at a turn's end and were rerun under a higher number, so a log may stop short.

jobs: `job58.sh`, `job59.sh`, `job60.sh`, `job64.sh`, `job65.sh`, `job66.sh`, `job67.sh`, `job68.sh`, `job69.sh`, `job70.sh`, `job71.sh`, `job72.sh`, `job73.sh`, `job74.sh`, `job75.sh`, `job76.sh`, `job77.sh`

logs: `j53-reseed.log`, `j54-build.log`, `j55-build.log`, `j56-build.log`, `j56-reseed.log`, `j57-build.log`, `j57-reseed.log`, `j58-rt.log`, `j58.log`, `j59-ans.log`, `j59-ob.log`, `j59-rl.log`, `j59.log`, `j60-ans.log`, `j60-build.log`, `j60-ob.log`, `j60-rl.log`, `j60-rt.log`, `j60.log`, `j61-ans.log`, `j62-rt.log`, `j63-build.log`, `j64.log`, `j65-ans.log`, `j66-rt.log`, `j67-rt.log`, `j67.log`, `j68-ans.log`, `j69-ans.log`, `j70-build.log`, `j70-rt.log`, `j70.log`, `j71.log`, `j72-ans.log`, `j72-rt.log`, `j72.log`, `j73-ans.log`, `j74-rt.log`, `j74.log`, `j75-rt.log`, `j75.log`, `j76.log`, `j77-ans.log`, `j77-rt.log`, `j77.log`

## 3. Patches made in /tmp (`patches/`)

As found. Those of the after-seed-44 to after-seed-47 batches are also in the repository (`results/applied-after-seed4N/`, `results/pending/`); `crossfast.patch` is `results/drafts/crossfast.patch`.

`buildgenes-after-seed47.patch`, `cellnames-after-seed45.patch`, `check5.patch`, `compiler-after-seed47.patch`, `crossfast.patch`, `dispoff-after-seed45.patch`, `divzero-after-seed44.patch`, `divzero-spn-after-seed45.patch`, `faulttrap-after-seed47.patch`, `fbufslots-after-seed44.patch`, `fsys5fast-after-seed43.patch`, `fsysread-after-seed44.patch`, `jitk-after-seed47.patch`, `jitos-after-seed45.patch`, `jittail-after-seed46.patch`, `lean-open-after-seed47.patch`, `names-after-seed45.patch`, `nobit7-after-seed46.patch`, `primfirst-after-seed46.patch`, `stackheads-after-seed44.patch`, `tailfix-after-seed46.patch`, `tty-after-seed45.patch`, `writeline-after-seed44.patch`

## 4. Scratch git trees in /tmp (`trees/<name>/`)

Per tree: `uncommitted.patch` (`git diff HEAD --binary`), `commits-past-clone.patch` where the tree has commits of its own (`git format-patch` from its clone point - none of these is in master; their content reached master as the patches in section 3), `untracked/` where there were untracked files, `STATUS.txt`. The `fresh*` trees are fresh-clone checks: a clone of master with the pending batch applied - their uncommitted changes are those patches.

| tree | HEAD | status entries | diff bytes | commits past clone | untracked |
|---|---|---|---|---|---|
| `/tmp/ansall` | 8953d4c Iteration 253: lab/evolve/progress-table.py and results/progress-by-run.md - every run's extremes, for the progress charts | 1 | 1014 | 0 | 0 |
| `/tmp/b44` | 6628c73 Iteration 224: the hidden-names findings captured in GOALS.md's register, deferred by the owner | 2 | 4275 | 0 | 0 |
| `/tmp/b44s` | 34814fc scratch: stackheads | 10 | 19245 | 4 | 0 |
| `/tmp/b45` | 57ef97e scratch: patch 5 (dispoff) | 3 | 9609 | 2 | 0 |
| `/tmp/b46` | 0470c07 scratch: primfirst | 8 | 27940 | 1 | 0 |
| `/tmp/b46b` | 5bd981a scratch: jittail | 1 | 1155 | 3 | 0 |
| `/tmp/b46c` | 85fe50d scratch: nobit7 | 5 | 13832 | 2 | 0 |
| `/tmp/base45` | ea9f79d scratch: names | 12 | 24873 | 2 | 0 |
| `/tmp/batch43` | e845899 scratch: guard-after-seed43.patch applied | 5 | 22154 | 3 | 0 |
| `/tmp/cmp43` | 6437350 Iteration 217: a survey of JITs and VM speed elsewhere (results/drafts/jit-vm-survey.md) - RPyForth's named stack window, CPython's cached-register stencil variants, copy-and-patch, Liftoff, Deegen, IP-update chains; seven items ranked, each with how to price it first | 0 | 0 | 0 | 0 |
| `/tmp/ec` | c0bf29d Iteration 248: seed 46 processed (not small, hypervolume +6.4%; every tail design died - the dispatch offsets broke gen-tail, fixed); the after-seed-46 batch applied (primfirst, nobit7, jittail, tailfix; reseeded); seed 47 for 6 hours | 2 | 1155 | 0 | 1 |
| `/tmp/ff` | cbc5db9 Iteration 254: the standard suite over all of seed 46's front - 127 of 127, 0 differ | 1 | 1273 | 0 | 0 |
| `/tmp/fresh43` | 6b09fab Iteration 213: the handoff - PROGRESS.md's last entry holds the state, the routine, the owner's standing decisions, open items and lessons; the Forth collection's useful items kept in reference/forth-archive (4.8 MB, licence policy kept) | 8 | 21268 | 0 | 4 |
| `/tmp/fresh44` | 6628c73 Iteration 224: the hidden-names findings captured in GOALS.md's register, deferred by the owner | 2 | 4275 | 0 | 0 |
| `/tmp/fresh44b` | 68f504f Iteration 225: the after-seed-44 batch begun (results/pending/) - native WRITE-LINE gives back the read-ahead; the file buffers' slots kept apart from their buffers, 24-36 KB less memory on every workload for designs with full buffers; 117 of 117 native front designs alive, the suite 0 of 2 differ | 5 | 8989 | 0 | 1 |
| `/tmp/fresh44c` | 188e513 Iteration 227: the owner's guidance on kernel words, helpers and long words recorded in GOALS.md | 5 | 9577 | 0 | 1 |
| `/tmp/fresh44d` | a25960f Iteration 228: the fourth after-seed-44 patch - the image loader's 32 KB local made static: gcc's stack-clash probing had touched 8 pages at every start; with the file-buffer patch, 16 to 60 KB less memory per workload on the front's designs; all 165 alive | 14 | 28701 | 0 | 1 |
| `/tmp/fresh45` | dbdf4cb Iteration 230: seed 44 processed - small, the first (hypervolume +0.9%); the after-seed-44 batch applied and reseeded (161 of 161 front designs alive, 0 of 12 differ); NEXT-RUN seed 45 6h proposed | 5 | 5649 | 0 | 0 |
| `/tmp/fresh45b` | 3f77217 Iteration 231: the after-seed-45 batch begun - native terminal output unbuffered (the owner's rule), the SPN engine throws -10 too; 161 of 161 alive; s6's bare-kernel image confirmed size-only, as documented | 17 | 33904 | 0 | 2 |
| `/tmp/fresh45c` | 8553601 Iteration 233: packed names captured in GOALS.md's register, deferred by the owner; the cell headers' UTF-8 fault next | 24 | 87229 | 0 | 2 |
| `/tmp/fresh45d` | 8553601 Iteration 233: packed names captured in GOALS.md's register, deferred by the owner; the cell headers' UTF-8 fault next | 24 | 89120 | 0 | 2 |
| `/tmp/fresh45e` | a5e837d Iteration 236: a compressed image and engine captured in the register, not built - on-disk only (LZSS: image 8,704 -> 6,659, engine 7,680 -> 4,605 on the smallest), memory unchanged, start-up pays | 26 | 63981 | 0 | 2 |
| `/tmp/fresh45f` | 1b62ab4 Iteration 238: unused JIT stencils (50-170 bytes) and a Bloom filter (dominated by the threads gene) priced, not built; the JIT translator -Os found: -416 to -800 bytes, proposed as a gene | 27 | 73328 | 0 | 2 |
| `/tmp/fresh46` | bf966d9 Iteration 241: seed 46 for 10 hours (the owner) - about 8 hours of evolution after the comparison's reserve | 27 | 94457 | 0 | 0 |
| `/tmp/fresh47` | 96200bb Iteration 243: HANDOFF refreshed - the state (seed 46 running, the after-seed-46 batch), the owner's decisions since Iteration 213, open items, lessons | 28 | 100233 | 0 | 0 |
| `/tmp/fresh48` | 4d07e3e Iteration 245: calls and returns at the fast end priced - the JIT already uses native call/ret; the gap to C -O2 is tail calls and registers; a jittail gene proposed | 32 | 113523 | 0 | 0 |
| `/tmp/fresh49` | c93f65a Iteration 251: the stack header captured (left, the owner); output lost on a signal death measured - 114 of 127 front designs have no fault handler; the owner's call | 5 | 5583 | 0 | 0 |
| `/tmp/fresh50` | 7aba7fe Iteration 256: the routine's steps 3 and 8 as tracked tools - seed-facts.py (names a death cause's shared genes: seed 46's tail=1 found by itself) and gate.py (148 of 148 on seed 46) | 5 | 8713 | 0 | 0 |
| `/tmp/fresh51` | 8e430f4 Iteration 258: a gap check against the literature - LTO found (-1.0 to -2.4% engines; stencils must stay out), Clang the owner's call | 11 | 34653 | 0 | 1 |
| `/tmp/fresh52` | 9250cbe Iteration 262: tools/gen-jitk.py out of master - it belongs to after-seed-47 patch 3, which adds it; the compiler gene's patch filed | 11 | 38360 | 0 | 1 |
| `/tmp/mo` | 4adbdb2 scratch: compiler | 0 | 0 | 5 | 0 |
| `/tmp/p13` | 8553601 Iteration 233: packed names captured in GOALS.md's register, deferred by the owner; the cell headers' UTF-8 fault next | 16 | 33904 | 0 | 1 |

## 5. Everything else this chat left outside the repository

`/home/claude` holds only the repository and tool dot-directories (`.cache`, `.config`, `.local`, `.npm`, `.npm-global`, `.npmrc`, `.wget-hsts`) - nothing written there by this chat outside `forth-vm-evolution/`. The full listing of `/tmp` as found, not packed unless named above (330 `relf-run-*-test-*.sh` files are run-tests.sh's own and are counted, not listed):

```
dir            /tmp/__pycache__
file     1303  /tmp/alive43.py
file     1740  /tmp/ans-hidden.py
file      131  /tmp/ans43.ids
file      153  /tmp/ans47-ids.txt
dir            /tmp/ansall
file     2294  /tmp/ansall-build.log
file     1264  /tmp/ansall-ids.txt
file      430  /tmp/ansjt.py
file      873  /tmp/apt-strace.log
file     8635  /tmp/apt.log
file      762  /tmp/audit43.py
file     2295  /tmp/b-cell.log
file     2295  /tmp/b-fault.log
file     2295  /tmp/b-new.log
file     2295  /tmp/b-old.log
file     2295  /tmp/b-restore.log
file     2295  /tmp/b43-build.log
dir            /tmp/b44
dir            /tmp/b44s
file     2292  /tmp/b44s-build.log
dir            /tmp/b45
dir            /tmp/b46
dir            /tmp/b46b
dir            /tmp/b46c
dir            /tmp/base45
dir            /tmp/batch43
file      696  /tmp/bis.py
file     2314  /tmp/build-stages.log
file    12128  /tmp/buildgenes-after-seed47.patch
dir            /tmp/c46
dir            /tmp/cb
file      289  /tmp/cbtime.sh
file    18648  /tmp/cc96QpP6.o
file    12288  /tmp/ccbbxKrq.s
file    24873  /tmp/cellnames-after-seed45.patch
dir            /tmp/cf43
dir            /tmp/cf44
dir            /tmp/cf45
file    12333  /tmp/check5.patch
file     1067  /tmp/cl.py
file     1629  /tmp/cl2.py
file      978  /tmp/cl3.py
file     1597  /tmp/cl4.py
file     9866  /tmp/clang-install.log
dir            /tmp/clangbin
file      667  /tmp/cm.py
dir            /tmp/cmp43
file    13165  /tmp/compiler-after-seed47.patch
file     1273  /tmp/crossfast.patch
file      332  /tmp/dbg.txt
file     2620  /tmp/diag.py
file     3578  /tmp/diag2.py
file     1070  /tmp/died46.py
file     1042  /tmp/died46b.py
file     1306  /tmp/disp.py
file    12333  /tmp/dispoff-after-seed45.patch
file     9624  /tmp/divzero-after-seed44.patch
file     1992  /tmp/divzero-spn-after-seed45.patch
file     1288  /tmp/dz-designs.py
file      429  /tmp/dz.py
file      179  /tmp/dz.txt
file      642  /tmp/dz2.py
dir            /tmp/ec
file      446  /tmp/elf.py
file      464  /tmp/eng-id.py
dir            /tmp/engA
dir            /tmp/engB
dir            /tmp/engB2
dir            /tmp/engC
dir            /tmp/engD
dir            /tmp/engE
dir            /tmp/engF
dir            /tmp/engG
dir            /tmp/engH
dir            /tmp/engI
dir            /tmp/engJ
dir            /tmp/engK
dir            /tmp/engL
dir            /tmp/engM
file     3283  /tmp/epi.py
file   137496  /tmp/evolve.py.cell
file   137543  /tmp/evolve.py.new
file   137523  /tmp/evolve.py.old
file     3537  /tmp/factor.py
file     3444  /tmp/factor0.py
file     3444  /tmp/factor1.py
file     4654  /tmp/facts43.py
file     5397  /tmp/facts46.py
file     5583  /tmp/faulttrap-after-seed47.patch
file     1504  /tmp/fbufslots-after-seed44.patch
file     2249  /tmp/fc-cell.log
file      398  /tmp/fc-run.sh
file     1504  /tmp/fc1.log
file     9863  /tmp/fc2.log
file        7  /tmp/fc2.log.done
file    14237  /tmp/fc3.log
dir            /tmp/ff
file      180  /tmp/ff-reseed.log
file     4708  /tmp/file-sysc5.4.cell
file     4451  /tmp/file-sysc5.4.new
file     3672  /tmp/file-sysc5.4.orig
file      180  /tmp/fresh-reseed.log
file      180  /tmp/fresh-reseed2.log
dir            /tmp/fresh43
dir            /tmp/fresh44
dir            /tmp/fresh44b
dir            /tmp/fresh44c
dir            /tmp/fresh44d
dir            /tmp/fresh45
dir            /tmp/fresh45b
dir            /tmp/fresh45c
dir            /tmp/fresh45d
dir            /tmp/fresh45e
dir            /tmp/fresh45f
dir            /tmp/fresh46
file      180  /tmp/fresh46-reseed.log
dir            /tmp/fresh47
file      180  /tmp/fresh47-reseed.log
dir            /tmp/fresh48
file      180  /tmp/fresh48-reseed.log
dir            /tmp/fresh49
dir            /tmp/fresh50
dir            /tmp/fresh51
dir            /tmp/fresh52
file     4338  /tmp/fs3-good.4
file     5033  /tmp/fsys-count.py
file    22154  /tmp/fsys5fast-after-seed43.patch
file     5520  /tmp/fsysread-after-seed44.patch
file      565  /tmp/gate44.py
file      601  /tmp/gate44b.py
file      689  /tmp/gate44c.py
file      550  /tmp/gate44d.py
file      980  /tmp/gate45.py
file     1003  /tmp/gate46.py
file      957  /tmp/gate46b.py
file      959  /tmp/gate46c.py
file      937  /tmp/gate47.py
file      522  /tmp/gate5.py
file      770  /tmp/gd.py
file      746  /tmp/gd2.py
file     1013  /tmp/gd3.py
file    15881  /tmp/gen-tos.py.bak
file      626  /tmp/hidden.txt
file     1160  /tmp/hist.py
dir            /tmp/hsperfdata_root
file       11  /tmp/in1.txt
file       15  /tmp/in2.txt
file       51  /tmp/in3.txt
file       71  /tmp/in4.txt
file     2294  /tmp/inl.py
file     1725  /tmp/inner.S
file    16168  /tmp/inner2
file      156  /tmp/j10-a.log
file     2293  /tmp/j10-b.log
file      156  /tmp/j10-bb.log
file      158  /tmp/j10.log
file     1703  /tmp/j11-var.log
file    13736  /tmp/j11.log
file     3288  /tmp/j12.log
file     2314  /tmp/j13-b.log
file     5134  /tmp/j13.log
file     2305  /tmp/j14.log
file     1766  /tmp/j15.log
file      134  /tmp/j19-b.log
file      134  /tmp/j19-m.log
file      382  /tmp/j20.log
file     1626  /tmp/j21-ob.log
file     4077  /tmp/j21-rt.log
file      882  /tmp/j21.log
file      444  /tmp/j22-after.log
file      540  /tmp/j22-master.log
file     4077  /tmp/j23-rt.log
file      443  /tmp/j23.log
file      286  /tmp/j24.log
file     1589  /tmp/j25-ob.log
file     4077  /tmp/j25-rt.log
file      651  /tmp/j25.log
file     1526  /tmp/j26-ans.log
file     4077  /tmp/j26-rt.log
file      517  /tmp/j26.log
file     1522  /tmp/j27-ob.log
file     4077  /tmp/j27-rt.log
file      665  /tmp/j27.log
file     1522  /tmp/j28-ob.log
file     4077  /tmp/j28-rt.log
file      582  /tmp/j28.log
file     1321  /tmp/j29-ans.log
file     1574  /tmp/j29-build.log
file     1523  /tmp/j29-ob.log
file     4009  /tmp/j29-rt.log
file     6452  /tmp/j29.log
file     2291  /tmp/j30-build.log
file     4077  /tmp/j31-rt.log
file       30  /tmp/j31.log
file     1321  /tmp/j32-ans.log
file     1522  /tmp/j32-ob.log
file      676  /tmp/j32-rl.log
file     4077  /tmp/j32-rt.log
file     1088  /tmp/j32.log
file     2294  /tmp/j33-build.log
file      284  /tmp/j33.log
file     1491  /tmp/j34-build.log
file      180  /tmp/j34-reseed.log
file     1269  /tmp/j34.log
file     1575  /tmp/j35-build.log
file     4118  /tmp/j35-rt.log
file     1131  /tmp/j35.log
file     2292  /tmp/j36-build.log
file      180  /tmp/j36-reseed.log
file     4077  /tmp/j36-rt.log
file     1240  /tmp/j36.log
file     1321  /tmp/j37-ans.log
file     1522  /tmp/j37-ob.log
file      677  /tmp/j37-rl.log
file      474  /tmp/j37.log
file     2291  /tmp/j38-build.log
file      168  /tmp/j38.log
file     2291  /tmp/j39-build.log
file      180  /tmp/j39-reseed.log
file      202  /tmp/j39.log
file     1522  /tmp/j40-ob.log
file      676  /tmp/j40-rl.log
file     4077  /tmp/j40-rt.log
file      340  /tmp/j40.log
file     1322  /tmp/j41-ans.log
file      414  /tmp/j41.log
file      952  /tmp/j42.log
file     2291  /tmp/j43-build.log
file     1253  /tmp/j44-ans.log
file     1522  /tmp/j44-ob.log
file     4077  /tmp/j44-rt.log
file      452  /tmp/j44.log
file     2291  /tmp/j45-build.log
file     2291  /tmp/j46-build.log
file     1185  /tmp/j47-ans.log
file     4077  /tmp/j47-rt.log
file      357  /tmp/j47.log
file     1526  /tmp/j48-ans.log
file     2314  /tmp/j48-build.log
file      180  /tmp/j48-reseed.log
file     4077  /tmp/j48-rt.log
file      463  /tmp/j48.log
file     2292  /tmp/j49-build.log
file     1147  /tmp/j49.log
file      180  /tmp/j50-reseed.log
file     2291  /tmp/j51-build.log
file     1321  /tmp/j52-ans.log
file     1522  /tmp/j52-ob.log
file      676  /tmp/j52-rl.log
file     4077  /tmp/j52-rt.log
file      531  /tmp/j52.log
file      180  /tmp/j53-reseed.log
file     2291  /tmp/j54-build.log
file     2295  /tmp/j55-build.log
file     2291  /tmp/j56-build.log
file      180  /tmp/j56-reseed.log
file     2292  /tmp/j57-build.log
file      180  /tmp/j57-reseed.log
file     4077  /tmp/j58-rt.log
file       65  /tmp/j58.log
file      223  /tmp/j59-ans.log
file      223  /tmp/j59-ob.log
file      223  /tmp/j59-rl.log
file      359  /tmp/j59.log
file        0  /tmp/j6-alive.done
file     6527  /tmp/j6-alive.log
file     1544  /tmp/j6-ans.log
file     2314  /tmp/j6-build.log
file     4077  /tmp/j6-tests.log
file      635  /tmp/j6-validate.log
file      143  /tmp/j6.log
file     1321  /tmp/j60-ans.log
file     2292  /tmp/j60-build.log
file     1522  /tmp/j60-ob.log
file      676  /tmp/j60-rl.log
file     4077  /tmp/j60-rt.log
file      420  /tmp/j60.log
file     1185  /tmp/j61-ans.log
file     4077  /tmp/j62-rt.log
file     2292  /tmp/j63-build.log
file       66  /tmp/j64.log
file     1594  /tmp/j65-ans.log
file     4202  /tmp/j66-rt.log
file     4195  /tmp/j67-rt.log
file      195  /tmp/j67.log
file     1253  /tmp/j68-ans.log
file     5029  /tmp/j69-ans.log
file     2314  /tmp/j7-build.log
file     1001  /tmp/j7.log
file     2290  /tmp/j70-build.log
file     4195  /tmp/j70-rt.log
file       57  /tmp/j70.log
file       72  /tmp/j71.log
file     1321  /tmp/j72-ans.log
file     4195  /tmp/j72-rt.log
file      453  /tmp/j72.log
file     1321  /tmp/j73-ans.log
file     4195  /tmp/j74-rt.log
file      121  /tmp/j74.log
file     4195  /tmp/j75-rt.log
file      129  /tmp/j75.log
file       72  /tmp/j76.log
file     1185  /tmp/j77-ans.log
file     4195  /tmp/j77-rt.log
file      237  /tmp/j77.log
file     4571  /tmp/j8.log
file     3053  /tmp/j9-28677d13b1.log
file     3052  /tmp/j9-cc6d168e0a.log
file     3054  /tmp/j9-fc09f6373d.log
file      419  /tmp/jitdis.py
file    28167  /tmp/jitk-after-seed47.patch
file     9609  /tmp/jitos-after-seed45.patch
file    13290  /tmp/jittail-after-seed46.patch
dir            /tmp/jitvar-b93g_smv
dir            /tmp/jitvar-noedttkg
file    32428  /tmp/jitvariants.json
file        2  /tmp/jk-step1
file      900  /tmp/jk1.py
dir            /tmp/jk2
file     1050  /tmp/jk2.py
file        0  /tmp/job1.done
file      512  /tmp/job1.sh
file        0  /tmp/job10.done
file      911  /tmp/job10.sh
file        0  /tmp/job11.done
file      449  /tmp/job11.sh
file        0  /tmp/job12.done
file      282  /tmp/job12.sh
file        0  /tmp/job13.done
file      379  /tmp/job13.sh
file        0  /tmp/job14.done
file      235  /tmp/job14.sh
file        0  /tmp/job15.done
file      200  /tmp/job15.sh
file        0  /tmp/job16.done
file     1674  /tmp/job16.sh
file        0  /tmp/job17.done
file     1334  /tmp/job17.sh
file        0  /tmp/job18.done
file     1421  /tmp/job18.sh
file        0  /tmp/job19.done
file      300  /tmp/job19.sh
file        0  /tmp/job2.done
file      952  /tmp/job2.sh
file        0  /tmp/job20.done
file      166  /tmp/job20.sh
file        0  /tmp/job21.done
file     2468  /tmp/job21.sh
file        0  /tmp/job22.done
file      351  /tmp/job22.sh
file        0  /tmp/job23.done
file     1002  /tmp/job23.sh
file        0  /tmp/job24.done
file      592  /tmp/job24.sh
file        0  /tmp/job25.done
file     1252  /tmp/job25.sh
file        0  /tmp/job26.done
file     1329  /tmp/job26.sh
file        0  /tmp/job27.done
file      963  /tmp/job27.sh
file        0  /tmp/job28.done
file     1535  /tmp/job28.sh
file        0  /tmp/job29.done
file     1244  /tmp/job29.sh
file        0  /tmp/job3.done
file      917  /tmp/job3.sh
file        0  /tmp/job31.done
file      171  /tmp/job31.sh
file        0  /tmp/job32.done
file     1225  /tmp/job32.sh
file        0  /tmp/job33.done
file      539  /tmp/job33.sh
file        0  /tmp/job34.done
file      524  /tmp/job34.sh
file        0  /tmp/job35.done
file      652  /tmp/job35.sh
file        0  /tmp/job36.done
file      821  /tmp/job36.sh
file        0  /tmp/job37.done
file      799  /tmp/job37.sh
file        0  /tmp/job38.done
file      786  /tmp/job38.sh
file        0  /tmp/job39.done
file      620  /tmp/job39.sh
file     1311  /tmp/job4.sh
file        0  /tmp/job40.done
file      858  /tmp/job40.sh
file        0  /tmp/job41.done
file      427  /tmp/job41.sh
file        0  /tmp/job42.done
file      182  /tmp/job42.sh
file        0  /tmp/job44.done
file     1013  /tmp/job44.sh
file        0  /tmp/job47.done
file      716  /tmp/job47.sh
file        0  /tmp/job48.done
file     1451  /tmp/job48.sh
file        0  /tmp/job49.done
file      347  /tmp/job49.sh
file        0  /tmp/job5.done
file      970  /tmp/job5.sh
file        0  /tmp/job52.done
file     1260  /tmp/job52.sh
file     1263  /tmp/job58.sh
file        0  /tmp/job59.done
file      801  /tmp/job59.sh
file        0  /tmp/job6.done
file      960  /tmp/job6.sh
file        0  /tmp/job60.done
file      823  /tmp/job60.sh
file        0  /tmp/job64.done
file      148  /tmp/job64.sh
file        0  /tmp/job65.done
file      176  /tmp/job65.sh
file        0  /tmp/job66.done
file      170  /tmp/job66.sh
file        0  /tmp/job67.done
file      531  /tmp/job67.sh
file        0  /tmp/job68.done
file      194  /tmp/job68.sh
file        0  /tmp/job69.done
file      157  /tmp/job69.sh
file        0  /tmp/job7.done
file      373  /tmp/job7.sh
file        0  /tmp/job70.done
file      421  /tmp/job70.sh
file        0  /tmp/job71.done
file      232  /tmp/job71.sh
file        0  /tmp/job72.done
file      842  /tmp/job72.sh
file        0  /tmp/job73.done
file      192  /tmp/job73.sh
file        0  /tmp/job74.done
file      389  /tmp/job74.sh
file      591  /tmp/job75.sh
file        0  /tmp/job76.done
file      218  /tmp/job76.sh
file        0  /tmp/job77.done
file      585  /tmp/job77.sh
file        0  /tmp/job8.done
file      258  /tmp/job8.sh
file        0  /tmp/job9.done
file      340  /tmp/job9.sh
file     1332  /tmp/kprof.py
file     1312  /tmp/kprof2.py
file       43  /tmp/kt-before.in
file      166  /tmp/kt-before.txt
file       43  /tmp/kt-fast.in
file       94  /tmp/kt-fast.txt
file     1818  /tmp/kt.py
file      752  /tmp/lcache.txt
file     3789  /tmp/lean-open-after-seed47.patch
file      804  /tmp/lines.py
file     1298  /tmp/lt.py
file     1030  /tmp/lto.py
file     1493  /tmp/lto2.py
file     1090  /tmp/lz.py
file     2254  /tmp/lz2.py
file     2314  /tmp/m-build.log
file      180  /tmp/m-reseed.log
file     4077  /tmp/m-rt.log
file     2314  /tmp/m2-build.log
file     1322  /tmp/main.c
file      950  /tmp/march.py
dir            /tmp/mb
file      415  /tmp/mkjt.py
dir            /tmp/mo
file     2290  /tmp/mo-build.log
file     2290  /tmp/mo-build2.log
file    32261  /tmp/names-after-seed45.patch
file     3249  /tmp/names-check.py
file     1634  /tmp/nib.py
file    10560  /tmp/nobit7-after-seed46.patch
dir            /tmp/node-compile-cache
file       19  /tmp/o.txt
dir            /tmp/old
file      658  /tmp/os.py
dir            /tmp/out
file      214  /tmp/p-after.log
file      214  /tmp/p-before.log
file     2291  /tmp/p-build.log
dir            /tmp/p13
file      765  /tmp/pages.py
file      704  /tmp/pages2.py
dir            /tmp/phantomjs
dir            /tmp/pm
file      628  /tmp/pm-build.py
file     2548  /tmp/pm-run.py
file    57324  /tmp/primfirst-after-seed46.patch
file       12  /tmp/rlc1.done
file      792  /tmp/rlc1.log
file      672  /tmp/rlc2.log
dir            /tmp/rs2
dir            /tmp/rs3
file     1361  /tmp/rs3.out
dir            /tmp/rs4
file      514  /tmp/rs4.sh
dir            /tmp/rs5
file       14  /tmp/run-tests.done
file     4077  /tmp/run-tests.log
file      379  /tmp/s1t.py
dir            /tmp/s44
dir            /tmp/s45
dir            /tmp/s46
file     8441  /tmp/s6-new.img
file     8433  /tmp/s6-nothrow.img
file     8441  /tmp/s6b.img
file     1024  /tmp/s6b.log
file    11784  /tmp/s6nb.img
file     1027  /tmp/s6nb.log
file      191  /tmp/s8in.txt
dir            /tmp/seed43
file      458  /tmp/size-cell.log
file      458  /tmp/size-new.log
file      458  /tmp/size-old.log
file      422  /tmp/sizes.py
file     1197  /tmp/st.txt
file      709  /tmp/stackheads-after-seed44.patch
file     5387  /tmp/sym-b45.txt
file     5120  /tmp/sym-p13.txt
file      410  /tmp/symdiff.py
file      483  /tmp/sz2.py
file      845  /tmp/sz3.py
file       11  /tmp/t0
file      392  /tmp/t1.py
file      642  /tmp/t2.py
file      356  /tmp/t3.py
file       62  /tmp/t5.fth
file      931  /tmp/t6.py
file      479  /tmp/tailfail.py
file      866  /tmp/tailfail2.py
file     1155  /tmp/tailfix-after-seed46.patch
dir            /tmp/tmp.1bb1Luqid3
dir            /tmp/tmp.2DCscqaJG8
dir            /tmp/tmp.6clAmlNlZS
dir            /tmp/tmp.NGSAIrRkDT
dir            /tmp/tmp.jRXowMZRB3
dir            /tmp/tmp.wAgc3Dxful
file      760  /tmp/tokfill.txt
file     1378  /tmp/tt.py
file    23004  /tmp/tt0-engine-before
file     1276  /tmp/tt2.py
file      927  /tmp/tt3.py
file      967  /tmp/tt4.py
file     1056  /tmp/tt5.py
file      846  /tmp/tt6.py
file     3657  /tmp/tty-after-seed45.patch
file      119  /tmp/utf.txt
file      110  /tmp/utf2.txt
file        0  /tmp/uv-ce9cd633bb00c47d.lock
file        0  /tmp/uv-setuptools-25a17d8eca85a703.lock
file        0  /tmp/uv-setuptools-485db6d65da711db.lock
file        0  /tmp/uv-setuptools-f4b63408ed8c7c10.lock
file     1217  /tmp/v-ans.log
file      422  /tmp/v-fault-A.log
file      430  /tmp/v-fault-B.log
file      137  /tmp/v-faultB.txt
file      124  /tmp/v-faults.log
file      264  /tmp/v-fc-tool.log
file      418  /tmp/v-gate.log
file     1654  /tmp/v-outbuf.log
file      915  /tmp/v-rlc.log
file       48  /tmp/v-tests.log
file      591  /tmp/v-validate.log
file      793  /tmp/v44.log
file     1626  /tmp/v44b-ob.log
file     4077  /tmp/v44b-rt.log
file      619  /tmp/v44b.log
file       14  /tmp/validate.done
file      635  /tmp/validate.log
file   111408  /tmp/vm-lab-both.c
file   115457  /tmp/vm-lab-jitos.c
file   117306  /tmp/vm-lab.c.bak
dir            /tmp/w230
file     2892  /tmp/writeline-after-seed44.patch
(and 330 relf-run-*.sh)
```

