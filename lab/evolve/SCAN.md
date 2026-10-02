# Mutational scan

Every single-gene change of every hand-made design, checked for
correctness only: corpus identical to the cell engine, kernel reproduced.

| design | changes | alive | the changes that die |
|---|---|---|---|
| s0-cell | 7 | 7 | - |
| s1-sod16 | 8 | 8 | - |
| s2-cpt16 | 12 | 10 | scale=2 (image did not convert); scale=3 (image did not convert) |
| s3-cpt16f | 16 | 16 | - |
| s4-cv8 | 28 | 25 | scale=0 (timed out); scale=1 (kernel workload); bytehdr=1 (kernel workload) |
| s5-cv8spec | 28 | 25 | scale=0 (timed out); scale=1 (timed out); bytehdr=1 (kernel workload) |
| s6-cv8b | 25 | 23 | doesfar=0 (kernel workload); varcall=0 (kernel workload) |

Every death is a limit the design really has:

- **s2-cpt16, scale 2 and 3**: skip-pad removes the alignment padding
  that 4- and 8-byte call granularity needs; the converter refuses
  (`call target not 4-aligned`).
- **CV8 at scale 0 or 1 with a two-byte-only form** - calls without
  `varcall`, or near DOES> calls: 2^14 units reach 16 KB or 32 KB, and the
  kernel workload's dictionary is larger. The same designs with both far
  forms live (s4 and s5 at scale 1, s5 at scale 0). The `bytehdr=1`
  changes are this case too: byte headers are built at scale 0.

The scan found the fourth mapping bug (far DOES> needs VARCALL, now a
rule in the genome), and the survival check's own flaw: the kernel
workload's directory started with a copy of the reference kernel, so a
design that died quietly before saving passed. Run it again with
`lab/evolve/scan.py --design NAME` for each design, then `--report`.
