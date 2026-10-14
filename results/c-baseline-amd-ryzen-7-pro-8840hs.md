# The designs against the same benchmarks in C, on the AMD Ryzen 7 PRO 8840HS (Iteration 285)

lab/evolve/c-baseline.py on the laptop (pack forth-vm-evolution-c-baseline-f607d18fb-fury-20261014-052000):
hand-made s6 and the newest front's fastest (e141550b9a), knee (037722ab8a, the best Q) and
smallest (7535695a36), each workload's long form against bench/c's C at -O2 and -O0 - CPU
milliseconds, and in brackets the multiple of C -O2's. The VM's numbers
(c-baseline-x86-64.md) were too noisy to keep; these replace them.

| workload (long) | C -O2 | C -O0 | s6 | e141550b9a | 037722ab8a | 7535695a36 |
|---|---|---|---|---|---|---|
| fib x2 | 2.3 | 7.3 (3.2x) | 43.3 (19.1x) | 10.2 (4.5x) | 13.8 (6.1x) | 46.8 (20.6x) |
| loop x10 | 2.5 | 4.2 (1.7x) | 76.9 (30.8x) | 9.1 (3.7x) | 9.9 (4.0x) | 85.7 (34.3x) |
| sieve x3 | 0.9 | 1.2 (1.3x) | 27.0 (29.1x) | 3.1 (3.3x) | 3.6 (3.9x) | 25.7 (27.7x) |
| bubble x12 | 0.9 | 1.1 (1.2x) | 31.9 (35.5x) | 3.0 (3.3x) | 3.0 (3.3x) | 32.3 (36.0x) |
| ackermann x23 | 0.8 | 2.0 (2.7x) | 12.6 (16.4x) | 3.9 (5.1x) | 4.6 (6.0x) | 13.1 (17.1x) |
| parse x3 | 4.3 | 5.8 (1.4x) | 84.9 (20.0x) | 12.0 (2.8x) | 13.5 (3.2x) | 213.5 (50.2x) |
| geometric mean, x C -O2 | 1 | 1.8x | 24.2x | 3.7x | 4.2x | 29.1x |

Start-up (ms): C -O2 0.42 ms; C -O0 0.72 ms; s6 0.65 ms; e141550b9a 0.37 ms; 037722ab8a 0.23 ms; 7535695a36 0.46 ms - the Forth
engines, built without the C library, start as fast as C or faster.

- **The fastest design is 3.7x C -O2 on the geometric mean** - 2.8x to 5.1x by workload - and
  2x C at -O0; the knee 4.2x. s6, the hand-made interpreter, is 24x; the smallest 29x.
- **parse, held out of the selection, is the smallest's weak side**: 50x C, where s6 is 20x -
  it carries none of the operations the evolution chose for parsing and lookup (kfast,
  kinput, klookup). Every other workload it runs within 10% of s6.
