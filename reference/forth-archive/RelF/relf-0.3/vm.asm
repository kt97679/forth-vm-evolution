; esp - data stack pointer
; ebp - return stack pointer
; esi - instruction pointer
; edx - top of stack

extern _rp
extern _ip
extern _dsp
extern _base
extern _exit
extern _getchar
extern _putchar
extern _printf

global _virtual_machine

section .text

_virtual_machine:
    cld
    mov esi, [_ip]
    mov ebp, [_rp]
    mov esp, [_dsp]
    pop edx
    add esi, 4
    call updatecode

; 0
vmdonext:
    lodsd ; eax = [esi], esi += 4
    jmp [codeidx + eax * 4]

;vmdonext:
;    mov eax, [esi]
;    add esi, 4
;    jmp [codeidx + eax * 4]

; 1
vmdolist:
    sub ebp, 4
    mov [ebp], esi
    add dword [ebp], 4
    add esi, [esi]

; 2
vmexit:
    mov esi, [ebp] 
    add ebp, 4

;vmexit:
;    xchg esp, ebp
;    pop esi
;    xchg esp, ebp

; 3
vmlit:
    lodsd
    push edx
    mov edx, eax

;vmlit:
;    push edx
;    mov edx, [esi]
;    add esi, 4

; 4
vmbranch:
    add esi, [esi]

; 5
;vm0branch:
;    test edx, edx
;    pop edx
;    jz vmbranch
;    add esi, 4
vm0branch:
    mov ecx, edx
    pop edx
    jecxz l5
    add esi, 4
    jmp l6
l5:
    add esi, [esi]
l6:

; 6
vmdrop:
    pop edx

; 7
vmdup:
    push edx

; 8
vmswap:
    pop eax
    push edx
    mov edx, eax

; 9
vmrot:
    pop ecx
    pop eax
    push ecx
    push edx
    mov edx, eax    

; 10
vmover:
    pop ecx
    push ecx
    push edx
    mov edx, ecx

; 11
vmcfetch:
    xor edx, 3
    movzx edx, byte [edx]

; 12
vmfetch:
    mov edx, [edx]

; 13
vmcstore:
    pop ecx
    xor edx, 3
    mov [edx], cl
    pop edx

; 14
vmstore:
    pop ecx
    mov [edx], ecx
    pop edx

; 15
vmand:
    pop ecx
    and edx, ecx

; 16
vmor:
    pop ecx
    or edx, ecx

; 17
vmxor:
    pop ecx
    xor edx, ecx

; 18
vmfromr:
    push edx
    mov edx, [ebp]
    add ebp, 4

; 19
vmtor:
    sub ebp, 4
    mov [ebp], edx
    pop edx

; 20
vmrfetch:
    push edx
    mov edx, [ebp]

; 21
vmeq:
    pop eax
    xor edx, eax
    sub edx, 1
    sbb edx, edx

; 22
vmugt:
     pop ecx
     cmp ecx, edx
     sbb edx, edx

; 23
vmgt:
    pop eax
    sub eax, edx
    cdq

; 24
vmplus:
    pop eax
    add edx, eax

; 25
vmnegate:
    neg edx

; 26
vmlshift:
    mov ecx, edx
    pop edx
    shl edx, cl

; 27
vmrshift:
    mov ecx, edx
    pop edx
    shr edx, cl

; 28
vmummult:
    mov ecx, edx
    pop eax
    mul ecx
    push eax

; 29
vmumdiv:
    mov ecx, edx
    pop edx
    pop eax
    div ecx
    push edx
    mov edx, eax

; 30
vmdplus:
    pop eax
    pop ecx
    add [esp], eax
    adc edx, ecx

; 31
vmemit:
    push edx
    mov eax, _putchar
    call eax
    pop eax
    pop edx

; 32
vmkey:
    push edx
    mov eax, _getchar
    call eax
    mov edx, eax

; 33
vmbye:
    push dword 0
    mov eax, _exit
    call eax

; 34
vmspfetch:
    push edx
    mov edx, esp

; 35
vmspstore:
    mov esp, edx

; 36
vmrpfetch:
    push edx
    mov edx, ebp

; 37
vmrpstore:
    mov ebp, edx
    pop edx

; 38
vmopenfile:
    nop
; 39
vmclosefile:
    nop
; 40
vmreadline: 
    nop
; 41
vmwriteline:
    nop
; 42
vmreadfile: 
    nop
; 43
vmwritefile:
    nop
; 44
vmsystem:   
    nop
; 45
vmreposfile:
    nop
; 46
vmfilepos:  
    nop
; 47
vmdelfile:  
    nop
; 48
vmfilesize: 
    nop

; 49
vmupdatecode:
    mov eax, updatecode
    call eax

; 50
vmlast:

updatecode:
    push esi
    push edx
    mov edi, codedata
    mov dword [codeidx], 0
    mov edx, [_base]
    add edx, [edx]
l3:
    mov ebx, [edx]
    add dword [codeidx], 4
    mov eax, [codeidx]
    add eax, codeidx
    mov [eax], edi
    push edx
    push ebx

    add edx, 4
    mov ecx, edx
    xor ecx, 3
    mov cl, [ecx]
    and ecx, 255
    jecxz l4
    mov ebx, 1
l2:
    mov eax, edx
    add eax, ebx
    xor eax, 3
    mov al, [eax]
    and eax, 255

    mov esi, [vmops + eax * 4]
    mov eax, [vmops + eax * 4 + 4]

copycode:
    movsb         ; [esi] -> [edi], esi++, edi++
    cmp eax, esi
    jne copycode

    inc ebx
    loop l2, ecx

    mov esi, [vmops]
    mov eax, [vmops + 4]

copycode2:
    movsb         ; [esi] -> [edi], esi++, edi++
    cmp eax, esi
    jne copycode2
l4:
    pop ebx
    pop edx
    add edx, ebx
    cmp ebx, 0
    jne l3
;	pushad			; save registers that printf wastes
;        sub edi, codedata
;	push	dword edi		; the argument string to display
;	push	dword format3		; the format string	
;	call	_printf
;	add	esp, 8			; remove the two parameters
;	popad
    pop edx
    pop esi
    ret

section .data

format3: db " %x", 0

vmops dd vmdonext, vmdolist, vmexit, vmlit, vmbranch, vm0branch, vmdrop,
       dd vmdup, vmswap, vmrot, vmover, vmcfetch, vmfetch, vmcstore, vmstore,
       dd vmand, vmor, vmxor, vmfromr, vmtor, vmrfetch, vmeq, vmugt, vmgt,
       dd vmplus, vmnegate, vmlshift, vmrshift, vmummult, vmumdiv, vmdplus,
       dd vmemit, vmkey, vmbye, vmspfetch, vmspstore, vmrpfetch, vmrpstore,
       dd vmopenfile, vmclosefile, vmreadline, vmwriteline, vmreadfile,
       dd vmwritefile, vmsystem, vmreposfile, vmfilepos, vmdelfile, vmfilesize,
       dd vmupdatecode, vmlast

codeidx
times 4096 db 0

codedata
times 16384 db 0
