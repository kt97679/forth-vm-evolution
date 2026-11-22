/* engine/data-layout.ld - the engine's writable data in a fixed layout (Iteration 734; results/drafts/early-games-713.md,
   the 8-bit games' hand-placed RAM, step 1). Given to GNU ld with -T: INSERT keeps the default script and adds three
   output sections to it. The engine is built with -fdata-sections, so every variable is a section of its own,
   .bss.NAME (a function's static: NAME, NAME.N or FUNCTION.NAME). In the order a start-up meets them:

     .data           as before - the initialized variables, on the file's last page
     .bss.hot        every small variable, from the next page on: the few hundred bytes a run touches on one page
                     with the tables after them. Not in the file page's tail: that page is the file's, and the first
                     write to it is a fault of its own (copy on write) - free only where .data is written anyway; the
                     least-memory role paid a fault for it (results/drafts/data-layout-734.txt)
     .bss.tab        the tables of 512 B to 2 KB a run touches (dispatch, the tag's maps, the JIT's per-word marks),
                     then the two buffers a run touches from their start: t_obuf (written from 0 at every output) and
                     the loader's heads (8 bytes a chain of its 32 KB) - so their used part continues the block
     .bss            whatever no pattern here names - empty on today's engines
     .bss.big        the other buffers of 4 KB and more, the stacks first; each touched only where it is used

   A section is placed by the first statement that names it, and the statements here come before the default
   script's, so .bss.big's and .bss.tab's names win over .bss.hot's catch-all. A buffer of 4 KB or more missing
   from the lists lands in .bss.hot and costs pages, not correctness: lab/evolve/data-layout-check.py lists
   each output section's members from the link map. Step 2 (the two stack tops on one page) is not here. */

SECTIONS
{
  .bss.big (NOLOAD) : ALIGN(4096)
  {
    *(.bss.stackmem)
    *(.bss.mem_dict)
    *(.bss.t_fbb .bss.g_altstack)
    *(.bss.jit_ic .bss.jit_st .bss.jit_k .bss.map .bss.map.* .bss.*.map)
    *(.bss.jn_w .bss.jn_end .bss.jp_w .bss.jp_at .bss.jp_t .bss.jp_l)
    *(.bss.buf .bss.buf.* .bss.*.buf .bss.dir .bss.dir.* .bss.*.dir)
    *(.bss.tw_ .bss.tw_.* .bss.*.tw_ .bss.tc_ .bss.tc_.* .bss.*.tc_)
    *(.bss.prof .bss.pair .bss.trip .bss.callc .bss.ipc .bss.rcnt .bss.rtgt .bss.tr_*)
  }
}
INSERT AFTER .bss;

SECTIONS
{
  .bss.tab (NOLOAD) :
  {
    *(.bss.dispatch .bss.dispatch.* .bss.*.dispatch)
    *(.bss.t2tab .bss.t2tab.* .bss.*.t2tab .bss.t2esc .bss.t2esc.* .bss.*.t2esc)
    *(.bss.dtab256 .bss.dtab256.* .bss.*.dtab256)
    *(.bss.jitk_tg .bss.tg .bss.tg.* .bss.*.tg .bss.jit_fz)
    *(.bss.t_obuf .bss.*.t_obuf)
    *(.bss.heads .bss.heads.* .bss.*.heads)
  }
}
INSERT BEFORE .bss;

SECTIONS
{
  .bss.hot (NOLOAD) : ALIGN(4096)
  {
    *(.bss.* COMMON)
  }
}
INSERT BEFORE .bss.tab;
