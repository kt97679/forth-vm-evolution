# Files from the chats of Iterations 213-265, second archive - MANIFEST

Packed 2026-10-13 21:57 UTC on the last chat's machine. Everything here is **as found**: copied, not rewritten; nothing reconstructed from memory. The first archive (forth-vm-evolution-prev-chat-files.tar.gz) holds the scripts of Iterations 244-265; this one holds every other script and source in /tmp with the extensions .py .sh .fth .4 .c .h .S .awk .patch .diff (no .h, .awk or .diff files were there; every .patch was in the first archive), the relf-run-* test leftovers left out, and the logs the job*.sh scripts wrote.

**How the iterations and figures were found:** from the two earlier chats' transcripts, as kept on the machine - T1 `/mnt/transcripts/2026-10-12-18-50-21-forth-vm-evolution-seed43-44.txt` (Iterations 213-222) and T2 `/mnt/transcripts/2026-10-13-03-42-11-forth-vm-evolution-seed46-work.txt` (223-241). The iteration is the first commit after the file's first appearance; the figure is what the tool output right after its run shows, quoted short. Files from the last chat after its compaction (Iterations 242-265) are not in those transcripts; they are marked "the last chat's live record". A file edited after its first run holds its last state - as found - while the figure is its first run's. Background jobs' figures are in their logs (section 2).

## 1. Scripts, sources and job scripts (`scripts/`, `jobs/`)

| original path | iteration | figure | record | status | in the archive |
|---|---|---|---|---|---|
| `/tmp/alive43.py` | - | the gate over seed 42/43 front designs (the check of the after-seed-43 batch); its result in that job's logs | the last chat's live record | as found | `scripts/alive43.py` |
| `/tmp/ans-hidden.py` | - | the standard suite on three designs with the unused names hidden (the hidden-names finding) | the last chat's live record | as found | `scripts/ans-hidden.py` |
| `/tmp/audit43.py` | - | audited the fast alive run: real builds; fsys 4 images changed by the rebind fix (e.g. 8dab7c6af4 fsys 4: image 9249, recorded 9265; engine 8512) | the last chat's live record | as found | `scripts/audit43.py` |
| `/tmp/cbtime.sh` | - | the C baseline's first timings with the CPU-time wrapper (sieve 0.95 0.89 0.97 ms, ackermann 0.62 0.62 0.70, loop 0.88 0.91 0.94, parse 2.29 2.34 2.40) | the last chat's live record | as found | `scripts/cbtime.sh` |
| `/tmp/diag.py` | - | diagnosed the hidden-names failures: the tools test (add5ec8937 toolstest.fth differs at line 10) and the JIT design crash | the last chat's live record | as found | `scripts/diag.py` |
| `/tmp/diag2.py` | - | widened the scan to sources loaded at run time (add5ec8937: hidden 65 by the first scan, 64 with coreext/locals/save-system/shell; written there: NEXT-NFA8) and bisected the crashing hidden name | the last chat's live record | as found | `scripts/diag2.py` |
| `/tmp/dz-designs.py` | - | division by zero on each engine kind (f20de05a64 msc: RIGHT, status 0; 4a351e360a tail: RIGHT; cc6d168e0a JIT: RIGHT ...) | the last chat's live record | as found | `scripts/dz-designs.py` |
| `/tmp/elf.py` | - | Iteration 250-251 (the last chat): readelf on 3456ac1e5e's engine - no sections, 2 program headers (LOAD + GNU_STACK), 0xb0 = 176 header bytes: the stack-header row in GOALS.md (Iteration 251). Missed by the first archive's list | the last chat's live record | as found | `scripts/elf.py` |
| `/tmp/eng-id.py` | - | the price switch changes no normal build: engines and images byte for byte (28677d13b1 23192 + 8416, cc6d168e0a 23672 + 10710, fc09f6373d 17048 + 8916, add5ec8937 7456 + 8680) | the last chat's live record | as found | `scripts/eng-id.py` |
| `/tmp/facts43.py` | - | seed 43's facts (records 38796, generations 0-153; status ok 31775, screened 6839, 182 reach-limit deaths; children by how made...) | the last chat's live record | as found | `scripts/facts43.py` |
| `/tmp/fc-run.sh` | - | the counting harness on three more designs (no kinput, the Q-best, the fastest) at fsys 4 and 5, detached; output in fc*.log | the last chat's live record | as found | `scripts/fc-run.sh` |
| `/tmp/fs3-good.4` | - | the fsys 3 library kept good while a fault was planted in READ's seekable path (the new check caught it: "READ from a stdin that is a file ... DIFFERS at fsys 3, 4, 5") | the last chat's live record | as found | `scripts/fs3-good.4` |
| `/tmp/fsys-count.py` | - | the counting harness: dispatches per word and system calls per workload at chosen fsys levels (e.g. be1620e346 kernel at fsys 4 and 5) | the last chat's live record | as found | `scripts/fsys-count.py` |
| `/tmp/gate44.py` | - | the gate for the WRITE-LINE fix (after-seed-44 patch 1); its result in that job's logs | the last chat's live record | as found | `scripts/gate44.py` |
| `/tmp/gate44b.py` | - | the gate for the file-buffer change with the WRITE-LINE fix; its result in that job's logs | the last chat's live record | as found | `scripts/gate44b.py` |
| `/tmp/gate44c.py` | - | the gate for the READ/FS-SEEK0 change (after-seed-44 patch 3); its result in that job's logs | the last chat's live record | as found | `scripts/gate44c.py` |
| `/tmp/gate44d.py` | - | the gate on all 165 front designs for the image loader's array change (after-seed-44 patch 4); its result in that job's logs | the last chat's live record | as found | `scripts/gate44d.py` |
| `/tmp/gate45.py` | - | steps 7-9 for seed 44: the gate over seed 44's front and the joint front; its result in that job's logs | the last chat's live record | as found | `scripts/gate45.py` |
| `/tmp/gate46.py` | - | steps 7-9 for seed 45: the gate over seed 45's front and the joint front; its result in that job's logs | the last chat's live record | as found | `scripts/gate46.py` |
| `/tmp/gate46b.py` | - | Iteration 242 (the last chat, after its compaction): made by job52.sh's sed from gate46.py for the primitives-first tree - alive: 128 of 128 (seed 45 front 105, joint front 66, 43 in both) | the last chat's live record | as found | `scripts/gate46b.py` |
| `/tmp/gate5.py` | - | the gate for the tightened fsys 5 (the after-seed-43 batch's verification); its result in that job's logs | the last chat's live record | as found | `scripts/gate5.py` |
| `/tmp/inl.py` | - | priced which hidden words could vanish entirely (add5ec8937: 65 hidden names with bodies; savings by kind: 'one call site' 36 ...) | the last chat's live record | as found | `scripts/inl.py` |
| `/tmp/inner.S` | - | the INNER loop timed three ways - the stencils as copied, three cells cached, the loop index in registers (results/price-jit-stack.md's microbenchmark); "same results: yes" | the last chat's live record | as found | `scripts/inner.S` |
| `/tmp/job1.sh` | - | background checks: not in the transcripts - no recorded figure of its own; what it wrote is in logs/ | the last chat's live record | as found | `jobs/job1.sh` |
| `/tmp/job10.sh` | - | background checks: not in the transcripts - no recorded figure of its own; what it wrote is in logs/ | the last chat's live record | as found | `jobs/job10.sh` |
| `/tmp/job11.sh` | - | background checks: not in the transcripts - no recorded figure of its own; what it wrote is in logs/ | the last chat's live record | as found | `jobs/job11.sh` |
| `/tmp/job12.sh` | - | background checks: not in the transcripts - no recorded figure of its own; what it wrote is in logs/ | the last chat's live record | as found | `jobs/job12.sh` |
| `/tmp/job13.sh` | - | background checks: not in the transcripts - no recorded figure of its own; what it wrote is in logs/ | the last chat's live record | as found | `jobs/job13.sh` |
| `/tmp/job14.sh` | - | background checks: not in the transcripts - no recorded figure of its own; what it wrote is in logs/ | the last chat's live record | as found | `jobs/job14.sh` |
| `/tmp/job15.sh` | - | background checks: not in the transcripts - no recorded figure of its own; what it wrote is in logs/ | the last chat's live record | as found | `jobs/job15.sh` |
| `/tmp/job16.sh` | - | background checks: not in the transcripts - no recorded figure of its own; what it wrote is in logs/ | the last chat's live record | as found | `jobs/job16.sh` |
| `/tmp/job17.sh` | - | background checks: not in the transcripts - no recorded figure of its own; what it wrote is in logs/ | the last chat's live record | as found | `jobs/job17.sh` |
| `/tmp/job18.sh` | - | background checks: not in the transcripts - no recorded figure of its own; what it wrote is in logs/ | the last chat's live record | as found | `jobs/job18.sh` |
| `/tmp/job19.sh` | - | background checks: not in the transcripts - no recorded figure of its own; what it wrote is in logs/ | the last chat's live record | as found | `jobs/job19.sh` |
| `/tmp/job2.sh` | - | background checks: not in the transcripts - no recorded figure of its own; what it wrote is in logs/ | the last chat's live record | as found | `jobs/job2.sh` |
| `/tmp/job20.sh` | - | background checks: not in the transcripts - no recorded figure of its own; what it wrote is in logs/ | the last chat's live record | as found | `jobs/job20.sh` |
| `/tmp/job21.sh` | - | background checks: not in the transcripts - no recorded figure of its own; what it wrote is in logs/ | the last chat's live record | as found | `jobs/job21.sh` |
| `/tmp/job22.sh` | - | background checks: not in the transcripts - no recorded figure of its own; what it wrote is in logs/ | the last chat's live record | as found | `jobs/job22.sh` |
| `/tmp/job23.sh` | - | background checks: not in the transcripts - no recorded figure of its own; what it wrote is in logs/ | the last chat's live record | as found | `jobs/job23.sh` |
| `/tmp/job24.sh` | - | background checks: not in the transcripts - no recorded figure of its own; what it wrote is in logs/ | the last chat's live record | as found | `jobs/job24.sh` |
| `/tmp/job25.sh` | - | background checks: not in the transcripts - no recorded figure of its own; what it wrote is in logs/ | the last chat's live record | as found | `jobs/job25.sh` |
| `/tmp/job26.sh` | - | background checks: not in the transcripts - no recorded figure of its own; what it wrote is in logs/ | the last chat's live record | as found | `jobs/job26.sh` |
| `/tmp/job27.sh` | - | background checks: not in the transcripts - no recorded figure of its own; what it wrote is in logs/ | the last chat's live record | as found | `jobs/job27.sh` |
| `/tmp/job28.sh` | - | background checks: not in the transcripts - no recorded figure of its own; what it wrote is in logs/ | the last chat's live record | as found | `jobs/job28.sh` |
| `/tmp/job29.sh` | - | background checks: not in the transcripts - no recorded figure of its own; what it wrote is in logs/ | the last chat's live record | as found | `jobs/job29.sh` |
| `/tmp/job3.sh` | - | background checks: not in the transcripts - no recorded figure of its own; what it wrote is in logs/ | the last chat's live record | as found | `jobs/job3.sh` |
| `/tmp/job31.sh` | - | background checks: not in the transcripts - no recorded figure of its own; what it wrote is in logs/ | the last chat's live record | as found | `jobs/job31.sh` |
| `/tmp/job32.sh` | - | background checks: not in the transcripts - no recorded figure of its own; what it wrote is in logs/ | the last chat's live record | as found | `jobs/job32.sh` |
| `/tmp/job33.sh` | - | background checks: not in the transcripts - no recorded figure of its own; what it wrote is in logs/ | the last chat's live record | as found | `jobs/job33.sh` |
| `/tmp/job34.sh` | - | background checks: not in the transcripts - no recorded figure of its own; what it wrote is in logs/ | the last chat's live record | as found | `jobs/job34.sh` |
| `/tmp/job35.sh` | - | background checks: not in the transcripts - no recorded figure of its own; what it wrote is in logs/ | the last chat's live record | as found | `jobs/job35.sh` |
| `/tmp/job36.sh` | - | background checks: not in the transcripts - no recorded figure of its own; what it wrote is in logs/ | the last chat's live record | as found | `jobs/job36.sh` |
| `/tmp/job37.sh` | - | background checks: not in the transcripts - no recorded figure of its own; what it wrote is in logs/ | the last chat's live record | as found | `jobs/job37.sh` |
| `/tmp/job38.sh` | - | background checks: not in the transcripts - no recorded figure of its own; what it wrote is in logs/ | the last chat's live record | as found | `jobs/job38.sh` |
| `/tmp/job39.sh` | - | background checks: not in the transcripts - no recorded figure of its own; what it wrote is in logs/ | the last chat's live record | as found | `jobs/job39.sh` |
| `/tmp/job4.sh` | - | background checks: not in the transcripts - no recorded figure of its own; what it wrote is in logs/ | the last chat's live record | as found | `jobs/job4.sh` |
| `/tmp/job40.sh` | - | background checks: not in the transcripts - no recorded figure of its own; what it wrote is in logs/ | the last chat's live record | as found | `jobs/job40.sh` |
| `/tmp/job41.sh` | - | background checks: not in the transcripts - no recorded figure of its own; what it wrote is in logs/ | the last chat's live record | as found | `jobs/job41.sh` |
| `/tmp/job42.sh` | - | background checks: not in the transcripts - no recorded figure of its own; what it wrote is in logs/ | the last chat's live record | as found | `jobs/job42.sh` |
| `/tmp/job44.sh` | - | background checks: not in the transcripts - no recorded figure of its own; what it wrote is in logs/ | the last chat's live record | as found | `jobs/job44.sh` |
| `/tmp/job47.sh` | - | background checks: not in the transcripts - no recorded figure of its own; what it wrote is in logs/ | the last chat's live record | as found | `jobs/job47.sh` |
| `/tmp/job48.sh` | - | background checks: not in the transcripts - no recorded figure of its own; what it wrote is in logs/ | the last chat's live record | as found | `jobs/job48.sh` |
| `/tmp/job49.sh` | - | Iteration 241: the walk regression found - profiling two small designs' dictionary walk (its output in j49.log) | the last chat's live record | as found | `jobs/job49.sh` |
| `/tmp/job5.sh` | - | background checks: not in the transcripts - no recorded figure of its own; what it wrote is in logs/ | the last chat's live record | as found | `jobs/job5.sh` |
| `/tmp/job52.sh` | - | Iteration 242 (the last chat): the primitives-first checks - run-tests PASS, 7 of 7, the gate 128 of 128, the suite 0 of 6 differ, outbuf and readline PASS (logs j52*.log, in the first archive) | the last chat's live record | as found | `jobs/job52.sh` |
| `/tmp/job6.sh` | - | background checks: not in the transcripts - no recorded figure of its own; what it wrote is in logs/ | the last chat's live record | as found | `jobs/job6.sh` |
| `/tmp/job7.sh` | - | background checks: not in the transcripts - no recorded figure of its own; what it wrote is in logs/ | the last chat's live record | as found | `jobs/job7.sh` |
| `/tmp/job8.sh` | - | background checks: not in the transcripts - no recorded figure of its own; what it wrote is in logs/ | the last chat's live record | as found | `jobs/job8.sh` |
| `/tmp/job9.sh` | - | background checks: not in the transcripts - no recorded figure of its own; what it wrote is in logs/ | the last chat's live record | as found | `jobs/job9.sh` |
| `/tmp/lines.py` | - | each line of the names program alone on s0 and s6 (s0-cell crashed with -11 on line 2: the UTF-8 name fault) | the last chat's live record | as found | `scripts/lines.py` |
| `/tmp/main.c` | - | inner.S's C driver (the same timing) | the last chat's live record | as found | `scripts/main.c` |
| `/tmp/names-check.py` | - | the first copy of lab/evolve/names-check.py, before the fix: 'the cell system (s0), the reference: status -11' - later moved into the repository | the last chat's live record | as found | `scripts/names-check.py` |
| `/tmp/pages.py` | - | counting the pages a design touches (the memory sweep) - the run hit the 300 s limit there | the last chat's live record | as found | `scripts/pages.py` |
| `/tmp/pages2.py` | - | every selection workload's memory with the image loader's array off the stack (add5ec8937: fib 80, loop 84, corpus 108, kernel 132, bubble 88, ackermann 80 KB ...) | the last chat's live record | as found | `scripts/pages2.py` |
| `/tmp/pk2-attr.py` | - | not in the transcripts - no recorded figure found | the last chat's live record | as found | `scripts/pk2-attr.py` |
| `/tmp/pk2-attr2.py` | - | not in the transcripts - no recorded figure found | the last chat's live record | as found | `scripts/pk2-attr2.py` |
| `/tmp/pk2-pack.py` | - | not in the transcripts - no recorded figure found | the last chat's live record | as found | `scripts/pk2-pack.py` |
| `/tmp/pm-build.py` | - | built d3149e10c6 and add5ec8937 for the page map | the last chat's live record | as found | `scripts/pm-build.py` |
| `/tmp/pm-run.py` | - | mapped which pages a design has present after a workload ("never waited" lines per workload) | the last chat's live record | as found | `scripts/pm-run.py` |
| `/tmp/s1t.py` | - | definitions tried on the SOD16 stage (w1/w8 crashed with -11 before the fix) | the last chat's live record | as found | `scripts/s1t.py` |
| `/tmp/sizes.py` | - | image bytes of the old, new and cell-copy fsys 5 library | the last chat's live record | as found | `scripts/sizes.py` |
| `/tmp/symdiff.py` | - | word-by-word comparison of the dumps, to explain the 662-byte image growth (the dump tool kept in every image - LINKC missing from DUMPTOOL) | the last chat's live record | as found | `scripts/symdiff.py` |
| `/tmp/t1.py` | - | Iteration 242 (the last chat): the new kernel image tried on simple input, definitions, extend.4 and PRIMITIVE? - PRIMITIVE? read 0 for every word (debugging) | the last chat's live record | as found | `scripts/t1.py` |
| `/tmp/t2.py` | - | Iteration 242 (the last chat): PRIMITIVE? on DUP, OPEN-FILE, COLD, (PRIMITIVES-END) - all 0; the second reseed stage crashed (-11) (debugging) | the last chat's live record | as found | `scripts/t2.py` |
| `/tmp/t3.py` | - | Iteration 242 (the last chat): printed the addresses and PRIMITIVE?'s compiled literal - 1792, START-relative, where the xts were absolute (debugging) | the last chat's live record | as found | `scripts/t3.py` |
| `/tmp/t5.fth` | - | Iteration 244 (the last chat): written for the coreext >NAME test and not used - t6.py (first archive) ran it; no recorded figure | the last chat's live record | as found | `scripts/t5.fth` |
| `/tmp/vm-lab-both.c` | - | debugging, no recorded figure: an engine source with both after-seed-44 changes, split into separate patches | the last chat's live record | as found | `scripts/vm-lab-both.c` |
| `/tmp/vm-lab-jitos.c` | - | debugging, no recorded figure: an engine source during the jitos gene (its first form; the command around it failed with a shell syntax error) | the last chat's live record | as found | `scripts/vm-lab-jitos.c` |

## 2. The logs the job*.sh scripts wrote (`logs/`)

| job | log | status |
|---|---|---|
| `job1.sh` | `/tmp/fc3.log` | as found |
| `job1.sh` | `/tmp/rlc2.log` | as found |
| `job2.sh` | `/tmp/b-cell.log` | as found |
| `job2.sh` | `/tmp/b-new.log` | as found |
| `job2.sh` | `/tmp/b-old.log` | as found |
| `job2.sh` | `/tmp/fc-cell.log` | as found |
| `job2.sh` | `/tmp/size-cell.log` | as found |
| `job2.sh` | `/tmp/size-new.log` | as found |
| `job2.sh` | `/tmp/size-old.log` | as found |
| `job3.sh` | `/tmp/v-ans.log` | as found |
| `job3.sh` | `/tmp/v-gate.log` | as found |
| `job3.sh` | `/tmp/v-outbuf.log` | as found |
| `job3.sh` | `/tmp/v-rlc.log` | as found |
| `job3.sh` | `/tmp/v-tests.log` | as found |
| `job3.sh` | `/tmp/v-validate.log` | as found |
| `job4.sh` | `/tmp/b-fault.log` | as found |
| `job4.sh` | `/tmp/b-restore.log` | as found |
| `job4.sh` | `/tmp/v-faults.log` | as found |
| `job5.sh` | `/tmp/b-fault.log` | as found |
| `job5.sh` | `/tmp/b-restore.log` | as found |
| `job5.sh` | `/tmp/v-fault-B.log` | as found |
| `job5.sh` | `/tmp/v-faultB.txt` | as found |
| `job5.sh` | `/tmp/v-fc-tool.log` | as found |
| `job6.sh` | `/tmp/j6-alive.log` | as found |
| `job6.sh` | `/tmp/j6-ans.log` | as found |
| `job6.sh` | `/tmp/j6-build.log` | as found |
| `job6.sh` | `/tmp/j6-tests.log` | as found |
| `job6.sh` | `/tmp/j6-validate.log` | as found |
| `job6.sh` | `/tmp/j6.log` | as found |
| `job7.sh` | `/tmp/j7-build.log` | as found |
| `job7.sh` | `/tmp/j7.log` | as found |
| `job8.sh` | `/tmp/j8.log` | as found |
| `job10.sh` | `/tmp/j10-a.log` | as found |
| `job10.sh` | `/tmp/j10-b.log` | as found |
| `job10.sh` | `/tmp/j10-bb.log` | as found |
| `job10.sh` | `/tmp/j10.log` | as found |
| `job11.sh` | `/tmp/j11-var.log` | as found |
| `job11.sh` | `/tmp/j11.log` | as found |
| `job12.sh` | `/tmp/j12.log` | as found |
| `job13.sh` | `/tmp/j13-b.log` | as found |
| `job13.sh` | `/tmp/j13.log` | as found |
| `job14.sh` | `/tmp/j14.log` | as found |
| `job15.sh` | `/tmp/j15.log` | as found |
| `job16.sh` | `/tmp/v44.log` | as found |
| `job17.sh` | `/tmp/p-after.log` | as found |
| `job17.sh` | `/tmp/p-before.log` | as found |
| `job17.sh` | `/tmp/p-build.log` | as found |
| `job18.sh` | `/tmp/v44b-ob.log` | as found |
| `job18.sh` | `/tmp/v44b-rt.log` | as found |
| `job18.sh` | `/tmp/v44b.log` | as found |
| `job19.sh` | `/tmp/j19-b.log` | as found |
| `job19.sh` | `/tmp/j19-m.log` | as found |
| `job20.sh` | `/tmp/j20.log` | as found |
| `job21.sh` | `/tmp/j21-ob.log` | as found |
| `job21.sh` | `/tmp/j21-rt.log` | as found |
| `job21.sh` | `/tmp/j21.log` | as found |
| `job22.sh` | `/tmp/j22-after.log` | as found |
| `job22.sh` | `/tmp/j22-master.log` | as found |
| `job23.sh` | `/tmp/j23-rt.log` | as found |
| `job23.sh` | `/tmp/j23.log` | as found |
| `job24.sh` | `/tmp/j24.log` | as found |
| `job25.sh` | `/tmp/j25-ob.log` | as found |
| `job25.sh` | `/tmp/j25-rt.log` | as found |
| `job25.sh` | `/tmp/j25.log` | as found |
| `job26.sh` | `/tmp/j26-ans.log` | as found |
| `job26.sh` | `/tmp/j26-rt.log` | as found |
| `job26.sh` | `/tmp/j26.log` | as found |
| `job27.sh` | `/tmp/j27-ob.log` | as found |
| `job27.sh` | `/tmp/j27-rt.log` | as found |
| `job27.sh` | `/tmp/j27.log` | as found |
| `job28.sh` | `/tmp/j28-ob.log` | as found |
| `job28.sh` | `/tmp/j28-rt.log` | as found |
| `job28.sh` | `/tmp/j28.log` | as found |
| `job29.sh` | `/tmp/j29-ans.log` | as found |
| `job29.sh` | `/tmp/j29-ob.log` | as found |
| `job29.sh` | `/tmp/j29-rt.log` | as found |
| `job29.sh` | `/tmp/j29.log` | as found |
| `job31.sh` | `/tmp/j31-rt.log` | as found |
| `job31.sh` | `/tmp/j31.log` | as found |
| `job32.sh` | `/tmp/j32-ans.log` | as found |
| `job32.sh` | `/tmp/j32-ob.log` | as found |
| `job32.sh` | `/tmp/j32-rl.log` | as found |
| `job32.sh` | `/tmp/j32-rt.log` | as found |
| `job32.sh` | `/tmp/j32.log` | as found |
| `job33.sh` | `/tmp/j33-build.log` | as found |
| `job33.sh` | `/tmp/j33.log` | as found |
| `job34.sh` | `/tmp/j34-build.log` | as found |
| `job34.sh` | `/tmp/j34-reseed.log` | as found |
| `job34.sh` | `/tmp/j34.log` | as found |
| `job35.sh` | `/tmp/j35-build.log` | as found |
| `job35.sh` | `/tmp/j35-rt.log` | as found |
| `job35.sh` | `/tmp/j35.log` | as found |
| `job36.sh` | `/tmp/j36-build.log` | as found |
| `job36.sh` | `/tmp/j36-reseed.log` | as found |
| `job36.sh` | `/tmp/j36-rt.log` | as found |
| `job36.sh` | `/tmp/j36.log` | as found |
| `job37.sh` | `/tmp/j37-ans.log` | as found |
| `job37.sh` | `/tmp/j37-ob.log` | as found |
| `job37.sh` | `/tmp/j37-rl.log` | as found |
| `job37.sh` | `/tmp/j37.log` | as found |
| `job38.sh` | `/tmp/j38-build.log` | as found |
| `job38.sh` | `/tmp/j38.log` | as found |
| `job39.sh` | `/tmp/j39-build.log` | as found |
| `job39.sh` | `/tmp/j39-reseed.log` | as found |
| `job39.sh` | `/tmp/j39.log` | as found |
| `job40.sh` | `/tmp/j40-ob.log` | as found |
| `job40.sh` | `/tmp/j40-rl.log` | as found |
| `job40.sh` | `/tmp/j40-rt.log` | as found |
| `job40.sh` | `/tmp/j40.log` | as found |
| `job41.sh` | `/tmp/j41-ans.log` | as found |
| `job41.sh` | `/tmp/j41.log` | as found |
| `job42.sh` | `/tmp/j42.log` | as found |
| `job44.sh` | `/tmp/j44-ans.log` | as found |
| `job44.sh` | `/tmp/j44-ob.log` | as found |
| `job44.sh` | `/tmp/j44-rt.log` | as found |
| `job44.sh` | `/tmp/j44.log` | as found |
| `job47.sh` | `/tmp/j47-ans.log` | as found |
| `job47.sh` | `/tmp/j47-rt.log` | as found |
| `job47.sh` | `/tmp/j47.log` | as found |
| `job48.sh` | `/tmp/j48-ans.log` | as found |
| `job48.sh` | `/tmp/j48-build.log` | as found |
| `job48.sh` | `/tmp/j48-reseed.log` | as found |
| `job48.sh` | `/tmp/j48-rt.log` | as found |
| `job48.sh` | `/tmp/j48.log` | as found |
| `job49.sh` | `/tmp/j49-build.log` | as found |
| `job49.sh` | `/tmp/j49.log` | as found |
| `job52.sh` | `/tmp/j52-ans.log` | as found |
| `job52.sh` | `/tmp/j52-ob.log` | as found |
| `job52.sh` | `/tmp/j52-rl.log` | as found |
| `job52.sh` | `/tmp/j52-rt.log` | as found |
| `job52.sh` | `/tmp/j52.log` | as found |

## 3. Source copies with other suffixes (`sources-other-suffixes/`)

Not in the requested extension list (their names end in .cell, .new, .old, .orig, .bak) but sources all the same - included so nothing of them is left behind.

| original path | figure | record | status | in the archive |
|---|---|---|---|---|
| `/tmp/evolve.py.cell` | Iteration 214: a copy of lab/evolve/evolve.py for the cell-copy fsys 5 variant (image bytes of old, new and cell-copy fsys 5) | T1 | as found | `sources-other-suffixes/evolve.py.cell` |
| `/tmp/evolve.py.new` | Iteration 214: a copy of lab/evolve/evolve.py for the new fsys 5 | T1 | as found | `sources-other-suffixes/evolve.py.new` |
| `/tmp/evolve.py.old` | Iteration 214: a copy of lab/evolve/evolve.py for the old fsys 5 | T1 | as found | `sources-other-suffixes/evolve.py.old` |
| `/tmp/file-sysc5.4.cell` | Iteration 214: the cell-copy variant of the fsys 5 library | T1 | as found | `sources-other-suffixes/file-sysc5.4.cell` |
| `/tmp/file-sysc5.4.new` | Iteration 214: the new fsys 5 library | T1 | as found | `sources-other-suffixes/file-sysc5.4.new` |
| `/tmp/file-sysc5.4.orig` | Iteration 214: the original fsys 5 library, kept before rewriting it | T1 | as found | `sources-other-suffixes/file-sysc5.4.orig` |
| `/tmp/vm-lab.c.bak` | Iteration 263 (the last chat): engine/vm-lab.c kept before the zero-divisor trim was tried in /tmp/mo, and restored from it | the last chat's live record | as found | `sources-other-suffixes/vm-lab.c.bak` |
| `/tmp/gen-tos.py.bak` | Iteration 263 (the last chat): tools/gen-tos.py kept before the same trial, and restored from it | the last chat's live record | as found | `sources-other-suffixes/gen-tos.py.bak` |

## 4. Notes

- Nothing is gone: every file named here was on the machine.
- `elf.py` (Iterations 250-251) belonged in the first archive - it produced the 176 header bytes of GOALS.md's stack-header row - and was missed there.
- `gate44.py`, `gate44c.py` and `gate46b.py` were written by `sed` inside job scripts (from earlier gate scripts), so they appear among those jobs' outputs too.
- `names-check.py` here is the /tmp copy from Iteration 232, before the fix; the repository's `lab/evolve/names-check.py` grew from it.
- Directories in /tmp (scratch trees, build copies such as rs2-rs5, jitvar-*) were not searched for sources: the scratch trees are in the first archive as patches; the rest are copies of repository files or generated outputs.

