
extern sbss
extern ebss
extern kmain
extern highlevel_handler

;Load IDT
mov dword[idtloc+2],itable
mov eax,idtloc
lidt[eax]

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

;set up stack
mov esp,0x90000

;clear bss
mov ecx,ebss
sub ecx,sbss
xor al,al
mov edi,sbss
;rep -> while(ecx != 0){ stosb; ecx--; }
;stosb -> mov [edi],al ; inc edi;
cld
rep stosb
jmp kmain

section .text	
global outb
outb:
	mov edx,[esp+8]
	mov eax,[esp+4]
	out dx,al
	ret
	
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

midlevel_handler:
	pushad
	cld
	call highlevel_handler
	popad
	add esp,8
	iret
	ret
	
section .data
itable:
	times 48 dq 0x00008e0000100000
	dq 0x0000ee0000100000
	times 207 dq 0x0000ee0000100000
	
idtloc:
	dw 2048
	dd 0