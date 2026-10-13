# Three ideas from the outside reviews, priced (Iteration 238)

## Dropping the JIT stencils a design never uses: not worth it

All 43 stencils together are about 1,000 bytes of a JIT engine (cc6d168e0a,
28677d13b1, b4bb7d554b: 1,007 / 1,007 / 995 bytes). The ones a design's own
operation table never names are 105-227 bytes - and two of them, st_call and
st_interp, the translator uses itself. What could go is 50-170 bytes, 0.2-0.5%
of a JIT design's binary + image. Not built.

## The JIT translator compiled for size: -416 to -800 bytes, found on the way

Where a JIT engine's extra bytes are: the translator, jit_body alone 3,456
bytes - not the stencils. It runs once per word translated, not per
instruction, so it need not be compiled for speed. jit.c under GCC's
`optimize ("Os")` (a pragma around its #include, `-DJITOS=1`):

| design | engine | translator -Os | fib, ms (VM, noisy) |
|---|---|---|---|
| cc6d168e0a | 23,452 | 22,652 (-800) | 12.1 -> 9.4 |
| 28677d13b1 | 23,036 | 22,620 (-416) | 16.2 -> 9.5 |
| b4bb7d554b | 15,996 | 15,996 (0: built -Os already) | 13.9 -> 13.7 |

All alive. The fib times are within the VM's noise; translation happens on
the kernel and corpus workloads too, so the trade belongs to evolution: a gene
`jitos` (0, 1), proposed.

## A Bloom filter for names not found: dominated by the threads gene

Where the smallest design's dispatches go (add5ec8937, 16 chains, the profiler's
count by word): the lookup - NEXT-NFA8, SEARCH-WORDLIST, NAME=?, FIND, NAME>BUF,
HASH - is 66.3% of the corpus's 59.0M dispatches, 69.0% of parse's 149.0M,
35.6% of the kernel's 8.5M. Names not found are 57% of the walk on the corpus
and 49% on parse (results/price-lookup-cache.md). A filter of 256 bytes over
~350 names (two hashes, ~8% false positives) would skip ~90% of those walks:
about a third of the corpus's and parse's dispatches, a sixth of the kernel's.

But the threads gene already offers more for the same bytes: 64 chains cut the
whole walk, found and not found, by three quarters (corpus 23.5 -> 6.1 entries a
lookup) for 384 bytes of heads more than 16 - and evolution has declined that
trade at the small end every run (16 chains on 85 of seed 44's 120, never 64 or
128). A filter would cost its bits (256 bytes in the image, or code to build
them at start-up) and its code in the lookup and in every header made (~100
bytes) for half the effect. Not built; it would be worth it only far cheaper.
