//keyboard.h
//#include <stdlib.h>
//#include <stdio.h>
//#include <string.h>

#define LINEBUF_SIZE 40

typedef int bool;
#define true 1
#define false 0

char scancodes[92];
char shcodes[92];
char shiftedscancodes[92];

int buffer_ready;
int global_counter;
char linebuff[LINEBUF_SIZE];
int buffer_ready;
int linesize;
char c;

/*
Important scancodes:
Esc:1
Return:28
Backspace:14
LShift:42
RShift:54
SpaceBar:57
1:2
2:3
3:4
4:5
5:6
Apostrophe:40
*/


int keyboard_getline(char* q);
void keyboard_inturrupt();