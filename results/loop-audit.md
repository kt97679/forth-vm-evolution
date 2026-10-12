# The loops in the Forth sources - an audit (Iteration 203, the owner)

The owner: loops cost an interpreter dearly - audit the Forth sources, find
where loops can be eliminated. Two halves: every loop in the image's Forth
(results/drafts/loop-audit-inventory.py), and what each costs in the eight
workloads - the smallest front design (0ceb043115, interpreted) profiled per
word: the profiler's executions per address within each word's range
(results/drafts/loop-audit-profile.py).

## Where the loops are, and what they cost

42 of the image's 276 colon definitions loop; 16 of them never ran in any
workload. The rest, by share of each workload's dispatches:

| word | source | corpus | parse | kernel | loop | bubble | sieve |
|---|---|---|---|---|---|---|---|
| NEXT-NFA8 | cv8bt.4 | 33.9% | 35.8% | 11.9% | - | 0.1% | 0.1% |
| SEARCH-WORDLIST | kernel.4 | 19.0% | 19.0% | 9.9% | - | 0.1% | - |
| FILL | kernel.4 | - | - | 7.6% | - | - | 14.7% |
| NAME=? | cv8bt.4 | 7.0% | 4.5% | 6.2% | - | - | - |
| SCAN | kernel.4 | 4.4% | 3.7% | 6.3% | - | - | - |
| FIND | kernel.4 | 4.0% | 4.7% | 4.6% | - | - | - |
| INTERPRET | kernel.4 | 2.1% | 2.7% | 0.6% | - | - | - |
| NUMBER?, >NUMBER, SKIP | kernel.4 | 4.5% | 6.8% | 2.4% | - | - | - |

And the loop runtime itself, colon words in this design: (LOOP) 59% of
loop's dispatches, (+LOOP) 46% of bubble's, I 13-18%. fib and ackermann run in
their own compiled code (80-100%).

**One loop dominates: the name lookup** - NEXT-NFA8, SEARCH-WORDLIST and
NAME=? walk a hash chain, about 60% of corpus and parse, 22% of the kernel.

## Already eliminated, in designs that chose it

klookup makes the lookup one opcode (78 of seed 41's 171 front designs),
kinput SCAN, SKIP and the input side (117), kfast NAME>BUF's fill and the
thread walk factored (163), FILL and CMOVE as opcodes, rtloop and rtloopall
the loop runtime (130 and 42), the format-10 opcodes I and (LOOP). Each moves
a loop into C - the loop runs, its dispatches go.

## Two assumptions this audit refuted

- thinhdr (all 171 front designs) does NOT make the dictionary one chain: it
  thins the image FILE's header, the loader's copy that only SOD16 read. The
  running dictionary has 32 chains.
- FIND does NOT search FORTH twice though the order lists it twice: it skips a
  last wordlist equal to the one before (kernel.4).

## One elimination tried, measured, not shipped

NAME=? compared names a byte an iteration (~14 dispatches a character); a
cell at a time - one masked compare for names of up to seven characters, no
loop - as the kernel's cell headers once did. Profiled: NAME=? itself 2.36M ->
2.04M dispatches in the corpus, the workloads -0.4%, +0.3%, -2.3%. SEARCH-
WORDLIST8 calls it only for names of equal length, and most of those differ at
the first character, where the byte loop exits after one pass. Reverted.

## What would cut the lookup loop

The cost is the entries a lookup visits, not the work at each. Modelled on the
corpus's tokens (results/drafts/loop-audit-chains.py, 299 words, the kernel's
hash of the length and two characters): a hit visits 6.6 entries at 32
chains, a miss (numbers, new names: most of the tokens) its whole chain, 10.8;
the longest chain 19. At 64 chains the walks halve, at 128 a quarter.

1. **More chains, a gene** - 64 or 128 heads: 256 or 768 bytes more per image
   (the wordlist's heads), for lookups ~2-4x shorter - the trade the owner's
   weighing exists for. Touches kernel.4's FORTH-WORDLIST, cross.4's THASH and
   the converter's NTHREADS together (they must agree); a reseed.
2. **A lookup cache** - name to word, direct-mapped by the hash; cleared on
   every definition and every change of the search order. Removes the walk on
   a repeated name, which is most hits; misses still walk unless remembered
   too. Larger, and its invalidation must be exact.

## The engine's side: SYSCALL (the owner)

With fsys, the file words left the engine; the shell's seventeen already had.
What remains native and is I/O: WRITE (EMIT and TYPE are Forth over it), READ,
READ-LINE, OPEN-FILE, CLOSE-FILE, WRITE-FILE, BYE. OPEN-FILE and CLOSE-FILE
wait on INCLUDED (compiled against them); WRITE carries the engine's output
buffer, so moving it costs speed unless the buffer moves to Forth too.

## Built: the gene threads (Iteration 204) - results/pending/threads-after-seed42.patch

The converter files the dictionary into 16, 32 (as built), 64 or 128 chains.
Counted on the smallest design (results/drafts/threads-profile.py):

| chains | kernel | corpus | parse (held out) | image |
|---|---|---|---|---|
| 16 | 6.29M (+17%) | 49.88M (+49%) | 128.47M (+53%) | -120 to -128 bytes |
| 32 | 5.39M | 33.49M | 83.70M | as before, byte for byte |
| 64 | 4.91M (-9%) | 23.97M (-28%) | 61.37M (-27%) | +240 to +248 |
| 128 | 4.66M (-14%) | 19.71M (-41%) | 47.59M (-43%) | +686 to +712 |

The standard suite 14 of 14 as s6 at 16, 64 and 128; run-tests PASS. Two
faults on the way: the link pass sized links by the dump's 32 chains
("link does not fit" at every other count), and a stale build after the
NAME=? revert, caught by the evolver's freshness check.
