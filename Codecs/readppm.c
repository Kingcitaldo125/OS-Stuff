#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <ctype.h>
int can_decode(const char* filename){
    FILE* fp = fopen(filename,"rb");
    if( !fp )
        return 0;
        
    char a,b,c;
    fscanf(fp,"%c%c%c",&a,&b,&c);
    if( a != 'P' || b != '6' || !isspace(c) ){
        fclose(fp);
        return 0;
    }
    int w,h,maxccv;
    fscanf(fp,"%d %d %d",&w,&h,&maxccv);
    
    if( maxccv != 255 ){
        fclose(fp);
        return 0;
    }
    
    fclose(fp);
    return 1;
}

    
int load(const char* filename, char** ibuff, int* pw, int* ph){
    *ibuff=0;
    
    FILE* fp = fopen(filename,"rb");
    if(!fp)
        return 0;
        
    char a,b,c;
    fscanf(fp,"%c%c%c",&a,&b,&c);
    if( a != 'P' || b != '6' || !isspace(c) ){
        fclose(fp);
        return 0;
    }
    
    int w,h,maxccv;
    fscanf(fp,"%d %d %d",&w,&h,&maxccv);
    
    *pw=w;
    *ph=h;
    
    if( maxccv != 255 )
        return 0;
        
    while(fgetc(fp) != '\n' && !feof(fp))
        ;
        
    char* buff = (char*) malloc(w*h*4);
    *ibuff = buff;
    
    int y,x;
    char* p = buff;
    for(y=0;y<h;++y){
        for(x=0;x<w;++x,p+=4){
            fread(p,1,3,fp);
            p[3]=255;
        }
    }
    fclose(fp);
    return 1;
}
