section .text
global main
extern printf
extern scanf
main:
	push dat
	call printf
	add esp,4
	
	push inf
	call printf
	add esp,4
	
	push num
	push scand
	call scanf
	add esp,8
	
	mov eax,[num]
	mov dword[nn],eax
	push dword[nn]
	push finalprint
	call printf
	add esp,8
	
	ret
	
section .data
finalprint:
	db "You are %d years old",10,0
inf:
	db "Enter your age",10,0
dat:
	db "Hello",10,0
printd:
	db "%d",10,0
scand:
	db "%d",0
nn:
	dd 0
num:
	dd 0