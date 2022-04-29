// gcc -static-pie -o rickrop1 rickrop1.c

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>


int echo(){
    char buf[250];
    int length; 
    int counter = 2;

    printf("Sometimes ROP is more art than science\n");
    
    for (; counter > 0; counter-- ){
        length = read(0, buf, 250);
        buf[length] = '\0';    

        printf(buf);
    }

    return 0;
}


void flush(){
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stdin, NULL, _IONBF, 0);
    fflush(stdout);
}


int main(int argc, char** argv){
    flush();

    printf("Wubba Lubba Dub Dub!\n");
    echo();

    return 0;
}
