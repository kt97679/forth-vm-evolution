# Inlining short words and Forth tail calls, priced (Iteration 89)

GOALS.md's next step 2 (the owner, Iterations 82-86): price two candidates
before anything is built - **inlining short words** (a call to a body of one
or two one-byte opcodes) and **Forth tail calls** (a call followed by EXIT as
a BRANCH) - by static sites and bytes saved, and by dynamic calls per
workload. Measured with `lab/evolve/callsites.py` as ported in Iteration 88,
on every design of the front of all runs (35, session 21), their genomes read
from results/ (Iteration 87). Counted on the VM - dispatches, not time.

## The answer

| | image: sites | image: bytes saved | dispatches saved |
|---|---|---|---|
| inlining short words | 0-15 | 0-11 | kernel 6.1-7.6% (faster designs), 3.8-4.5% (7.4 KB), 1.6-2.8% (smallest); sieve 0.3-0.6%; parse, corpus 0-1.0%; fib, loop 0 |
| tail calls | 48-55 | -4 to +9 | kernel 0.3-1.8%, corpus 0.1-1.8%, parse 0-1.0%; fib, loop, sieve 0 |
| constants (outside the agreed definition: a literal and EXIT) | 17-24 | 0 | kernel, parse, corpus 0.1-2.2% |

Calls are 7-21% of every workload's dispatches.

**Neither pays in the image.** Inlining finds nothing there: the converter
already made the short kernel words opcodes - the tiny words (`spec tiny`),
the folds, the format-10 words. On the fastest design no callee is short:
145 call another word within their first operations, 116 are longer, 61 carry
an operand, 37 are data, 9 use an escaped code. Tail calls find ~50 sites but
no bytes: a 16-bit BRANCH (3 bytes) is as long as a 2-byte call and its EXIT;
BRANCH8 reaches 11-12 of them, and 3-4 EXITs must stay (branch targets).
Eight sites call words that read their own return address (DNEGATE, FM/MOD,
`<BRANCH,`, QUIT, WARM) and are left out.

**The one lever is code compiled at run time, and mostly one word.** The
image's compiler compiles a call to every colon word; the kernel workload's
cross-compiler (cross.4, compiled at run time) calls `CHARS` - `: CHARS ;`,
an empty body - for 12.6% of its calls on the fastest design: a call and an
EXIT that do nothing, 5.2 of the 6.1 points inlining saves there. The rest:
`2DROP` (4.3% of the sieve's calls), `-`, `2DUP`, `<>`, `>`, `2*`, `INVERT` -
opcodes in the image (the tiny words), calls in run-time code.

**So, if anything is built: inlining at run time, starting with the empty
word.** The image's compiler compiling nothing for a call to a word whose
body is only EXIT is a few bytes of Forth behind a gene - 85% of the kernel
workload's 6.1 points; the general form (copying one or two safe one-byte
opcodes) adds the rest and needs a table of the codes that are not safe (the
return stack's, those with operands). Not built. Tail calls: not worth
building on these numbers - at most 1.8% of dispatches, no bytes.

**Not priced here: the JIT.** jit.c refuses any run-time word that calls a
kernel word (a callee without the JIT header), so on JIT designs every run-
time word calling CHARS or 2DROP stays bytecode. Inlining could let more of
the cross-compiler and the sieve go native - possibly worth more than the
dispatches above. Measured next (Iteration 90).

On designs with the JIT, fib and loop run native and dispatch a few thousand
times: their percentages there are of almost nothing.

How each is counted (lab/evolve/callsites.py): inlining - a callee whose body
is at most two operations, each a one-byte code without an operand, then EXIT
(or the last folded with it), none touching the return stack; a site saves
the call's bytes less the operations', a run the call and the callee's EXIT.
Tail calls - a call followed by EXIT, as BRANCH8 where it reaches, else
BRANCH; a run saves the caller's EXIT. Bytes are counted, not laid out again.

## Every design of the front of all runs

Per design: the image's sites and bytes, and the dispatches saved on each workload (image and run-time code), kernel/fib/parse/corpus/loop/sieve.

| design | speed | image | inlining: sites | bytes | dispatches saved | tail calls: sites | bytes | dispatches saved | constants: sites | bytes | dispatches saved |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 2cbcf427f6 | 0.173 | 7,880 | 0 | 0 | 6.1/0.0/0.0/0.3/0.0/0.6 | 51 | 8 | 1.2/1.3/0.0/0.7/1.2/0.0 | 23 | 0 | 0.8/1.1/1.1/1.0/1.0/0.0 |
| c5f28c89a3 | 0.190 | 8,680 | 2 | 0 | 7.0/0.0/0.0/0.2/0.0/0.6 | 51 | 7 | 1.2/1.0/0.0/0.6/1.1/0.0 | 24 | 0 | 0.8/1.1/1.1/1.0/1.1/0.0 |
| 9cd36dffec | 0.194 | 7,888 | 1 | 0 | 6.7/0.0/0.0/0.0/0.0/0.6 | 53 | -4 | 1.8/2.6/1.0/1.8/2.5/0.0 | 23 | 0 | 0.7/1.0/1.0/0.9/1.0/0.0 |
| 0911457251 | 0.192 | 7,480 | 1 | 0 | 6.9/0.0/0.0/0.0/0.0/0.6 | 52 | 9 | 1.2/1.3/0.0/0.7/1.2/0.0 | 23 | 0 | 0.7/1.1/1.1/1.0/1.0/0.0 |
| 49b6b108eb | 0.210 | 7,408 | 2 | 0 | 6.1/0.0/0.0/0.1/0.0/0.6 | 51 | 9 | 1.2/1.2/0.0/0.7/1.2/0.0 | 23 | 0 | 0.8/1.1/1.1/1.0/1.0/0.0 |
| 9c5ba1a6ad | 0.236 | 7,685 | 0 | 0 | 6.2/0.0/0.0/0.3/0.0/0.6 | 52 | 8 | 1.2/0.0/0.0/0.6/0.0/0.0 | 22 | 0 | 0.8/0.0/1.1/1.0/0.0/0.0 |
| 122b924056 | 0.252 | 7,678 | 0 | 0 | 6.2/0.0/0.0/0.3/0.0/0.6 | 52 | 8 | 1.2/0.0/0.0/0.6/0.0/0.0 | 22 | 0 | 0.8/0.0/1.1/1.0/0.0/0.0 |
| e83972af52 | 0.253 | 7,840 | 1 | 0 | 7.0/0.0/0.0/0.0/0.0/0.6 | 52 | 8 | 1.2/0.0/0.0/0.6/0.0/0.0 | 22 | 0 | 0.8/0.0/1.1/1.0/0.0/0.0 |
| bffb84ea89 | 0.282 | 7,757 | 1 | 0 | 7.0/0.0/0.0/0.0/0.0/0.6 | 52 | 8 | 1.2/0.0/0.0/0.6/0.0/0.0 | 22 | 0 | 0.8/0.0/1.1/1.0/0.0/0.0 |
| 6d8bd2033f | 0.295 | 7,702 | 1 | 0 | 6.2/0.0/1.0/1.0/0.0/0.6 | 52 | 8 | 1.2/0.0/0.0/0.6/0.0/0.0 | 22 | 0 | 0.8/0.0/1.1/1.0/0.0/0.0 |
| ffe230e21c | 0.312 | 7,316 | 1 | 0 | 7.0/0.0/0.0/0.0/0.0/0.6 | 52 | 9 | 1.2/0.0/0.0/0.6/0.0/0.0 | 22 | 0 | 0.8/0.0/1.1/1.0/0.0/0.0 |
| 40eeafca34 | 0.316 | 7,299 | 1 | 0 | 7.0/0.0/0.0/0.0/0.0/0.6 | 52 | 9 | 1.2/0.0/0.0/0.6/0.0/0.0 | 22 | 0 | 0.8/0.0/1.1/1.0/0.0/0.0 |
| cbd0601e2f | 0.374 | 7,282 | 4 | 3 | 6.7/0.0/1.0/0.8/0.0/0.6 | 52 | 9 | 1.2/0.0/0.0/0.6/0.0/0.0 | 19 | 0 | 1.4/0.0/2.2/2.0/0.0/0.0 |
| 41125022e8 | 0.375 | 7,239 | 1 | 0 | 7.0/0.0/0.0/0.2/0.0/0.4 | 48 | 8 | 1.2/0.0/0.0/0.5/0.0/0.0 | 22 | 0 | 0.8/0.0/1.1/0.9/0.0/0.0 |
| 57bb263077 | 0.351 | 7,146 | 2 | 0 | 7.6/0.0/1.0/0.7/0.0/0.4 | 48 | 8 | 1.2/0.0/0.0/0.5/0.0/0.0 | 22 | 0 | 0.8/0.0/1.1/0.9/0.0/0.0 |
| d435767f07 | 0.404 | 7,104 | 1 | 0 | 7.1/0.0/0.0/0.2/0.0/0.4 | 48 | -3 | 1.1/0.0/0.0/0.5/0.0/0.0 | 22 | 0 | 0.7/0.0/0.9/0.8/0.0/0.0 |
| ac3fa4bc74 | 0.411 | 7,065 | 2 | 0 | 6.9/0.0/0.8/0.8/0.0/0.4 | 50 | 8 | 1.6/0.0/0.9/1.3/0.0/0.0 | 22 | 0 | 0.7/0.0/0.9/0.7/0.0/0.0 |
| 670010e0ef | 0.435 | 7,059 | 2 | 0 | 6.9/0.0/0.8/0.8/0.0/0.4 | 50 | 8 | 1.6/0.0/0.9/1.3/0.0/0.0 | 22 | 0 | 0.7/0.0/0.9/0.7/0.0/0.0 |
| e1328696cc | 0.495 | 7,035 | 1 | 0 | 4.5/0.0/0.4/0.4/0.0/0.4 | 50 | 8 | 1.3/0.0/0.5/0.9/0.0/0.0 | 21 | 0 | 0.3/0.0/0.0/0.0/0.0/0.0 |
| a6deb41b86 | 0.574 | 8,032 | 4 | 0 | 3.9/0.0/0.5/0.5/0.0/0.3 | 55 | -4 | 0.9/0.0/0.6/0.8/0.0/0.0 | 23 | 0 | 0.4/0.0/0.6/0.5/0.0/0.0 |
| 057a9ef15c | 0.606 | 7,435 | 4 | 0 | 4.0/0.0/0.5/0.5/0.0/0.3 | 51 | -3 | 0.9/0.0/0.6/0.8/0.0/0.0 | 23 | 0 | 0.4/0.0/0.6/0.5/0.0/0.0 |
| badb229f1c | 0.601 | 7,435 | 4 | 0 | 4.0/0.0/0.5/0.5/0.0/0.3 | 51 | -3 | 0.9/0.0/0.6/0.8/0.0/0.0 | 23 | 0 | 0.4/0.0/0.6/0.5/0.0/0.0 |
| 3fef1aec0a | 0.652 | 7,433 | 15 | 11 | 3.8/0.0/0.4/0.5/0.0/0.3 | 51 | -3 | 0.9/0.0/0.5/0.8/0.0/0.0 | 17 | 0 | 0.7/0.0/1.0/0.8/0.0/0.0 |
| ebedb45723 | 0.645 | 7,426 | 9 | 5 | 3.8/0.0/0.4/0.5/0.0/0.3 | 51 | -3 | 0.9/0.0/0.5/0.7/0.0/0.0 | 23 | 0 | 0.4/0.0/0.5/0.4/0.0/0.0 |
| 21cebb3e48 | 0.658 | 7,419 | 4 | 0 | 3.8/0.0/0.4/0.5/0.0/0.3 | 51 | -3 | 0.9/0.0/0.5/0.8/0.0/0.0 | 23 | 0 | 0.4/0.0/0.5/0.4/0.0/0.0 |
| e4f2b9440b | 0.663 | 7,417 | 4 | 0 | 3.9/0.0/0.9/0.8/0.0/0.3 | 51 | -3 | 0.9/0.0/0.5/0.8/0.0/0.0 | 23 | 0 | 0.4/0.0/0.5/0.4/0.0/0.0 |
| 6c81b714a4 | 0.790 | 7,302 | 3 | 0 | 2.8/0.0/0.1/0.1/0.0/0.3 | 49 | -3 | 0.5/0.0/0.2/0.3/0.0/0.0 | 21 | 0 | 0.1/0.0/0.0/0.0/0.0/0.0 |
| 999558b47a | 0.794 | 7,286 | 8 | 5 | 2.7/0.0/0.1/0.1/0.0/0.3 | 51 | -3 | 0.8/0.0/0.5/0.6/0.0/0.0 | 21 | 0 | 0.1/0.0/0.0/0.0/0.0/0.0 |
| ddd41f6824 | 1.276 | 7,279 | 3 | 0 | 1.6/0.0/0.0/0.1/0.0/0.3 | 51 | -3 | 0.5/0.0/0.2/0.3/0.0/0.0 | 21 | 0 | 0.1/0.0/0.0/0.0/0.0/0.0 |
| 9a58ef1476 | 1.311 | 7,271 | 3 | 0 | 1.6/0.0/0.0/0.1/0.0/0.3 | 49 | -3 | 0.3/0.0/0.1/0.1/0.0/0.0 | 21 | 0 | 0.1/0.0/0.0/0.0/0.0/0.0 |
| 4eb88d9be5 | 0.741 | 7,218 | 1 | 0 | 3.6/0.0/0.2/0.1/0.0/0.3 | 49 | 8 | 0.7/0.0/0.3/0.5/0.0/0.0 | 21 | 0 | 0.2/0.0/0.0/0.0/0.0/0.0 |
| c079be4f87 | 0.784 | 7,177 | 0 | 0 | 2.8/0.0/0.0/0.0/0.0/0.3 | 49 | 8 | 0.7/0.0/0.3/0.4/0.0/0.0 | 21 | 0 | 0.2/0.0/0.0/0.0/0.0/0.0 |
| c51f2dda32 | 1.137 | 7,148 | 2 | 0 | 1.7/0.0/0.0/0.0/0.0/0.3 | 49 | 8 | 0.4/0.0/0.1/0.2/0.0/0.0 | 21 | 0 | 0.1/0.0/0.0/0.0/0.0/0.0 |
| 516b8d327a | 1.147 | 7,147 | 0 | 0 | 1.6/0.0/0.0/0.0/0.0/0.3 | 49 | 8 | 0.4/0.0/0.1/0.2/0.0/0.0 | 21 | 0 | 0.1/0.0/0.0/0.0/0.0/0.0 |
| faf72cef8e | 1.177 | 7,107 | 0 | 0 | 1.6/0.0/0.0/0.0/0.0/0.3 | 49 | 8 | 0.4/0.0/0.1/0.2/0.0/0.0 | 21 | 0 | 0.1/0.0/0.0/0.0/0.0/0.0 |

## Four designs in detail

The fastest, the middle, the small engine, the smallest; every other design: `python3 lab/evolve/callsites.py ID`.

### 2cbcf427f6 - image 7,880 bytes, 42,816 total with the engine; speed 0.173

368 call sites in the image's code to 131 targets (2 bytes: 352, 4 bytes: 16; 16 before an inline operand).

| workload | dispatches | calls | from the image | from run-time code | inlining saves: image | run-time | tail calls save: image | run-time |
|---|---|---|---|---|---|---|---|---|
| kernel | 1,919,751 | 397,139 (20.7%) | 26.9% | 73.1% | 0.0% | 6.1% | 0.5% | 0.8% |
| fib | 9,237 | 1,580 (17.1%) | 100.0% | 0.0% | 0.0% | 0.0% | 1.3% | 0.0% |
| parse | 3,182,112 | 484,343 (15.2%) | 100.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| corpus | 744,733 | 120,381 (16.2%) | 91.3% | 8.7% | 0.0% | 0.3% | 0.7% | 0.0% |
| loop | 7,725 | 1,308 (16.9%) | 100.0% | 0.0% | 0.0% | 0.0% | 1.2% | 0.0% |
| sieve | 4,788,808 | 660,525 (13.8%) | 0.3% | 99.7% | 0.0% | 0.6% | 0.0% | 0.0% |

(Dispatches saved, as a share of the workload's. Constants - outside the agreed definition: kernel 0.8%, fib 1.1%, parse 1.1%, corpus 1.0%, loop 1.0%, sieve 0.0%; in the image 23 sites, 0 bytes. Tail calls whose callee reads its return address are left out: kernel 0.0%, fib 0.0%, parse 0.0%, corpus 0.1%, loop 0.0%, sieve 0.0%.)

**Inlining, the image**: 0 sites to 0 short words, 0 bytes (0 where the call is longer than the body). Not short: a call 145, longer 116, an operand 61, not code 37, an escaped code 9.


The short words most called, everywhere (image and run-time code): CHARS 12.6%/0.0%/0.0%/0.0%/0.0%/0.0%; 2DROP 0.7%/0.0%/0.0%/0.0%/0.0%/4.3%; - 2.8%/0.0%/0.0%/0.1%/0.0%/0.0%; 2DUP 0.8%/0.0%/0.0%/0.0%/0.0%/0.0%; <> 0.0%/0.0%/0.0%/0.7%/0.0%/0.0%; > 0.1%/0.0%/0.0%/0.0%/0.0%/0.0%; 2* 0.0%/0.0%/0.0%/0.2%/0.0%/0.0%; INVERT 0.0%/0.0%/0.0%/0.0%/0.0%/0.0% (share of each workload's calls, in the order kernel/fib/parse/corpus/loop/sieve).

**Tail calls, the image**: 51 sites, 8 bytes - the EXIT goes at 47, stays (a branch target) at 4; BRANCH8 reaches at 12. Callees reading their return address, left out: 8 sites (DNEGATE 2, FM/MOD 2, <BRANCH, 2, QUIT 1, WARM 1). 0 sites are inlining's too.

### e83972af52 - image 7,840 bytes, 29,968 total with the engine; speed 0.253

355 call sites in the image's code to 131 targets (2 bytes: 340, 4 bytes: 15; 15 before an inline operand).

| workload | dispatches | calls | from the image | from run-time code | inlining saves: image | run-time | tail calls save: image | run-time |
|---|---|---|---|---|---|---|---|---|
| kernel | 1,928,961 | 395,630 (20.5%) | 26.7% | 73.3% | 0.0% | 7.0% | 0.4% | 0.8% |
| fib | 29,626,950 | 2,694,055 (9.1%) | 0.1% | 99.9% | 0.0% | 0.0% | 0.0% | 0.0% |
| parse | 3,250,075 | 500,322 (15.4%) | 100.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| corpus | 762,948 | 122,985 (16.1%) | 90.6% | 9.4% | 0.0% | 0.0% | 0.6% | 0.0% |
| loop | 2,013,088 | 2,069 (0.1%) | 61.3% | 38.7% | 0.0% | 0.0% | 0.0% | 0.0% |
| sieve | 4,789,218 | 660,484 (13.8%) | 0.3% | 99.7% | 0.0% | 0.6% | 0.0% | 0.0% |

(Dispatches saved, as a share of the workload's. Constants - outside the agreed definition: kernel 0.8%, fib 0.0%, parse 1.1%, corpus 1.0%, loop 0.0%, sieve 0.0%; in the image 22 sites, 0 bytes. Tail calls whose callee reads its return address are left out: kernel 0.0%, fib 0.0%, parse 0.0%, corpus 0.1%, loop 0.0%, sieve 0.0%.)

**Inlining, the image**: 1 sites to 1 short words, 0 bytes (0 where the call is longer than the body). Not short: a call 139, longer 119, an operand 48, not code 37, an escaped code 8, return stack 3.

| short word | body | sites | bytes | runs: kernel | runs: fib | runs: parse | runs: corpus | runs: loop | runs: sieve |
|---|---|---|---|---|---|---|---|---|---|
| * | UM* DROP;EXIT | 1 | 0 | 27,345 | 0 | 0 | 0 | 0 | 0 |

The short words most called, everywhere (image and run-time code): CHARS 12.7%/0.0%/0.0%/0.0%/0.0%/0.0%; * 6.9%/0.0%/0.0%/0.0%/0.0%/0.0%; 2DROP 0.8%/0.0%/0.0%/0.0%/0.0%/4.3%; 2DUP 0.8%/0.0%/0.0%/0.0%/0.0%/0.0%; > 0.1%/0.0%/0.0%/0.0%/0.0%/0.0%; INVERT 0.0%/0.0%/0.0%/0.0%/0.0%/0.0%; a run-time word: EXIT < call 0.0%/0.0%/0.0%/0.0%/0.0%/0.0% (share of each workload's calls, in the order kernel/fib/parse/corpus/loop/sieve).

**Tail calls, the image**: 52 sites, 8 bytes - the EXIT goes at 48, stays (a branch target) at 4; BRANCH8 reaches at 12. Callees reading their return address, left out: 8 sites (DNEGATE 2, FM/MOD 2, <BRANCH, 2, QUIT 1, WARM 1). 0 sites are inlining's too.

### a6deb41b86 - image 8,032 bytes, 26,064 total with the engine; speed 0.574

397 call sites in the image's code to 142 targets (2 bytes: 378, 4 bytes: 19; 19 before an inline operand).

| workload | dispatches | calls | from the image | from run-time code | inlining saves: image | run-time | tail calls save: image | run-time |
|---|---|---|---|---|---|---|---|---|
| kernel | 3,732,196 | 436,083 (11.7%) | 33.3% | 66.7% | 0.0% | 3.9% | 0.6% | 0.4% |
| fib | 29,644,317 | 2,694,638 (9.1%) | 0.1% | 99.9% | 0.0% | 0.0% | 0.0% | 0.0% |
| parse | 6,485,268 | 648,509 (10.0%) | 100.0% | 0.0% | 0.5% | 0.0% | 0.6% | 0.0% |
| corpus | 1,638,964 | 160,949 (9.8%) | 90.4% | 9.6% | 0.4% | 0.1% | 0.8% | 0.0% |
| loop | 9,634,748 | 803,016 (8.3%) | 0.2% | 99.8% | 0.0% | 0.0% | 0.0% | 0.0% |
| sieve | 9,091,344 | 963,945 (10.6%) | 0.3% | 99.7% | 0.0% | 0.3% | 0.0% | 0.0% |

(Dispatches saved, as a share of the workload's. Constants - outside the agreed definition: kernel 0.4%, fib 0.0%, parse 0.6%, corpus 0.5%, loop 0.0%, sieve 0.0%; in the image 23 sites, 0 bytes. Tail calls whose callee reads its return address are left out: kernel 0.2%, fib 0.0%, parse 0.6%, corpus 0.5%, loop 0.0%, sieve 0.0%.)

**Inlining, the image**: 4 sites to 3 short words, 0 bytes (0 where the call is longer than the body). Not short: longer 163, a call 137, an operand 48, not code 37, an escaped code 5, return stack 3.

| short word | body | sites | bytes | runs: kernel | runs: fib | runs: parse | runs: corpus | runs: loop | runs: sieve |
|---|---|---|---|---|---|---|---|---|---|
| S>D | DUP 0< EXIT | 2 | 0 | 0 | 0 | 0 | 141 | 0 | 1 |
| * | UM* DROP;EXIT | 1 | 0 | 27,345 | 0 | 0 | 0 | 0 | 0 |
| U> | SWAP U<;EXIT | 1 | 0 | 1,574 | 46 | 32,009 | 5,759 | 37 | 71 |

The short words most called, everywhere (image and run-time code): CHARS 11.5%/0.0%/0.0%/0.0%/0.0%/0.0%; U> 0.4%/0.0%/4.9%/3.6%/0.0%/0.0%; * 6.3%/0.0%/0.0%/0.0%/0.0%/0.0%; 2DROP 0.7%/0.0%/0.0%/0.0%/0.0%/3.0%; - 2.5%/0.0%/0.0%/0.0%/0.0%/0.0%; 2DUP 0.8%/0.0%/0.0%/0.0%/0.0%/0.0%; <> 0.0%/0.0%/0.0%/0.5%/0.0%/0.0%; > 0.1%/0.0%/0.0%/0.0%/0.0%/0.0%; 2* 0.0%/0.0%/0.0%/0.1%/0.0%/0.0%; S>D 0.0%/0.0%/0.0%/0.1%/0.0%/0.0% (share of each workload's calls, in the order kernel/fib/parse/corpus/loop/sieve).

**Tail calls, the image**: 55 sites, -4 bytes - the EXIT goes at 51, stays (a branch target) at 4; BRANCH8 reaches at 0. Callees reading their return address, left out: 12 sites (DNEGATE 2, FM/MOD 2, CMOVE 2, <BRANCH, 2, UNLOOP 2, QUIT 1). 0 sites are inlining's too.

### faf72cef8e - image 7,107 bytes, 25,139 total with the engine; speed 1.177

466 call sites in the image's code to 145 targets (2 bytes: 454, 4 bytes: 12; 12 before an inline operand).

| workload | dispatches | calls | from the image | from run-time code | inlining saves: image | run-time | tail calls save: image | run-time |
|---|---|---|---|---|---|---|---|---|
| kernel | 7,440,242 | 685,075 (9.2%) | 57.6% | 42.4% | 0.0% | 1.6% | 0.2% | 0.2% |
| fib | 29,675,924 | 2,697,241 (9.1%) | 0.2% | 99.8% | 0.0% | 0.0% | 0.0% | 0.0% |
| parse | 35,798,620 | 2,653,053 (7.4%) | 100.0% | 0.0% | 0.0% | 0.0% | 0.1% | 0.0% |
| corpus | 5,864,482 | 447,632 (7.6%) | 96.5% | 3.5% | 0.0% | 0.0% | 0.2% | 0.0% |
| loop | 9,658,959 | 805,036 (8.3%) | 0.5% | 99.5% | 0.0% | 0.0% | 0.0% | 0.0% |
| sieve | 8,897,565 | 967,795 (10.9%) | 0.7% | 99.3% | 0.0% | 0.3% | 0.0% | 0.0% |

(Dispatches saved, as a share of the workload's. Constants - outside the agreed definition: kernel 0.1%, fib 0.0%, parse 0.0%, corpus 0.0%, loop 0.0%, sieve 0.0%; in the image 21 sites, 0 bytes. Tail calls whose callee reads its return address are left out: kernel 0.0%, fib 0.0%, parse 0.0%, corpus 0.0%, loop 0.0%, sieve 0.0%.)

**Inlining, the image**: 0 sites to 0 short words, 0 bytes (0 where the call is longer than the body). Not short: a call 190, not code 169, longer 93, an escaped code 8, return stack 3, an operand 3.


The short words most called, everywhere (image and run-time code): CHARS 7.3%/0.0%/0.0%/0.0%/0.0%/0.0%; 2DROP 0.4%/0.0%/0.0%/0.0%/0.0%/2.9%; - 1.6%/0.0%/0.0%/0.0%/0.0%/0.0%; 2DUP 0.5%/0.0%/0.0%/0.0%/0.0%/0.0%; > 0.1%/0.0%/0.0%/0.0%/0.0%/0.0%; 2* 0.0%/0.0%/0.0%/0.0%/0.0%/0.0%; INVERT 0.0%/0.0%/0.0%/0.0%/0.0%/0.0%; a run-time word: EXIT AND call 0.0%/0.0%/0.0%/0.0%/0.0%/0.0% (share of each workload's calls, in the order kernel/fib/parse/corpus/loop/sieve).

**Tail calls, the image**: 49 sites, 8 bytes - the EXIT goes at 46, stays (a branch target) at 3; BRANCH8 reaches at 11. Callees reading their return address, left out: 8 sites (DNEGATE 2, FM/MOD 2, <BRANCH, 2, QUIT 1, WARM 1). 0 sites are inlining's too.
