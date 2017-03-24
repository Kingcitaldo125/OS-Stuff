n.exe : n.asm
	nasm -f win32 --prefix _ -o n.o n.asm
	gcc -m32 -o n.exe n.o