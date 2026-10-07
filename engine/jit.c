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
       S_N };                                    /* spn_table's order, the first 44 */

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

static void jit_scan(void) {
    int i, k;
    for (i = S_LIT; i < S_N && i < spn_table_len; i++) {
        struct jit_st *s = &jit_st[i];
        const unsigned char *a = spn_table[i], *hi = a + 64, *end = 0, *p;
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
static const unsigned short jit_one[64] = {
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
    for (wd = 2; wd <= 4; wd++) {
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
static void jit_dump(int fd) {
    char b[96];
    int i, k, m;
    for (k = 0; k < 64; k++)
        if (jit_one[k] < (unsigned)JIT_NOPS && jit_ops[jit_one[k]].ok) { m = snprintf(b, sizeof b, "S %d\n", k); write(fd, b, (size_t)m); }
    for (i = 0; i < jn_n; i++) {
        UNS64 w = jn_w[i], end = jn_end[i], a = w + 5;
        uint32_t f = jit_ld32(w + 1);
        m = snprintf(b, sizeof b, "J %llu %llu %u\n", (unsigned long long)(w - jit_cbase), (unsigned long long)(end - jit_cbase), f);
        write(fd, b, (size_t)m);
        while (f < 2 && a < end) {
            UNS8 c = BYTE(a);
            if (c >= 0x40) {
                int wd = c < 0x80 ? 2 : c < 0xC0 ? 3 : 4, j;
                UNS64 t = c & 0x3F;
                for (j = 1; j < wd; j++) t = t << 8 | BYTE(a + j);
                if (jit_cbase + t != w) {
                    m = snprintf(b, sizeof b, "B %llu c %llu\n", (unsigned long long)(w - jit_cbase), (unsigned long long)t); write(fd, b, (size_t)m); }
                a += (UNS64)wd;
            } else {
                unsigned L = jit_one[c];
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

/* Translate the word whose JIT opcode is at w. The native offset, or 0. */
static uint32_t jit_word(UNS64 w, int depth) {
    UNS64 at[JIT_MAXOPS + 1], arg[JIT_MAXOPS], end, a;
    uint32_t nat[JIT_MAXOPS + 1], size = 0, off;
    unsigned short opl[JIT_MAXOPS];     /* the logical operation; 0xFFFF a call to w, 0xFFFE a call resolved */
    int n = 0, i, j;
    end = w + 5 + (jit_ld32(w + 1) & 0x7FFFFFFFu);
    JITNOTE(w, end);
    jit_st32(w + 1, 0);                 /* meanwhile, and if it fails: not native */
    if (depth > 4 || !jit_init()) return 0;
    for (a = w + 5; a < end; n++) {     /* decode, as the engine does */
        UNS8 b = BYTE(a);
        if (n >= JIT_MAXOPS) return 0;
        at[n] = a;
        if (b >= 0x40) {                /* a call of 2, 3 or 4 bytes */
            int wd = b < 0x80 ? 2 : b < 0xC0 ? 3 : 4; UNS64 t = b & 0x3F;
            for (i = 1; i < wd; i++) t = t << 8 | BYTE(a + i);
            arg[n] = jit_cbase + t; opl[n] = 0xFFFF; a += (UNS64)wd;
        } else {
            unsigned L = jit_one[b];
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
        }
    }
    if (a != end) return 0;
    at[n] = end;
    for (i = 0; i < n; i++) {           /* callees first: native, or no translation */
        uint32_t f;
        if (opl[i] != 0xFFFF || arg[i] == w) continue;
        if (BYTE(arg[i]) != JIT_CODE) return 0;
        f = jit_ld32(arg[i] + 1);
        if (f & 0x80000000u) f = jit_word(arg[i], depth + 1);
        if (f < 2) return 0;
        arg[i] = (UNS64)(uintptr_t)(jit_mem + f); opl[i] = 0xFFFE;
    }
    for (i = 0; i < n; i++) {           /* sizes, and every stencil usable */
        nat[i] = size;
        if (opl[i] >= 0xFFFE) { if (!jit_usable(S_CALL)) return 0; size += (uint32_t)jit_len(S_CALL); continue; }
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
        if (opl[i] >= 0xFFFE) {
            jit_put(p, S_CALL, 0, 0, opl[i] == 0xFFFF ? (UNS64)(uintptr_t)(jit_mem + off) : arg[i]);
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
    jit_used = off + size;
    jit_st32(w + 1, off);
    return off;
}
#endif

#ifdef JIT_SCAN_MAIN
/* tools/jit-check.sh: how this compiler shaped every stencil */
#include <stdio.h>
int main(void) {
    static const char *nm[S_N] = { "next", "jump", "call", "lit", "dup", "drop", "swap", "over", "rot",
        "plus", "addi", "eq", "gt", "lt", "xor", "and", "negate", "0branch", "branch", "call", "exit",
        "addi32", "dup_gti_br", "tor", "fromr", "rfetch", "fetch", "store", "cfetch", "cstore", "or",
        "ult", "lshift", "rshift", "interp", "do", "qdo", "loop", "ploop", "i", "j", "unloop", "leave", "pick" };
    int i;
    jit_scan();
    for (i = S_LIT; i < S_N; i++)
        printf("%-10s len %3d  imm %3d imm32 %3d rp %3d  next %d jump %d call %d  tail %d\n", nm[i],
               jit_st[i].len, jit_st[i].imm, jit_st[i].imm32, jit_st[i].rp,
               jit_st[i].nnext, jit_st[i].njump, jit_st[i].ncall, jit_st[i].tailnext);
    return 0;
}
#endif
