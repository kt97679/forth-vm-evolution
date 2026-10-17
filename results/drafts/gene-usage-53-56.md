# What the search chose: every gene on the fronts of seeds 53-56 (Iteration 372)

722 front designs (seeds 53, 54, 55, 56: 172, 195, 168, 187), each genome expressed (express(canon(g))
- what is built). **A gene absent from an expression is at its default, off** - the first count read
only the values present and called compiler=1 "on every design" (it is absent wherever it is 0, GCC):
clang is on 181 of the 722, GCC 541. Count absence as off, or the default value hides.

| | genes |
|---|---|
| **never on** (0 of 722) | msc, scale, tail |
| **on under 10 % of every front** (designs on in 53/54/55/56) | d256 (0/0/0/4), escape (4/0/4/6), guard (4/2/0/18), nocrossjump (1/5/6/11), nogcse (0/2/0/0), rtfuse (4/0/1/3), rtimm (12/6/5/8), supers (4/0/4/6 - inert besides: results/drafts/supers-tag2.md) |
| **on in every design** (722 of 722) | bss, bytehdr, doesfar, enc (cv8), folds, fsys, lean, ops10, spec, tag2, thinhdr, varcall |
| **on in 90-99 %** | factor 700, opbody 708, rtloop 654, threads 684, tos 715 |
| **mixed** | jit 445; compiler: clang 181, GCC 541; opt: Os 495, O2 226, O3 1 |

By GOALS.md's measure - a mechanism earns its place, and comes out if it buys nothing - this is the
search's own evidence: three mechanisms never chosen in four runs (tail and msc whole engine
generators; scale, call scaling, which tag-2's call encoding does without), eight rarely, and the off
side of twelve unused (tag2's alternative is the whole plain CV8 encoding). **Not to act on before
seed 57**: it is the first run selected at both widths, and tag2 costs 36 % at 32 bits
(results/drafts/skew-32.md) - the off side of an always-on gene may come back there. After seed 57
(and 58, for supers): the review - each never-chosen mechanism removed or kept by the owner, each
always-on gene frozen or kept as a gene. Method: this file's counts come from express() over the seed
reports' front records; rerun for later seeds the same way.
