# Source audit 3: where seed 50's fastest designs still dispatch (Iteration 299)

The third look, by exact counts (lab/evolve/hotwords.py, lab/evolve/word-cost.py - the
JIT off, every dispatch charged to the word whose body holds it), at seed 50's fastest
design without the JIT (658ed9b9f8), fastest with it (e23b0e4770), smallest
(4c2b4e4485) and Q-best (ed821c2edc). The first two audits found 2@, 2! and DEPTH
(results/source-audit-2.md) and, pricing a digit table, NUMBER? - all now opcodes, or
a gene, applied after seed 50.

The hottest words, as a mean share over the six selection workloads:

| design | the hottest words |
|---|---|
| 658ed9b9f8 | 2@ 5.8%, INTERPRET 4.8%, PARSE-WORD 2.3%, NUMBER? 2.2%, > 2.0%, 2! 1.9%, 0= 1.4%, ?STACK 1.3% |
| e23b0e4770 | 2@ 5.9%, WORD 2.4%, INTERPRET 2.4%, > 2.0%, NUMBER? 2.0%, (F2) 1.6%, 2! 1.6%, PARSE-WORD 1.4% |
| 4c2b4e4485 | NEXT-NFA8 8.5%, (LOOP) 7.7%, (+LOOP) 6.8%, I 6.1%, SEARCH-WORDLIST 4.7%, SCAN 2.9%, (F37) 2.9%, 2@ 2.0% |
| ed821c2edc | 2@ 5.9%, INTERPRET 4.9%, PARSE-WORD 2.4%, NUMBER? 2.2%, > 2.0%, 2! 1.6%, 0= 1.4%, ?STACK 1.3% |

Per workload, on 658ed9b9f8: **> is 11.7% of bubble's dispatches, 0= 7.7% of
ackermann's, ?STACK 7.4% of the corpus's** - each under 1% elsewhere.

- **> and 0=**: kernel colon words (`SWAP <`, `0 =`) that code compiled at run time
  calls - the benchmarks' own. Built (after-seed-51 patch 2): pool words and opbody's,
  so opinline compiles them in. Measured with them first, opbody and opinline:
  bubble -11.7%, ackermann -7.7%; the kernel +5.5% and the corpus +8.7% for the two
  words they pushed out of a full list - evolution places them.
- **?STACK** (corpus 7.4%): it needs the stack's base, S0, as DEPTH does - an opcode
  given S0 @ by an overlay's wrapper, as knumber is given BASE: a gene for later.
- **INTERPRET, PARSE-WORD, WORD**: the outer interpreter's loop, long words calling
  others - nothing an opcode takes whole.
- **The smallest design's** costs are the lookup and the loops in Forth - the size
  trade the evolution made (no klookup, few format-10 words), not a gap.
- (F2), (F37): factor's shared bodies - its own trade.
