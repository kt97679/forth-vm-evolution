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
