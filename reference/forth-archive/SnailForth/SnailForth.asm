; nasm SnailForth.asm -fbin -l SnailForth.lst -o SnailForth && chmod +x SnailForth

%define link 0
%define immediate 080h

%macro head 3       ; macro with 3 arguments: 1 - name for forth dictionary, 2 - name for nasm label, 3 - additional flags
%%link dd link      ; %% defines label local to macro
%define link %%link ; link is redefined (to be used in next word definition)
%strlen %%count %1  ; length of the word name goes to 'count'
db %3 + %%count, %1 ; %3 contains flags value (e.g. for immediate words)
xt_ %+ %2:          ; %+ concatenates strings
%endmacro

; primitive and colon macros are the same
; primitives are distinguished from colons by their location in the code
; all primitives are in the beginning of the file before docolon label

%macro primitive 2-3 0 ; 0 - default value for the 3rd paramseter (no flags)
head %1, %2, %3
%endmacro

%macro colon 2-3 0
head %1, %2, %3
%endmacro

%macro variable 3
head %1, %2, 0, dovar
val_ %+ %2 dd %3
%endmacro

%define TEXTORG 0x00400000
%define MEMSIZE 1048576
%define TIBSIZE 80
%define STACKSIZE 4096
%define TIBPTR TEXTORG + MEMSIZE - TIBSIZE
%define SP0 TIBPTR - 4
%define RP0 SP0 - STACKSIZE

BITS 32
        org     TEXTORG

ehdr:                           ; Elf32_Ehdr
        db   0x7F, "ELF", 1, 1, 1, 0     ; e_ident
        times 8 db   0
        dw   2                  ; e_type
        dw   3                  ; e_machine
        dd   1                  ; e_version
        dd   _start       ; e_entry
        dd   phdr - $$  ; e_phoff
        dd   0                  ; e_shoff
        dd   0                  ; e_flags
        dw   ehdrsize   ; e_ehsize
        dw   phdrsize   ; e_phentsize
        dw   1                  ; e_phnum
        dw   0                  ; e_shentsize
        dw   0                  ; e_shnum
        dw   0                  ; e_shstrndx

ehdrsize   equ   $ - ehdr

phdr:                           ; Elf32_Phdr
        dd   1                  ; p_type
        dd   0                  ; p_offset
        dd   $$                 ; p_vaddr
        dd   $$                 ; p_paddr
        dd   filesize   ; p_filesz
        dd   MEMSIZE    ; p_memsz
        dd   7                  ; p_flags
        dd   0x1000             ; p_align

phdrsize   equ   $ - phdr

; esi - forth instruction pointer
d_sp dd SP0
r_sp dd RP0
reg0 dd 0
reg1 dd 0

    primitive 'lit', lit
        lodsd
        mov esp, [d_sp]
        push eax
        mov [d_sp], esp
        jmp next

    primitive '+', plus
        mov esp, [d_sp]
        pop eax
        pop ebx
        add eax, ebx
        push eax
        mov [d_sp], esp
        jmp next

    primitive '@', fetch
        mov esp, [d_sp]
        pop eax
        push dword[eax]
        jmp next

    primitive '!', store
        mov esp, [d_sp]
        pop eax
        pop dword[eax]
        mov [d_sp], esp
        jmp next

    primitive 'exit', exit
        mov esp, [r_sp]
        pop esi
        mov [r_sp], esp
        jmp next

    primitive 'syscall', syscall
        mov esp, [d_sp]
        pop eax
        pop ebx
        pop ecx
        pop edx
        int 80h
        push eax
        mov [d_sp], esp
        jmp next

docolon mov esp, [r_sp]
        push esi
        mov [r_sp], esp
        mov esi, eax
next    lodsd
        cmp eax, $ ; if eax contains address from below
        ja docolon ; this is a colon definition, jump to the docolon
        jmp eax    ; otherwise this is a primitive, jump to the appropriate address

    colon 'drop', drop
        dd xt_lit, reg0
        dd xt_store
        dd xt_exit

    colon 'swap', swap
        dd xt_lit, reg0
        dd xt_store
        dd xt_lit, reg1
        dd xt_store
        dd xt_lit, reg0
        dd xt_fetch
        dd xt_lit, reg1
        dd xt_fetch
        dd xt_exit

;    colon 'accept', accept
;        dd xt_swap    ; buffer goes to ecx, byte count to edx
;        dd xt_lit, 3  ; sys_read, eax
;        dd xt_lit, 0  ; stdin, ebx
;        dd xt_syscall
;        dd xt_lit, -1 ; read byte count includes terminating CR, decrementing
;        dd xt_plus
;        dd xt_exit

    colon 'type', type
        dd xt_swap    ; buffer goes to ecx, byte count to edx
        dd xt_lit, 1  ; stdout, ebx
        dd xt_lit, 4  ; sys_write, eax
        dd xt_syscall
        dd xt_drop
        dd xt_exit

    colon 'bye', bye
        dd xt_lit, 0 ; edx not used
        dd xt_lit, 0 ; ecx not used
        dd xt_lit, 42 ; ebx exit code
        dd xt_lit, 1 ; eax sys_exit
        dd xt_syscall

hello db 'Hello', 10

_start:
    mov esi, xt_interpret
    jmp next

    colon 'interpret', interpret
        dd xt_lit, hello
        dd xt_lit, 6
        dd xt_type
        dd xt_bye

filesize   equ   $ - $$
