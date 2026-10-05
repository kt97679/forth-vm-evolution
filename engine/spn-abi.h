/*
 *  spn-abi.h - the native convention SPN's stencils, markers and engine
 *  share (Iteration 30: x86-64 and 32-bit ARM).
 *
 *  THE STATE (sp, tos) travels in registers both ways: in as the first two
 *  arguments, out as the return value. On x86-64 a two-word struct does
 *  that - rdi, rsi in; rax, rdx out. On 32-bit ARM a struct that size
 *  would come back through memory, so the state is one 64-bit value: r0
 *  and r1 in, r0 and r1 out - sp in the low word, tos in the high.
 *
 *  A cell is a pointer's size: 8 bytes on x86-64, 4 on 32-bit ARM - as the
 *  interpreter's own cells (UNS64 in spn.c).
 */
#ifndef SPN_ABI_H
#define SPN_ABI_H
#include <stdint.h>
typedef intptr_t cell;
typedef uintptr_t ucell;
#if defined(__x86_64__)
typedef struct { cell *sp; cell tos; } spn_st;
#define SPN_ST(s, t)  ((spn_st){ (s), (t) })
#define SPN_SP(r)     ((r).sp)
#define SPN_TOS(r)    ((r).tos)
#elif defined(__arm__)
typedef uint64_t spn_st;
#define SPN_ST(s, t)  ((uint64_t)(uint32_t)(uintptr_t)(s) | (uint64_t)(uint32_t)(t) << 32)
#define SPN_SP(r)     ((cell *)(uintptr_t)(uint32_t)(r))
#define SPN_TOS(r)    ((cell)(int32_t)(uint32_t)((r) >> 32))
#else
#error "SPN knows x86-64 and 32-bit ARM"
#endif
typedef spn_st (*spn_fn)(cell *sp, cell tos);
#endif
