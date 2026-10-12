extern _exit
extern _putchar

global _virtual_machine

section .text

_virtual_machine:
    mov edi, data
    mov edx, datatbl
l3:
    mov ebx, [edx]
    push edx
    push ebx

    add edx, 4
    xor ecx, ecx
    mov cl, [edx]
    mov ebx, 1
l2:
    xor eax, eax
    mov al, [edx + ebx]
    mov esi, [dataidx + eax * 4]
    mov eax, [dataidx + eax * 4 + 4]

copycode:
    movsb         ; [esi] -> [edi], esi++, edi++
    cmp eax, esi
    jne copycode

    inc ebx
    loop l2, ecx

    pop ebx
    pop edx
    add edx, ebx
    cmp ebx, 0
    jne l3

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
    mov ebx, data
l1:
    mov eax, [ebx]
    cmp eax, 0
    je done
    push eax
    call _putchar
    pop eax
    inc ebx
    jmp l1
done:
    push dword 0
    call _exit

section .data

data1 db '1.'
data2 db '22.'
data3 db '333.'
data4 db '4444.'
data5
datatbl
    dd 9
    db 3, 2, 1, 0, 0
datatbl2
    dd 9
    db 2, 2, 0, 0, 0
    dd 0
    db 4, 0, 1, 2, 3
dataseq db 3, 2, 0, 1
dataidx dd data1, data2, data3, data4, data5
data times 1024 db 0
