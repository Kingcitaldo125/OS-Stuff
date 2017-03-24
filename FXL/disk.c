//#include "errno.h"
#include "util.h"
#include "disk.h"
#include "kprintf.h"

#pragma pack(push,1)

struct PTE {
    char junk[8];
    unsigned start;
    unsigned size;
};

struct MBR {
    char code[446];
    struct PTE ptable[4];
    char sig[2];
};

struct VBR
{
	unsigned char           jmp[3];
	char                    oem[8];
	unsigned short          bytes_per_sector;
	unsigned char           sectors_per_cluster;
	unsigned short          vbr_sectors;
	unsigned char           num_fats;
	unsigned short          num_root_dir_entries;
	unsigned short          num_sectors_small;
	unsigned char           id;
	unsigned short          sectors_per_fat;
	unsigned short          sectors_per_track;
	unsigned short          num_heads;
	unsigned int            first_sector;
	unsigned int            num_sectors_big;
	unsigned char           drive_number;
	unsigned char           reserved;
	unsigned char           sig1;
	unsigned int            serial_number;
	char                    label[11];
	char                    fstype[8];
} ;

struct DirEntry{
	char base[8];
	char ext[3];
	unsigned char attrib;
	char reserved[10];
	unsigned short time;
	unsigned short date;
	unsigned short start;
	unsigned int size;
};
#pragma pack(pop)

char sector_buffer[512];
struct VBR vbr;
struct MBR mbr;
unsigned short fat[65536];

//int Phi = vbr.num_root_dir_entries*sizeof(struct DirEntry_);
//int PhiTwo = Phi/512;
//unsigned int rs = vbr.first_sector + vbr.vbr_sectors + vbr.sectors_per_fat * 2;

void disk_init(){
    disk_read_sector(0,&mbr);
    disk_read_sector(mbr.ptable[0].start, &vbr);
    int i;
    int sn = vbr.first_sector+vbr.vbr_sectors;
    for(i=0;i<vbr.sectors_per_fat;++i,++sn){
        disk_read_sector(sn,&fat[256*i]);
    }
}

int file_open(char* fname, int flags, File* fp){
    fp->in_use = 0;
    
    char baseAndExt[11];
    int i;

	//copy first 8 chars
    for(i=0;i<8 && fname[i] && fname[i] != '.' ;++i){
        baseAndExt[i] = fname[i];
    }

    //if base is more than 8 characters, it cannot match.
    if( fname[i] && fname[i] != '.' )
        return -ENOENT;
        
	//pad with spaces to the 9th item (=index 8)
    for( ; i<8;++i){
		baseAndExt[i]= ' ';
	}

    int j=8;
	//if we have an extension, copy it
	if( fname[i] == '.' ){
		i++;
		for( ; fname[i] && j<11 ; ++i,++j){
			baseAndExt[j] = fname[i];
		}
	}

    //if extension is more than three characters, it cannot match
    if( fname[i] )
        return -ENOENT;
        
	for( ; j<11;++j)
		baseAndExt[i] = ' ';
		
    
    unsigned sn = vbr.first_sector + vbr.vbr_sectors + 2*vbr.sectors_per_fat;
    struct DirEntry* de = (struct DirEntry*) sector_buffer;
    for( i=0; i<vbr.num_root_dir_entries*32/512;++i){
        int rv = disk_read_sector(sn,sector_buffer);
        if( rv )
            return -EIO;
        int j;
        for(j=0;j<16;++j){
            if( de[j].base[0] != 0 && de[j].base[0] != 0xe5){
                if( kmemcmp(de[j].base,baseAndExt,11) == 0 ){
                    fp->in_use=1;
                    fp->offset=0;
                    fp->first_cluster=de[j].start;
                    fp->size=de[j].size;
                    fp->flags=flags;
                    return SUCCESS;
                }
            }
        }
    }
    return -ENOENT;     //no such dir entry
}

int min(int a, int b){
	return (a<b) ? a:b;
}

//read up to 'capacity' bytes from file fp into memory at addr.
int file_read( File* fp, void* addr, int capacity){
	char* p = (char*) addr;
	unsigned cluster = fp->first_cluster;
    
    //where data area starts on the disk
	int data_start_sector = vbr.first_sector + 1 + vbr.num_fats*vbr.sectors_per_fat + vbr.num_root_dir_entries * 32 / 512;
	
    //number of bytes read
    int num_read=0;
    
	int bytes_per_cluster =  (vbr.sectors_per_cluster*512);

	//kprintf("%d ",bytes_per_cluster);
    //if we're at EOF already, stop.
	if( fp->offset >= fp->size )
		return 0;
		
	int num_clusters_to_skip = fp->offset / bytes_per_cluster;
	while(num_clusters_to_skip > 0 ){
		cluster = fat[cluster];
		if( cluster > 0xfff6 ){
			//end of file. But how?
			kprintf("Early EOF!");
			return -EIO;
		}
		--num_clusters_to_skip;
	}
	
	while( capacity > 0 && fp->offset < fp->size ){
		//sector where cluster data starts
		int sn = data_start_sector + (cluster-2)*vbr.sectors_per_cluster;
		
		//number of bytes to skip at the start of the cluster
		int start_reading = fp->offset % bytes_per_cluster;
		
		//number of sectors to skip 
		int sector_offset = start_reading / 512;
		
		int i;
		for(i=sector_offset; i<vbr.sectors_per_cluster && fp->offset < fp->size && capacity > 0; i++ ){
			if( 0 != disk_read_sector(sn+i, sector_buffer) )
				return -EIO;
                
            //num bytes to skip at start of sector
            int num_bytes_skipped = fp->offset % 512;
            
            //num bytes left in the sector
			int num_to_copy = 512 - num_bytes_skipped;
            
            //clamp num_to_copy to min( bytes left in file , capacity )
			if( fp->size-fp->offset < num_to_copy )
				num_to_copy = fp->size-fp->offset;
			if( capacity < num_to_copy )
				num_to_copy = capacity;
			
			kmemcpy( p, sector_buffer+num_bytes_skipped, num_to_copy);
            
			p += num_to_copy;
			fp->offset += num_to_copy;
			num_read += num_to_copy;
			capacity -= num_to_copy;
		}
		cluster = fat[cluster];
	}
	return num_read;
}

int file_write(File* fp, void* buf, int count){
    return -ENOSYS;
}

int file_close(File* fp){
    if( fp->in_use == 0 )
        return -EINVAL;
    fp->in_use=0;
    return 0;
}

int file_seek(File* fp, int offset, int whence){
    //Note: whence = SEEK_SET (0), SEEK_CUR (1) or SEEK_END (2)
    if( fp->in_use == 0 )
        return -EINVAL;
    if(whence == SEEK_SET){
        if(offset < 0 )
            return -EINVAL;
        else
            fp->offset = offset;
    }
    else if(whence == SEEK_CUR){
        if( offset + fp->offset < 0 )
            return -EINVAL;
        else
            fp->offset += offset;
    }
    else if(whence == SEEK_END){
        if( offset + fp->size < 0 )
            return -EINVAL;
        else
            fp->offset = fp->size + offset;
    }
    else{
        return -EINVAL;
    }
    return 0;
}

int disk_read_sector(unsigned sector, void* buffv){
    unsigned short* buff = (unsigned short*) buffv;
    int rv;
    
    do{
        rv = inb(0x1f7);
    }while(rv & 0x80 );

    if( rv & 0x21 )
        return -EIO;
        
    outb(0x2, 0x3f6);
    outb(1,0x1f2);
    outb(sector&0xff,0x1f3);
    outb((sector>>8)&0xff,0x1f4);
    outb((sector>>16)&0xff,0x1f5);
    outb( 0xe0|(sector>>24) , 0x1f6);
    outb(0x20, 0x1f7);
    
    do{
        rv = inb(0x1f7);
    }while(rv & 0x80);
    
    if( rv & 0x21 )
        return -EIO;
    
    while( (rv & 8) == 0 )
        rv = inb(0x1f7);
        
    int i;
    for(i=0;i<256;++i){
        buff[i] = inw(0x1f0);
    }
    
    return 0;
}
    