; ----------------------------------------------------------------------------
; echo.asm
;
; NASM implementation of a program that displays its commandline arguments,
; one per line.
; ----------------------------------------------------------------------------	

	global	_main
	extern	_printf
        extern  _exit
        extern _putchar
	
	section .text
_main:
;    call print3
;    push dword 0
;    call _exit
;    jmp print
    mov edi, codedata
    mov esi, print3
    mov eax, end3

copycode:
    movsb         ; [esi] -> [edi], esi++, edi++
    cmp eax, esi
    jne copycode

;    jmp codedata
    call codedata

	push	ecx			; save registers that printf wastes
	push	edx
	
	push	dword eax		; the argument string to display
	push	dword format		; the format string	
	call	_printf
	add	esp, 8			; remove the two parameters
	
	pop	edx			; restore registers printf used
	pop	ecx

    ret
    mov ebx, codedata
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

	
	ret

print:
	push	ecx			; save registers that printf wastes
	push	edx
	
	xor eax, eax
	push	dword eax		; the argument string to display
	push	dword format		; the format string	
	call	_printf
	add	esp, 8			; remove the two parameters
	
	pop	edx			; restore registers printf used
	pop	ecx

        push dword 0
        call _exit
end:
print2:
db 'abcdef 12345', 10, 0
end2:
print3:
    mov eax, [intdata + 4]
    push dword 65
    mov eax, _putchar
    call eax
    pop eax
    ret
end3:

section .data

format:
	db	'eax : %x', 10, 0
codedata:
times 1024 db 0
intdata
dd 9,8,7,6,5,4,3,2,1,0