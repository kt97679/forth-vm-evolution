LX_lit: PUSHT(OPND16(ip)); ip += 2; EXITNEXT();
LX_cstore: BYTE(tos) = (UNS8)NOS; tos = CELL(dsp + CELL_BYTES); dsp += 2 * CELL_BYTES; EXITNEXT();
LX_ugt: tos = -(UNS64)(NOS < tos); dsp += CELL_BYTES; EXITNEXT();
