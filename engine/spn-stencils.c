/*
 *  spn-stencils.c - SPN: Stencil-Patched Native.
 *
 *  Every function here is a STENCIL: one Forth operation written as an
 *  ordinary C function. They are never called. The Forth side reads their
 *  machine code out of this binary, copies it back to back into executable
 *  memory, and patches the holes. See forth/spn.4.
 *
 *  THE STATE. A stencil takes the data stack as (sp, tos): tos is the top
 *  item, sp points at the second. Under the calling convention both arrive
 *  in registers and leave in registers, so the top of stack is register-
 *  cached across the whole native sequence with no allocator anywhere.
 *
 *  THE HOLES. A stencil marks what the patcher must fill in by referring
 *  to one of four things, and the Forth side finds each reference exactly
 *  rather than by guessing:
 *
 *    spn_next(...)   a tail call - "continue with the next operation".
 *                    Found as a 32-bit relative jump whose target is
 *                    exactly &spn_next. Retargeted to the next stencil,
 *                    or dropped when the next stencil follows directly.
 *    spn_jump(...)   a branch target. Same test against &spn_jump.
 *    spn_call(...)   a call to another native word. Same test.
 *    SPN_IMM         a literal. Emitted as an 8-byte immediate, found by
 *                    its value.
 *
 *  A stencil that does not have the expected shape when the Forth side
 *  inspects it is simply not used, so an unexpected compiler makes SPN
 *  slower, never wrong.
 *
 *  RULES for writing a stencil: no calls except through the four markers,
 *  no static data, nothing PC-relative - the code is moved.
 */
#include <stdint.h>

typedef int64_t cell;
typedef struct { cell *sp; cell tos; } spn_st;     /* returned in rax:rdx */

#define SPN_IMM_VALUE 0x5ea1ed5ea1ed5ea1LL
/* A 32-bit hole, for when the literal fits. The compiler folds it into
   the instruction itself - add $imm32, cmp $imm32 - one instruction where
   the 64-bit hole needs a load and an operation. Chosen so its bytes do
   not occur inside the 64-bit marker's. */
#define IMM32 0x3c1a5e77L
#define IMM() ({ cell _v; __asm__("movabs %1, %0" : "=r"(_v) : "i"(SPN_IMM_VALUE)); _v; })

/* The markers. Only DECLARED here, and defined in spn-markers.c. That is
   deliberate: if the compiler can see a marker's body it learns the
   marker never returns, clones it, strips its arguments and turns the tail
   jumps into calls - every one of which breaks the stencil. Declared
   extern, a marker is an opaque function and each call to it compiles to
   the plain relative jump or call the patcher expects. */
extern spn_st spn_next(cell *sp, cell tos);
extern spn_st spn_jump(cell *sp, cell tos);
extern spn_st spn_call(cell *sp, cell tos);

#define S(name) __attribute__((noinline, used)) spn_st name(cell *sp, cell tos)
#define GO(sp, tos) return spn_next(sp, tos)

S(st_lit)   { *--sp = tos; GO(sp, IMM()); }
S(st_dup)   { *--sp = tos; GO(sp, tos); }
S(st_drop)  { GO(sp + 1, *sp); }
S(st_swap)  { cell t = *sp; *sp = tos; GO(sp, t); }
S(st_over)  { cell t = *sp; *--sp = tos; GO(sp, t); }
S(st_rot)   { cell a = sp[1], b = sp[0]; sp[1] = b; sp[0] = tos; GO(sp, a); }
S(st_plus)  { GO(sp + 1, tos + *sp); }
S(st_addi)  { GO(sp, tos + IMM()); }
S(st_eq)    { GO(sp + 1, -(*sp == tos)); }
S(st_gt)    { GO(sp + 1, -(*sp > tos)); }
S(st_lt)    { GO(sp + 1, -(*sp < tos)); }
S(st_xor)   { GO(sp + 1, tos ^ *sp); }
S(st_and)   { GO(sp + 1, tos & *sp); }
S(st_negate){ GO(sp, -tos); }

S(st_addi32) { GO(sp, tos + IMM32); }

/* DUP n < IF, fused. IF jumps when the flag is FALSE - when NOT tos < n,
   which is tos > n-1 - so the translator patches in n-1. Written as a
   strict > on purpose: given tos >= C the compiler emits cmp $(C-1),
   moving the constant, and the hole would no longer be found. The
   comparison, the branch and the DUP that feeds it become one cmp and
   one conditional jump, with nothing written to the stack. */
S(st_dup_gti_br) { if (tos > IMM32) return spn_jump(sp, tos); GO(sp, tos); }

/* ?BRANCH: take the flag, then either fall through or jump. */
S(st_0branch) {
    cell f = tos; tos = *sp++;
    if (f == 0) return spn_jump(sp, tos);
    GO(sp, tos);
}
S(st_branch) { return spn_jump(sp, tos); }

/* A call to another native word, which hands back the new stack state. */
S(st_call)  { spn_st r = spn_call(sp, tos); GO(r.sp, r.tos); }

/* EXIT: leave the native word, returning the state to the caller. */
__attribute__((noinline, used)) spn_st st_exit(cell *sp, cell tos)
{ spn_st r = { sp, tos }; return r; }

/* The table the Forth side reads. Order matters: SPN-TABLE hands it over
   as-is, and forth/spn.4 names the entries by position. */
const void *const spn_table[] = {
    (const void *)spn_next, (const void *)spn_jump, (const void *)spn_call,
    (const void *)st_lit, (const void *)st_dup, (const void *)st_drop,
    (const void *)st_swap, (const void *)st_over, (const void *)st_rot,
    (const void *)st_plus, (const void *)st_addi, (const void *)st_eq,
    (const void *)st_gt, (const void *)st_lt, (const void *)st_xor,
    (const void *)st_and, (const void *)st_negate, (const void *)st_0branch,
    (const void *)st_branch, (const void *)st_call, (const void *)st_exit,
    (const void *)st_addi32, (const void *)st_dup_gti_br,
};
const int spn_table_len = sizeof spn_table / sizeof spn_table[0];
