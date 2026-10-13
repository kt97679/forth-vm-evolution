/*  bench/c/bench.c - the Forth benchmarks in C: a native baseline for the
 *  Forth designs (lab/evolve/c-baseline.py, Iteration 235).
 *
 *  bench WORKLOAD [REPEAT [PARSE-FILE]]
 *
 *  Each workload does exactly the work of bench/WORKLOAD.fth's BENCH, REPEAT
 *  times - the long versions the evolver times repeat BENCH as evolve.py's
 *  LONG says (fib 2, loop 10, sieve 3, parse 3, bubble 12, ackermann 23).
 *  Cells are 64-bit and wrap, as Forth's. Inputs come through volatile reads
 *  and results go to stdout, so the compiler can neither fold the work into a
 *  constant nor drop it.
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

typedef uint64_t cell;
static volatile cell v_fib = 30, v_outer = 400, v_inner = 1000, v_size = 8190, v_sieve_reps = 15,
                     v_elements = 300, v_seed = 74755, v_ack_m = 3, v_ack_n = 5;
static volatile cell sink;

/* fib.fth: : FIB DUP 2 < IF DROP 1 ELSE DUP -1 + RECURSE SWAP -2 + RECURSE + THEN ; 30 FIB DROP */
static cell fib(int64_t n) { return n < 2 ? 1 : fib(n - 1) + fib(n - 2); }
static void b_fib(void) { sink = fib((int64_t)v_fib); }

/* loop.fth: : INNER 1000 0 DO DUP I + XOR LOOP ; 1 400 0 DO INNER LOOP DROP */
static void b_loop(void) {
    cell x = 1, outer = v_outer, inner = v_inner;
    for (cell k = 0; k < outer; k++)
        for (cell i = 0; i < inner; i++) x ^= x + i;
    sink = x;
}

/* sieve.fth: 8190 flags, 15 passes of PRIMES, the count printed */
static unsigned char flags[65536];
static void b_sieve(void) {
    cell size = v_size, reps = v_sieve_reps, count = 0;
    for (cell r = 0; r < reps; r++) {
        memset(flags, 1, size); count = 0;
        for (cell i = 0; i < size; i++)
            if (flags[i]) {
                cell prime = i + i + 3;
                for (cell k = prime + i; k < size; k += prime) flags[k] = 0;
                count++;
            }
    }
    printf("%llu\n", (unsigned long long)count);
}

/* bubble.fth: 300 cells from SEED's generator, sorted by adjacent swaps,
   checked, the first and last printed (descending: the Forth swaps when the
   later cell is greater) */
static cell list[4096];
static void b_bubble(void) {
    cell n = v_elements, seed = v_seed;
    for (cell i = 0; i < n; i++) { seed = (seed * 1309 + 13849) & 65535; list[i] = seed; }
    for (cell i = 1; i < n; i++)
        for (cell j = 0; j < n - i; j++)
            if ((int64_t)list[j + 1] > (int64_t)list[j]) { cell t = list[j]; list[j] = list[j + 1]; list[j + 1] = t; }
    for (cell j = 0; j + 1 < n; j++)
        if ((int64_t)list[j + 1] > (int64_t)list[j]) { puts("BUBBLE-SORT: NOT SORTED"); exit(1); }
    printf("%lld %lld\n", (long long)list[0], (long long)list[n - 1]);
}

/* ackermann.fth: : -ack ( y x -- n ) - A(3, 5), printed */
static cell ack(cell m, cell n) {
    if (m == 0) return n + 1;
    if (n != 0) return ack(m - 1, ack(m, n - 1));
    return ack(m - 1, 1);
}
static void b_ackermann(void) { printf("%llu\n", (unsigned long long)ack(v_ack_m, v_ack_n)); }

/* parse.fth: the outer interpreter's work in C - each token looked up in a
   dictionary of 300 names hashed as kernel.4's HASH does (32 chains), a miss
   converted as a number, the words + XOR DROP (and the last line's S" TYPE
   CR) done on a 64-cell stack; backslash comments skipped */
#define NWORDS 300
static char names[NWORDS][12]; static int nlen[NWORDS], nxt[NWORDS], heads[32];
static int hash(const char *s, int u) { int h = (unsigned char)s[0] << 1; if (u > 1) h ^= (unsigned char)s[1] << 2; return (h ^ u) & 31; }
static void dict_init(void) {
    static const char *real[] = { "+", "XOR", "DROP", "S\"", "TYPE", "CR", "BYE" };
    for (int i = 0; i < 32; i++) heads[i] = -1;
    for (int i = 0; i < NWORDS; i++) {
        if (i < 7) strcpy(names[i], real[i]); else snprintf(names[i], sizeof names[i], "W%dX", i);
        nlen[i] = (int)strlen(names[i]); int h = hash(names[i], nlen[i]); nxt[i] = heads[h]; heads[h] = i;
    }
}
static void b_parse(const char *text, size_t len) {
    cell st[64]; int sp = 0; size_t p = 0;
    while (p < len) {
        while (p < len && (unsigned char)text[p] <= ' ') p++;
        size_t s = p; while (p < len && (unsigned char)text[p] > ' ') p++;
        int u = (int)(p - s); if (!u) break;
        if (u == 1 && text[s] == '\\') { while (p < len && text[p] != '\n') p++; continue; }
        int w = heads[hash(text + s, u)];
        while (w >= 0 && !(nlen[w] == u && !memcmp(names[w], text + s, u))) w = nxt[w];
        if (w == 0) { sp--; st[sp - 1] += st[sp]; }
        else if (w == 1) { sp--; st[sp - 1] ^= st[sp]; }
        else if (w == 2) { sp--; }
        else if (w == 3) { size_t q = ++p; while (p < len && text[p] != '"') p++;          /* S" ccc" */
                           st[sp++] = (cell)(uintptr_t)(text + q); st[sp++] = (cell)(p - q); if (p < len) p++; }
        else if (w == 4) { sp -= 2; fwrite((const char *)(uintptr_t)st[sp], 1, (size_t)st[sp + 1], stdout); }
        else if (w == 5) { putchar('\n'); }
        else if (w == 6) { break; }                                                       /* BYE */
        else if (w > 6) { puts("unexpected word"); exit(1); }
        else { cell v = 0; for (size_t k = s; k < p; k++) { if (text[k] < '0' || text[k] > '9') { puts("not a number"); exit(1); } v = v * 10 + (cell)(text[k] - '0'); }
               if (sp == 64) { puts("stack overflow"); exit(1); } st[sp++] = v; }
    }
    sink = (cell)sp;
}

int main(int argc, char **argv) {
    if (argc < 2) { fputs("usage: bench fib|loop|sieve|bubble|ackermann|parse [REPEAT [PARSE-FILE]]\n", stderr); return 2; }
    int rep = argc > 2 ? atoi(argv[2]) : 1;
    const char *w = argv[1];
    if (!strcmp(w, "parse")) {
        FILE *f = fopen(argc > 3 ? argv[3] : "bench/parse.fth", "rb"); if (!f) { perror("parse file"); return 2; }
        static char text[1 << 20]; size_t len = fread(text, 1, sizeof text, f); fclose(f);
        dict_init();
        for (int r = 0; r < rep; r++) b_parse(text, len);
        return 0;
    }
    void (*fn)(void) = !strcmp(w, "fib") ? b_fib : !strcmp(w, "loop") ? b_loop : !strcmp(w, "sieve") ? b_sieve
                     : !strcmp(w, "bubble") ? b_bubble : !strcmp(w, "ackermann") ? b_ackermann : 0;
    if (!fn) { fprintf(stderr, "unknown workload %s\n", w); return 2; }
    for (int r = 0; r < rep; r++) fn();
    return 0;
}
