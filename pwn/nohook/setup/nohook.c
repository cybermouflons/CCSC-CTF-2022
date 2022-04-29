// gcc -o nohook nohook.c
// patchelf --set-interpreter ld-linux-x86-64.so.2 --set-rpath ./ nohook

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

#define MAX_CHUNK_SIZE 0x408
#define MAX_ALLOCATIONS 21

size_t idx = 0;
char* moves[MAX_ALLOCATIONS] = { 0 }; 
size_t freed[MAX_ALLOCATIONS]= { 0 };
size_t sizes[MAX_ALLOCATIONS]= { 0 };

void flush(){
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stdin, NULL, _IONBF, 0);
    fflush(stdout);
    fflush(stdin);
}

int create(){
    // get size
    size_t size = 0x18;  // default size
    printf("Size: ");
    scanf("%zu",&size);

    // check max size reached
    if (idx >= MAX_ALLOCATIONS ){
        puts("Max. moves reached\n");
        return 0;
    }

    // limit max size
        if (size <= MAX_CHUNK_SIZE) {
            moves[idx] = malloc(size); // assign memory for move name
            sizes[idx] = size;
            idx = idx + 1; // increment idx
        }
        else{
            puts("Move size must be less than or equal to 0x1000");
        } 
    return 0;
}

void delete(){
    size_t idx_del = 65;

    printf("Index: ");
    scanf("%zu",&idx_del);

   // check max size reached
   if (idx_del >= idx){
        puts("Invalid index");
        return;
    }

    // check if already freed
    if (freed[idx_del] == 0) {
        printf("Deleting move at index %zu\n", idx_del);
        free(moves[idx_del]);
        freed[idx_del] = 1;
    }
    else {
        puts("Move already free");
    }
    return;
}

void view(){
    size_t idx_view;
    printf("Index: ");
    scanf("%zu",&idx_view);

    // check max size reached
    if (idx_view >= idx){
        puts("Invalid index");
        return;
    }

    // view move
    printf("Move: %s\n", moves[idx_view]);
}

void edit(){
    size_t idx_edit = 65;

    printf("Index: ");
    scanf("%zu",&idx_edit);

    // check max size reached
    if (idx_edit >= idx){
        puts("Invalid index");
        return;
    }

    // check for UAF
    if (freed[idx_edit] == 0) {
        // edit move name
        puts("New Move name: ");
        read(0, moves[idx_edit], sizes[idx_edit]);
        moves[idx_edit][sizes[idx_edit]] = '\0';  // null-byte overflow
        flush();
    }
    else{
        puts("Cannot edit freed move");
    }
    return;
}

int main(int argc, char** argv){
    flush();

    int menu_option = 0;
    puts("\n------------------------------------------");
    puts("       Get that parkour!!!");
    puts("------------------------------------------");

    do {
        menu_option = 0;
        puts("\n1. Create move. (max. 21)");
        puts("2. Delete move.");
        puts("3. View move.");
        puts("4. Edit move.");
        puts("5. Exit.");
        printf("Please enter an option from the main menu: ");
        flush();

        int menu_check = scanf("%d", &menu_option);
        if (!menu_check){
            menu_option = 0;
            continue;
        }

        switch(menu_option){
            case 1:
                create();
                break;
            case 2:             
                delete();
                break;
            case 3:             
                view();
                break;
            case 4:
                edit();
                break;
            case 5:
                puts("Exiting...");                           
                return 0;
            default:
                puts("Invalid input, try again!");
        } 
    } while(1);
    return 0;
}
