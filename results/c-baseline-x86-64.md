# The Forth designs against the same benchmarks in C (lab/evolve/c-baseline.py)

Milliseconds of CPU time, the median of 5 runs, start-up subtracted; each design also as a multiple of C -O2. Host: Linux-6.18.44-fc-v114-x86_64-with-glibc2.39. On the development VM timing is noisy (~10%).

| workload (long) | C -O2 | C -O0 | s6 | 28677d13b1 | 0af26c8e89 | add5ec8937 |
|---|---|---|---|---|---|---|
| fib x2 | 2.7 | 14.2 (5.2x) | 78.2 (28.6x) | 13.9 (5.1x) | 15.6 (5.7x) | 59.7 (21.9x) |
| loop x10 | 2.8 | 9.0 (3.3x) | 89.7 (32.5x) | 4.7 (1.7x) | 4.3 (1.6x) | 87.2 (31.6x) |
| sieve x3 | 0.8 | 1.9 (2.5x) | 27.6 (35.7x) | 2.7 (3.5x) | 2.9 (3.7x) | 25.5 (32.9x) |
| bubble x12 | 1.0 | 1.3 (1.3x) | 34.6 (33.1x) | 3.6 (3.4x) | 4.7 (4.5x) | 35.4 (34.0x) |
| ackermann x23 | 0.5 | 6.7 (13.4x) | 13.0 (26.1x) | 8.4 (16.8x) | 8.5 (17.0x) | 14.0 (28.0x) |
| parse x3 | 5.9 | 9.6 (1.6x) | 80.9 (13.7x) | 11.5 (1.9x) | 25.5 (4.3x) | 172.7 (29.3x) |
| geometric mean, x C -O2 | 1 | 3.2x | 27.1x | 3.9x | 4.7x | 29.3x |
