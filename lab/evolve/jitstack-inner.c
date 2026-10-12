/* jitstack-inner.c - the loop workload's hot word timed five ways (Iterations 218-219):
   the JIT's stencils as copied today, three cells cached, the loop
   index in registers too, and the fixed-register design at K = 2 and 3 (jitvariants.py).
   Placement decides much on some cores: lab/evolve/jitstack-inner-sweep.sh runs it at eight.
       gcc -O2 -no-pie -o /tmp/inner lab/evolve/jitstack-inner.c lab/evolve/jitstack-inner.S && /tmp/inner  */
#include <stdio.h>
#include <stdint.h>
#include <time.h>
extern uint64_t rpvar;
typedef uint64_t (*fn)(uint64_t *sp, uint64_t tos);
uint64_t inner_now(uint64_t *, uint64_t), inner_cached(uint64_t *, uint64_t), inner_regloop(uint64_t *, uint64_t), inner_fixed2(uint64_t *, uint64_t), inner_fixed3(uint64_t *, uint64_t);
static uint64_t ds[64], rs[8];
static double run(fn f, uint64_t n, uint64_t *out) {
    struct timespec a, b; double best = 1e9;
    for (int r = 0; r < 7; r++) {
        rs[0] = 0; rs[1] = n; rpvar = (uint64_t)(uintptr_t)rs;
        clock_gettime(CLOCK_MONOTONIC, &a);
        *out = f(ds + 32, 12345);
        clock_gettime(CLOCK_MONOTONIC, &b);
        double t = (b.tv_sec - a.tv_sec) + (b.tv_nsec - a.tv_nsec) / 1e9;
        if (t < best) best = t;
    }
    return best;
}
int main(void) {
    uint64_t n = 200000000, ra, rb, rc;
    uint64_t r2, r3; double ta = run(inner_now, n, &ra), tb = run(inner_cached, n, &rb), tc = run(inner_regloop, n, &rc), t2 = run(inner_fixed2, n, &r2), t3 = run(inner_fixed3, n, &r3);
    printf("fixed2   %.3f s  %.2f ns/iteration  (%.2f of now) %s\n", t2, t2 / n * 1e9, t2 / ta, r2 == ra ? "" : "WRONG RESULT");
    printf("fixed3   %.3f s  %.2f ns/iteration  (%.2f of now) %s\n", t3, t3 / n * 1e9, t3 / ta, r3 == ra ? "" : "WRONG RESULT");
    printf("same results: %s (%llu %llu %llu)\n", ra == rb && rb == rc ? "yes" : "NO", (unsigned long long)ra, (unsigned long long)rb, (unsigned long long)rc);
    printf("now      %.3f s  %.2f ns/iteration\n", ta, ta / n * 1e9);
    printf("cached   %.3f s  %.2f ns/iteration  (%.2f of now)\n", tb, tb / n * 1e9, tb / ta);
    printf("+loop    %.3f s  %.2f ns/iteration  (%.2f of now)\n", tc, tc / n * 1e9, tc / ta);
    return 0;
}
