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
#if JITHELP
       S_CALLC,                                  /* Iteration 344: the gene jithelp */
#endif
#if JITMUL
       S_UMSTAR, S_UMMOD,                        /* Iteration 472: the gene jitmul */
       S_SPFETCH, S_ALIGNED,                     /* Iteration 484: jitmul's too */
#endif
#if JITEXEC
       S_EXECUTE, S_CALLX,                       /* Iterations 476, 486: the gene jitexec */
#endif
       S_N };                                    /* spn_table's order, the first 44 (45 with jitx) */
#if JITK
#include "jitk-map.h"                            /* Iteration 259, the gene jitk: tools/gen-jitk.py's */
#define JIT_NST (S_N + JITK_N)                   /* the variants after the base stencils, spn_ktable's order */
#else
#define JIT_NST S_N
#endif

#define JIT_IMM64 0x5ea1ed5ea1ed5ea1ULL         /* spn-stencils.c's SPN_IMM_VALUE */
#define JIT_FN64 0x6ea1ed5ea1ed5e66ULL          /* spn-stencils.c's SPN_FN_VALUE: a helper's address (jithelp) */
#define JIT_RP64  0x7ea1ed5ea1ed5e77ULL         /* SPN_RP_VALUE */
#define JIT_IMM32 0x3c1a5e77U                   /* IMM32 */

#if JITMUL
#define JIT_TH64 0x3ea1ed5ea1ed5e33ULL         /* Iteration 475: spn-stencils.c's SPN_TH_VALUE, the throw helper's hole */
#endif
#if JITEXEC
#define JIT_EX64 0x2ea1ed5ea1ed5e22ULL         /* Iteration 476: SPN_EX_VALUE, EXECUTE's helper's hole */
#endif
struct jit_st {             /* a stencil as read: offsets into its body, -1 for none */
    const unsigned char *src;
    int len, imm, imm32, rp, tailnext;          /* tailnext: the body ends "jmp NEXT" - dropped */
#if JITMUL
    int th;                                     /* Iteration 475: the throw helper's hole, or -1 */
#endif
#if JITEXEC
    int ex;                                     /* Iteration 476: EXECUTE's helper's hole, or -1 */
#endif
    int nnext, njump, ncall;                    /* how many holes of each */
#if JITHELP
    int fn;                                     /* Iteration 344: the function hole's offset, or -1 */
#endif
};
static struct jit_st jit_st[JIT_NST];

static int32_t jit_rel32(const unsigned char *p) { int32_t v; memcpy(&v, p, 4); return v; }
static int jit_relto(const unsigned char *p, const void *t) { return p + 4 + jit_rel32(p) == (const unsigned char *)t; }

/* Iteration 129: a stencil is read up to the next table function, or this
   far. 64 cut (+LOOP)'s stencil (87 bytes since Iteration 125's rule) before
   either exit, and (?DO)'s (76) after its fall-through, before its skip -
   neither was mapped until the gene jitloop, which reads further. */
/* Iteration 312: 160 in every build - jitloop-less builds read 64, and seed 52 found a design
   whose (LOOP) stencil was 72 bytes there: read to its fall-through, its loop-back missed,
   copied short, a segmentation fault on the corpus's first loop. The end is the last jump to
   NEXT or JUMP, which only stencils make, and the next table function still bounds a scan. */
#define JIT_SCAN_MAX 160
static const unsigned char *jit_addr(int i) {
#if JITK
    if (i >= S_N) return (const unsigned char *)spn_ktable[i - S_N];
#endif
    return (const unsigned char *)spn_table[i];
}
#if JITRET && defined(__x86_64__)
/*  Iteration 404, the gene jitret: EXIT leaves a native word by a pop and an indirect jmp, not ret. A ret
 *  is predicted by the return predictor, a stack of the last 32 or so calls: recursion deeper than that -
 *  the JIT's ackermann nests past 250 - mispredicts every return beyond it. An indirect jmp is predicted as
 *  any jump is, by the history of its targets. rcx is free at a return: the state comes back in rax and
 *  rdx, and no caller keeps anything in rcx across a call. EXIT's stencil (mov, mov, ret) is copied with
 *  its ret made pop %rcx; jmp *%rcx. Correct where ret is - the same address, the same stack pointer.  */
static unsigned char jit_exit_jmp[32];
#endif
static void jit_scan(void) {
    int i, k;
    for (i = S_LIT; i < JIT_NST; i++) {
        struct jit_st *s = &jit_st[i];
        const unsigned char *a0, *a, *hi, *end = 0, *p;
        if (i < S_N && i >= spn_table_len) continue;
        a0 = a = jit_addr(i); hi = a + JIT_SCAN_MAX;
        s->len = -1;
        if (a[0] == 0xF3 && a[1] == 0x0F && a[2] == 0x1E && a[3] == 0xFA) a += 4;     /* endbr64 */
        for (k = 0; k < spn_table_len; k++) {
            const unsigned char *e = spn_table[k];
            if (e > a0 && e < hi) hi = e;
        }
#if JITK
        for (k = 0; k < spn_ktable_len; k++) {          /* a variant may follow a base stencil */
            const unsigned char *e = spn_ktable[k];
            if (e > a0 && e < hi) hi = e;
        }
#endif
        if (i == S_EXIT) { for (p = a; p < hi; p++) if (*p == 0xC3) { end = p + 1; break; } }
        else for (p = a; p + 5 <= hi; p++)
            if (*p == 0xE9 && (jit_relto(p + 1, spn_table[J_NEXT]) || jit_relto(p + 1, spn_table[J_JUMP]))) end = p + 5;
        if (!end) continue;
        s->src = a; s->len = (int)(end - a); s->imm = s->imm32 = s->rp = -1;
#if JITMUL
        s->th = -1;
#endif
#if JITEXEC
        s->ex = -1;
#endif
#if JITHELP
        s->fn = -1;
#endif
        s->nnext = s->njump = s->ncall = 0;
        for (p = a; p < end; p++) {
            uint64_t v; uint32_t w;
            if (p + 8 <= end) { memcpy(&v, p, 8); if (v == JIT_IMM64) s->imm = (int)(p - a); if (v == JIT_RP64) s->rp = (int)(p - a);
#if JITMUL
                if (v == JIT_TH64) s->th = (int)(p - a);
#endif
#if JITEXEC
                if (v == JIT_EX64) s->ex = (int)(p - a);
#endif
#if JITHELP
                if (v == JIT_FN64) s->fn = (int)(p - a);
#endif
            }
            if (p + 4 <= end) {
                memcpy(&w, p, 4); if (w == JIT_IMM32) s->imm32 = (int)(p - a);
                if (jit_relto(p, spn_table[J_NEXT])) s->nnext++;
                if (jit_relto(p, spn_table[J_JUMP])) s->njump++;
                if (jit_relto(p, spn_table[J_CALL])) s->ncall++;
            }
        }
        s->tailnext = end - 5 >= a && end[-5] == 0xE9 && jit_relto(end - 4, spn_table[J_NEXT]);
#if JITRET && defined(__x86_64__)
        if (i == S_EXIT && s->len >= 1 && s->len + 2 <= (int)sizeof jit_exit_jmp && s->src[s->len - 1] == 0xC3) {
            memcpy(jit_exit_jmp, s->src, (size_t)s->len - 1);
            memcpy(jit_exit_jmp + s->len - 1, "\x59\xFF\xE1", 3);           /* pop %rcx; jmp *%rcx */
            s->src = jit_exit_jmp; s->len += 2;
        }
#endif
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
#if JITHELP
struct jit_op { unsigned char ok, n, opnd; signed char k; unsigned char st[5]; void *fn; };
/* Iteration 344, the gene jithelp: the C primitives the outer interpreter stops at, as functions
   with the stencils' signature - called from native code through st_callc. Each the handler's own
   work (vm-lab.c), on the stencils' stack: tos in a register, sp[0] the item below. */
#include "spn-abi.h"
static spn_st h_place(cell *sp, cell tos) {            /* PLACE ( s n d -- ): vm-lab.c L_x_place */
    unsigned char *d = (unsigned char *)(uintptr_t)tos; ucell n = (ucell)sp[0];
    const unsigned char *s = (const unsigned char *)(uintptr_t)sp[1];
    *d++ = (unsigned char)n; while (n--) *d++ = *s++;
    return SPN_ST(sp + 3, sp[2]);
}
static spn_st h_parse(cell *sp, cell tos) {            /* (PARSE) ( a u c -- s len adv ): vm-lab.c L_x_parse */
    ucell c = (ucell)tos, u = (ucell)sp[0];
    const unsigned char *a = (const unsigned char *)(uintptr_t)sp[1], *p = a, *s;
    if (c == 32) {                                      /* a space: any control character too */
        while (u && *p <= 32) { p++; u--; } s = p;
        while (u && *p > 32) { p++; u--; }
    } else {
        while (u && (ucell)*p == c) { p++; u--; } s = p;
        while (u && (ucell)*p != c) { p++; u--; }
    }
    sp[1] = (cell)(uintptr_t)s; sp[0] = (cell)(p - s);
    return SPN_ST(sp, (cell)((p - a) + (u ? 1 : 0)));
}
#else
struct jit_op { unsigned char ok, n, opnd; signed char k; unsigned char st[5]; };
#endif
/* Iteration 344: an operand that fills the first literal hole - kinds 1-5, and with jitvar the slot
   kinds 8 and 9 (without them vf's literal took k, 0: a fetch from 0 - latent while no word with vf
   was translated). Without JITVAR the very expression it was. */
#if JITVAR
#define JIT_LITOPND(o) (((o)->opnd >= 1 && (o)->opnd <= 5) || (o)->opnd >= 8)
#else
/* the original tokens exactly - unparenthesized: a && b && (c && d) is another tree than a && b &&
   c && d, and GCC compiled three of seed 55's JIT designs differently from it */
#define JIT_LITOPND(o) o->opnd >= 1 && o->opnd <= 5
#endif
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
#if JITEXEC
static spn_st jit_exec(cell *sp, cell tos, cell xt, cell *ic);   /* Iteration 476: below, after jit_body; 481: its cache */
#define JIT_NIC 4096                    /* 481: EXECUTE's inline caches, three cells a site; the last shared when full */
static cell jit_ic[JIT_NIC][3]; static int jit_nic;
#endif
#if JITRE || JITEXEC   /* 476: jitexec uses jitre's way into the interpreter and back */
/*  Iteration 346, the gene jitre: native code calling bytecode (vm-lab.c's jit_interp) - a callee the
 *  JIT cannot translate is interpreted instead of refusing its caller. The interpreter leaves through
 *  a sentinel return address: [the JIT opcode][2], a "word" whose native code, at offset 2 (free:
 *  offsets below 16 hold nothing native), is a trampoline to jit_leave.  */
static spn_st jit_interp(cell *sp, cell tos, cell body);
static spn_st jit_leave(cell *sp, cell tos);
#define JIT_LEAVE_OFF 2
static UNS8 jit_sentinel[5];
#endif
static ucell jit_rp;                    /* the return stack while native code runs: IMM_RP */
#if JITMUL
/*  Iteration 475: the throw path. The interpreter enters native code through jit_call, which keeps a return
 *  point (__builtin_setjmp - an engine links no C library, as jit_interp's); UM/MOD's stencil, at a zero divisor,
 *  calls jit_throw0, which longjmps there with the stack; the interpreter then does what L_umdiv does: -10 where
 *  the divisor was, and THROW. The native frames are dropped with the C stack; the return stack is jit_rp's.  */
static void **jit_tb; static cell *jit_tsp;
static spn_st jit_throw0(cell *sp, cell tos) { (void)tos; jit_tsp = sp; __builtin_longjmp(jit_tb, 1); }
static int jit_call(uint32_t f, cell *sp, cell tos, spn_st *r) {
    void *tb[5]; void **prev = jit_tb; jit_tb = tb;
    if (__builtin_setjmp(tb)) { jit_tb = prev; return 1; }
    *r = ((spn_st (*)(cell *, cell))(void *)(jit_mem + f))(sp, tos);
    jit_tb = prev; return 0;
}
#endif
static UNS64 jit_cbase;                 /* the image base: calls are offsets from it */
#if JITLOG
/*  Iteration 340: why a word is left to the interpreter (lab/evolve/jitleft.py --why) - a build for
 *  the analysis only: each refusal written "R word address why" (image offsets) to the file JITLOG
 *  names. why: 1 an operation the decoder has no mapping for, 2 the return stack's order, 3 a
 *  stencil not usable, 4 a callee not translated (address: the callee), 5 the JIT's memory full;
 *  Iteration 471 (lab/evolve/jitapps.py): 6 longer than JIT_MAXOPS, and a fifth field - for why 1 the
 *  operation without stencils, jit_ops[]'s index (vm-jit-ops.h names it), else -1.  */
#include <stdio.h>
#include <stdlib.h>
static UNS64 jitlog_at; static int jitlog_why; static int jitlog_op = -1;    /* 471: the operation (jit_ops[]'s index) */
static void jitlog_note(int c, UNS64 a, UNS64 b, UNS64 v) {    /* scratch */
    static FILE *f; const char *p;
    if (!f && (p = getenv("JITLOG")) != NULL) f = fopen(p, "a");
    if (f) { int q_; fprintf(f, "%c %lx %lx %lx ", c, (unsigned long)(a - jit_cbase), (unsigned long)(b - jit_cbase), (unsigned long)v);
             for (q_ = 16; q_ > 0; q_--) { UNS8 ch_ = BYTE(a - q_); fputc(ch_ > 32 && ch_ < 127 ? ch_ : '.', f); } fputc('\n', f); fflush(f); }
}
static void jitlog_refused(UNS64 w) {
    static FILE *f; const char *p;
    if (!f && (p = getenv("JITLOG")) != NULL) f = fopen(p, "a");
    if (f) { int q_; fprintf(f, "R %lu %lu %d %d", (unsigned long)(w - jit_cbase), (unsigned long)(jitlog_at - jit_cbase), jitlog_why,
                     jitlog_why == 1 ? jitlog_op : -1);
             fprintf(f, " w:"); for (q_ = 0; q_ < 8; q_++) fprintf(f, "%02x", BYTE(w + q_));          /* 485: the bytes, for a puzzle */
             fprintf(f, " at:"); for (q_ = 0; q_ < 8; q_++) fprintf(f, "%02x", BYTE(jitlog_at + q_)); fprintf(f, "\n"); fflush(f); }
}
#endif

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
#if JITRE || JITEXEC
        if (state == 1) {                       /* movabs rax, jit_leave; jmp rax - and the sentinel */
            UNS8 *t_ = jit_mem + JIT_LEAVE_OFF; UNS64 a_ = (UNS64)(uintptr_t)jit_leave; uint32_t o_ = JIT_LEAVE_OFF;
            t_[0] = 0x48; t_[1] = 0xB8; memcpy(t_ + 2, &a_, 8); t_[10] = 0xFF; t_[11] = 0xE0;
            jit_sentinel[0] = (UNS8)JIT_CODE; memcpy(jit_sentinel + 1, &o_, 4);
        }
#endif
    }
    return state == 1;
}
/* A stencil the translator may use: read, and no call hole unless CALL. */
static int jit_usable(int s) {
    /* Iterations 129, 312: a stencil with two exits - on, and to its branch target - read
       without both holes would jump nowhere, so it is not used: slower, never wrong. Every
       build, every branching stencil - Iteration 129 checked (+LOOP) and (?DO) only, and
       only with jitloop, and a (LOOP) read short (seed 52) went through. */
    if ((s == S_0BRANCH || s == S_LOOP || s == S_PLOOP || s == S_QDO || s == S_DUP_GTI_BR)
        && (jit_st[s].nnext < 1 || jit_st[s].njump != 1)) return 0;
    if ((s == S_BRANCH || s == S_LEAVE) && jit_st[s].njump != 1) return 0;
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
#if JITHELP
    if (t->fn >= 0) {                                  /* a helper call: its value is the helper */
        UNS64 fv_ = val;
#if JITRE
        if (t->imm >= 0) fv_ = (UNS64)(uintptr_t)jit_interp;   /* 348: st_interp by its holes - a function and a literal (st_callc has only the first); by index it would miss JITK's variants */
#endif
        memcpy(dst + t->fn, &fv_, 8);
    }
#endif
    if (t->rp >= 0) { UNS64 v = (UNS64)(uintptr_t)&jit_rp; memcpy(dst + t->rp, &v, 8); }
#if JITMUL
    if (t->th >= 0) { UNS64 v = (UNS64)(uintptr_t)jit_throw0; memcpy(dst + t->th, &v, 8); }
#endif
#if JITEXEC
    if (t->ex >= 0) { UNS64 v = (UNS64)(uintptr_t)jit_exec; memcpy(dst + t->ex, &v, 8); }
#endif
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

/* Iteration 441: out of JITX's block - jitre (Iteration 346) calls it without jitx; three of seed 63's designs did not compile */
static inline int jit_ends(unsigned L) { const struct jit_op *o = &jit_ops[L]; return o->n && o->st[o->n - 1] == S_EXIT; }
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
#if JITEXEC
/* Iteration 476: a word whose body is >R then EXIT - the kernel's `: EXECUTE >R ;` (layout.py) - is EXECUTE */
static int jit_isexec(UNS64 a) {
    unsigned L; UNS8 b;
    if (BYTE(a) == JIT_CODE) a += 5;
    b = BYTE(a); if (T2_CALL(b)) return 0;
    L = jit_one[T2_ONEIX(b)]; a++; if (L == T2_ESC) { L = jit_esc[BYTE(a)]; a++; }
    if (L >= (unsigned)JIT_NOPS || !jit_ops[L].ok) return 0;
    if (jit_ops[L].n == 2 && jit_ops[L].st[0] == S_TOR && jit_ops[L].st[1] == S_EXIT) return 1;   /* >R;EXIT, fused */
    if (jit_ops[L].n != 1 || jit_ops[L].st[0] != S_TOR) return 0;
    b = BYTE(a); if (T2_CALL(b)) return 0;
    L = jit_one[T2_ONEIX(b)]; a++; if (L == T2_ESC) { L = jit_esc[BYTE(a)]; a++; }
    return L < (unsigned)JIT_NOPS && jit_ops[L].ok && jit_ops[L].n == 1 && jit_ops[L].st[0] == S_EXIT;
}
#endif
/* Translate the word whose JIT opcode is at w. The native offset, or 0. */
static uint32_t jit_word(UNS64 w, int depth) {
    UNS64 end = w + 5 + (jit_ld32(w + 1) & 0x7FFFFFFFu);
    uint32_t f;
    JITNOTE(w, end);
    jit_st32(w + 1, 0);                 /* meanwhile, and if it fails: not native */
    f = jit_body(w, w + 5, end, depth);
#if JITLOG
    if (!f) jitlog_refused(w);
    jitlog_note('T', w, w, f);
#endif
    if (f) jit_st32(w + 1, f);
    return f;
}
#if JITEXEC
/* Iteration 476: EXECUTE from native code - the token's word native when it is, translated now when it can be
   (a word with the JIT's header by jit_word, one without by its kslot, as a call's callee is), else run by the
   interpreter (jit_interp, jitre's: a sentinel return address, a longjmp back) - and the stack handed back. */
static spn_st jit_exec(cell *sp, cell tos, cell xt, cell *ic) {
    UNS64 w = (UNS64)xt; uint32_t f = 0;
    if (BYTE(w) == JIT_CODE) { f = jit_ld32(w + 1); if (f & 0x80000000u) f = jit_word(w, 0); }
    else if (BYTE(w) != JIT_DOVAR) { uint32_t *k = jit_kslot(w);
        if (k) { if (*k & 0x80000000u) { *k = 1; *k = jit_body(w, w, 0, 0); } f = *k; } }
    if (f > 1) {                        /* 481: native - this site's cache remembers it */
        ic[1] = 0; ic[0] = xt; ic[2] = (cell)jit_ld32(w + 1); ic[1] = (cell)(uintptr_t)(jit_mem + f);
        return ((spn_st (*)(cell *, cell))(void *)(jit_mem + f))(sp, tos);
    }
#if JITLOG
    {   static UNS64 tw_[256]; static unsigned long tc_[256]; int k_;     /* 481: interpreted targets, counted - a line at each power of 2 */
        for (k_ = 0; k_ < 256 && tw_[k_] && tw_[k_] != w; k_++) ;
        if (k_ < 256) { tw_[k_] = w; tc_[k_]++; if (!(tc_[k_] & (tc_[k_] - 1))) jitlog_note('X', w, w, tc_[k_]); } }
#endif
    return jit_interp(sp, tos, (cell)w);
}
#endif
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

#if JITK
/*  Iteration 259, the gene jitk: the top K cells in registers across the copied
 *  code (gen-jitk.py; results/price-jit-stack.md). jitk_cs is the cache state
 *  while an operation is planned: a base stencil with a variant for it becomes
 *  the variant (and the state it leaves); any other - control, calls, loops,
 *  exits - runs in state 1, after the canonicaliser. So does every branch
 *  target: the operation before it ends in state 1. Both the size pass and the
 *  copying pass plan each operation here, so they agree byte for byte. A plan
 *  entry is (stencil, which): which >= 0 the operation's own stencil number,
 *  -1 a canonicaliser, -2 the call.  */
static unsigned char jitk_tg[JIT_MAXOPS + 1];   /* operation i is a branch target */
static int jitk_cs;
static int jitk_canon(int st[], int wh[], int k) {
    if (jitk_cs == 1) return k;
    if (!jitk_canon1[jitk_cs]) return -1;
    st[k] = S_N + jitk_canon1[jitk_cs] - 1; wh[k] = -1; jitk_cs = 1;
    return k + 1;
}
static int jitk_op(int i, int n, const unsigned short *opl, const UNS64 *arg, const UNS64 *at, int st[], int wh[]) {
    int j, k = 0;
    struct jit_op lit_op = { 1, 1, 1, 0, { S_LIT, 0, 0, 0, 0 } };
    const struct jit_op *o = &lit_op;
    (void)arg; (void)at;
    if (opl[i] >= 0xFFFE) {                             /* a call: in state 1 */
        if ((k = jitk_canon(st, wh, 0)) < 0) return -1;
#if JITTAIL
        st[k] = jit_tail(i, n, opl, arg, at) ? S_BRANCH : S_CALL;
#else
        st[k] = S_CALL;
#endif
        wh[k++] = -2; jitk_cs = 1;
        return k;
    }
    if (opl[i] != 0xFFFD) o = &jit_ops[opl[i]];         /* else jitx's literal: S_LIT with its value */
    for (j = 0; j < o->n; j++) {
        int s = o->st[j], v = jitk_v1[s][jitk_cs];
        if (v && jit_usable(S_N + v - 1)) { st[k] = S_N + v - 1; wh[k++] = j; jitk_cs = jitk_vout[v - 1]; continue; }
        if ((k = jitk_canon(st, wh, k)) < 0) return -1;
        st[k] = s; wh[k++] = j; jitk_cs = 1;
    }
    if (i + 1 < n && jitk_tg[i + 1]) k = jitk_canon(st, wh, k);
    return k;
}
#endif

#if JITRE
/* Iteration 349: does the word at a read or pop the return stack below its own entry - its caller's
   return address (a (S") reading the string after its call)? Then its caller cannot be translated past
   the call: what follows the call is data. Read to its EXIT, an operation unknown, or 64 operations. */
static int jit_rtouch(UNS64 a) {
    int d = 0, n_, j;
    if (BYTE(a) == JIT_CODE) a += 5;
    for (n_ = 0; n_ < 64; n_++) {
        UNS8 b = BYTE(a);
        if (T2_CALL(b)) { a += (UNS64)T2_CALLW(b); continue; }
        {   unsigned L = jit_one[T2_ONEIX(b)]; a++;
            if (L == T2_ESC) { L = jit_esc[BYTE(a)]; a++; }
            if (L >= (unsigned)JIT_NOPS || !jit_ops[L].ok) return 1;     /* 350: unknown - it may read its caller's frame: refused, to be safe */
            for (j = 0; j < jit_ops[L].n; j++) {
                int s = jit_ops[L].st[j];
                if (s == S_TOR) d++;
                else if (s == S_FROMR || s == S_RFETCH) { if (!d) return 1; if (s == S_FROMR) d--; }
            }
            switch (jit_ops[L].opnd) { case 1: case 5: case 6: a += 1; break; case 2: case 7: a += 2; break;
                case 3: a += 4; break; case 4: a += 8; break; default: break; }
            if (jit_ends(L)) return 0;
        }
    }
    return 1;                           /* 350: no EXIT in 64 operations: not seen to be safe */
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
#if JITLOG
        jitlog_at = a; jitlog_why = 1; jitlog_op = -1;
#endif
#if JITDOES && JITX
        /*  Iteration 473, the gene jitdoes: a DOES> child - [DODOES][4-byte call of its DOES> code][pad][PFA] - is
         *  what the interpreter runs as the PFA pushed on the return stack and a jump to the DOES> code, whose first
         *  operation, R>, takes it back. Here: a literal of the PFA, then the DOES> code from after that R>, to its
         *  EXIT - the return stack never touched, so the code's own order holds (results/drafts/jitapps-471.md).  */
        if (n == 0 && JIT_DODOES >= 0 && JIT_FROMR >= 0 && b == (UNS8)JIT_DODOES && (a == w || a == w + 5)) {   /* 473: a child has
                                         no header, as a variable has none - reached as a callee, translated once (jit_kslot) */
            UNS64 t_ = ((UNS64)(BYTE(a + 1) & 0x3F) << 24) | ((UNS64)BYTE(a + 2) << 16) | ((UNS64)BYTE(a + 3) << 8) | BYTE(a + 4);
            UNS64 tail = jit_cbase + t_;
            at[0] = a; opl[0] = 0xFFFD; arg[0] = (a + 1 + 4 + CELL_BYTES - 1) & ~(UNS64)(CELL_BYTES - 1);
            if (BYTE(tail) == (UNS8)JIT_FROMR) { n = 1; a = tail + 1; }    /* the R> dropped: the PFA stays on the data stack */
            else {                      /* 484: R> fused with what follows (CONSTANT's, VALUE's DOES> @): the PFA pushed to the
                                           return stack as DODOES does, and the DOES> code from its start, that R> and all */
                static int l_tor = -2; int q_;
                if (l_tor == -2) { l_tor = -1; for (q_ = 0; q_ < (int)JIT_NOPS; q_++) if (jit_ops[q_].ok && jit_ops[q_].n == 1 && jit_ops[q_].st[0] == S_TOR) { l_tor = q_; break; } }
                if (l_tor < 0) return 0;
                at[1] = a + 1; opl[1] = (unsigned short)l_tor; arg[1] = 0; n = 2; a = tail;
            }
            end = 0; b = BYTE(a);
        }
#endif
#if JITLOG
        if (n >= JIT_MAXOPS) { jitlog_why = 6; return 0; }           /* 471: too long, told apart */
#else
        if (n >= JIT_MAXOPS) return 0;
#endif
        at[n] = a;
        if (T2_CALL(b)) {               /* a call of 2, 3 or 4 bytes (2 or 4: t2wide) */
            int wd = T2_CALLW(b); UNS64 t = b & 0x3F;
            for (i = 1; i < wd; i++) t = t << 8 | BYTE(a + i);
            arg[n] = jit_cbase + t; opl[n] = 0xFFFF; a += (UNS64)wd;
#if JITEXEC
            /* Iteration 485: (S") and (.") read the counted string after their call - a call native code cannot make
               (its return address is no bytecode), and decoded as code it was refused at the count byte (gc16's GC at
               ` ." HEAP FULL"`, every caller with it). Here: the string's address and length as literals, and for (.")
               TYPE through EXECUTE's helper; the decoding goes on after the string, aligned as the run-time words do.
               The added operations get addresses no branch can name.  */
            if (JIT_W_SQ >= 0 && JIT_W_DQ >= 0 && JIT_W_TYPE >= 0 &&
                (arg[n] == jit_cbase + (UNS64)JIT_W_SQ || arg[n] == jit_cbase + (UNS64)JIT_W_DQ)) {
                UNS64 s_ = a; unsigned c_ = BYTE(s_); int dq_ = arg[n] == jit_cbase + (UNS64)JIT_W_DQ;
                if (n + 4 >= JIT_MAXOPS) return 0;
                opl[n] = 0xFFFD; arg[n] = s_ + 1;
                n++; at[n] = ((UNS64)1 << 63) | (s_ + 1); opl[n] = 0xFFFD; arg[n] = c_;
                if (dq_) { n++; at[n] = ((UNS64)1 << 63) | (s_ + 2); opl[n] = 0xFFFD; arg[n] = jit_cbase + (UNS64)JIT_W_TYPE;
                           n++; at[n] = ((UNS64)1 << 63) | (s_ + 3); opl[n] = JIT_L_EXECUTE;
                           arg[n] = (UNS64)(uintptr_t)jit_ic[jit_nic < JIT_NIC - 1 ? jit_nic++ : JIT_NIC - 1]; }
                a = (s_ + 1 + c_ + CELL_BYTES - 1) & ~(UNS64)(CELL_BYTES - 1);
            }
#endif
        } else {
            unsigned L = jit_one[T2_ONEIX(b)];
            a++;
            if (L == T2_ESC) { L = jit_esc[BYTE(a)]; a++; }
#if JITLOG
            jitlog_op = (int)L;
#endif
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
#if JITVAR
            /* Iteration 342, the gene jitvar: a variable's slot - vf and vs (getstatic, putstatic) as
               a literal of the address, then @ or ! - the address the engine's SLOT() makes */
            case 8: arg[n] = jit_cbase + ((UNS64)LD16(a) << SCALE); a += 2; break;
            case 9: { UNS64 t_ = BYTE(a);       /* VARSLOT: two bytes, or three with the top bit */
                if (t_ & 0x80) { t_ = ((t_ & 0x7F) << 16) | ((UNS64)BYTE(a + 1) << 8) | BYTE(a + 2); a += 3; }
                else { t_ = (t_ << 8) | BYTE(a + 1); a += 2; }
                arg[n] = jit_cbase + (t_ << SCALE); } break;
#endif
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
#if JITX && JITCFA
    {   /* Iteration 482, the gene jitcfa: the same rule along the paths, not down the page - the depth before each
           operation (dv), a branch's target given the depth at the branch, the code after an unconditional jump or an
           EXIT starting again from the depth its target was given; a backward branch must meet the depth its loop's
           head had. fcp's evalLP: >R at the start, R> ... >R in one arm, R> and EXIT in another - balanced on every
           path, refused by the linear check below.  */
        signed char dv[JIT_MAXOPS + 1], dt[JIT_MAXOPS + 1]; int d = 0, live = 1, k;
        for (i = 0; i <= n; i++) dv[i] = dt[i] = -1;
        for (i = 0; i < n; i++) {
            if (dt[i] >= 0) { if (live && d != dt[i]) return 0; d = dt[i]; live = 1; }
            if (!live) continue;                  /* reached by no path yet: a later backward branch to it is refused */
            dv[i] = (signed char)d;
            if (opl[i] >= 0xFFFD) continue;
#if JITLOG
            jitlog_at = at[i]; jitlog_why = 2;
#endif
            {   const struct jit_op *o_ = &jit_ops[opl[i]]; int unc_ = 0;
                for (j = 0; j < o_->n; j++) {
                    int s = o_->st[j];
                    if (s == S_TOR) { if (d >= 100) return 0; d++; }
                    else if (s == S_FROMR) { if (!d) return 0; d--; }
                    else if (s == S_RFETCH) { if (!d) return 0; }
                    else if (s == S_EXIT) { if (d) return 0; unc_ = 1; }
                    else if (s == S_BRANCH || s == S_LEAVE) unc_ = 1;
                }
                if (o_->opnd >= 6) {                 /* a branch: its target is given this depth */
                    for (k = 0; k < n && at[k] != arg[i]; k++) ;
                    if (k == n) return 0;
                    if (k <= i) { if (dv[k] != d) return 0; }
                    else if (dt[k] >= 0) { if (dt[k] != d) return 0; }
                    else dt[k] = (signed char)d;
                }
                if (unc_) live = 0;
            }
        }
    }
#elif JITX
    {   int d = 0;                      /* the return stack in order: never below the entry, at it at every EXIT */
        for (i = 0; i < n; i++) {
            if (opl[i] >= 0xFFFD) continue;      /* 474: a call, or a literal - jitdoes's PFA, the first operation - no return-stack effect */
#if JITLOG
            jitlog_at = at[i]; jitlog_why = 2;
#endif
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
#if JITRE
        if (arg[i] < jit_cbase || arg[i] >= jit_cbase + ((UNS64)64 << 20)) return 0;   /* 350: a call to nowhere - the data after a refused callee, decoded */
#endif
#if JITEXEC
        if (jit_isexec(arg[i])) {                                         /* 476: a call of EXECUTE - its helper; 481: its cache */
            opl[i] = JIT_L_EXECUTE; arg[i] = (UNS64)(uintptr_t)jit_ic[jit_nic < JIT_NIC - 1 ? jit_nic++ : JIT_NIC - 1]; continue; }
#endif
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
            if (*k & 0x80000000u) { *k = 1; *k = jit_body(arg[i], arg[i], 0, depth + 1);
#if JITLOG
                if (!*k) jitlog_refused(arg[i]);
#endif
            }
            f = *k;
        }
#else
        else return 0;
#endif
#if JITLOG
        if (f < 2) { jitlog_at = arg[i]; jitlog_why = 4; }
        jitlog_note('C', w, arg[i], f);                 /* scratch: each callee's decision */
#endif
#if JITRE
        if (f < 2 && jit_rtouch(arg[i])) return 0;        /* 349: it pops its caller's return address - (S")'s inline data: refused, as before */
        if (f < 2) {                                      /* Iteration 346: interpreted, not refused - arg[i] its body */
            if (BYTE(arg[i]) == JIT_CODE) arg[i] += 5;      /* 347: past the header - entered at it, L_x_jit would repoint the "caller", the sentinel */
            opl[i] = JIT_L_INTERP; continue;
        }
#endif
#if JITEXEC
        if (f < 2) {                                        /* 486: a cold word left bytecode - called through the helper */
            static const long cold_[] = { JIT_W_COLD }; int c_;
            for (c_ = 0; c_ < (int)(sizeof cold_ / sizeof cold_[0]); c_++)
                if (cold_[c_] >= 0 && arg[i] == jit_cbase + (UNS64)cold_[c_]) break;
            if (c_ < (int)(sizeof cold_ / sizeof cold_[0])) {
                cell *ic_ = jit_ic[jit_nic < JIT_NIC - 1 ? jit_nic++ : JIT_NIC - 1];
                ic_[1] = 0; ic_[0] = (cell)arg[i]; ic_[2] = 0;
                opl[i] = JIT_L_CALLX; arg[i] = (UNS64)(uintptr_t)ic_; continue;
            }
        }
#endif
        if (f < 2) return 0;
        arg[i] = (UNS64)(uintptr_t)(jit_mem + f); opl[i] = 0xFFFE;
    }
#if JITK
    memset(jitk_tg, 0, (size_t)n + 1);  /* the branch targets: state 1 there */
    for (i = 0; i < n; i++)
        if (opl[i] < 0xFFFD && jit_ops[opl[i]].opnd >= 6) {
            for (j = 0; j < n && at[j] != arg[i]; j++) ;
            if (j < n) jitk_tg[j] = 1;
        }
    jitk_cs = 1;
#endif
    for (i = 0; i < n; i++) {           /* sizes, and every stencil usable */
        nat[i] = size;
#if JITLOG
        jitlog_at = at[i]; jitlog_why = 3;
#endif
#if JITK
        {
            int st_[16], wh_[16], m_ = jitk_op(i, n, opl, arg, at, st_, wh_), q_;
            if (m_ < 0) return 0;
            for (q_ = 0; q_ < m_; q_++) {
                int s = st_[q_];
                if (!jit_usable(s) || (wh_[q_] >= 0 && opl[i] < 0xFFFD && jit_st[s].njump && jit_ops[opl[i]].opnd < 6)) return 0;
                size += (uint32_t)jit_len(s);
            }
            continue;
        }
#endif
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
#if JITLOG
    if (off + size > JIT_MEM) { jitlog_at = w; jitlog_why = 5; }
#endif
    if (off + size > JIT_MEM) return 0;
#if JITK
    jitk_cs = 1;
#endif
    for (i = 0; i < n; i++) {           /* copy and patch */
        unsigned char *p = jit_mem + off + nat[i];
        const struct jit_op *o;
        UNS64 jt = 0;
        int lit = 1;
#if JITK
        {
            int st_[16], wh_[16], m_ = jitk_op(i, n, opl, arg, at, st_, wh_), q_;
            const struct jit_op *o_ = opl[i] < 0xFFFD ? &jit_ops[opl[i]] : 0;
            if (m_ < 0) return 0;
            if (o_ && o_->opnd >= 6) {              /* a branch: to one of this word's operations */
                for (j = 0; j < n && at[j] != arg[i]; j++) ;
                if (j == n) return 0;
                jt = (UNS64)(uintptr_t)(jit_mem + off + nat[j]);
            }
            for (q_ = 0; q_ < m_; q_++) {
                int s = st_[q_];
                if (wh_[q_] == -2) {                /* the call, or the tail call's jump */
                    UNS64 to = opl[i] == 0xFFFF ? (UNS64)(uintptr_t)(jit_mem + off) : arg[i];
                    p = s == S_CALL ? jit_put(p, S_CALL, 0, 0, to) : jit_put(p, S_BRANCH, 0, to, 0);
                } else if (wh_[q_] == -1) p = jit_put(p, s, 0, 0, 0);       /* a canonicaliser */
                else {
                    UNS64 v = o_ ? (UNS64)(INT64)o_->k : arg[i];               /* no o_: jitx's literal */
#if JITHELP
                    if (o_ && o_->fn) v = (UNS64)(uintptr_t)o_->fn;
#endif
                    if (o_ && jit_st[s].imm >= 0 && lit && JIT_LITOPND(o_)) { v = arg[i]; lit = 0; }
                    p = jit_put(p, s, v, jt, 0);
                }
            }
            (void)o;
            continue;
        }
#endif
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
#if JITHELP
            if (o->fn) v = (UNS64)(uintptr_t)o->fn;
#endif
            if (jit_st[s].imm >= 0 && lit && JIT_LITOPND(o)) { v = arg[i]; lit = 0; }
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
