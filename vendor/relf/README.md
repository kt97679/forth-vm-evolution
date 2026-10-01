# vendor/relf - relf today, as a reference system

[relf](https://github.com/kt97679/relf) is where this project's encoding
ladder led: CV8 as a product, with the shell built on it. This directory
carries its engine (`cv8.c`, `cv8-ops.h`, `opcodes.tab`) and kernel
images (`kernel64.img`, `kernel32.img`), unmodified, at the commit in
`UPSTREAM`. `tools/update-relf.sh [REV]` refreshes them; the default is
`origin/article-2026`, the branch relf is being stabilised on.

`tools/build-stages.sh` builds the engine as relf's Makefile does -
`cc -O2 -Wall`, and `-fno-pie -no-pie` for 32 bits - with this lab's
layout variants, so its figures carry error bars like every stage's, but
never with `ENGINE_RT` or `ENGINE_CFLAGS`: it is measured as shipped. It
is `relf-64`, `relf-s64.img` in `build/`, and `relf` in every table.

**It runs its own kernel** - 103 primitives against the stages' 68, and a
different word set - so it is compared as a whole system, not as an
encoding: a difference may come from the engine or from the kernel. It
passes the shared CORE corpus with output byte-identical to the cell
engine's, and cross-compiles this project's kernel to the same image.

**Its standard input is one byte per read().** Descriptor 0 is shared with
every child, and a byte read ahead is a byte taken from whatever runs
next, so relf's KEY takes exactly one; the stages buffer 4 KB, which is
why their shell fails `printf 'cat\nhello\n' | sh` and relf's does not.
Any workload fed on standard input therefore measures relf's system calls
as much as its engine: see FINDINGS-OUTER-INTERPRETER.md.
