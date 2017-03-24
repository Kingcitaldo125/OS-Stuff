#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>

const char* format(){
    return "ppm";
}

int save(const char* outfile, char* ibuff, int w, int h){
    FILE* fp = fopen(outfile,"wb");
    if(!fp)
        return 0;
    fprintf(fp,"P6 %d %d 255\n",w,h);
    int y,x;
    for(y=0;y<h;++y){
        for(x=0;x<w;++x,ibuff+=4){
            fwrite(ibuff,1,3,fp);
        }
    }
    fclose(fp);
    return 1;
}
