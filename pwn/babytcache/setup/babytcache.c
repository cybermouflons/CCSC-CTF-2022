// gcc -o babytcache babytcache.c
// patchelf --set-interpreter ld-linux-x86-64.so.2 --set-rpath ./ babytcache

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

size_t idx = 0;
char* pickles[8]; 

int create(){
    // check max size reached
    if (idx > 7){
        printf("Max. limit reached\n");
        return 0;
    }

    // assign memory for pickle name
    pickles[idx] = malloc(0x18);
    
    // get name
    printf("Name (max 8 chars): ");
    read(0, pickles[idx], 8);
    
    // increment idx
    idx = idx + 1; 
    return 0;
}


void delete(){
    size_t idx_del;
    printf("Index: \n");
    scanf("%zu",&idx_del);

    // check max size reached
    printf("Checking pickle at index %zu\n", idx_del);
    if (idx_del > idx){
        printf("Invalid index\n");
        return;
    }

    printf("Deleting pickle at index %zu\n", idx_del);
    // delete pickle
    free(pickles[idx_del]);
}

void flush(){
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stdin, NULL, _IONBF, 0);
    fflush(stdout);
}


int main(int argc, char** argv){
    flush();

    int menu_option = 0;
    printf("\n------------------------------------------\n");
    printf("       Create a new pickle!!!\n");
    printf("------------------------------------------\n\n");
    printf("Here's a useful leak [printf]: %p\n", &printf);

    do {
        menu_option = 0;
        printf("\nMain Menu\n");
        printf("1. Create pickle. (max. 8)\n");
        printf("2. Delete pickle.\n");
        printf("3. Exit.\n");
        printf("Please enter an option from the main menu: ");
        scanf("%d", &menu_option);
        flush();

        switch(menu_option){
            case 1:
                create();
                break;
            case 2:             
                delete();
                break;
            case 3:
                printf("\nExiting...\n");                           
                exit(0);
            default:
                printf("\nInvalid input, try again!\n");
                break;
        } 
    } while(menu_option != 3);
    return 0;
}
