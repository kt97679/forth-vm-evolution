# Are the winning designs original? (Iteration 605)

The owner, 605: the search was meant to find good designs "not covered by any existing project or publication"; "it
would be interesting to see if best designs we found are really original or they were described somewhere else".
Iteration 539 answered for the method (results/drafts/ask-related-work-answers-539.md: every technique prior art, the
integration not); this asks it of the designs - the nine of results/handoff-relf-601.md, by what they are built from.
From 539's verified list and five searches here (605); which winners use what, from their genomes (evolve.express). A literature search can show a mechanism is known; it cannot show
a combination is new - Forth's folklore lives largely on comp.lang.forth and in EuroForth proceedings, not in papers.

## What the winners are built from, and where each was described

| mechanism (the genes) | in the winners | described | how close |
|---|---|---|---|
| byte-coded threading, the top bit splitting primitives from calls (CV8: `enc`) | all nine | Koopman on comp.compilers, 1996 ("128 byte codes, and use the top bit to flag" an address); uxForth, 2016 (the token's top bit an address); Open Firmware's FCode (IEEE 1275-1994), byte codes with an escape | the idea is folklore; uxForth's token is CV8's two-byte call in all but name (the top bit a call, the rest its address); base-relative addressing for relocation and shorter references: Rose's ART-FORTH, 1986 (607); relative offsets from the dictionary's start for calls and xts: Enforth; not found: the variable length - two or three bytes |
| superinstructions - pairs fused into one opcode (`supers`) | three of the nine, one to five pairs (run-time fusion, `rtfuse`, in none) | Ertl and Gregg, PLDI 2003 and EuroForth 2003 (Gforth); Casey, Ertl, Gregg, TOPLAS 2007; selection automated: Miedema 2020 (JVM), Hu, Zhao, Scholz, VMIL 2024 (EVM) | known; here chosen per design from its own profile, by the search |
| specialised opcodes for literals, variables, short branches (`spec`); a word and its EXIT as one opcode (`folds`); relf's format-10 opcodes (`ops10`) | `spec` six of the nine (not the three smallest and leanest); `folds` and `ops10` all nine | vmgen's specialisations (Ertl, Gregg, Krall, Paysan, SPE 2002); quickening generally | known |
| the top of stack in a register; multi-state stack caching (`tos`, `msc`) | `tos` five of the nine (the four JIT designs, c2ef9488ff); `msc` none | Ertl, PLDI 1995; Ertl and Gregg, IVME 2004 and EuroForth 2005; in production in Gforth (Ertl and Paysan, 2025) | known |
| the JIT - native code copied from C-compiled fragments and patched (`jit` and its genes) | the four x86 winners | Ertl and Gregg, PACT 2004; Gregg and Ertl, Concurrency and Computation 18(11), 2006 - "based on an existing implementation of the Forth language"; Gforth's code copying; Xu and Kjolstad's copy-and-patch, OOPSLA 2021; CPython from 3.13 | known, in Forth since 2004; the lab's stencil choices (which words, the stack cache in registers - `jitk`) are its own, not checked against Gforth's |
| dictionary in hash chains (`threads`) | five of the nine | classic Forth (vocabulary threads) | known |
| byte headers - the link a distance of one to three bytes, decoded backwards from the name (part one, s6) | all nine | a relative link: Rose's ART-FORTH, 1986 - "2 bytes: relative offset to next nfa in hashed chain"; Enforth's relative name field, the high bit its flag and its value its length (607) | the relative link known since 1986; not found: one to three bytes, read backwards |
| compiler and flags as genes (`compiler`, `opt`, `nogcse`, ...) | all nine | COLE (Hoste and Eeckhout, CGO 2008), multi-objective evolutionary search over compiler settings | the method known |
| a genetic algorithm over an interpreter's design | the search | Huang, Marr, Ugawa, "Optimizing the Order of Bytecode Handlers in Interpreters using a Genetic Algorithm", ACM SAC 2023 - one decision (handler order), and the orders found "do not generalize" across machines; Langdon's MAGPIE, 2025 - genetic improvement of an interpreter's code | the nearest; one decision each, not the design |

## The answer, as far as a search can give it

Technique by technique, nothing in the winners is new: the byte encoding is folklore, the fusion, specialisation, stack
caching and the copying JIT are Ertl and Gregg's line of work and in Gforth, the flag search is COLE's. Two details looked new at 605 and have
fixed-length precedents (607, below): base-relative calls and a relative header link; only their variable-length forms
were not found. And no system or paper was found with any winner's combination -
which, for the reason above, is not the same as none existing. The search's own claim stays 539's: the integration -
one search over the encoding, fusion, caching, headers, variable access, flags and the JIT's own choices, with size,
speed at both widths and memory as equal objectives, the winners checked on held-out workloads and three machines -
and one finding the nearest prior work shares: what wins on one machine does not carry to another (the Tegra against
the laptop: Spearman 0.08 on the forty; Huang et al.'s handler orders likewise).

## The deeper check (Iteration 607; the owner: check the two before asking)

Searched for each again, specifically - EuroForth, the Rochester conference proceedings, comp.lang.forth, Forths on
GitHub. Both have precedents in fixed length: Anthony Rose, "Design of a fast 68000-based subroutine threaded FORTH with
inline code & an optimiser", Proceedings of the 1986 Rochester Forth Conference (JFAR 4(2), 285-288) - every address
relative to a base pointer (relocatable, 4-byte references against 6), a header's "2 bytes: relative offset to next nfa
in hashed chain", 256 hash links; uxForth (2016) - a token whose top bit marks a call to the address in its other 15
bits; Enforth (github.com/malyn/Enforth) - calls and execution tokens as relative offsets from the dictionary's start, a
relative name field flagged by its high bit. Still not found: the variable-length forms - a call of two or three bytes
by its second bit, a link of one to three bytes decoded backwards from the name - and any winner's whole combination.
The article asks about exactly those.

## Where a better answer would come from

The readers: ForthHub is where the people who would know are (Gforth's authors among them) - so the article ends by
asking, specifically: has a byte-coded Forth with relative two-to-three-byte calls and no table been described; has a
dictionary header with a backward-decoded link; has any Forth combined these with a copying JIT. A deeper literature
search (EuroForth proceedings 1985-2025, comp.lang.forth) is a few hours' reading, if the owner wants it before posting.
