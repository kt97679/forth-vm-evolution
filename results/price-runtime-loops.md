# Loop words in code compiled at run time, and the far-call reach - priced by counting

Iteration 28, on the development VM: dispatch counts and addresses are the
same on every machine, so nothing here needs the laptop.
`lab/evolve/loopwords.py 2db525ff95 9e50623ac1 8dc0f97f2c --db <seed 5's>`.

**Loop words at run time - priced, not built.** If code compiled at run
time used the format-10 loop opcodes instead of calling (LOOP), I and the
rest - and dropped the alignment NOOPs before their operands:

| workload | fewer dispatches |
|---|---|
| kernel | 0.1% |
| fib, parse | 0 (no counted loops in code compiled at run time) |
| corpus | 0.8-1.0% |
| loop (held out) | 68-70% |

On what selection measures, about a quarter of a per cent - not worth the
compiler change. The held-out loop would lose two thirds of its dispatches
(400,400 entries to (LOOP), 400,000 to I, 400,800-801,200 NOOPs): the case
for it is real programs with counted loops, and building it for the
held-out benchmark would make the held-out benchmark mean nothing. Kept as
a known gap; revisit if a selection workload compiles counted loops.

**The far-call reach - measured, not checked.** The highest code address any
workload runs: about 68 KB (the kernel workload; the others under 19 KB).
The far form reaches 2 MB at scale 0 with one-byte calls, 4 MB without:
30 times the room. A check in cv8.4's compiler would cost bytes in every
image to guard against programs these workloads come nowhere near. A
documented limit, not a check.

## The counts

pinned to cpu 0 (it and its sibling 0% busy; BENCH_CPU=N to choose)
## 2db525ff95 - 14,017 bytes, format-10 words in the image: I, (DO), UNLOOP, J, (?DO), (+LOOP), (LEAVE)

| workload | dispatches | run-time entries: (DO), (?DO), (LOOP), (+LOOP), (LEAVE), I, J, UNLOOP | in their bodies | NOOPs outside the image | the price: fewer dispatches |
|---|---|---|---|---|---|
| kernel | 6757707 | 47, 46, 156, 124, 0, 312, 0, 0 | 32463 | 1410 | 7472 (0.1%) |
| fib | 26975790 | 0, 0, 0, 0, 0, 0, 0, 0 | 564 | 0 | 0 (0.0%) |
| parse | 26845670 | 0, 0, 0, 0, 0, 0, 0, 0 | 384 | 0 | 0 (0.0%) |
| corpus | 4919775 | 1176, 0, 2036, 20, 1, 1857, 26, 2 | 56833 | 12386 | 49821 (1.0%) |
| loop | 9654444 | 401, 0, 400400, 0, 0, 400000, 0, 0 | 6808399 | 801200 | 6808006 (70.5%) |

## 9e50623ac1 - 13,073 bytes, format-10 words in the image: I, (DO), UNLOOP, J, (LOOP), (?DO), (+LOOP), (LEAVE)

| workload | dispatches | run-time entries: (DO), (?DO), (LOOP), (+LOOP), (LEAVE), I, J, UNLOOP | in their bodies | NOOPs outside the image | the price: fewer dispatches |
|---|---|---|---|---|---|
| kernel | 6887936 | 47, 46, 156, 124, 0, 312, 0, 0 | 6388 | 1474 | 7177 (0.1%) |
| fib | 29669971 | 0, 0, 0, 0, 0, 0, 0, 0 | 0 | 0 | 0 (0.0%) |
| parse | 28121833 | 0, 0, 0, 0, 0, 0, 0, 0 | 0 | 0 | 0 (0.0%) |
| corpus | 5094627 | 1176, 0, 2036, 20, 1, 1857, 26, 2 | 39517 | 12507 | 46906 (0.9%) |
| loop | 9254418 | 401, 0, 400400, 0, 0, 400000, 0, 0 | 6407206 | 801200 | 6407605 (69.2%) |

## 8dc0f97f2c - 9,458 bytes, format-10 words in the image: I, (DO), UNLOOP, J, (LOOP), (?DO), (+LOOP), (LEAVE)

| workload | dispatches | run-time entries: (DO), (?DO), (LOOP), (+LOOP), (LEAVE), I, J, UNLOOP | in their bodies | NOOPs outside the image | the price: fewer dispatches |
|---|---|---|---|---|---|
| kernel | 7083412 | 47, 46, 156, 124, 0, 312, 0, 0 | 6388 | 1864 | 7567 (0.1%) |
| fib | 29671740 | 0, 0, 0, 0, 0, 0, 0, 0 | 0 | 0 | 0 (0.0%) |
| parse | 31150169 | 0, 0, 0, 0, 0, 0, 0, 0 | 0 | 0 | 0 (0.0%) |
| corpus | 5419660 | 1176, 0, 2036, 20, 1, 1857, 26, 2 | 39517 | 10906 | 45305 (0.8%) |
| loop | 8854853 | 401, 0, 400400, 0, 0, 400000, 0, 0 | 6407206 | 400800 | 6007205 (67.8%) |

