# The answers to the related-work prompt, checked (Iteration 539)

Five answers to results/drafts/ask-related-work-537.md (the owner, 539), for the article. Their references checked;
the ones that matter for the article's claims found by search.

## What the prior work is - verified

| work | what it established | checked |
|---|---|---|
| Bell, "Threaded Code", CACM 16(6), 1973 | threaded code itself | known |
| Graves and Stigall, "Investigation of Threaded Code", Univ. of Missouri-Rolla tech. report 120, 1991 | a classification of threaded-code designs; token and variable-depth indirect threading measured for code size and time in a Forth on a transputer | **found** |
| Ertl, "Stack Caching for Interpreters", PLDI 1995 | stack caching | known (Ertl alone - one answer added Gregg) |
| Ertl, Gregg, Krall, Paysan, "vmgen - a generator of efficient virtual machine interpreters", SPE 2002 | threaded code, TOS caching, superinstructions generated from descriptions - a generator, not a search | known |
| Casey, Ertl, Gregg, "Optimizing Indirect Branch Prediction Accuracy in Virtual Machine Interpreters", TOPLAS 2007 | static and dynamic superinstructions and replication, in Forth and Java | **found** |
| Hoste and Eeckhout, "COLE: Compiler Optimization Level Exploration", CGO 2008 | multi-objective evolutionary search for Pareto-optimal compiler settings - size, speed, compile time | known; **the method is prior art** |
| Kulkarni et al., VISTA phase-sequence search, LCTES 2003 / TACO 2005; Cooper, Schielke, Subramanian, GA for code size, LCTES 1999 | genetic search over compiler phases, code size as an objective | known |
| Miedema, "QuickInterp", Univ. of Twente M.Sc. thesis, 2020 | profile-driven, iterative selection of a JVM's superinstruction set, the interpreter generated | **found** |
| Hu, Zhao, Scholz, "Synthesizing Efficient Super-Instruction Sets for Ethereum Virtual Machine", VMIL 2024 | automated superinstruction synthesis (compression and greedy heuristics), a meta-compiler generating the interpreter | **found** |
| Xu and Kjolstad, "Copy-and-Patch Compilation", OOPSLA 2021 | the JIT technique - a fixed stencil library | known |

**Wrong or unverifiable**: one answer (80) gave copy-and-patch's origin as "Shuf et al., 'Exploiting Hoops', IBM c. 2001" -
the technique is Xu and Kjolstad's (2021); also "Ertl, Efficient Representation of Polymorphic Code, PEPM 2001" and
"Chang and Uno 1999", not found. Venue examples in another (81) - particular Habr articles - unchecked; they are
illustrations, not citations.

## What would be new - their consensus, and ours

Every technique is prior art - threaded and token codes, stack caching, static and dynamic superinstructions, interpreter
generation, automated superinstruction selection, copy-and-patch, and multi-objective evolutionary search over a
system's settings (COLE). **What none of the verified work does is the integration**: one search over the encoding
itself, the fusion, caching, headers, variable access, compiler flags *and the JIT's own choices* as genes, with size,
speed and memory equal and the winners checked on held-out programs and other machines. Claim that, as an empirical
study - not "the first evolutionary optimisation of a VM", not "the first automatic interpreter optimiser". (Answer
82's suggested wording is a good start.)

## For the article - what they agree readers will want

The numbers first (14 KB; 0.13-0.15 of the reference's time - written as 7 times faster, not "0.14x faster"); the
Pareto front plotted; a table of what the search kept and what it refused; the lineage credited (Bell, Ertl and Gregg,
vmgen, Xu and Kjolstad, COLE); objectives defined exactly (which bytes, which programs, how memory is read);
comparisons with Forths readers know (Gforth, eForth, Mecrisp, JonesForth); and the artefacts - repository, gene
schema, a script that reruns a small search. **One addition worth taking (82)**: a baseline of plain random search (or
an ablation) at the same budget, so the article can say what the evolutionary search itself contributed.

## The answers, ranked

82 the best: verified references, a careful table of which claims are new and which are not, exact advice on defining
the objectives, the random-search baseline. 79 accurate and suitably hedged. 81 useful, with some unverifiable examples.
80 good audience advice, but a fabricated origin for copy-and-patch and other doubtful references. 78 thin.
