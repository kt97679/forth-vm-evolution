LS_0: /* SWAP R> */
    /* swap    */ t = DS0; DS0 = DS1; DS1 = t; goto LSB_0;
LSB_0:
   /* r>      */ PUSH(RS); rp += CELL_BYTES; NEXT();
