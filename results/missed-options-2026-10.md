# Options missed so far? A gap check (Iteration 258)

Method: the project's inventory - every gene (lab/evolve/GENES.md), the 35 rows
of GOALS.md's "Rejected or deferred", the price-* write-ups and the surveys -
against current interpreter literature (CPython 3.14's tail-calling
interpreter; Gforth's papers: dynamic and static superinstructions, multi-state
stack caching, the IP-update optimization, Ertl 2024 on interpreter vs.
compiler speed), and a quick experiment wherever a gap showed.

## Already covered

Dynamic superinstructions / code copying (Gforth's most important
optimisation) - our copy-and-patch JIT; static superinstructions (supers),
multi-state stack caching (msc), explicit register allocation (regpin), branch
target alignment (alignfn, align1), tail-call threading (tail), one-byte
opcodes and calls (the tag), name hashing (threads), native lookup (klookup).
The IP-update optimization (Ertl & Paysan 2025) is the laptop's open perf item.

## Found and measured here

| option | measured | status |
|---|---|---|
| **Link-time optimisation** (-flto) across the engine and its runtime | engines -72 (3456ac1e5e, -1.0%), -352 (fe3c9c3940, -2.1%), -512 (3bb2087f9d, -2.4%), corpus right; interpreters' speed within noise (corpus +1.5%, fib -2.2%). On JIT designs LTO changed the stencils: the JIT stopped translating (fib 2.5x, loop 3.9x slower) | worth a gene, with engine/spn-stencils.c compiled outside LTO; the laptop times it |
| Clang as the engines' compiler | not here: the VM and the laptop have GCC 13.3 only. CPython 3.14's tail-calling interpreter needed Clang 19's musttail *and* preserve_none (musttail alone was slow); GCC 13 has neither, GCC 15 musttail only. Clang's tail duplication also differs for computed goto (LLVM 19's regression) | the owner's: install clang on the laptop, then a compiler gene |
| -march=x86-64-v3 | engines +32, -32, +224 bytes; speed would need the laptop; the binaries would need an AVX2-class CPU | not proposed |
| Runs of the 15 commonest one-byte operations packed two to a byte | 27 bytes in the smallest design: Forth code alternates calls and operations, runs of four or more are rare (40) | not worth it |

## After the broad sweep (Iterations 259-260)

The research report (an Advanced Research sweep of the 2000-2026 literature,
delivered in the chat) ranked the missing techniques. What became of them:

| technique | outcome |
|---|---|
| Stack caching in the JIT's copied code | built: the gene jitk (0, 2, 3) - tools/gen-jitk.py; after-seed-47 patch 3. VM: loop -9%, bubble -5%, corpus -4%, fib +16% at K=2 and flat at K=3; +2.3-2.8 KB. The laptop decides |
| Link-time optimisation | built: the gene lto, the stencils outside it; patch 4. -32 to -160 bytes after patch 2's runtime savings |
| GCC's max-goto-duplication-insns | built: the gene gotodup (default, 32, 128); patch 4. Interpreted engines +704-800 bytes |
| The echo instruction (LZ77 executed) | priced: 283-427 bytes of the smallest image (3.3-4.9%), new semantics in every engine - the owner's call |
| VM IP-update optimisations | deferred: the loop form needs the laptop's timing; interpreted designs only |
| Removing section headers; JIT code apart from data | covered already |
| Correct peak-memory accounting | covered: the laptop's kernel (6.17) counts it exactly at exit; the version is in every pack's machine.txt |
| Clang / GCC 16 preserve_none + musttail | the owner's: a toolchain change |
| Mutation weighted by regime (from the interaction study) | priced, not built: ~1.4% of evaluations |
