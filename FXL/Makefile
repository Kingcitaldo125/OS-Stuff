

#linux
#NASMFORMAT ?= elf
#LDFORMAT ?= -melf_i386
#NASMPREFIX ?= 
#QEMU ?= qemu-system-i386
#PYTHON ?= python3

NASMFORMAT ?= win32
NASMPREFIX ?= _
LDFORMAT ?= -mi386pe
QEMU ?= C:/Users/Paul/Documents/qemu/qemu.exe
PYTHON ?= /cygdrive/c/Python32/python.exe

CC=gcc -m32 -Wall -Werror -fno-builtin
NASM=nasm -f $(NASMFORMAT) --prefix "$(NASMPREFIX)"

all:
	$(NASM) kernelasm.s -o kernelasm.o
	$(NASM) kernelinb.s -o kernelinb.o
	$(CC) -c kernelc.c
	$(CC) -c util.c
	$(CC) -c kprintf.c
	$(CC) -c console.c
	$(CC) -c keyboard.c
	
	ld $(LDFORMAT) -Map kernelmap.txt -T linkerscript.txt -o kernel.tmp kernelasm.o kernelinb.o kernelc.o util.o kprintf.o console.o keyboard.o
	objcopy -O binary kernel.tmp kernel.bin
	
	$(PYTHON) diskutil.py hd1.img mkdisk --size=64
	$(PYTHON) diskutil.py hd1.img mcp kernel.bin kernel.bin
	
	$(QEMU) -monitor vc:80Cx27C hd1.img
	
	
clean: 
	-/bin/rm $(wildcard *.o) $(wildcard *.exe) $(wildcard *.img) $(wildcard *.vmdk) kernelmap.txt $(wildcard *.tmp) $(wildcard *.bin)