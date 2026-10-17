# The after-seed-54 batch - applied (Iteration 333)

| # | patch | what it does |
|---|---|---|
| 1 | cell32-after-seed54.patch | The 32-bit checks at native cell width (the owner, Iterations 324-331): 8-byte cells on a 64-bit host, 4 on a 32-bit one. **evolve.py** - cellw() (4 on a host whose pointers are 4 bytes, or EVOLVE_CELL=4 with EVOLVE_CC='gcc -m32'), from which the kernel variants (k32- from s0-cell-32 and kernel32.img, the same overlays), the converter's width, the references and the kernel workload at 4 bytes (cross.4 retargeted as tools/reseed.sh does it, against kernel32-seed.img) follow; CCV()/cc() and EVOLVE_CC's compiler not jailed by sh(); rt() links -m32 builds with the static i386 runtime; setup() takes EVOLVE_PREBUILT_REF. **engine/vm-lab.c, relf.c** - for 32-bit hosts: the system-call table with the file overlays' calls (read, write, open, close, lseek, munmap, ioctl, mremap, exit, unlink) and ARM's exit_group, SYSC's guard admitting ARM, mmap through the library, Linux's legacy layout at start (personality, one execve: ALLOCATE's mmap below 2 GB, where file-sysc.4's 0< reads it right), MAP_32BIT 0 where the host has none. **forth/cross.4** - @-T sign-extends when the target cell is narrower than the host's own, as its comment said: it read "8 <", and on a 32-bit host -1 32 LSHIFT is a full-width shift. **tools/layout.py** - tag 2 at 4-byte cells: cfd(), a CREATE'd word's code field align_up(5, CELL) - 8 bytes at both widths. **xcheck.py** - --sample --cell 4: each design built and alive as a static 32-bit x86 engine before it goes, and the 4-byte references in the bundle (build32/); the host's byte order and cell width recorded and reported. **remote-checks.sh, REMOTES** - several checks a host, one after another under the host's lock, each deadline from its own start; prebuilt32 (dream.lan's 32-bit check: the laptop's static builds and references); rage.lan back, native at its own 4-byte cells. FORMAT-TAG2.md and the evolver README with it. No gene; no reseed; ids unchanged. |

    git apply results/applied-after-seed54/cell32-after-seed54.patch

Tested in master's working tree (Iterations 324-331):
- **64 bits unchanged**: six recorded designs of seed 53's front (three JIT, three interpreted) built
  from a clean clone of master and from the patched tree - engines and images byte-identical;
  gene-equiv.py against master: PASS - 3,733 recorded genomes, the operator draws too (no new gene);
  run-tests PASS, 63 engine paths; validate 7 of 7 IDENTICAL; the gate 245 of 245 alive (seed 53's
  front 172, the joint front 118, 45 in both); three tag-2 images of seed 53's front converted by the
  old converter and the new - identical; the cross compiler on a 64-bit host: the same HERE after its
  definitions (4,344,888) and kernel-seed.img reproduced.
- **32-bit x86 at 4-byte cells** (gcc -m32): 14 of 14 alive - s6 and 13 of seed 53's front, every
  one tag 2, fsys 1-5: the corpus right and the 4-byte kernel rebuilt byte for byte by the design's
  own run of the cross compiler; static engines (the i386 runtime) alive too.
- **ARMv7 at 4-byte cells** (arm-linux-gnueabihf-gcc, run under qemu-arm): 5 of 5 alive. qemu does
  not fault an unaligned 64-bit load as a Cortex-A9 may: the Tegra's first run says.
- **The checks**, with a stand-in ssh and scp (unknown hosts exit 255, missing files fail): a host
  with a 64-bit and a 32-bit prebuilt check - the second waited for the first's lock, both
  measured and gathered, the 32-bit report "little-endian, 4-byte cells - measured on the host";
  a simulated 32-bit native host (the Tegra's mode) - 2 of 2 measured. A bug found so - the shipped
  reference's work directory set inside the else branch - fixed and the check run again.
- On a fresh clone of master after Iteration 332 it applies and reproduces the tested files.

Before seed 55: nothing more from the owner - ssh keys to dream.lan and rage.lan as before. The
Tegra's first real check is seed 55's: native builds there, its byte order recorded, alignment met.

**Applied on master at Iteration 333**: build-stages; run-tests PASS, 63 engine paths; validate 7 of
7 IDENTICAL; the gate 259 of 259 alive (seed 54's front 195, the joint front 125, 61 in both) - a
front the batch was not developed against.

