# The tag without its 3-byte call - the gene t2wide (Iteration 95)

The owner's question (Iteration 94): calls as continuation bytes, to get
128 one-byte opcodes and unlimited reach? Priced first on the front
(fastest e22d91cd94, middle e83972af52, smallest b3707c69dc): the designs
have 159-169 operations, 63 with one-byte codes; 139-305 escaped uses in
their images; and escapes run as 4.2-8.1% of the dispatches of kernel,
parse and corpus - each an extra byte and a second, poorly predicted jump.
Continuation calls would not change today's images (every image call is 2
bytes either way) but would make the call path a loop, hide a call's length
from its first byte and touch every decoder. So, agreed with the owner,
the cheaper route: **keep the two-bit tag, drop its 3-byte call**.

## The format, under t2wide

| first byte | meaning | bytes | reach |
|---|---|---|---|
| `00xxxxxx` | opcode: 63 codes and the escape (0x3F) | 1 | - |
| `01xxxxxx` | call, 14-bit offset | 2 | 16 KB |
| `10xxxxxx` | **opcode: 64 more codes** | 1 | - |
| `11xxxxxx` | call, 30-bit offset | 4 | 1 GB |

127 one-byte codes, assigned by the same ranking; the length of a call is
still in its first byte. Images are unchanged in their calls (all 2 bytes,
4 before an inline operand); calls compiled at run time between 16 KB and
1 GB take 4 bytes instead of 3. Links keep their own tag.

Built: the engine's table (vm-lab.c, T2WIDE: 0x80-0xBF through the map's
second half; no 3-byte call handler) and the profiler; the JIT's decoder and
jit_repoint (widths 2 and 4); the converter (layout.py --tag2-wide: the
ranking's 127 codes, the 128-entry map, calls of 2 or 4 bytes - and CALL,'s
3-byte limit, 4194304, patched to 16384 in its body, so cv8t.4 and every
recorded image stay as they are); the gene in the evolver. Not yet for
multi-state caching (tools/gen-msc.py builds its tables with three call
widths): the gene is not expressed there.

## The counts (VM)

| design | engine form | image | escapes run before (kernel / parse / corpus) | after | binary |
|---|---|---|---|---|---|
| e22d91cd94 | cached top, the JIT, 256-entry | -208 bytes | 6.3% / 8.1% / 8.0% | 0.0% | +0 |
| e83972af52 | tail calls | -302 bytes | 4.2% / 4.7% / 5.7% | 0.0% | +0 |
| b3707c69dc | plain | -121 bytes | 6.2% / 5.0% / 6.0% | 0.0% | +4,352 (sections +288) |

Every variant through the gate; the dispatches counted are the same (an
escape was never counted twice) - what goes is the escape's second byte and
second jump. Calls compiled 5 MB out, where only the 4-byte call reaches,
return the right value (hand-made s6, the old format, cannot compile there:
"Undefined word 1+"). With the gene off, all 68 designs of the front of all
runs and seed 24's front build to their recorded image size, binary size
and id; the tests pass; the hand-made stages are identical.

**A 4 KB step in the binary**: the smallest engine grew 288 bytes of
sections (the table's second half, the fill), but its stripped file 4,352:
the 16 MB memory area is page-aligned (vm-lab.c, `mem`), so `.bss` asks for
4,096 and the linker's layout pads the file up to a page when the code's end
crosses a boundary - luck, for any design and any change. The other two
engines grew +0. Worth a fix of its own (the owner's decision: it changes
every engine's file, as Iteration 82's link flags did).
