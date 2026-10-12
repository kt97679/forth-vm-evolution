; This is nasm source of RelF engine. To compile use:
; nasmw -f bin -o relf.com relf.asm
; after that concatenate RelF kernel with resulting executable.
; This is intermediate result while trying to pack RelF engine into
; regular PC bootsector.
; There is no i/o except reading from the keyboard and writing to the screen.

[bits 16]
[org 100h]

    mov      AX,CS          ;Make sure all segments
    mov      DS,AX          ;point to this code

; first of all we need to setup table of function pointers, implementing
; RelF engine primitives. There are 36 primitives. If we would organize table
; during compilation it would occupy 144 bytes. Instead of that we use vmdata
; array, which contains byte lengths of each primitive (36 bytes). Code,
; which transforms vmdata into final table occupies 38 bytes. So instead of
; 144 bytes we used only 74.

    mov eax, vmlabels + 144
    mov ebx, vmrpstore
    mov cx, 36
    xor edx, edx
adjust_labels:
    sub eax, 4
    mov dl, [vmdata - 1 + ecx]
    sub ebx, edx
    mov [eax], ebx
    loop adjust_labels

; table setup complete
; now lets init other stuff
; edi - interpreter Instruction Pointer
; esp - interpreter Data Stack Pointer
; ebp - interpreter Return Stack Pointer

    mov di, code
    mov ebp, 0xff00
    mov esp, 0xfffc
    push edi
next:
    mov eax, [edi]
    add edi, 4
    mov ecx, eax
    and al, 1
    jz high_level
    jmp [ecx + vmops]
high_level:
    sub ebp, 4
    mov [ebp], edi
    add edi, ecx
    jmp next

vmdata:
db vmexit - vmnoop 
db vmlit - vmexit 
db vmbranch - vmlit 
db vm0branch - vmbranch 
db vmdrop - vm0branch
db vmdup - vmdrop 
db vmswap - vmdup 
db vmrot - vmswap 
db vmover - vmrot 
db vmcfetch - vmover 
db vmfetch - vmcfetch 
db vmcstore - vmfetch 
db vmstore - vmcstore 
db vmand - vmstore 
db vmor - vmand 
db vmxor - vmor 
db vmfromr - vmxor 
db vmtor - vmfromr 
db vmrfetch - vmtor 
db vmzeroeq - vmrfetch 
db vmugt - vmzeroeq 
db vmgt - vmugt 
db vmplus - vmgt 
db vmnegate - vmplus 
db vmrshift - vmnegate 
db vmlshift - vmrshift 
db vmummult - vmlshift 
db vmumdiv - vmummult 
db vmdplus - vmumdiv 
db vmemit - vmdplus 
db vmkey - vmemit 
db vmspfetch - vmkey 
db vmspstore - vmspfetch
db vmrpfetch - vmspstore
db vmrpstore - vmrpfetch
db 0

vmnoop:
    jmp next

vmexit:
    mov edi, [ebp] 
    add ebp, 4
    jmp next

vmlit:
    push dword [edi]
    add edi, 4
    jmp next

vmbranch:
    add edi, [edi]
    jmp next

vm0branch:
    pop ecx
    jecxz vmbranch
    add edi, 4
    jmp next

vmdrop:
    pop eax
    jmp next

vmdup:
    pop eax
    push eax
    push eax
    jmp next

vmswap:
    pop eax
    pop ecx
    push eax
    push ecx
    jmp next

vmrot:
    pop ecx
    pop edx
    pop eax
    push edx
    push ecx
    push eax    
    jmp next

vmover:
    pop eax
    pop ecx
    push ecx
    push eax
    push ecx
    jmp next

vmcfetch:
    xor edx, edx
    pop ecx
    xor ecx, 3
    mov dl, [ecx]
    push edx
    jmp next

vmfetch:
    pop eax
    push dword [eax]
    jmp next

vmcstore:
    pop edx
    pop ecx
    xor edx, 3
    mov [edx], cl
    jmp next

vmstore:
    pop edx
    pop ecx
    mov [edx], ecx
    jmp next

vmand:
    pop eax
    pop ecx
    and eax, ecx
    push eax
    jmp next

vmor:
    pop eax
    pop ecx
    or eax, ecx
    push eax
    jmp next

vmxor:
    pop eax
    pop ecx
    xor eax, ecx
    push eax
    jmp next

vmfromr:
    push dword [ebp]
    add ebp, 4
    jmp next

vmtor:
    pop eax
    sub ebp, 4
    mov [ebp], eax
    jmp next

vmrfetch:
    push dword [ebp]
    jmp next

vmzeroeq:
    pop ecx
    jecxz vmzeroeq_true
    push dword 0
    jmp next
vmzeroeq_true:
    push dword -1
    jmp next

vmugt:
    pop ecx
    pop eax
    cmp eax, ecx
    jb l1
    push dword 0
    jmp next
l1:
    push dword -1
    jmp next

vmgt:
    pop ecx
    pop eax
    sub eax, ecx
    jnl vmgt_false
    push dword -1
    jmp next
vmgt_false:
    push dword 0
    jmp next

vmplus:
    pop eax
    pop ecx
    add eax, ecx
    push eax
    jmp next

vmnegate:
    pop eax
    neg eax
    push eax
    jmp next

vmrshift:
    pop ecx
    pop eax
    shr eax, cl
    push eax
    jmp next

vmlshift:
    pop ecx
    pop eax
    shl eax, cl
    push eax
    jmp next

vmummult:
    pop ecx
    pop eax
    mul ecx
    push eax
    push edx
    jmp next

vmumdiv:
    pop ecx
    pop edx
    pop eax
    div ecx
    push edx
    push eax
    jmp next

vmdplus:
    pop ecx
    pop eax
    add [esp + 4], eax
    adc [esp], ecx
    jmp next

vmemit:
    pop eax
    mov ah, 14
    int 10h
    jmp next

vmkey:
    xor eax, eax
    int 0x16
    push eax
    jmp next

vmspfetch:
    mov eax, esp
    push eax
    jmp next

vmspstore:
    pop esp
    jmp next

vmrpfetch:
    push ebp
    jmp next

vmrpstore:
    pop ebp
    jmp next

vmlabels:

vmops equ vmlabels - 1

TIMES   1024-($-$$) DB 0		

code:
