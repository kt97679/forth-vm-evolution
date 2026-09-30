# The fastest C dispatch loop for Forth

`dispatch.c` is one small Forth machine written six ways, running the
same three programs; `run.py` checks that every way gives the same
answers and then times them, interleaved, through `tools/cputime` -
cycles and instructions per cycle where the hardware counters can be
read, CPU time otherwise.

    lab/dispatch/run.py [ROUNDS]

| design | how it dispatches |
|---|---|
| `switch` | a switch on compact word code - the textbook baseline |
| `token` | the same code, computed goto through a table (the CV8 engine) |
| `direct` | direct threading: the code is the label addresses |
| `tail` | tail-call threading: each primitive a C function, the machine's state in argument registers, each ending in a jump to the next |
| `native` | as `tail`, with Forth CALL a real machine call and EXIT a real return, for the return predictor |
| `native2` | as `native`, with the top two stack items in registers |

Each also runs with superinstructions (`-s`): `DUP n < IF` and `n +`
fused, as SPN fuses them. And `run.py` builds everything twice: with the
compiler's defaults, and with `-fcf-protection=none`, which drops the
`endbr64` Ubuntu's compiler puts at every indirect-jump target - Linux
does not enforce it for user programs, so it is decode overhead on every
dispatch. With clang installed it adds a clang build, where GCC before
15 has no `musttail`: the tail calls rely on `-O2`, and every handler
was checked to end in a jump.

Programs: recursive `fib` (calls), a countdown loop (pure dispatch), and
the classic byte sieve (memory and nested loops).

## Development VM (Intel Xeon, virtualised), CPU ms, best of 5

| design | fib | loop | sieve |
|---|---|---|---|
| `switch` | 129.3 (1.00) | 424.1 (1.00) | 197.5 (1.00) |
| `switch` + super | 75.9 (0.59) | 355.7 (0.84) | 153.1 (0.78) |
| `token` | 70.7 (0.55) | 195.0 (0.46) | 124.1 (0.63) |
| `token` + super | 48.1 (0.37) | 166.7 (0.39) | 94.5 (0.48) |
| `direct` | 66.8 (0.52) | 212.4 (0.50) | 108.7 (0.55) |
| `direct` + super | 41.8 (0.32) | 177.2 (0.42) | 79.9 (0.40) |
| `tail` | 61.2 (0.47) | 212.9 (0.50) | 101.0 (0.51) |
| `tail` + super | 41.8 (0.32) | 178.1 (0.42) | 78.5 (0.40) |
| `native` | 65.6 (0.51) | 213.5 (0.50) | 100.8 (0.51) |
| `native2` | 77.8 (0.60) | 232.0 (0.55) | 118.1 (0.60) |
| `tail` + super, no `endbr64` | 40.1 (0.31) | 160.4 (0.38) | 80.2 (0.41) |

- **Superinstructions are the largest single win** in every design,
  30-40% off fib. Once off `switch`, what is fused matters more than how
  it is dispatched.
- **Tail-call threading is the fastest pure dispatch** on fib and sieve,
  and with superinstructions the fastest or tied everywhere; direct
  threading with superinstructions is within about 5%.
- **Dropping `endbr64` is free:** up to 17% for `switch`, about 8% for
  token and tail threading; direct threading unchanged.
- **Real calls and returns lost here** - fib 7% slower than `tail`. The
  call handler saves registers around each call, which costs more than
  the return predictor saves on this processor.
- **Two stack items in registers lost** by 10-20%: every push and pop
  now also moves a value between the two registers. A single fixed
  caching state does not pay; several states would, at the price of
  several copies of every primitive.

One virtualised Intel processor, CPU time: the ordering, not the third
digit. Real hardware with cycle counts decides - especially `native`,
whose premise is a return predictor this VM may not show.

## What carried over to the real engines

**Dropping `endbr64` did not, mostly.** Built with
`ENGINE_CFLAGS=-fcf-protection=none` (tools/engine-rt.sh), the cell
engine ran about 5% faster, consistently; CV8 and SPN moved by under 2%
either way. The lab's 8% for token threading was not the real CV8
engine's, whose dispatch cost lies elsewhere. The default is unchanged:
it would shift every ratio - the cell engine is the baseline - for
nothing on the systems that matter.

**Superinstructions did.** Profiling what feeds CV8's ?BRANCH chose
eight compare-and-branch fusions for SPN: 3-5% faster on kernel, corpus
and parse (FINDINGS-SPN.md, "Compare-and-branch, fused").
