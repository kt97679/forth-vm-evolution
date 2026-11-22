# The final shipping path rehearsed on today's tree (Iteration 737)

The owner (seed 97 running: "start with 1"): the end of the work - the final roles exported into designs/, shipped
self-built, packed and handed to relf - last ran at 718-726; since then the engine's data layout (734: a linker script
each design's Makefile must carry), the genes' dumps (-bg, 735), numfirst and chainorder (733-736, self-hosted at 736)
and lld's ARM links with the script. Rehearsed on the ten roles as designs/ has them (results/relf-designs-718.md's
records), in a scratch clone - results/drafts/ship-rehearsal-737.sh, roles-build-718.sh's two phases in the packages'
order; nothing sent.

| step | result |
|---|---|
| phase 1: the stages, validate, export-designs.py | build, 7 of 7 IDENTICAL, the ten exported (every engine the lab's bytes, the libc builds running) |
| export-arm.py (clang, lld) | first FAILED - lld found no ARM libgcc: this sandbox was set up without CROSS=1's packages (lld, qemu-user, libc6-dev-armhf-cross, libgcc-13-dev-armhf-cross); with them, 3 designs, the lab's bytes, running under qemu-arm - the data layout's script under lld for ARM |
| export-arm.py --gcc (the cross GCC, gcc-multilib out) | 3 designs, the lab's bytes, running; gcc-multilib back after (export-arm builds its 4-byte reference with gcc -m32 - with the cross GCC in, `asm/errno.h` is missing: the clang step must come first, as 718 ordered it) |
| phase 2: selfhost-ship.sh | first run without the gate's verdicts: all ten self-built, the three JIT roles' images then not designs/'s (725 shipped them translator-built - the gate's speed half); with TRANSLATOR= 725's verdicts (from a file: their text has quotes), seven self-built, three translator-built, as shipped |
| the designs' make, test, selfhost, 32, libc | all 0; test 17 ok, selfhost 14 rebuilt byte for byte (the seven at both widths) |
| pack-designs.py | 20 of 20 builds 9 of 9 right |
| the images | **20 of 20 byte for byte designs/'s** - what differs is the engines (727-736's changes: the layout's addresses, vm.c, jit.c), the Makefiles (-Wl,-T,src/data-layout.ld - src32/, srcarm/ - each design carrying its copy), genes.4 (736's lists) |
| relf-handoff-726.py | byte for byte results/handoff-relf-726.md |

For the final handoff, then: the sandbox set up with CROSS=1 before phase 1; the gate's verdicts on the final roles
(selfhost-speed.py on the laptop) handed to phase 2 as TRANSLATOR=, from a file; a new handoff generator for the new
roles' text (726's reproduces its document, its rows and claims 718's); the package pack-designs.py's directory
tarred, as 726's.
