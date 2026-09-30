# Footprint: start-up, memory and size

What the systems cost to start and to keep resident, and what shrinks it.
Measured on the development VM in CPU time; the Ryzen figures in
`results/COMPARISON.md` are with the C library.

## Without the C library

**Where it went.** Of the CV8 engine's 1,264 KB resident, 1,132 KB were
the C library (900) and the dynamic loader (232); the engine's own code
was 32 KB and the Forth system's memory 56 KB. Start-up was the same
story: `/bin/true`, a C program that does nothing, takes 0.62 ms; a
program with no library 0.066 ms; the CV8 engine 0.67 ms - its own work
the last 0.05. Linking statically does not help: the library moves into
the engine, and 716 KB of it stay resident at 0.62 ms.

**What the engines use of it** - found by linking, not by reading: the
system calls for files, processes, directories and limits; an allocator;
the environment; one user-database lookup; `strlen`; and `snprintf` in
SPN's diagnostics. No stdio. `engine/rt-linux-x86_64.c`, about 300 lines
over raw x86-64 Linux system calls, is exactly that, and
`ENGINE_RT=nolibc tools/build-stages.sh` links every 64-bit engine
against it instead of the library (`tools/engine-rt.sh`). The engine's
machine code grows by under 1 KB.

**Checked**, against the C-library build:

- 25 of 31 images byte-identical - every one but SPN's. Building runs the
  engines: cross-compiling the kernel, saving images, reading sources.
  The six SPN images differ in the run-dependent pointers two C-library
  builds also differ in, and s8's stencil record in its hash of its own
  engine's stencils - by design, a different engine's.
- 616/616 on all 15 systems; the save-and-reboot tests; the corpus 20
  times on each of four SPN images, all clean.
- Every system primitive the corpus does not reach, output identical:
  the environment set, changed and removed, and a child started by
  SYSTEM seeing each change; directories; both allocator paths, a huge
  request refused; `~name`, found and not; a pipe; the file-size limit.

**Result** - development VM, CPU time; resident at the end of the
corpus, and private (resident less shared libraries):

| stage | start-up, C library | none | resident, KB | none | private, KB | none |
|---|---|---|---|---|---|---|
| `s0-cell` | 0.69 ms | 0.12 | 1,260 | 80 | 124 | 80 |
| `s5-cv8spec` | 0.71 | 0.12 | 1,280 | 108 | 144 | 108 |
| `s6-cv8b` | 0.70 | 0.12 | 1,280 | 100 | 144 | 100 |
| `s7-spn` | 2.51 | 1.97 | 1,508 | 280 | 308 | 280 |
| `s8-spncv8` | 1.96 | 1.40 | 1,528 | 312 | 328 | 312 |
| `s8-lazy` | 1.68 | 1.15 | 1,532 | 324 | 332 | 324 |
| `s8-full` | 8.14 | 7.78 | 1,548 | 328 | 348 | 328 |

CV8 starts almost six times faster and keeps a thirteenth of the memory
resident. SPN starts about 0.55 ms sooner, and keeps a fifth; its
private memory barely moves, because its own tables and native code are
most of it. End to end, 1-11% faster, from the start-up; one figure
slower, s6-cv8b on fib by 3.4%, the layout-sensitive workload in a
binary laid out differently.

**Given up.** `~name` comes from `/etc/passwd` alone. The C library's
lookup goes through NSS - LDAP, SSSD, systemd-homed - and finds users
this does not. x86-64 Linux only; 32-bit engines and other platforms
keep the C library.

**Status:** opt-in. The default build still links the C library.
