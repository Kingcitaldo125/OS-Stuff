//disk.h
//#include <stdlib.h>
//#include <stdio.h>
//#include <string.h>

#pragma once
#define SUCCESS 0
#define EIO 1
#define EINVAL 1
#define ENOENT 2
#define ENOSYS 3
#define SEEK_SET 0
#define SEEK_CUR 1
#define SEEK_END 2

typedef struct File_
{
	int in_use;
	int flags;
	int first_cluster;
	int size;
	int offset;
}File;

void disk_init();
int file_open(char* fname,int flags,File* fp);
int file_close(File* fp);
int file_write(File* fp,void* addr,int cap);
int file_read(File* fp,void* addr,int capacity);
int file_seek(File* fp,int offset,int whence);
int disk_read_sector(unsigned sector, void* buffv);
int min(int a,int b);