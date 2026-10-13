/*
 *  jit.c - a minimal lazy JIT (JIT.md, Iteration 74): phase 1, x86-64.
 *
 *  SPN's stencils (spn-stencils.c: one Forth operation an ordinary C
 *  function, never called) are read out of the running engine, copied
 *  back to back into executable memory and patched - the rules of
 *  forth/spn.4, in C. This file, so far: reading the stencils.
 *
 *  A stencil's body starts at its address (after an endbr64) and ends
 *  after its last jump to NEXT or JUMP - or, for EXIT, at its first ret.
 *  Its holes are found exactly: a 32-bit relative field aimed precisely
 *  at a marker (NEXT, JUMP, CALL), or one of the magic constants (an
 *  8-byte literal, the 4-byte literal, the return stack's address). A
 *  stencil of any other shape is not used: slower, never wrong.
 */
#include <stdint.h>
#include <string.h>
#include "spn-abi.h"
extern const void *const spn_table[];
extern const int spn_table_len;

enum { J_NEXT, J_JUMP, J_CALL,                  /* the markers: only their addresses matter */
       S_LIT, S_DUP, S_DROP, S_SWAP, S_OVER, S_ROT, S_PLUS, S_ADDI, S_EQ, S_GT, S_LT, S_XOR,
       S_AND, S_NEGATE, S_0BRANCH, S_BRANCH, S_CALL, S_EXIT, S_ADDI32, S_DUP_GTI_BR, S_TOR,
       S_FROMR, S_RFETCH, S_FETCH, S_STORE, S_CFETCH, S_CSTORE, S_OR, S_ULT, S_LSHIFT,
       S_RSHIFT, S_INTERP, S_DO, S_QDO, S_LOOP, S_PLOOP, S_I, S_J, S_UNLOOP, S_LEAVE, S_PICK,
#if JITX
       S_FILL,                                   /* Iteration 108: forth-vm-evolution's own */
#endif
#if JITINL
       S_DPLUS,                                  /* Iteration 137: the gene jitinl */
#endif
       S_N };                                    /* spn_table's order, the first 44 (45 with jitx) */

#define JIT_IMM64 0x5ea1ed5ea1ed5ea1ULL         /* spn-stencils.c's SPN_IMM_VALUE */
#define JIT_RP64  0x7ea1ed5ea1ed5e77ULL         /* SPN_RP_VALUE */
#define JIT_IMM32 0x3c1a5e77U                   /* IMM32 */

struct jit_st {             /* a stencil as read: offsets into its body, -1 for none */
    const unsigned char *src;
    int len, imm, imm32, rp, tailnext;          /* tailnext: the body ends "jmp NEXT" - dropped */
    int nnext, njump, ncall;                    /* how many holes of each */
};
static struct jit_st jit_st[S_N];

static int32_t jit_rel32(const unsigned char *p) { int32_t v; memcpy(&v, p, 4); return v; }
static int jit_relto(const unsigned char *p, const void *t) { return p + 4 + jit_rel32(p) == (const unsigned char *)t; }

/* Iteration 129: a stencil is read up to the next table function, or this
   far. 64 cut (+LOOP)'s stencil (87 bytes since Iteration 125's rule) before
   either exit, and (?DO)'s (76) after its fall-through, before its skip -
   neither was mapped until the gene jitloop, which reads further. */
#if JITLOOP
#define JIT_SCAN_MAX 160
#else
#define JIT_SCAN_MAX 64
#endif
static void jit_scan(void) {
    int i, k;
    for (i = S_LIT; i < S_N && i < spn_table_len; i++) {
        struct jit_st *s = &jit_st[i];
        const unsigned char *a = spn_table[i], *hi = a + JIT_SCAN_MAX, *end = 0, *p;
        s->len = -1;
        if (a[0] == 0xF3 && a[1] == 0x0F && a[2] == 0x1E && a[3] == 0xFA) a += 4;     /* endbr64 */
        for (k = 0; k < spn_table_len; k++) {
            const unsigned char *e = spn_table[k];
            if (e > (const unsigned char *)spn_table[i] && e < hi) hi = e;
        }
        if (i == S_EXIT) { for (p = a; p < hi; p++) if (*p == 0xC3) { end = p + 1; break; } }
        else for (p = a; p + 5 <= hi; p++)
            if (*p == 0xE9 && (jit_relto(p + 1, spn_table[J_NEXT]) || jit_relto(p + 1, spn_table[J_JUMP]))) end = p + 5;
        if (!end) continue;
        s->src = a; s->len = (int)(end - a); s->imm = s->imm32 = s->rp = -1;
        s->nnext = s->njump = s->ncall = 0;
        for (p = a; p < end; p++) {
            uint64_t v; uint32_t w;
            if (p + 8 <= end) { memcpy(&v, p, 8); if (v == JIT_IMM64) s->imm = (int)(p - a); if (v == JIT_RP64) s->rp = (int)(p - a); }
            if (p + 4 <= end) {
                memcpy(&w, p, 4); if (w == JIT_IMM32) s->imm32 = (int)(p - a);
                if (jit_relto(p, spn_table[J_NEXT])) s->nnext++;
                if (jit_relto(p, spn_table[J_JUMP])) s->njump++;
                if (jit_relto(p, spn_table[J_CALL])) s->ncall++;
            }
        }
        s->tailnext = end - 5 >= a && end[-5] == 0xE9 && jit_relto(end - 4, spn_table[J_NEXT]);
    }
}

#ifndef JIT_SCAN_MAIN
/* ---- the translator (Iteration 80): phase 1, x86-64, the two-bit tag ----
 *
 *  A colon word compiled at run time begins [JIT][four bytes] (forth/
 *  cv8t-jit.4): its body's length, top bit set, until its first call;
 *  then the native code's offset in jit_mem, or 0 - it stays bytecode.
 *  All or nothing: every operation must have stencils (vm-jit-ops.h, the
 *  converter's, from the operation's name) and every call must reach a
 *  native word or this one. Native words call each other with the C
 *  stack's call and ret; loops and the return stack use the engine's
 *  return stack, through jit_rp.  */
#include <sys/mman.h>
struct jit_op { unsigned char ok, n, opnd; signed char k; unsigned char st[5]; };
#include "vm-jit-ops.h"                 /* jit_ops[], JIT_CODE: this design's */
#define JIT_NOPS ((int)(sizeof jit_ops / sizeof jit_ops[0]))
#ifndef T2_ESC
#define T2_ESC  0xFFFE
#define T2_NONE 0xFFFF
#endif
#if T2WIDE   /* Iteration 95, the gene t2wide: calls 01 and 11 only, 10xxxxxx one-byte codes too */
#define T2_JONES 128
#define T2_CALL(b) ((b) & 0x40)
#define T2_CALLW(b) ((b) < 0x80 ? 2 : 4)
#define T2_ONEIX(b) ((b) < 64 ? (b) : (b) - 64)
#define T2_WSTEP 2
#else
#define T2_JONES 64
#define T2_CALL(b) ((b) >= 0x40)
#define T2_CALLW(b) ((b) < 0x80 ? 2 : (b) < 0xC0 ? 3 : 4)
#define T2_ONEIX(b) (b)
#define T2_WSTEP 1
#endif
static const unsigned short jit_one[T2_JONES] = {
#include "vm-tag2-one.h"
};
static const unsigned short jit_esc[256] = {
#include "vm-tag2-esc.h"
};
#define JIT_MEM    (1u << 20)           /* the executable region: reserved; touched as used */
#define JIT_MAXOPS 256                  /* a longer word stays bytecode */
static unsigned char *jit_mem;
static uint32_t jit_used = 16;             /* offsets 0 and 1 mean: not native */
static ucell jit_rp;                    /* the return stack while native code runs: IMM_RP */
static UNS64 jit_cbase;                 /* the image base: calls are offsets from it */

static uint32_t jit_ld32(UNS64 a) {
    return (uint32_t)BYTE(a) | (uint32_t)BYTE(a + 1) << 8 | (uint32_t)BYTE(a + 2) << 16 | (uint32_t)BYTE(a + 3) << 24;
}
static void jit_st32(UNS64 a, uint32_t v) {
    BYTE(a) = (UNS8)v; BYTE(a + 1) = (UNS8)(v >> 8); BYTE(a + 2) = (UNS8)(v >> 16); BYTE(a + 3) = (UNS8)(v >> 24);
}
static int jit_init(void) {
    static int state;                   /* 0 not yet, 1 ready, -1 none */
    if (!state) {
        void *m = mmap(0, JIT_MEM, PROT_READ | PROT_WRITE | PROT_EXEC, MAP_PRIVATE | MAP_ANONYMOUS, -1, 0);
        jit_scan();
        if (m == MAP_FAILED) state = -1; else { jit_mem = m; state = 1; }
    }
    return state == 1;
}
/* A stencil the translator may use: read, and no call hole unless CALL. */
static int jit_usable(int s) {
#if JITLOOP
    /* Iteration 129: (+LOOP) and (?DO) have two exits - on, and to their
       branch target. A stencil read without both holes would jump nowhere,
       so it is not used: slower, never wrong. */
    if ((s == S_PLOOP || s == S_QDO) && (jit_st[s].nnext < 1 || jit_st[s].njump != 1)) return 0;
#endif
    return jit_st[s].len > 0 && jit_st[s].ncall == (s == S_CALL) && jit_st[s].njump <= 1;
}
static int jit_len(int s) { return jit_st[s].len - (jit_st[s].tailnext ? 5 : 0); }
/* Copy stencil s to dst and patch it: the literal, the return stack, NEXT
   (the end of the copy), JUMP and CALL. Its trailing jmp NEXT is dropped. */
static unsigned char *jit_put(unsigned char *dst, int s, UNS64 val, UNS64 jump, UNS64 call) {
    const struct jit_st *t = &jit_st[s];
    int n = jit_len(s), p;
    memcpy(dst, t->src, (size_t)n);
    for (p = 0; p + 4 <= n; p++) {
        UNS64 to = 0;
        if (jit_relto(t->src + p, spn_table[J_NEXT])) to = (UNS64)(uintptr_t)(dst + n);
        else if (jit_relto(t->src + p, spn_table[J_JUMP])) to = jump;
        else if (jit_relto(t->src + p, spn_table[J_CALL])) to = call;
        if (to) { int32_t r = (int32_t)(to - (UNS64)(uintptr_t)(dst + p + 4)); memcpy(dst + p, &r, 4); p += 3; }
    }
    if (t->imm >= 0) memcpy(dst + t->imm, &val, 8);
    if (t->rp >= 0) { UNS64 v = (UNS64)(uintptr_t)&jit_rp; memcpy(dst + t->rp, &v, 8); }
    return dst + n;
}
/* Iteration 81: a word that stays bytecode should cost its callers
   nothing. The call that reached w's JIT opcode ends at ra, the return
   address: if the 2, 3 or 4 bytes before ra are a call naming w exactly,
   point it past the header - that call site then skips the JIT dispatch
   for good. Anything else (EXECUTE, a target past the width) is left. */
static void jit_repoint(UNS64 w, UNS64 ra) {
    UNS64 t = w + 5 - jit_cbase, x;
    int wd, i;
    for (wd = 2; wd <= 4; wd += T2_WSTEP) {
        UNS64 a = ra - (UNS64)wd;
        UNS8 b = BYTE(a);
        if ((b >> 6) != wd - 1) continue;                 /* tag 01: 2 bytes, 10: 3, 11: 4 */
        for (x = b & 0x3F, i = 1; i < wd; i++) x = x << 8 | BYTE(a + i);
        if (jit_cbase + x != w) continue;
        if (t >> (8 * wd - 2)) return;                    /* past the header: too far for this width */
        BYTE(a) = (UNS8)((b & 0xC0) | (t >> (8 * (wd - 1))));
        for (i = 1; i < wd; i++) BYTE(a + i) = (UNS8)(t >> (8 * (wd - 1 - i)));
        return;
    }
}
#if PROFILE
/* Iteration 90 (lab/evolve/callsites.py): every word the translator was
   asked for and, for each left bytecode, every call in it and the first
   operation without stencils - what keeps it from going native. And the
   one-byte codes that have stencils. Profiling builds only: no design's
   engine has this. */
#include <stdio.h>
static UNS64 jn_w[4096], jn_end[4096];
static int jn_n;
#define JITNOTE(w, e) do { if (jn_n < 4096) { jn_w[jn_n] = (w); jn_end[jn_n] = (e); jn_n++; } } while (0)
#if JIT_PRICE
/* Iteration 218: every operation of every word translated - where it is, its
   logical operation (0xFFFD a literal, 0xFFFE a call resolved, 0xFFFF a call
   to the word itself) and a branch's target - for lab/evolve/jitstack.py. */
#define JP_N 65536
static UNS64 jp_w[JP_N], jp_at[JP_N], jp_t[JP_N];
static unsigned short jp_l[JP_N];
static int jp_n;
#define JITPRICE(w, a, l, t) do { if (jp_n < JP_N) { jp_w[jp_n] = (w); jp_at[jp_n] = (a); jp_l[jp_n] = (l); jp_t[jp_n] = (t); jp_n++; } } while (0)
#endif
static void jit_dump(int fd) {
    char b[96];
    int i, k, m;
#if JIT_PRICE
    for (i = 0; i < JIT_NOPS; i++) if (jit_ops[i].ok) {
        m = snprintf(b, sizeof b, "L %d %d %d %d %d %d %d %d %d\n", i, jit_ops[i].opnd, jit_ops[i].k, jit_ops[i].n,
                     jit_ops[i].st[0], jit_ops[i].st[1], jit_ops[i].st[2], jit_ops[i].st[3], jit_ops[i].st[4]); write(fd, b, (size_t)m); }
    for (i = 0; i < jn_n; i++) {        /* Iteration 220: every call of every word met, translated or not */
        UNS64 w = jn_w[i], end = jn_end[i], a = w + 5;
        while (a < end) {
            UNS8 c = BYTE(a);
            if (T2_CALL(c)) {
                int wd = T2_CALLW(c), j;
                UNS64 t = c & 0x3F;
                for (j = 1; j < wd; j++) t = t << 8 | BYTE(a + j);
                m = snprintf(b, sizeof b, "K %llu %llu %llu\n", (unsigned long long)(w - jit_cbase), (unsigned long long)(a - jit_cbase),
                             (unsigned long long)t); write(fd, b, (size_t)m);
                a += (UNS64)wd;
            } else {
                unsigned L = jit_one[T2_ONEIX(c)];
                a++;
                if (L == T2_ESC) { L = jit_esc[BYTE(a)]; a++; }
                if (L >= (unsigned)JIT_NOPS || !jit_ops[L].ok) break;
                switch (jit_ops[L].opnd) {
                case 1: case 5: case 6: a += 1; break;
                case 2: case 7: a += 2; break;
                case 3: a += 4; break;
                case 4: a += 8; break;
                default: break;
                }
            }
        }
    }
    for (i = 0; i < jp_n; i++) {
        m = snprintf(b, sizeof b, "O %llu %llu %u %llu\n", (unsigned long long)(jp_w[i] - jit_cbase),
                     (unsigned long long)(jp_at[i] - jit_cbase), jp_l[i], (unsigned long long)(jp_t[i] ? jp_t[i] - jit_cbase : 0));
        write(fd, b, (size_t)m); }
#endif
    for (k = 0; k < T2_JONES; k++)
        if (jit_one[k] < (unsigned)JIT_NOPS && jit_ops[jit_one[k]].ok) { m = snprintf(b, sizeof b, "S %d\n", k < 64 ? k : k + 64); write(fd, b, (size_t)m); }
    for (i = 0; i < jn_n; i++) {
        UNS64 w = jn_w[i], end = jn_end[i], a = w + 5;
        uint32_t f = jit_ld32(w + 1);
        m = snprintf(b, sizeof b, "J %llu %llu %u\n", (unsigned long long)(w - jit_cbase), (unsigned long long)(end - jit_cbase), f);
        write(fd, b, (size_t)m);
        while (f < 2 && a < end) {
            UNS8 c = BYTE(a);
            if (T2_CALL(c)) {
                int wd = T2_CALLW(c), j;
                UNS64 t = c & 0x3F;
                for (j = 1; j < wd; j++) t = t << 8 | BYTE(a + j);
                if (jit_cbase + t != w) {
                    m = snprintf(b, sizeof b, "B %llu c %llu\n", (unsigned long long)(w - jit_cbase), (unsigned long long)t); write(fd, b, (size_t)m); }
                a += (UNS64)wd;
            } else {
                unsigned L = jit_one[T2_ONEIX(c)];
                int e = 0;
                a++;
                if (L == T2_ESC) { e = BYTE(a); L = jit_esc[e]; a++; }
                if (L >= (unsigned)JIT_NOPS || !jit_ops[L].ok) {
                    m = snprintf(b, sizeof b, "B %llu o %d %d\n", (unsigned long long)(w - jit_cbase), c, e); write(fd, b, (size_t)m); break; }
                switch (jit_ops[L].opnd) {
                case 1: case 5: case 6: a += 1; break;
                case 2: case 7: a += 2; break;
                case 3: a += 4; break;
                case 4: a += 8; break;
                default: break;
                }
            }
        }
    }
}
#else
#define JITNOTE(w, e)
#endif

#if JITX
/*  Iteration 108, the gene jitx: the translator reaches further (results/
 *  jit-kernel-words.md).
 *  - A call to a variable (DOVAR) is a literal: its parameter field's
 *    address, align8(body + 5) under the tag (L_dovar) - fixed for the run.
 *  - A word without the JIT header - a kernel word in the image, a CONSTANT
 *    made at run time - is translated too, once, kept by its address in
 *    jit_k; its end found as the converter finds a body's: the first EXIT
 *    no branch reaches past.
 *  - >R, R> and R@ have stencils (layout.py --jitx), in a word whose return
 *    stack balances in order - never below its entry, back to it at every
 *    EXIT: a word that reads its own return address stays bytecode, since
 *    native words return through the C stack, not the engine's.  */
#define JIT_DEPTH 8
#define JIT_KN 256
static struct { UNS64 w; uint32_t f; } jit_k[JIT_KN];   /* f: native offset; 0 bytecode; 1 being translated; top bit: not yet */
static uint32_t *jit_kslot(UNS64 w) {
    unsigned h = (unsigned)((w * 0x9E3779B97F4A7C15ULL) >> 56), n;
    for (n = 0; n < JIT_KN; n++, h = (h + 1) % JIT_KN) {
        if (jit_k[h].w == w) return &jit_k[h].f;
        if (!jit_k[h].w) { jit_k[h].w = w; jit_k[h].f = 0x80000000u; return &jit_k[h].f; }
    }
    return 0;                           /* full: the rest stay bytecode */
}
static int jit_ends(unsigned L) { const struct jit_op *o = &jit_ops[L]; return o->n && o->st[o->n - 1] == S_EXIT; }
#else
#define JIT_DEPTH 4
#endif

#if JITINL
/* Iteration 137 (the gene jitinl): a word of one operation and EXIT - 1+,
   0=, CELL+ - is that operation in its caller, not a call: call and return
   were a quarter of a small recursive word's native time. Not an operation
   that branches, ends the word, or touches the return stack or the
   interpreter, whose meaning a call changes; anything else stays a call. */
static int jit_inl1(UNS64 a, unsigned short *op, UNS64 *v) {
    UNS8 b = BYTE(a); unsigned L, L2, j; UNS64 x;
    if (T2_CALL(b)) return 0;
    L = jit_one[T2_ONEIX(b)]; a++;
    if (L == T2_ESC) { L = jit_esc[BYTE(a)]; a++; }
    if (L >= (unsigned)JIT_NOPS || !jit_ops[L].ok || jit_ops[L].opnd >= 6) return 0;
    for (j = 0; j < jit_ops[L].n; j++) {
        int s = jit_ops[L].st[j];
        if (s == S_EXIT || s == S_CALL || s == S_INTERP || s == S_TOR || s == S_FROMR || s == S_RFETCH ||
            s == S_DO || s == S_QDO || s == S_LOOP || s == S_PLOOP || s == S_I || s == S_J ||
            s == S_UNLOOP || s == S_LEAVE || jit_st[s].njump) return 0;
    }
    switch (jit_ops[L].opnd) {
    case 0: x = (UNS64)(INT64)jit_ops[L].k; break;
    case 1: x = BYTE(a); a += 1; break;
    case 2: x = LD16(a); a += 2; break;
    case 3: x = (UNS64)(INT64)(int32_t)jit_ld32(a); a += 4; break;
    case 4: x = (UNS64)jit_ld32(a) | (UNS64)jit_ld32(a + 4) << 32; a += 8; break;
    case 5: x = (UNS64)(INT64)(int8_t)BYTE(a); a += 1; break;
    default: return 0;
    }
    b = BYTE(a);
    if (T2_CALL(b)) return 0;
    L2 = jit_one[T2_ONEIX(b)]; a++;
    if (L2 == T2_ESC) { L2 = jit_esc[BYTE(a)]; a++; }
    if (L2 >= (unsigned)JIT_NOPS || !jit_ops[L2].ok || jit_ops[L2].n != 1 || jit_ops[L2].st[0] != S_EXIT) return 0;
    *op = (unsigned short)L; *v = x; return 1;
}
#endif
#if JITX
static uint32_t jit_body(UNS64 w, UNS64 a, UNS64 end, int depth);
#else       /* without jitx, called once: inlined, the engine as it was */
static inline __attribute__((always_inline)) uint32_t jit_body(UNS64 w, UNS64 a, UNS64 end, int depth);
#endif
/* Translate the word whose JIT opcode is at w. The native offset, or 0. */
static uint32_t jit_word(UNS64 w, int depth) {
    UNS64 end = w + 5 + (jit_ld32(w + 1) & 0x7FFFFFFFu);
    uint32_t f;
    JITNOTE(w, end);
    jit_st32(w + 1, 0);                 /* meanwhile, and if it fails: not native */
    f = jit_body(w, w + 5, end, depth);
    if (f) jit_st32(w + 1, f);
    return f;
}
#if JITTAIL
/*  Iteration 246, the gene jittail (results/price-jit-calls.md): a call to a
 *  native word whose next operation is EXIT - or a BRANCH, or a chain of them,
 *  ending at an EXIT - becomes a jump to that word: its ret returns to our
 *  caller, and tail recursion runs in place. Return addresses are on the
 *  machine stack, so >R, R> and the loops' parameters are untouched; anything
 *  else after the call (R>, LOOP, UNLOOP) is not a tail call.  */
static int jit_tail(int i, int n, const unsigned short *opl, const UNS64 *arg, const UNS64 *at) {
    int k = i + 1, hops = 0, j;
    if (!jit_usable(S_BRANCH)) return 0;
    while (k < n && hops++ < 8) {
        const struct jit_op *o;
        if (opl[k] >= 0xFFFD) return 0;
        o = &jit_ops[opl[k]];
        if (o->n == 1 && o->st[0] == S_EXIT) return 1;
        if (!(o->n == 1 && o->st[0] == S_BRANCH && o->opnd >= 6)) return 0;
        for (j = 0; j < n && at[j] != arg[k]; j++) ;
        k = j;
    }
    return 0;
}
#endif

/* The operations from a to end - end 0: find it, a word without a header
   (jitx) - of the word w: a call to w is a call to this code itself. */
#if JITX
static uint32_t jit_body(UNS64 w, UNS64 a, UNS64 end, int depth) {
#else
static inline __attribute__((always_inline)) uint32_t jit_body(UNS64 w, UNS64 a, UNS64 end, int depth) {
#endif
    UNS64 at[JIT_MAXOPS + 1], arg[JIT_MAXOPS], far = 0;
    uint32_t nat[JIT_MAXOPS + 1], size = 0, off;
    unsigned short opl[JIT_MAXOPS];     /* the logical operation; 0xFFFF a call to w, 0xFFFE a call resolved, 0xFFFD a literal */
#if JITTAIL
    unsigned char tl[JIT_MAXOPS];       /* Iteration 246: this call is a tail call - a jump */
#endif
    int n = 0, i, j;
    (void)far;
    if (depth > JIT_DEPTH || !jit_init()) return 0;
#if JITX
    for (; !end || a < end; n++) {      /* decode, as the engine does */
#else
    for (; a < end; n++) {
#endif
        UNS8 b = BYTE(a);
        if (n >= JIT_MAXOPS) return 0;
        at[n] = a;
        if (T2_CALL(b)) {               /* a call of 2, 3 or 4 bytes (2 or 4: t2wide) */
            int wd = T2_CALLW(b); UNS64 t = b & 0x3F;
            for (i = 1; i < wd; i++) t = t << 8 | BYTE(a + i);
            arg[n] = jit_cbase + t; opl[n] = 0xFFFF; a += (UNS64)wd;
        } else {
            unsigned L = jit_one[T2_ONEIX(b)];
            a++;
            if (L == T2_ESC) { L = jit_esc[BYTE(a)]; a++; }
            if (L >= (unsigned)JIT_NOPS || !jit_ops[L].ok) return 0;
            opl[n] = (unsigned short)L;
            switch (jit_ops[L].opnd) {
            case 0: arg[n] = (UNS64)(INT64)jit_ops[L].k; break;
            case 1: arg[n] = BYTE(a); a += 1; break;
            case 2: arg[n] = LD16(a); a += 2; break;
            case 3: arg[n] = (UNS64)(INT64)(int32_t)jit_ld32(a); a += 4; break;
            case 4: arg[n] = (UNS64)jit_ld32(a) | (UNS64)jit_ld32(a + 4) << 32; a += 8; break;
            case 5: arg[n] = (UNS64)(INT64)(int8_t)BYTE(a); a += 1; break;
            case 6: arg[n] = a + (UNS64)(INT64)(int8_t)BYTE(a); a += 1; break;
            case 7: arg[n] = a + (UNS64)(INT64)(int16_t)LD16(a); a += 2; break;
            default: return 0;
            }
#if JITX
            if (jit_ops[L].opnd >= 6 && arg[n] > far) far = arg[n];
            if (!end && jit_ends(L) && a > far) { n++; end = a; break; }   /* the end: an EXIT no branch reaches past */
#endif
        }
    }
    if (a != end) return 0;
    at[n] = end;
#if JITX
    {   int d = 0;                      /* the return stack in order: never below the entry, at it at every EXIT */
        for (i = 0; i < n; i++) {
            if (opl[i] == 0xFFFF) continue;
            for (j = 0; j < jit_ops[opl[i]].n; j++) {
                int s = jit_ops[opl[i]].st[j];
                if (s == S_TOR) d++;
                else if (s == S_FROMR) { if (!d) return 0; d--; }
                else if (s == S_RFETCH) { if (!d) return 0; }
                else if (s == S_EXIT && d) return 0;
            }
        }
    }
#endif
    for (i = 0; i < n; i++) {           /* callees first: native, or no translation */
        uint32_t f;
        if (opl[i] != 0xFFFF || arg[i] == w) continue;
        if (BYTE(arg[i]) == JIT_CODE) {
            f = jit_ld32(arg[i] + 1);
            if (f & 0x80000000u) f = jit_word(arg[i], depth + 1);
        }
#if JITX
        else if (BYTE(arg[i]) == JIT_DOVAR) {         /* a variable: its address, a literal */
            arg[i] = (arg[i] + 5 + 7) & ~(UNS64)7; opl[i] = 0xFFFD; continue;
        }
#if JITINL
        else if (jit_inl1(arg[i], &opl[i], &arg[i])) continue;     /* one operation: inline */
#endif
        else {                                      /* a word without the header: translated once */
            uint32_t *k = jit_kslot(arg[i]);
            if (!k) return 0;
            if (*k & 0x80000000u) { *k = 1; *k = jit_body(arg[i], arg[i], 0, depth + 1); }
            f = *k;
        }
#else
        else return 0;
#endif
        if (f < 2) return 0;
        arg[i] = (UNS64)(uintptr_t)(jit_mem + f); opl[i] = 0xFFFE;
    }
    for (i = 0; i < n; i++) {           /* sizes, and every stencil usable */
        nat[i] = size;
#if JITX
        if (opl[i] == 0xFFFD) { if (!jit_usable(S_LIT)) return 0; size += (uint32_t)jit_len(S_LIT); continue; }
#endif
#if JITTAIL
        if (opl[i] >= 0xFFFE) {
            int c = (tl[i] = (unsigned char)jit_tail(i, n, opl, arg, at)) ? S_BRANCH : S_CALL;
            if (!jit_usable(c)) return 0;
            size += (uint32_t)jit_len(c); continue;
        }
#else
        if (opl[i] >= 0xFFFE) { if (!jit_usable(S_CALL)) return 0; size += (uint32_t)jit_len(S_CALL); continue; }
#endif
        for (j = 0; j < jit_ops[opl[i]].n; j++) {
            int s = jit_ops[opl[i]].st[j];
            if (!jit_usable(s) || (jit_st[s].njump && jit_ops[opl[i]].opnd < 6)) return 0;
            size += (uint32_t)jit_len(s);
        }
    }
    nat[n] = size;
    off = (jit_used + 15) & ~15u;
    if (off + size > JIT_MEM) return 0;
    for (i = 0; i < n; i++) {           /* copy and patch */
        unsigned char *p = jit_mem + off + nat[i];
        const struct jit_op *o;
        UNS64 jt = 0;
        int lit = 1;
#if JITX
        if (opl[i] == 0xFFFD) { jit_put(p, S_LIT, arg[i], 0, 0); continue; }
#endif
        if (opl[i] >= 0xFFFE) {
#if JITTAIL
            UNS64 to = opl[i] == 0xFFFF ? (UNS64)(uintptr_t)(jit_mem + off) : arg[i];
            if (tl[i]) jit_put(p, S_BRANCH, 0, to, 0);      /* a tail call: a jump */
            else jit_put(p, S_CALL, 0, 0, to);
#else
            jit_put(p, S_CALL, 0, 0, opl[i] == 0xFFFF ? (UNS64)(uintptr_t)(jit_mem + off) : arg[i]);
#endif
            continue;
        }
        o = &jit_ops[opl[i]];
        if (o->opnd >= 6) {             /* a branch: to one of this word's operations */
            for (j = 0; j < n && at[j] != arg[i]; j++) ;
            if (j == n) return 0;
            jt = (UNS64)(uintptr_t)(jit_mem + off + nat[j]);
        }
        for (j = 0; j < o->n; j++) {    /* the operand's value fills the first literal hole; k the rest */
            int s = o->st[j];
            UNS64 v = (UNS64)(INT64)o->k;
            if (jit_st[s].imm >= 0 && lit && o->opnd >= 1 && o->opnd <= 5) { v = arg[i]; lit = 0; }
            p = jit_put(p, s, v, jt, 0);
        }
    }
#if PROFILE && JIT_PRICE
    for (i = 0; i < n; i++)
        JITPRICE(w, at[i], opl[i], (opl[i] < 0xFFFD && jit_ops[opl[i]].opnd >= 6) ? arg[i] : 0);
#endif
    jit_used = off + size;
    return off;
}
#endif

#ifdef JIT_SCAN_MAIN
/* tools/jit-check.sh: how this compiler shaped every stencil */
#include <stdio.h>
int main(void) {
    static const char *nm[S_N + 1] = { "next", "jump", "call", "lit", "dup", "drop", "swap", "over", "rot",
        "plus", "addi", "eq", "gt", "lt", "xor", "and", "negate", "0branch", "branch", "call", "exit",
        "addi32", "dup_gti_br", "tor", "fromr", "rfetch", "fetch", "store", "cfetch", "cstore", "or",
        "ult", "lshift", "rshift", "interp", "do", "qdo", "loop", "ploop", "i", "j", "unloop", "leave", "pick",
#if JITX
        "fill",
#endif
#if JITINL
        "dplus",
#endif
    };
    int i;
    jit_scan();
    for (i = S_LIT; i < S_N; i++)
        printf("%-10s len %3d  imm %3d imm32 %3d rp %3d  next %d jump %d call %d  tail %d\n", nm[i],
               jit_st[i].len, jit_st[i].imm, jit_st[i].imm32, jit_st[i].rp,
               jit_st[i].nnext, jit_st[i].njump, jit_st[i].ncall, jit_st[i].tailnext);
    return 0;
}
#endif
