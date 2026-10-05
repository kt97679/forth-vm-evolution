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
| `itc` | indirect threading (Iteration 29): every reference the address of a code field holding the handler's address - two loads before the jump; a colon word's code field holds `docol` |
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

**The 256-entry table, already in the engine lab, never measured.** CV8
tells an opcode from a call with `if (t < 0x80)` on every dispatch - a
data-dependent branch, mispredicted whenever the run of opcodes and
calls is irregular. `-DDISPATCH256=1` (ENGINE_CFLAGS) indexes a table by
the whole byte instead, every call byte leading to the shared call
path, so the decision moves into the indirect jump's predicted target.
`-DSIGNTEST=1` changed nothing on x86: GCC already compiles `t < 0x80`
as a sign test (the option is for RISC-V).

Measured first, it made s8 two to four times SLOWER while passing every
test: the table was a local array refilled - 256 stores - on every entry
to the interpreter, and s8 enters it each time native code runs a word
it could not translate. Now it is static and filled once. Development
VM, end to end, two builds' worth of layouts:

|  | kernel | fib | corpus | parse |
|---|---|---|---|---|
| `s5-cv8spec` | +1% | -6 to -9% | -4 to -9% | -10 to -14% |
| `s6-cv8b` | +1% | -3 to +1% | -4 to -7% | -10 to -14% |
| s8 | -3 to +1% | | | |

A real gain for the interpreters where calls and opcodes interleave
most; not yet the default.

## Iteration 29: indirect threading, priced

Added as `itc` - fig-Forth's, eForth's, gforth-itc's dispatch - and timed
with the rest on the development VM (one CPU, no cycle counters: CPU time,
the median of 5 rounds - `run.py` keeps the median since this iteration,
as the evolver does since Iteration 25):

```
gcc - CPU ms, median of 5; ratio to switch without superinstructions
    variant                                  fib                      loop                     sieve
    switch                          142.8  1.000              324.6  1.000              165.2  1.000
    switch + super                   77.3  0.541              270.4  0.833              145.4  0.880
    token                            84.8  0.594              186.8  0.575              111.3  0.674
    token + super                    49.4  0.346              160.6  0.495               85.5  0.517
    direct                           69.6  0.488              194.3  0.599               98.9  0.599
    direct + super                   43.7  0.306              156.7  0.483               79.0  0.478
    itc                              81.8  0.573              191.9  0.591              102.5  0.621
    itc + super                      54.2  0.380              159.9  0.493               76.7  0.464
    tail                             65.8  0.461              190.0  0.585               97.4  0.590
    tail + super                     44.9  0.314              177.2  0.546               78.6  0.476
    native                           67.3  0.472              189.2  0.583              104.9  0.635
    native + super                   45.7  0.320              155.8  0.480               76.6  0.464
    native2                          73.7  0.516              202.3  0.623              112.1  0.679
    native2 + super                  48.7  0.341              158.4  0.488               83.8  0.507

gcc, no endbr64 - CPU ms, median of 5; ratio to switch without superinstructions
    variant                                  fib                      loop                     sieve
    switch                          123.4  1.000              334.1  1.000              160.9  1.000
    switch + super                   82.2  0.666              283.2  0.848              129.1  0.802
    token                            73.9  0.599              187.4  0.561              114.1  0.709
    token + super                    63.0  0.511              159.1  0.476               88.7  0.551
    direct                           68.2  0.553              202.0  0.605              139.2  0.865
    direct + super                   44.5  0.361              155.4  0.465               80.0  0.498
    itc                              82.6  0.670              185.3  0.555              104.3  0.648
    itc + super                      47.4  0.384              179.2  0.536               81.1  0.504
    tail                             76.2  0.617              223.1  0.668              107.4  0.667
    tail + super                     44.5  0.361              170.7  0.511               82.5  0.513
    native                           81.9  0.664              217.5  0.651              107.9  0.671
    native + super                   47.9  0.389              179.4  0.537               81.9  0.509
    native2                          69.7  0.565              187.1  0.560               98.3  0.611
    native2 + super                  42.6  0.345              155.8  0.466               74.5  0.463
```

On this machine the lab's repeats of one variant differ by 10-40% (direct
threading on sieve: 0.599 in one build, 0.865 in the other), so it does not
separate `itc` from `token` and `direct`: it lands in their band, faster on
some cells and slower on others. By construction it cannot beat direct
threading - direct threading's work and one load more. **Priced, not built
as a gene**: its code is a cell (8 bytes) a reference against CV8's 1-3,
which puts it beside hand-made s0-cell - 25,144 bytes at 1.2 of s6's time,
never near a front - with no speed to pay for the size.
