# The next keeping forms, priced again (Iteration 222)

The handoff's open item 6: after DUP+I and DUP<I (Iteration 176, fib -36%),
the next "keeping" forms - an operation that leaves an operand it reads,
absorbing the DUP or OVER before it - as results/price-hybrid.md listed them
on seed 40's smallest. Re-priced with lab/evolve/regprice.py on seed 43's
smallest (add5ec8937, interpreted): the largest absorbable patterns, as
shares of each workload's image-code dispatches (the share is the absorbed
run's own dispatches - what one form would save):

| pattern | kernel | corpus | parse | sieve | bubble |
|---|---|---|---|---|---|
| DUP before a short ?BRANCH (DUP?BRANCH8, exists) | 5.4% | 6.3% | 6.4% | 3.4% | - |
| OVER before C@ | 3.0% | 1.7% | 1.4% | - | - |
| DUP before C@ | 1.3% | 2.8% | 2.9% | - | - |
| SWAP OVER before C@ | 0.9% | 1.7% | 2.0% | - | - |
| DUP before @ | - | - | - | 3.4% | 2.1% |
| DUP ROT before + | - | - | - | - | 4.2% |

**Not built.** The largest, DUP before ?BRANCH, already has its form
(DUP?BRANCH8, Iteration 33): 121 of seed 43's 165 front designs list it, 28
have it - the format-10 names a design lists are realised in order while its
one-byte codes last, and the small designs (escape 0) realise 10-14 of the 31
they list. The small end is exactly where these patterns are hot (the JIT
designs run their hot code native, and realise all they list: 35-37), and
there the codes - and the engine bytes each handler costs - are what is short;
evolution already leaves DUP?BRANCH8 out there. New forms would queue behind
it for the same codes. If anything moves this, it is the codes: pinning a form
to a one-byte code, as DUP+I and DUP<I were for the run-time compiler, takes
one from something else - priced only by a run.
