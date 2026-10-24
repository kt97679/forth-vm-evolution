/* results/drafts/arm-cp-poc-512.c (Iteration 512) - the five answers to ask-arm-jit-511.md, tested.
   arm-linux-gnueabihf-gcc -O2 -marm -march=armv7-a -mfpu=neon -mfloat-abi=hard -fno-pic -fno-pie -no-pie
       -fno-stack-protector -static -o poc arm-cp-poc-512.c && qemu-arm ./poc     -> tos 42, depth 1
   (Ubuntu's GCC protects the stack by default: its canary load is a literal pool - -fno-stack-protector is needed.)
   A copy-and-patch round trip on ARMv7 A32: three stencils copied, two holes patched, the tail jumps dropped,
   (sp, tos) in r0:r1 in and out as a uint64_t, the code flushed and run - the answers' consolidated plan. */
#include <stdint.h>
#include <stdio.h>
#include <string.h>
#include <sys/mman.h>
typedef int32_t cell; typedef uint64_t st;
#define ST(s, t) ((uint64_t)(uint32_t)(uintptr_t)(s) | (uint64_t)(uint32_t)(t) << 32)
extern st next(cell *, cell);
__attribute__((noinline)) st s_lit(cell *sp, cell tos) { cell v; __asm__("movw %0, #0xed01\n\tmovt %0, #0x5ea1" : "=r"(v)); *--sp = tos; return next(sp, v); }
__attribute__((noinline)) st s_plus(cell *sp, cell tos) { return next(sp + 1, tos + *sp); }
__attribute__((noinline)) st s_end(cell *sp, cell tos) { return ST(sp, tos); }
__attribute__((noipa)) st next(cell *sp, cell tos) { return ST(sp, tos); }   /* the marker: opaque, never reached in copied code */
static int body(const uint32_t *f, int tail) {                   /* words up to the tail b next (dropped), or bx lr (kept) */
    for (int i = 0; i < 64; i++) {
        uint32_t w = f[i];
        if (tail && (w & 0x0F000000u) == 0x0A000000u) {            /* B: cond 1010 imm24 */
            int32_t off = (int32_t)(w << 8) >> 6;                  /* sign-extended imm24 * 4 */
            if ((uintptr_t)&f[i] + 8 + off == (uintptr_t)next) return i;
        }
        if (!tail && w == 0xE12FFF1Eu) return i + 1;               /* bx lr */
        if ((w & 0x0F7F0000u) == 0x051F0000u) return -1;           /* LDR Rt, [PC, #+-imm]: a literal pool - refused */
    }
    return -1;
}
static void patch(uint32_t *c, int n, uint32_t magic, uint32_t v) {   /* MOVW then MOVT, one register, the magic's halves */
    for (int i = 0; i + 1 < n; i++) {
        uint32_t a = c[i], b = c[i + 1];
        if ((a & 0x0FF00000u) == 0x03000000u && (b & 0x0FF00000u) == 0x03400000u && ((a >> 12) & 15) == ((b >> 12) & 15)
            && (((a >> 4) & 0xF000u) | (a & 0xFFFu)) == (magic & 0xFFFFu) && (((b >> 4) & 0xF000u) | (b & 0xFFFu)) == magic >> 16) {
            c[i] = (a & 0xFFF0F000u) | ((v & 0xF000u) << 4) | (v & 0xFFFu);
            c[i + 1] = (b & 0xFFF0F000u) | (((v >> 16) & 0xF000u) << 4) | ((v >> 16) & 0xFFFu);
            return;
        }
    }
}
int main(void) {
    uint32_t *m = mmap(0, 4096, PROT_READ | PROT_WRITE, MAP_PRIVATE | MAP_ANONYMOUS, -1, 0), *p = m;
    int nl = body((uint32_t *)s_lit, 1), np = body((uint32_t *)s_plus, 1), ne = body((uint32_t *)s_end, 0);
    printf("words: lit %d, plus %d, end %d\n", nl, np, ne);
    if (nl < 0 || np < 0 || ne < 0) return 1;
    memcpy(p, s_lit, 4 * nl); patch(p, nl, 0x5ea1ed01u, 40); p += nl;
    memcpy(p, s_lit, 4 * nl); patch(p, nl, 0x5ea1ed01u, 2); p += nl;
    memcpy(p, s_plus, 4 * np); p += np;
    memcpy(p, s_end, 4 * ne); p += ne;
    __builtin___clear_cache((char *)m, (char *)p);
    if (mprotect(m, 4096, PROT_READ | PROT_EXEC)) return 2;
    cell stack[16]; st r = ((st (*)(cell *, cell))(void *)m)(stack + 16, 0);
    printf("tos %d, depth %d\n", (cell)(r >> 32), (int)(stack + 16 - (cell *)(uintptr_t)(uint32_t)r));
    return 0;
}
