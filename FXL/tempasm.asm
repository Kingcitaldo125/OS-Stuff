%assign i 0
%rep 256
lowlevel_handler_%+i:
    %if i==8 || i==10 || i==11 || i==12 || i==13 || i==14 || i==17
        ;already pushed opcode
    %else
        push 0xbeefbeef
    %endif
    push i
    jmp midlevel_handler
    %assign i i+1
%endrep

itable:
	times 48 dq 0x00008e0000100000
	dq 0x0000ee0000100000
	times 207 dq 0x0000ee0000100000
	ret

midlevel_handler:
	pushad
	cld
	call highlevel_handler
	popad
	add esp,8
	iret

mov ecx,itable
%assign i 0
%rep 256
	mov eax,lowlevel_handler_%+i
	mov [ecx],ax
	shr eax,16
	mov [ecx+6],ax
	add ecx,8
	%assign i i+1

%endrep

;Load IDT
mov dword[idtloc+2],itable
mov eax,idtloc
lidt[eax]
	
section .data
idtloc:
	dw 2048
	dd 0