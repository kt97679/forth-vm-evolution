# How a session finds what the documents hold - an audit (Iteration 568)

The owner: are the documents indexed so a session gets what it needs from them with the least effort? Measured on
master at Iteration 568: the documents' sizes, each index's shape, ten lookups a session makes, and this chat's own
lookups (567-568).

## How a session finds things today

Three moves, in this order: HANDOFF.md read whole (14.6 KB); an index read or grepped for a topic; `git grep` across
the tree for a term. handoff-check.py keeps every document in an index (388 indexed), so nothing is lost - the question
is the cost of reaching it.

| document | size | read | holds |
|---|---|---|---|
| HANDOFF.md | 14.6 KB | whole, every session | the state, the routine, the conventions |
| GOALS.md | 27 KB | a section when needed | the goals, the stopping rule |
| results/README.md | 54.6 KB | grepped | one line per results document - 203 files and 88 drafts |
| lab/evolve/README.md | 58.2 KB | the tools section | the tools (17.5 KB) and the evolver's history, phases 1-6 (40.7 KB) |
| HANDOFF-REFERENCE.md | 61.2 KB | a section when needed | the owner's decisions, history to 562 (21.2 KB), the open items of 369 and 505 (21.0 KB), the processing steps, the lessons |
| results/predictions.md | 71.0 KB | its tail | every prediction and its score |
| PROGRESS.md | 710 KB | grepped, never whole | 556 entries |

## What the measures say

**The index narrows a lookup well where it names the topic.** Ten terms a session asks about: results/README.md has 2-9
lines on each of eight (the stopping rule 9, seed 77 7, alignhot 5, the confirmation run 2, jit_scan 2...) against
12-77 files a grep across the tree returns; each line carries its conclusion, so the document often need not be opened.
Two have none: carry-check (a tool - in lab/evolve/README.md's tools) and the curse (a review-checks report).

**But the results index is one flat list where it matters most.** "The evolution, run by run" holds 170 of the index's
252 lines: per-run records, comparisons, and 99 lines on drafts (documents and scripts), in no order a reader can use - neither by
iteration nor by subject (567's two lines went in near its top). The "Drafts" section holds 11. Fifty lines run past
300 characters, the longest 768 - small documents in themselves.

**Two reference documents are two-thirds history.** lab/evolve/README.md: the tools index is 17.5 KB of 58.2 KB.
HANDOFF-REFERENCE.md: 42 KB of 61 KB is the state to 562 and two superseded open-item lists. A session reading either
for a decision or a tool pays for the history.

**What cost this chat lookups** (567-568): conventions that lived only in code - a batch's patch names and ORDER.md's
shape, read from process-run.sh and an applied batch (now in HANDOFF's conventions); who reads regressions.json (a
grep of the tools); handoff-check's disposable format (learned by failing once); and a restated fact gone stale (seed
81's checklist). None from a missing index line.

## Proposals, by what they save

| # | what | effort |
|---|---|---|
| 1 | HANDOFF.md's "Where things are" becomes a question-to-place map: the dozen questions every session asks (the state, a run's results, the stopping rule and its ledger, a fault's history, a gene, a tool, a convention, an owner's decision, a prediction, a batch, the article, a past iteration) each with the first place to look and the term to grep - about 15 lines in the one document read whole | small |
| 2 | The history out of the two reference documents: lab/evolve/README.md's phases to lab/evolve/HISTORY.md (the README its tools and how a run works, about 20 KB); HANDOFF-REFERENCE.md's open items of 369 and 505 to a drafts archive (about 40 KB left) - references followed | small - mechanical |
| 3 | results/README.md's run-by-run section in subsections by subject - the runs' records; faults and their fixes; the stopping rule and the end of the phase; the JIT; across machines; the search's method; the article - each line in the subsection its subject puts it, newest first | medium - a line's subject is judgment |
| 4 | handoff-check warns on an index line past 300 characters: the line says what and what was found; the document says the rest | small |

Not proposed: an index of PROGRESS.md (a grep on "## Iteration N" or a term does what an index would, and a 556-line
index would be another 50 KB); an index of predictions.md (HANDOFF names the predictions due; the newest are at the
end).

1 and 2 cut what a session reads; 3 cuts the lines a grep of the index returns; 4 keeps the index an index.

## Done (Iteration 568, the owner: all four)

1. HANDOFF.md's "Where to look": twelve questions, each with its first place and the term to grep (the card 14.6 ->
   15.9 KB).
2. The history moved verbatim: lab/evolve/README.md 58.2 -> 16.1 KB (lab/evolve/HISTORY.md, 39.6 KB);
   HANDOFF-REFERENCE.md 61.2 -> 19.1 KB (HANDOFF-HISTORY.md, 42.5 KB); the citations followed.
3. results/README.md's run-by-run section is "The evolution, by subject": ten subsections - each run's records, the
   checks on other machines, the batches, the checklists, faults, the JIT, machines and widths, the search, the end of
   the phase, other models' answers - each oldest first, a script beside its document. batch-make.sh puts a pending
   line after the last batch, so the order holds.
4. The 67 index lines past 300 characters cut at a sentence or clause - the document holds the rest
   (results/README.md 54.6 -> 49.1 KB); handoff-check's 12 fails a longer one.

The prompts: 21's item 10 - make finding cheap.
