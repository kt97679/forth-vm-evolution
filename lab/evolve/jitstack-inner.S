# INNER's loop body three ways (bench/loop.fth: DUP I + XOR inside DO ... LOOP), as the JIT copies it today
# (the stencils' instructions verbatim) and with the stack cached - lab/evolve/jitstack.py's audit, Iteration 218
    .data
    .globl rpvar
rpvar: .quad 0
    .text
# A: today - (sp, tos) in rdi, rsi; every cell below the top in memory; I and LOOP through the rp variable
    .globl inner_now
inner_now:
.LA:
    mov %rsi,-0x8(%rdi)          # dup
    sub $0x8,%rdi
    movabs $rpvar,%rdx           # i
    mov (%rdx),%rdx
    mov %rsi,%rax
    sub $0x8,%rdi
    mov (%rdx),%rsi
    mov %rax,(%rdi)
    add (%rdi),%rsi              # +
    add $0x8,%rdi
    xor (%rdi),%rsi              # xor
    add $0x8,%rdi
    movabs $rpvar,%rcx           # loop
    mov (%rcx),%rdx
    mov (%rdx),%rax
    add $0x1,%rax
    cmp %rax,0x8(%rdx)
    je .LAx
    mov %rax,(%rdx)
    jmp .LA
.LAx:
    mov %rsi,%rax
    ret
# B: three cells cached - dup a rename, I into a register, + and xor on registers; LOOP as today
    .globl inner_cached
inner_cached:
.LB:
    movabs $rpvar,%rdx           # i
    mov (%rdx),%rdx
    mov (%rdx),%rcx
    lea (%rsi,%rcx),%rax         # dup i +
    xor %rax,%rsi                # xor
    movabs $rpvar,%rcx           # loop, as today
    mov (%rcx),%rdx
    mov (%rdx),%rax
    add $0x1,%rax
    cmp %rax,0x8(%rdx)
    je .LBx
    mov %rax,(%rdx)
    jmp .LB
.LBx:
    mov %rsi,%rax
    ret
# C: B with the loop's index and limit in registers too
    .globl inner_regloop
inner_regloop:
    movabs $rpvar,%rdx
    mov (%rdx),%rdx
    mov (%rdx),%rcx
    mov 0x8(%rdx),%r8
.LC:
    lea (%rsi,%rcx),%rax
    xor %rax,%rsi
    add $0x1,%rcx
    cmp %rcx,%r8
    jne .LC
    mov %rsi,%rax
    ret
# D, E: the fixed-register design (lab/evolve/jitvariants.py) - its compiled stencils for DUP I + XOR at
# K = 2 and 3, as gcc built them with the fastest design's flags (Iteration 219); LOOP as today
    .globl inner_fixed2
inner_fixed2:
.LF2:
    # st_dup_1: 1 instructions
    mov    %rsi,%rdx
    # st_i_2: 7 instructions
    movabs $rpvar,%rax
    mov    (%rax),%rax
    sub    $0x8,%rdi
    mov    (%rax),%rax
    mov    %rdx,(%rdi)
    mov    %rsi,%rdx
    mov    %rax,%rsi
    # st_plus_2: 1 instructions
    add    %rdx,%rsi
    # st_xor_1: 2 instructions
    xor    (%rdi),%rsi
    add    $0x8,%rdi
    # loop
    movabs $rpvar,%rcx
    mov (%rcx),%rdx
    mov (%rdx),%rax
    add $0x1,%rax
    cmp %rax,0x8(%rdx)
    je .LF2x
    mov %rax,(%rdx)
    jmp .LF2
.LF2x:
    mov %rsi,%rax
    ret
    .globl inner_fixed3
inner_fixed3:
.LF3:
    # st_dup_1: 1 instructions
    mov    %rsi,%rdx
    # st_i_2: 6 instructions
    movabs $rpvar,%rax
    mov    (%rax),%rax
    mov    %rdx,%rcx
    mov    %rsi,%rdx
    mov    (%rax),%rax
    mov    %rax,%rsi
    # st_plus_3: 4 instructions
    mov    %rsi,%rax
    mov    %rdx,%rsi
    mov    %rcx,%rdx
    add    %rax,%rsi
    # st_xor_2: 1 instructions
    xor    %rdx,%rsi
    # loop
    movabs $rpvar,%rcx
    mov (%rcx),%rdx
    mov (%rdx),%rax
    add $0x1,%rax
    cmp %rax,0x8(%rdx)
    je .LF3x
    mov %rax,(%rdx)
    jmp .LF3
.LF3x:
    mov %rsi,%rax
    ret
