# The hybrid stack/register design, priced again (Iteration 172)

The owner asked for it at Iteration 163; then only the stack shuffles were
measured (23-46% of dispatches, results/tracer.md). Iteration 32's price
(results/price-register-stage1.md) covered the image's code only - and four of
today's six selection workloads (fib, loop, bubble, ackermann) are compiled at
run time. This prices every executed dispatch, run-time code included, from
the profiler's dynamic opcode pairs (JIT off - for a JIT design the saving is
in the copied handlers, not in dispatches). The tool: results/drafts/
hybprice.py; the full tables: results/drafts/hybprice-iter172.txt.

**A measurement bug found on the way:** regprice.py's opcode names (Iteration
32) are computed from the primitive list's order, which has moved since (the
single SYSCALL, TABS>BL out, newer genes): on evolved designs it names opcodes
wrongly - a NOOP at 8% of loop's dispatches - while every opcode still gets a
name, so nothing looks unnamed. The converter writes each opcode's real name in
CALLMAP's O records; this price takes them from there. regprice.py needs the
same fix before it is used again.

| design | moves: the bound | a move feeding the next operation | return stack feeding one | unnamed |
|---|---|---|---|---|
| s6 | 17-27% | 0-12% (fib 0, loop 4.3, bubble 4.2) | 0-4% | 0-19% |
| 9932cc5c32, the fastest | 11-27% | 0-8% (fib, loop, bubble 0) | 0-3%, loop 20% | 0-30% |
| b40b6b7e2d, the smallest | 17-27% | 0-10% (fib 0, loop 4.2, bubble 5.8) | 0-4% | 0-20% |

Evolution has not taken the moves out: a fifth to a quarter of every design's
dispatches. The simplest absorbing form - a move feeding the next operation -
would save 4-12% on the image-heavy workloads (kernel, corpus, parse, sieve),
little on the run-time ones. That is the count's blind spot, not the
design's: in fib every move feeds a literal first (DUP 2 <, DUP 1 -, SWAP 2 -),
seen only by a triple, and the designs' immediate-operand opcodes are not yet
classified as uses. fib's moves alone are 23% of its dispatches.

**Next:** (1) the profiler's triples (a move, then any two) and every opcode
kind named - the price of operand-carrying forms with immediates, which is
what the selection's workloads need; (2) if that is 10% or more of the
selection's dispatches: the gene - forms in the converter, in the run-time
compiler (where fib, loop, bubble and ackermann are compiled), handlers in
the engines, the JIT copying them; (3) the laptop's measurement in the run
after seed 40's batch.
