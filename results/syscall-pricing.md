# One SYSCALL - priced (Iteration 132)

The question (the owner, agreed in principle): the engine's operating-system primitives replaced by
one SYSCALL, the OS words written in Forth on it - what it saves, what it costs.

## Measured

s6's engine as the evolver builds it (20,248 bytes), recompiled with -g, every instruction's bytes
attributed to its source line (objdump -dl), summed per handler and per runtime function. Exact.

**The 29 OS handlers: 3,153 bytes** of the dispatch function's 8,012 for all handlers - READ-LINE
424, SYSTEM 214, FILE-SIZE 186, PIPE 183, WAITPID 159, WRITE-LINE 151, the fsize pair 295,
OPEN-FILE 142, FILE-POSITION 116, READ-FILE 104, WRITE-FILE 95, FORK 89, the argument pair 173,
the home directory 87, EXECVE 83, GETCWD 82, DELETE-FILE 81, REPOSITION-FILE 72, SETENV 68, DUP2 61,
the terminal pair 101, CLOSE-FILE 51, CHDIR 51, GETENV 44, the exits 41.

**The runtime (engine/rt-linux-x86_64.c): 3,400 bytes** - the environment (setenv 349, unsetenv
215, take_env 240, getenv 130, and the allocator they use: malloc 217, realloc 198, free 56) about
1,400; getpwnam 329 (the home directory); the system-call machinery about 1,190; memcmp, memcpy,
memset, snprintf, open, mmap the rest.

## The estimate

Out of the engine: the handlers but one (~3,000 bytes), the environment and getpwnam moved to Forth
(~1,700) - **~4.7 KB**. Into the image: the file words, READ-LINE with its own buffer, SYSTEM over
FORK, EXECVE and WAITPID, the environment kept in the dictionary - **~1-1.5 KB** of bytecode at
CV8's density. **Net ~3-3.5 KB smaller, every design** - ~11% of s6's 30.5 KB, ~16% of seed 37's
smallest (20,430). The largest size lever priced so far; fbuf's 26 KB were memory, not bytes.

## What it would cost

- **Portability.** Linux's system-call numbers differ by architecture (x86-64, i386 - the 4-byte
  build - and any later port). An engine-side table mapping the image's own numbers to the host's
  (~20 entries) keeps the image portable, at ~60 bytes.
- **Speed.** READ-LINE in Forth costs dispatches per character where the C one costs none: the
  corpus reads ~40 KB of source - ~200 k dispatches against its 47 M (+0.4%); REFILL's tab loop
  already runs in Forth.
- **Work.** The largest change since the libc-free runtime: the engine variant without the handlers
  and the image with the wrappers must switch together - one gene, like kinput - and the tests
  (DELETE-FILE, the file-word fixes, the shell's pipes and redirections, the jail) must pass on it.

**The owner's decision**: build it (as a gene, after seed 39), or not.
