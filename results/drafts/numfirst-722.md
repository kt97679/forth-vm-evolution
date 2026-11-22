# numfirst priced on a prototype (Iteration 722)

The gene proposed at 717 (results/drafts/esolangs-717.md): a token of the form [0-9]+ converted before the lookup,
while BASE is at least 10 and no name of that form is defined. The prototype: results/drafts/numfirst-722.4 (INTERPRET8,
loaded last among a design's overlays - the converter's X8 swap gives INTERPRET its body; the digit test in Forth, a
first-character test inline, then the rest of the token, BASE and the flag). Not built: the header word setting the flag
(a test per definition, not per token), a leading '-' (the old path). Measured by results/drafts/numfirst-722.py: the
lab's translator build of each record, with and without the overlay, each on its own build's profiling engine
(dispatches, VMPROF's I lines) and under cachegrind (instructions), 8-byte cells; every output the same.

| design | workload | dispatches proto / base | instructions proto / base |
|---|---|---|---|
| smallest 219878ec89 (the lookup in Forth) | kernel | 0.9922 | 0.9925 |
| | corpus | **0.7479** | 0.7529 |
| | parse (held out) | **0.6720** | 0.6743 |
| | apps | 0.9905 | 0.9917 |
| portable-fastest d727605472 (kfast, kinput, klookup, knumber: FIND and NUMBER? one dispatch each, in C) | kernel | 1.0103 | 1.0053 |
| | corpus | 1.0954 | 0.9835 |
| | parse (held out) | 1.1549 | 0.9812 |
| | apps | 1.0014 | 1.0007 |

Images: smallest 9,185 B against 9,037 (+148: the prototype is a whole second INTERPRET and two words - a gene would
change INTERPRET in place, so less); portable-fastest 10,394 against 10,256 (+138).

**Read**: where the lookup is Forth, 717's estimate holds - a quarter of the corpus's dispatches and a third of parse's
go, the kernel and apps about 1 % (their literals a smaller share, 717's 7.4 % and 10.8 %); fib, loop, bubble and
ackermann do not interpret. Where FIND and NUMBER? are one dispatch each (klookup, knumber), the Forth digit test costs
more dispatches than the lookup it skips (+9.5 % corpus, +15.5 % parse), though the C walk it saves still nets about
-2 % of instructions on both; there the test belongs in C - (NUMBER?)'s own scan, or FIND's opcode refusing a
digits-only token - an engine change, not priced. So numfirst is two forms: the Forth test for designs without
klookup (+~100 B, -25 % on the corpus), the C test for those with it (+tens of engine bytes, ~-2 % instructions on
the corpus) - offered to the reopened search as a gene (the owner's call), the Forth form first.
