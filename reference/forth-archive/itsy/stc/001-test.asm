; nasm itsy-linux.asm -fbin -l itsy-linux.lst -o itsy-linux && chmod +x itsy-linux

%define link 0
%define immediate 080h

%macro header 2-3 0
%%link dd link
%define link %%link
%strlen %%count %1
db %3 + %%count, %1
%2:
%endmacro

%define TEXTORG 0x00400000
%define MEMSIZE 1048576

BITS 32
        org     TEXTORG

ehdr:                           ; Elf32_Ehdr
        db   0x7F, "ELF", 1, 1, 1, 0     ; e_ident
        times 8 db   0
        dw   2                  ; e_type
        dw   3                  ; e_machine
        dd   1                  ; e_version
        dd   interpret       ; e_entry
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

;  EAX       Top of Stack
;  EBP       Data Stack
; [EBP]      Second item on Stack
;  ESP       Return Stack
;  EDI       Thread data pointer

    header 'dup', dupe
        xchg ebp, esp
        push eax
        xchg ebp, esp
        ret

    header 'lit', lit
        call dupe
        pop esi
        lodsd
        jmp esi

    header 'emit', emit
        xchg ebp, esp
        push eax
        mov eax, 4   ; sys_write
        mov ebx, 1   ; stdout
        mov ecx, esp ; buffer
        mov edx, 1   ; write byte count
        int 80h
        pop eax
        pop eax
        xchg ebp, esp
        ret

    header 'bye', bye
        mov bl, 42
        xor eax, eax
        inc eax
        int 0x80

    header 'interpret', interpret
        mov ebp, TEXTORG + MEMSIZE - 2048
        mov esp, TEXTORG + MEMSIZE - 1024

        call lit
        dd 65
        call emit
        call bye

filesize      equ     $ - $$

