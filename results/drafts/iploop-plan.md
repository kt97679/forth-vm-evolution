# The IP-update loop form - a plan, and the measurement that decides it (Iteration 295)

Deferred since Iteration 260, left open by the laptop's counters (Iteration 285,
results/counters-amd-ryzen-7-pro-8840hs.md). Not built: what to build depends on a
measurement not made yet.

## What is known

- On the compute workloads (fib, loop, bubble, ackermann) every interpreted design
  mispredicts at most 0.54 branches per thousand instructions: dispatch is predicted.
- Yet the evolved interpreted designs run 1.7-2.9 instructions per cycle, s6
  2.75-3.9, with as few misses.
- A lower IPC is not by itself a fault: the evolved designs do fewer, heavier
  instructions a dispatch - superinstructions, fused operations, the cached top - and
  are faster for it. The question is what bounds them now.

## Three explanations

1. **The instruction pointer's chain** (Ertl and Paysan): every dispatch loads the next
   opcode through ip, which the handler has just moved, and jumps on it. A form that
   loads the next opcode before the handler's own work - dispatch prefetch - takes the
   load off that chain. This is the IP-update loop form.
2. **The data stack through memory**: a push and the pop after it are a store and a
   load, store-to-load forwarding on the critical path. The cached top (gene tos)
   removes one; the multi-state cache (msc) more - and msc is on none of seed 49's
   front.
3. **The front end**: a large interpreter's code - fetch, decode, the op cache.

## The measurement, before anything is built

1. On the laptop, between runs:

       sh lab/evolve/next-run.sh experiment counters.py --extra stalled-cycles-frontend:u,stalled-cycles-backend:u

   (counters.py --extra, Iteration 295: each extra event a column, as a share of cycles;
   one the CPU cannot count is n/a.) Back-end stalls dominating say 1 or 2; front-end, 3.
2. If back-end: a hand-made variant of the fastest interpreted design whose handlers
   load the next opcode first, against its own engine - cycles on fib, loop and bubble.
   A drop says 1; none says 2.
3. Only then a gene: dispatch prefetch in the generators (1), or more of the stack in
   registers (2) - or neither (3).
