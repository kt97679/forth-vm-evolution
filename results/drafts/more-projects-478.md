# Another model's list of projects to check - verified, and what each holds for us (Iteration 478)

The owner asked another model for more projects to study and shared its answer. Every repository it named exists
(checked on GitHub); their own READMEs, read here, say what each is. Weighed against what this project already has:

| project | what it is (its README) | for us |
|---|---|---|
| benhoyt/nibbleforth | an idea, unbuilt: variable-length opcodes in nibbles, the most frequent the shortest (exit, then jz and jmp, by its analysis of Gforth's programs); token threading so user words get short codes too; common sequences factored into words, LZW-like; words used once inlined | **the most useful**: CV8 already has frequency-assigned one-byte operations, an escape page and one-byte calls to the hottest words (hotcalls); new to us are a whole-program pass factoring repeated sequences into words (size), and inlining words used once (size and speed) |
| kragen/tokthr | a token-threaded x86 Forth, about 1,400 bytes, 399 of them machine code | hand-written assembly; our engines are C the search compiles - little to take |
| zevv/zForth | variable-length dictionary cells - small numbers take less space, 30-50% claimed | CV8 has it already: literals of 1, 2, 4 or 8 bytes, calls of 2 to 4 bytes, byte headers |
| mkicjn/paraforth | a native, subroutine-threaded Forth under 1 KB, primitive inlining by { }; about 4 times gforth-fast 0.7.3, 1.08 times 0.7.9 | native code at definition time - what SPN (Iteration 30) and the JIT do; its inlining is the wider jitinl proposed at 462 |
| mitranim/astil_forth | a JIT and AOT snapshots, register allocation (its README has sections on both) | the next steps after jitk: register allocation across a word; and native code saved with the image - no translation at run time, and a way to native code where no JIT runs |
| romforth/romforth | baremetal, ported to many 8-64-bit instruction sets, a stepwise porting toolkit | its porting method, if the JIT ever goes to ARM |
| rrthomas/bee | a simple word-threaded VM for Forth | a baseline; nothing new |
| fuzzballcat/milliForth, cesarblum/sectorforth | Forths in 336 and 512 bytes, eight-odd primitives | minimal primitive sets; our goals keep speed and the standard words |

**What it did not weigh**: this session's finding that the selection's six workloads are kernels, and on applications
the fast designs kept a quarter of their lead or less until the JIT covered more (results/drafts/appbench-468.md,
jitapps-471.md). Density ideas move bytes; the largest open lever is still speed on real programs, and whether the
applications should join the selection.

**Proposed, the owner's calls**: from nibbleforth, two size genes - a factoring pass (repeated operation sequences made
words, priced by bytes saved against calls added) and single-use words inlined; from astil_forth, later, native code
saved with the image.
