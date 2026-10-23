# Appbench on our Forth - three applications run, checked (Iteration 467)

The owner (466-467) downloaded Appbench 1.4 (appbench.zip, kept outside this repository) and asked to continue: which of
its programs run on our Forth, under what terms, and how they could become held-out workloads. The tools of this study
are beside this note (results/drafts/appbench/: fold.py, prelude.fth, run.py); results/drafts/appbench-466.md says why
applications matter (deep stacks, frequent calls - unlike our six workloads and sieve).

## The programs and their terms

| program | what | terms (from its files) |
|---|---|---|
| brainless | chess, David Kühling | public domain |
| fcp | chess, Ian Osgood | no notice |
| cd16sim | a CD16 CPU simulator running a Forth | no notice |
| benchgc | a garbage collector, Anton Ertl | GPL |
| lexex | a lexical-analyser generator, Gerry Jackson | GPL, version 2 or later |
| brew | an evolution simulation | GPL |

Only brainless could be copied into this repository freely, so none is: run.py reads the zip where the owner keeps it.

## What it took

**Case.** Our words are upper case; the programs are written in lower case, for Forths that fold case (Gforth,
SwiftForth, VFX). fold.py upper-cases their source but keeps strings, comments, the names INCLUDE, REQUIRE, [CHAR],
NEEDS and brainless's LOAD-PART take, a name after CHAR outside a definition; upper-cases a string EVALUATE takes unless
it holds a '/' (fcp's chess position, whose letters are pieces); turns $hex numbers decimal.

**Words.** s6 lacks 61 of 140 commonly used standard words (NIP, TUCK, .(, [IF], VALUE, TO, DEFER, IS, CASE, COMPARE,
:NONAME, ...) - but **our own forth/extend.4 and forth/coreext.4 define nearly all of them** (loaded in that order, as
ans-check.py does). prelude.fth loads them, then a few stubs: CELL, CELL-, -ROT, ON, OFF, BOUNDS, TOLOWER, INCLUDE,
[DEFINED], timers (MS@ counts calls - fcp divides by it), KEY?, PAGE, ENVIRONMENT? answering MAX-U and MAX-UD, the float
sizes and alignments (no float arithmetic).

## What runs - on the hand-made s6, each with a check of its own output

| program | time here | check | result |
|---|---|---|---|
| fcp | 6.8 s | three 5-ply searches end at 120,287 nodes | **PASS** - and one alias: fcp evaluates a lower-case "setup" |
| brainless | 4.1 s | 110,023 nodes, 163,278 evaluations | **PASS** |
| cd16sim | 6.5 s | its own "22136 4660 4131 0 should be 22136 4660 4131 0" | **PASS** |
| lexex | - | - | loads all its files; stops on a lower-case name in the text it parses (".r") |
| benchgc | - | - | loads its compatibility layer; stops on a lower-case "sweep" not yet traced |
| brew | not tried | - | terminal-bound, and Gforth's own runs of it stop at times (Appbench's README) |

The two that stop do so for one reason: **our dictionary search is case-sensitive**, and these programs build or read
names at run time (EVALUATE, parsed input) where no source folding reaches. A case-insensitive FIND - what the systems
Appbench was written for do - would let all five run without per-program shims.

## Proposed (the owner's calls)

1. **A held-out tier of applications**: fcp, brainless and cd16sim beside sieve - each run on a design with run.py's
   method, its check required, its time reported per program (heldout.py's job, or the gate's). Each design then also
   loads extend.4 and coreext.4 - part of the timed run unless timed apart.
2. **Case-insensitive lookup** - in the kernel (FIND and the hashing of names; the hand-made stages' images change,
   validate would say so) or as a gene. Then lexex and benchgc, and real programs generally, run unshimmed.
3. **NIP, .( , [IF] and the rest in the default image** - today they need extend.4 and coreext.4 loaded first.
