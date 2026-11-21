LX_drop: POPT(); EXITNEXT();
LX_ugt: tos = -(UNS64)(NOS < tos); dsp += CELL_BYTES; EXITNEXT();
LX_plus: tos += NOS; dsp += CELL_BYTES; EXITNEXT();
