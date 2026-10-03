# The full-scale rehearsal, on the development VM

`--pop 32 --gens 40 --rounds 3 --seed 1`, run in chunks of four and a
half minutes (the environment's limit on one command), resumed each time
from the database. **These are not the results**: one virtual core of an
unnamed Intel Xeon under KVM, shared, without hardware counters. Evolution
optimises for the machine it measures on; the run on the Ryzen 7 PRO
8840HS is the one that counts. The rehearsal was for the machinery.

## The run

1,306 designs (26 founders and hand-made, then 40 generations of 32),
1,092 alive, about 3 s each. Every kind of design evaluated in 1.7-2.6 s;
no gene is slow at scale.

Deaths: 181 the known reach limit - byte-granular designs without the
three-byte call form, or with near DOES> calls, whose dictionary outgrows
16 KB (most die on the kernel workload, a few already on the corpus);
32 conversion refusals - the known skip-pad alignment (cpt16) and 31 CV8
designs that converted when built again (below); 1 compile failure (below).

## The front, measured again

| design | in the run | re-measured (4 rounds) | size |
|---|---|---|---|
| 32600cab87 | 0.660 | 0.685 | 13,656 |
| 05617039f6 | 0.671 | 0.722 | 13,488 |
| 57a9dcc7cb | 0.677 | 0.701 | 13,480 |
| 0b1d16def9 | 0.702 | 0.715 | 13,464 |
| 312ad2edaa | 0.713 | 0.718 | 13,456 |
| 8cbc6dd05c | 0.739 | 0.775 | 9,809 |
| 6738aed13f | 0.752 | 0.732 | 9,793 |
| 595fc2b8f4 | 0.781 | 0.769 | 9,761 |

CPU time over hand-made s6's, so 0.685 is 31.5% less. Every design on the
front descends from the founder with the escape, seven format-10 words
and 24 pairs; all have multi-state caching but the last, guard pages for
the stack checks, and about 21 pairs. Tail calls are not on it. The fast
end drops byte headers (13.5 KB); the small end keeps them (9.8 KB). The
best design by hand-combining genes had been 0.826; no hand-made stage is
on the front (s5 0.880, s6 1.000).

## What the rehearsal found

- **A resumed run forked instead of resuming.** Two decisions looked at
  the whole database, which on a resume already holds what the first
  attempt made later; and the Pareto ranking walked a set of ids, whose
  order changes with each process's string hashing. Fixed: a replay of a
  finished run evaluates nothing new, and every chunk after the fix added
  only designs from where the last one stopped.
- **A latent bug in gen-super.py**, exposed by the per-design pair pools:
  a pair whose first half has no cached body of its own (`D+`) ends in
  FILLNEXT(), which the generator mangled. Fixed.
- **31 conversions failed, and converted when rebuilt** - not at chunk
  boundaries, not for lack of disk. Every death now records the tool's
  last error line, and the run on the Ryzen named the cause: `--bytehdr
  requires --v8 --cpt 0`. canon() makes every design with byte headers
  byte-granular, and identity is computed from canon(g), but evaluate()
  built the raw genome: a mutation turning on byte headers in a design
  with scaled calls was refused, and the death recorded under the identity
  of the byte-granular design - which converts, as rebuilding from the
  stored (canonical) genome showed. Not transient at all. Fixed: evaluate()
  builds canon(g). (A retry added on the wrong diagnosis is gone again.)
- **The winner's curse**: the front re-measured 3-6% slower than in the
  run, two designs slightly faster - noise both ways, the leader stays.
  `--remeasure N` measures the front again for the report.

## The same front, measured again on the Ryzen 7 PRO 8840HS

`--remeasure 6` on the laptop, after a fresh build (616 cases on all 15
systems, the hand-made stages validating). CPU time over hand-made s6's,
both measured there, back to back:

| design | VM, in the run | Ryzen, re-measured | size | multi-state |
|---|---|---|---|---|
| 57a9dcc7cb | 0.677 | **0.605** | 13,480 | yes |
| 05617039f6 | 0.671 | 0.637 | 13,488 | yes |
| 32600cab87 | 0.660 | 0.641 | 13,656 | yes |
| 312ad2edaa | 0.713 | 0.652 | 13,456 | yes |
| 6738aed13f | 0.752 | 0.656 | 9,793 | no |
| 595fc2b8f4 | 0.781 | 0.673 | 9,761 | no |
| 0b1d16def9 | 0.702 | 0.699 | 13,464 | yes |
| 8cbc6dd05c | 0.739 | 0.729 | 9,809 | yes |

The front found on the VM holds on the Ryzen, and mostly better: every
design between 0.60 and 0.73 of s6's CPU time. Among these eight, four
stay on the front there - 57a9dcc7cb (0.605), 312ad2edaa (0.652), and the
two small ones with byte headers, 6738aed13f (0.656 at 9,793 bytes) and
595fc2b8f4 (0.673 at 9,761), nearly as fast as the big ones at three
quarters of their size.

The order changed: the two designs without multi-state caching gained
most from the move (0.752 to 0.656, 0.781 to 0.673), those with it least.
I read that as multi-state caching buying less on Zen 4 - wrongly: in the
run on the Ryzen itself, every design on the front has it. Eight
re-measured designs are no basis for a claim about a gene.
