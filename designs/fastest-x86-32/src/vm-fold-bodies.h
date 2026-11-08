LX_lit: PUSHT(OPND16(ip)); ip += 2; EXITNEXT();
LX_drop: POPT(); EXITNEXT();
LX_cstore: BYTE(tos) = (UNS8)NOS; tos = CELL(dsp + CELL_BYTES); dsp += 2 * CELL_BYTES; EXITNEXT();
LX_plus: tos += NOS; dsp += CELL_BYTES; EXITNEXT();
