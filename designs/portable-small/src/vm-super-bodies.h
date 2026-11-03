LS_0: /* DUP >R */
     /* dup     */ PUSH(DS1); goto LSB_0;
LSB_0:
     /* >r      */ RPUSH(DS0); dsp += CELL_BYTES; NEXT();
LS_1: /* C! R> */
  /* c!      */ BYTE(DS0) = (UNS8)DS1; dsp += 2 * CELL_BYTES; goto LSB_1;
LSB_1:
   /* r>      */ PUSH(RS); rp += CELL_BYTES; NEXT();
LS_2: /* >R C! */
     /* >r      */ RPUSH(DS0); dsp += CELL_BYTES; goto LSB_2;
LSB_2:
  /* c!      */ BYTE(DS0) = (UNS8)DS1; dsp += 2 * CELL_BYTES; NEXT();
LS_3: /* ROT DUP */
     /* rot     */ t = DS2; DS2 = DS1; DS1 = DS0; DS0 = t; goto LSB_3;
LSB_3:
     /* dup     */ PUSH(DS1); NEXT();
LS_4: /* @ + */
   /* @       */ DS0 = CELL(DS0); goto LSB_4;
LSB_4:
    /* +       */ DS1 += DS0; dsp += CELL_BYTES; NEXT();
