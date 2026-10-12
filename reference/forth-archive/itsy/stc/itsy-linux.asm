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

%macro constant 3
header %1,%2
call doconst
val_ %+ %2 dd %3
%endmacro

%macro variable 3
head %1,%2
call dovar
val_ %+ %2 dd %3
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
        dd   abort       ; e_entry
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

    variable 'state', state, 0
    variable '>in', to_in, 0
    variable '#tib', number_t_i_b, 0
    variable 'dp', dp, freemem
    variable 'base', base, 10
    variable 'last', last, final
    constant 'tib', t_i_b, TEXTORG + 32768

    header 'abort', abort
        mov eax, dword[val_number_t_i_b]
        mov dword[val_to_in], eax
        xor ebp, ebp
        mov dword[val_state], ebp
        mov ebp, TEXTORG + MEMSIZE - 2048
        mov esp, TEXTORG + MEMSIZE - 1024
        call interpret

; stack manipulations

    header 'drop', drop
        xchg ebp, esp
        pop eax
        xchg ebp, esp
        ret

    header 'dup', dupe
        xchg ebp, esp
        push eax
        xchg ebp, esp
        ret

    header 'swap', swap
        xchg eax, [ebp]
        ret

    header 'rot', rote
        xchg ebp, esp
        pop ebx
        pop ecx
        push ebx
        push eax
        mov eax, ecx
        xchg ebp, esp
        ret

; memory manipilations

    header '@', fetch
        mov eax, [eax]
        ret

    header '!', store
        xchg ebp, esp
        pop edx
        mov [eax], edx
        pop eax
        xchg ebp, esp
        ret

    header ',', comma
        mov edi, dword[val_dp]
        stosd
        mov dword[val_dp], edi
        call drop
        ret

    header 'lit', lit
        call dupe
        pop esi
        lodsd
        jmp esi

; control flow

    header 'execute', execute
        mov edx, eax
        xchg ebp, esp
        pop eax
        xchg ebp, esp
        call edx
        ret

    header '0branch', zero_branch
        xchg ebp, esp
        pop ebx
        xchg ebp, esp
        xchg eax, ecx
        pop esi
        lodsd
        xchg eax, ebx
        test ecx, ecx
        jz [ebx]
        jmp [esi]

; IO

    header 'accept', accept
        mov edx, 3
        xchg edx, eax ; now edx contains buffer length and eax contains 3 (sys_read)
        mov ebx, 0   ; stdin
        xchg ebp, esp
        pop ecx      ; buffer address
        xchg ebp, esp
        int 80h      ; eax after sys_read contains number of bytes read (negative number means error)
        dec eax      ; last char is CR, ignore it
        ret

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

; misc

    header '+', plus
        xchg ebp, esp
        pop ebx
        add eax,ebx
        xchg ebp, esp
        ret

    header '=', equals
        xchg ebp. esp
        pop ebx
        xchg ebp, esp
        sub eax, ebx
        sub eax, 1
        sbb eax, eax
        ret

    header 'count', count
        xor ebx, ebx
        mov bl, byte[eax]
        inc eax
        call dupe
        mov ebx, ebx
        ret

    header '>number', to_number
        xchg ebp, esp
        pop edi
        pop ecx
        pop ebx
to_numl test eax,eax
        je to_numz
        push ebx
        mov bl,byte[edi]
        cmp bl,'a'
        jc to_nums
        sub bl,32
to_nums cmp bl,'9'+1
        jc to_numg
        cmp bl,'A'
        jc to_numh
        sub bl,7
to_numg sub bl,48
        and ebx,0xff
        cmp bl,byte[val_base]
        jnc to_numh
        xchg ebx,edx
        pop ebx
        push edx
        xchg ebx,ecx
        mul dword[val_base]
        xchg ebx,ecx
        mul dword[val_base]
        add ecx,edx
        pop edx
        add ebx,edx
        dec eax
        inc edi
        jmp to_numl
to_numz push ebx
to_numh push ecx
        push edi
        xchg ebp, esp
        ret

    header 'word', word
        xchg ebp, esp
        mov edi, dword[val_dp]
        push edi
        mov edx, eax
        mov eax, dword[val_t_i_b]
        mov ecx, eax
        add eax, dword[val_to_in]
        add ecx, dword[val_number_t_i_b]
wordf   cmp ecx, eax
        je wordz
        mov bl, byte[eax]
        inc eax
        cmp bl, dl
        je wordf
wordc   inc edi
        mov byte[edi], bl
        cmp ecx, eax
        je wordz
        mov bl, byte[eax]
        inc eax
        cmp bl, dl
        jne wordc
wordz   mov byte[edi + 1], 32
        mov ebx, dword[val_dp]
        xchg ebx, edi
        sub ebx, edi
        mov byte[edi], bl
        sub eax, dword[val_t_i_b]
        mov dword[val_to_in], eax
        pop eax
        xchg ebp, esp
        ret

    header 'find', find
        xchg ebp, esp
        mov edi, val_last
findl   push edi
        push eax
        mov cl, byte[eax]
        and ecx, 0xff
        inc ecx
findc   mov bl, byte[edi + 4]
        and bl, 07Fh
        cmp bl, byte[eax]
        je findm
        pop eax
        pop edi
        mov edi, dword[edi]
        test edi, edi
        jne findl
findnf  push eax
        xor eax, eax
        ret
findm   inc edi
        inc eax
        loop findc
        pop eax
        pop edi
        mov eax, 1
        inc edi
        inc edi
        inc edi
        inc edi
        mov bl, byte[edi]
        test bl, 080h
        jne findi
        neg eax
findi   and ebx, 31
        add edi, ebx
        inc edi
        push edi
        xchg ebp, esp
        ret

    header ':', colon
        call lit
        dd -1
        call state
        call store
        call create
        ret

    header ';', semicolon, immediate
        call lit
        dd 0xC3 ; ret
        call comma
        call lit
        dd 0
        call state
        call store
        ret

    colon 'create', create
        call dp
        call fetch
        call last
        call fetch
        call comma
        call last
        call store
        call lit
        dd 32
        call word
        call count
        call plus
        call dp
        call store
        call lit
        dd 0
        call comma
        ret

final:

    header 'interpret', interpret
interpt call number_t_i_b
        call fetch
        call to_in
        call fetch
        call equals
        call zero_branch
        dd intpar
        call t_i_b
        call lit
        dd 50
        call accept
        call number_t_i_b
        call store
        call lit
        dd 0
        call to_in
        call store
intpar  call lit
        dd 32
        call word
        call find
        call dupe
        call zero_branch
        dd intnf
        call state
        call fetch
        call equals
        call zero_branch
        dd intexc
        call comma
        jmp intdone
intexc  call execute
        jmp intdone
intnf   call dupe
        call rote
        call count
        call to_number
        call zero_branch
        dd intskip
        call state
        call fetch
        call zero_branch
        dd intnc
        call last
        call fetch
        call dupe
        call fetch
        call last
        call store
        call dp
        call store
intnc   call abort
intskip call drop
        call drop
        call state
        call fetch
        call zero_branch
        dd intdone
        call lit
        dd lit
        call comma
        call comma
intdone jmp interpt

freemem:

filesize   equ   $ - $$
