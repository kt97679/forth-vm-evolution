# Small VMs and interpretable code compression - against the register (Iteration 742)

The owner (741: "can you think of anything else we can check?"; 742: "continue"): two sources the earlier surveys
(other Forths 196, JITs and VMs 217, the early games and computers 713, esoteric languages 717, the demoscene and the
IOCCC 727) did not cover - virtual machines built for small images and little RAM, and the research on bytecode that
stays interpretable while compressed. Each against what the lab has; the measure is dispatches, bytes and pages.

## Small VMs

| source | its technique | here |
|---|---|---|
| Java Card (CAP files, token-based linking) | references as small tokens (package, class, method numbers) resolved when the applet is loaded; the converter drops the constant pool | ours: the converter resolves everything (tools/layout.py), words as one-byte opcodes (ops10, opbody), headerless names - nothing to take |
| HP's RPL (HP-28 to HP-50g, System RPL) | every object starts with its prolog's address; objects of any type inline in the instruction stream; the system in ROM | ours: the code field (DOCOL, DOVAR) is the prolog; LIT, short literals and inline strings are the inline objects; the image is the ROM - the threading itself, nothing new |
| PostScript Level 2 (binary tokens, binary object sequences, early name binding) | a system name by a 1-byte index into a fixed table; integers in 1, 2 or 4 bytes; `bind` replacing names by operators at definition | ours: opcodes for primitives, literals sized by value, compilation itself is early binding. A pre-tokenized program input would change what the kernel and corpus workloads measure (reading text) - not for us |
| MicroPython (frozen bytecode, interned strings, const()) | compiled code and constant data kept in flash, not the heap; const() folded at compile time | ours: the image is compiled ahead (the converter, the self-hosting compiler); rtconst is const(); names interned by the chain hash (hashk) |
| eLua's rotables (Lua Tiny RAM), NodeMCU's Lua Flash Store | module tables read-only in flash - 20-25 KB of RAM saved on an ESP8266 | the same aim as our memory measure. The image from its file (mapped, never written) was priced at 713 (1-2 pages at most - images are three pages). The engine's tables: the base dispatch table is already const (.rodata); DISPOFF is the deliberate inverse (offsets in the file, a pointer table built at start-up: bytes for a page); the tag's t2tab and t2esc (256 entries each, built at start-up in .bss) could be const like dispatch[] - 4 KB more in the file (x86-64) for about one written page fewer, a trade only a memory-first design could want: priced on paper, not built |

## Interpretable code compression

| source | its technique | here |
|---|---|---|
| Proebsting, "Optimizing an ANSI C interpreter with superoperators" (POPL 1995) | operations synthesized from frequent operator trees - smaller and faster | ours: supers, folds (with Ertl and Gregg's superinstructions, credited) |
| Ernst, Evans, Fraser, Lucco, Proebsting, "Code compression" (PLDI 1997) - BRISC; later split-stream dictionary compression | an interpretable byte-coded RISC with operand specialization and opcode combination; a dictionary of instruction sequences | ours as genes: spec (operand specialization), supers and ops10 (combination), short literals |
| Fraser, the echo instruction (2006) | replay n bytes from earlier in the code - LZ77 executed | priced at 260 (GOALS.md's register): 3.3-4.9 % of the smallest image before its handler - the owner's call |
| Evans and Fraser, "Bytecode compression via profiled grammar rewriting" (PLDI 2001; CACM 2003) | the bytecode's grammar expanded by rules learned on a training set (operands and contexts in the rules); the program is its derivation under the new grammar, and the interpreter is generated from the old one and the rules | the general form of what supers, folds, spec and short literals do by hand. The room left: the smallest design's 21,673 B are 4,246 of engine, 9,037 of image and 8,390 of the five programs' code - about 80 % bytecode; xz brings the four smallest images to 62-64 % (5.6-6.4 KB) and an order-1 model to an optimistic 46-47 %, ceilings no interpretable code reaches, before the generated interpreter's bytes. A converter pass and a generated engine: a large piece, for a later search (the same family as the echo instruction) |

## What it comes to

Nothing for the series or the roles: every technique is here already, was priced, or changes the measure. Two paper
candidates for a later search - the tag's tables as const data (memory-first designs; ~one page against 4 KB of file),
and a learned grammar over the bytecode (Evans and Fraser; the size objective, the image and the programs' code being 80 %
of the smallest). The toolchain side of the same question (Thumb-2, the machine outliner): results/drafts/thumb-742.txt.

## Sources

- Java Card token-based linking: US patent 6,880,155 (Schwabe and Susser, Sun Microsystems); Oracle's Java Card converter
  guide, https://docs.oracle.com/en/java/javacard/3.1/guide/running-converter.html
- RPL: https://en.wikipedia.org/wiki/RPL_(programming_language); Kalinowski and Dominik, Programming in System RPL,
  https://literature.hpcalc.org/community/prog-sysrpl-ed2.pdf
- PostScript Language Reference, third edition, 3.12 Early Name Binding and 3.14 Binary Encoding Details; Ghostscript's
  psi/iscanbin.c
- MicroPython: https://docs.micropython.org/en/latest/develop/optimizations.html,
  https://docs.micropython.org/en/latest/reference/constrained.html
- eLua LTR: https://eluaproject.net/en_arch_ltr.html; NodeMCU LFS: https://nodemcu.readthedocs.io/en/dev/lfs/
- Proebsting 1995: https://www2.cs.arizona.edu/~collberg/Teaching/553/2011/Resources/superops.pdf
- Ernst et al. 1997: https://cwf.github.io/pro/Ernst%20et%20al.%20Code%20compression.pdf
- Evans and Fraser 2001: https://www.cs.ubc.ca/~will/papers/bytecode.pdf; CACM 2003,
  https://cacm.acm.org/research/grammar-based-compression-of-interpreted-code
