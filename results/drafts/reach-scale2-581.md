# Why only threads=2 reaches the scale-2 limit (Iteration 581)

Seed 85's 69 kernel-workload deaths at scale 2 all had threads=2 - 128 chains a wordlist (576 accepted them as the reach
limit, deaths-check's expected()). Rebuilt here (reach-scale2-581.py on seed 85's db.jsonl), the first three:

| design | threads 0 (32) | 1 (64) | 2 (128) | 3 (16) |
|---|---|---|---|---|
| 6a587954c8 | right, 16,321 B | right, 16,577 | **WRONG**, 17,089 | right, 16,193 |
| d214e20b62 | right, 17,545 | right, 18,057 | **WRONG**, 19,081 | right, 17,289 |
| 9cf2fc0481 | right, 17,936 | right, 18,448 | **WRONG**, 19,472 | right, 17,680 |

At threads 2 (6a587954c8, d214e20b62 - both died with varcall 1, doesfar 0): both far forms on - right; scale 3 - right;
scale 1 - WRONG. So it is the reach: the near DOES> form at scale 1 or 2 cannot reach what the kernel workload compiles
past it. The image itself grows only 1-2 KB with 128 chains; the growth that matters is at run time - the kernel
workload's meta-compiler makes wordlists, and each takes 128 cells at 128 chains (inferred, not traced). No fault: the
designs die at the kernel workload, as 576 judged, and deaths-check's expected() names them.
