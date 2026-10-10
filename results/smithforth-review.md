# SmithForth, reviewed for reuse (Iteration 149)

https://dacvs.neocities.org/SF/ - David Smith, 2022: a subroutine-threaded
Forth for x86-64 Linux in 1000 hand-written bytes of machine code (no
assembler, no C) and 1000 lines of Forth appended to the binary and compiled at
every start. The owner asked what can be reused.

**Code: none.** No licence is stated (the source says only "David Smith
2022"), so ideas only - and hand-written machine code would not fit engines
generated from C anyway.

**The idea that counts: the executable is its headers and one segment.**
SmithForth's file is a 64-byte ELF header, one program header - a single
read-write-execute segment over the whole file, its p_memsz the dictionary -
and nothing else. The evolved engines were already most of the way there: one
RWE segment from just past the headers, the dictionary and stacks in its
memory size. What they still carried, after the strip the size objective has
measured since Iteration 75: the section headers, their names and the
compiler's .comment - 616 to 620 bytes in every engine, which the kernel
never reads. tools/elf_tight.py drops them (ELF32 and ELF64; every segment
with file bytes kept); the evolver builds, runs, gates, times and measures that
file and keeps the full one as engine.full for tail_offenders and anyone with
nm or gdb. Every byte past the ELF header is the full engine's. 20 front
designs: the gate, the tab test, 616-620 bytes each; the hand-made stages,
64- and 32-bit, glibc's dynamic ones too, run tight. The seventh pending patch
of the after-seed-39 batch - a measurement change: sizes and speeds from before
the batch are not to be compared with those after.

**Not taken.** Subroutine threading - the JIT already compiles calls. The
source appended to the binary - Forth source is larger than our images. The
1000-byte machine-code core - a measure of how small a core can be, not a
technique for engines generated from C.
