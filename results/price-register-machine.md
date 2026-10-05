# A register machine, priced by counting

Iteration 29, on the development VM - dispatch counts are the same on every
machine. `lab/evolve/stackops.py 9e50623ac1 8dc0f97f2c 2db525ff95 --db
<seed 5's>`: for three of seed 5's front designs - which already carry pairs
and stack caching - the share of dispatches that only move values (DUP DROP
SWAP OVER ROT >R R> R@ 2DUP 2DROP, I J UNLOOP, and pairs of those) or push
a literal alone, which a register instruction would carry as operands.

| workload | moves only | literals alone | the bound |
|---|---|---|---|
| kernel | 34-35% | 4% | 38-39% |
| fib | 23-25% | 23-25% | 45-50% |
| parse | 31-38% | 6-8% | 39-45% |
| corpus | 34-38% | 5-6% | 39-43% |
| loop (held out) | 48-50% | 0 | 48-50% |

**The prize is the largest left**: up to 38-50% of dispatches, the 46% Shi,
Gregg and Beatty found for a register JVM. It is a bound: Forth words take
and return everything on the stack, so moves at every call and return stay
- fib, a call and a return a level, keeps more of them than the rest. Pairs
already fold some (DUP >R, R@ ROT are among the biggest movers) and stack
caching saves their memory traffic, not their dispatches.

**The cost is the largest too**: operands in every instruction (the JVM's
+26% of code; against CV8's one-byte, operand-free instructions likely
more), a stack-to-register translation in the converter, register forms of
the engine's handlers in every engine family, and either register code from
the run-time compiler or a machine that runs both. A staged plan in
GOALS.md; not started.

## The counts

pinned to cpu 0 (it and its sibling 1% busy; BENCH_CPU=N to choose)
## 9e50623ac1 - 13,073 bytes

| workload | dispatches | moves only | literals alone | bound on what registers remove | the biggest movers |
|---|---|---|---|---|---|
| kernel | 6887936 | 34.7% | 3.6% | 38.3% | SWAP 7.3%, DUP 6.1%, DUP >R 5.0%, R@ ROT 3.8% |
| fib | 29669971 | 22.7% | 22.7% | 45.4% | DUP 13.6%, SWAP 4.6%, DROP 4.5%, DUP >R 0.0% |
| parse | 28121833 | 35.6% | 6.4% | 42.0% | DUP 8.1%, SWAP 7.6%, DUP >R 4.6%, R@ ROT 3.6% |
| corpus | 5094627 | 35.9% | 5.0% | 40.9% | SWAP 7.9%, DUP 6.9%, DUP >R 5.0%, R@ ROT 3.7% |
| loop | 9254418 | 47.8% | 0.0% | 47.8% | DUP 13.0%, R> 13.0%, >R 8.7%, R@ 8.7% |

## 8dc0f97f2c - 9,458 bytes

| workload | dispatches | moves only | literals alone | bound on what registers remove | the biggest movers |
|---|---|---|---|---|---|
| kernel | 7083412 | 34.0% | 3.9% | 37.9% | SWAP 6.9%, DUP 6.8%, DUP >R 4.9%, R@ ROT 3.7% |
| fib | 29671740 | 22.7% | 22.7% | 45.4% | DUP 13.6%, SWAP 4.5%, DROP 4.5%, DUP >R 0.0% |
| parse | 31150169 | 30.7% | 7.8% | 38.6% | DUP 9.0%, SWAP 5.6%, DUP >R 4.1%, R@ ROT 3.3% |
| corpus | 5419660 | 33.5% | 5.9% | 39.3% | DUP 7.9%, SWAP 6.8%, DUP >R 4.7%, R@ ROT 3.5% |
| loop | 8854853 | 49.9% | 0.0% | 49.9% | DUP 13.6%, R> 13.6%, >R 9.1%, R@ 9.0% |

## 2db525ff95 - 14,017 bytes

| workload | dispatches | moves only | literals alone | bound on what registers remove | the biggest movers |
|---|---|---|---|---|---|
| kernel | 6757707 | 35.3% | 3.8% | 39.1% | SWAP 6.8%, DUP 6.2%, DUP >R 4.5%, R@ ROT 3.8% |
| fib | 26975790 | 25.0% | 25.0% | 50.0% | DUP 15.0%, SWAP 5.0%, DROP 5.0%, DUP >R 0.0% |
| parse | 26845670 | 37.7% | 6.9% | 44.6% | DUP 8.6%, SWAP 7.6%, DUP >R 4.4%, R@ ROT 3.8% |
| corpus | 4919775 | 37.6% | 5.3% | 42.9% | SWAP 7.6%, DUP 7.3%, DUP >R 4.6%, R@ ROT 3.8% |
| loop | 9654444 | 49.9% | 0.0% | 50.0% | R> 12.5%, DUP 12.5%, >R 12.5%, R@ 8.3% |

