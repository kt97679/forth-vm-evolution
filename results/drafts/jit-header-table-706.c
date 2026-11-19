#include <stdint.h>
/* Mechanism 9, variant V1 (Iteration 706, priced only): the native offset of a word compiled at run time kept beside the
   JIT's code instead of in a 4-byte field after the JIT opcode - open addressing, the key the word's offset from cbase
   (never 0: the image starts with the kernel). 1024 slots: brainless lays 641 definitions, the five 175. */
#define JT_BITS 10
static uint32_t jt_k[1 << JT_BITS], jt_v[1 << JT_BITS];
#define JT_H(w) (((w) * 2654435761u) >> (32 - JT_BITS))
__attribute__((noinline)) void jt_put(uint32_t w, uint32_t off) {
    uint32_t h = JT_H(w);
    while (jt_k[h] && jt_k[h] != w) h = (h + 1) & ((1u << JT_BITS) - 1);
    jt_k[h] = w; jt_v[h] = off;
}
__attribute__((noinline)) uint32_t jt_get(uint32_t w) {
    uint32_t h = JT_H(w);
    for (;;) { uint32_t k = jt_k[h]; if (k == w) return jt_v[h]; if (!k) return 0x80000000u; h = (h + 1) & ((1u << JT_BITS) - 1); }
}
