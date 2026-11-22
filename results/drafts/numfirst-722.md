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

## 723: the C form priced

results/drafts/numfirst-c-723.py: (FIND) - klookup's C lookup - answers c-addr 0 at once for a token of the form
-?[0-9]+, what its walk would answer while no name of that form is defined (the flag assumed clear: none of the
workloads defines one); INTERPRET's NUMBER? converts it as before, so BASE does not enter and nothing else changes.
The engine's copy patched at L_x_find (vm-lab.c's and gen-tos.py's TOS body) under -DNUMFIRST_C=1, the image the
same. Every role with klookup (nine; smallest has none - the Forth form is its), 8-byte cells, instructions under
cachegrind, C form / base; dispatches 1.0000 everywhere (by construction, checked); every output the same.

| design | kernel | corpus | parse (held out) | apps | engine bytes |
|---|---|---|---|---|---|
| best-all-round df097ba2e2 | 1.0037 | 0.9870 | 0.9709 | 1.0003 | +144 |
| fastest-x86-32 11f956db93 | 1.0033 | 0.9864 | 0.9763 | 1.0001 | +80 |
| fastest-x86-64 9b15ba26f7 | 1.0037 | 0.9902 | 0.9774 | 1.0002 | +64 |
| least-memory fb0d57c8a2 | 1.0001 | 0.9742 | 0.9761 | 0.9999 | +96 |
| portable-arm a8d35bdccc | 1.0017 | 0.9908 | 0.9864 | 1.0000 | +320 |
| portable-fastest d727605472 | 1.0009 | **0.9287** | **0.9226** | 0.9997 | +96 |
| portable-knee 48a012411a | 1.0001 | **0.9054** | **0.8974** | 0.9995 | +80 |
| portable-small ae99617f06 | 0.9993 | **0.9251** | **0.9227** | 0.9996 | +96 |
| small-jit 15eda54ebd | 0.9989 | **0.9160** | **0.9139** | 0.9908 | +96 |

**Read**: the C form costs no dispatch and saves 1-10 % of the corpus's instructions and 1.4-10 % of parse's - most on
the portable designs and small-jit, least on the three fastest (why not traced); the kernel workload, its
tokens nearly all names, pays the test on every FIND: up to +0.37 % on the fastest three, nothing elsewhere; apps flat.
The real gene adds the flag (one load in (FIND), the header word's test per definition). So numfirst prices as two
forms: the Forth one for designs without klookup (smallest: dispatches corpus 0.748), the C one with it (instructions
corpus 0.905-0.990) - for the reopened search, the owner's call.
