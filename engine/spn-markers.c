/*  spn-markers.c - the three SPN marker functions.
 *
 *  Their ADDRESSES are what matter: a stencil's reference to one of them
 *  is how forth/spn.4 finds a hole. They live in their own file so the
 *  compiler, building the stencils, cannot see these bodies - see the
 *  comment in spn-stencils.c. Never executed; each body differs so no
 *  toolchain can fold two of them onto one address.  */
#include <stdint.h>
#include <stdlib.h>
#include "spn-abi.h"
spn_st spn_next(cell *sp, cell tos) { (void)sp; (void)tos; abort(); }
spn_st spn_jump(cell *sp, cell tos) { (void)sp; (void)tos; exit(97); }
spn_st spn_call(cell *sp, cell tos) { (void)sp; (void)tos; exit(98); }
