#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include "heapAllocator.h"

size_t idx = 0;
char *gms[64];

void flush();

int create()
{
    // check max size reached
    if (idx > 10)
    {
        printf("Max. limit reached\n");
        return 0;
    }

    // assign memory for gms name
    gms[idx] = my_malloc(64);

    // get name
    printf("Name: ");
    int t = read(0, gms[idx], 0x64);
    gms[idx][63] = '\0'; // null-terminate name
    idx = idx + 1;       // increment idx
    return 0;
}

void delete ()
{
    int idx_del;
    printf("Index: \n");
    int t = scanf("%d", &idx_del);

    // check max size reached
    if (idx_del > idx || gms[idx_del] == NULL)
    {
        printf("Invalid index\n");
        return;
    }

    // delete gms
    my_free(gms[idx_del]);
    gms[idx_del] = NULL;
}

void edit()
{
    int idx_edit;
    printf("Index: ");
    int t = scanf("%d", &idx_edit);

    // check max size reached
    if (idx_edit >= idx)
    {
        printf("Invalid index\n");
        return;
    }

    // edit gms
    flush();
    printf("New name: ");
    t = read(0, gms[idx_edit], 64);
}

void view()
{
    int idx_view;
    printf("Index: ");
    int t = scanf("%d", &idx_view);

    // check max size reached
    if (idx_view >= idx)
    {
        printf("Invalid index\n");
        return;
    }

    // view gms
    printf("Grand Master: %s\n", gms[idx_view]);
}

void flush()
{
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stdin, NULL, _IONBF, 0);
    fflush(stdout);
}

int main(int argc, char **argv)
{
    flush();
    char empty[128];

    for (int i = 0; i < 128; i++)
    {
        memset(empty, 0, 8);
    }

    int menu_option = 0;
    printf("\n------------------------------------------\n");
    printf("       Create a new Grand Master!!!\n");
    printf("------------------------------------------\n");

    do
    {
        printf("\nMain Menu\n");
        printf("1. Create Grand Master.\n");
        printf("2. Delete Grand Master.\n");
        printf("3. View Grand Master.\n");
        printf("4. Edit.\n");
        printf("5. Exit.\n");
        printf("Please enter an option from the main menu: ");
        int t = scanf("%d", &menu_option);
        flush();

        switch (menu_option)
        {
        case 1:
            create();
            break;
        case 2:
            delete ();
            break;
        case 3:
            view();
            break;
        case 4:
            edit();
            break;
        case 5:
            printf("\nExiting...\n");
            exit(0);
        default:
            printf("\nInvalid input, try again!\n");
            break;
        }
    } while (menu_option != 5);
    return 0;
}