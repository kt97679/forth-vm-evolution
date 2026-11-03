LS_0: /* + C@ */
    /* +       */ DS1 += DS0; dsp += CELL_BYTES; goto LSB_0;
LSB_0:
  /* C@      */ DS0 = BYTE(DS0); NEXT();
