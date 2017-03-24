section .text
global inb
inb:
	xor eax,eax
	mov dx,[esp+4]
	in al,dx
	ret
	
global inw
inw:
	xor eax,eax
	mov dx,[esp+4]
	in ax,dx
	ret