#include <stdio.h>
#define memory_size 0xFFFFF
#define min_block_size 0x10

struct block_meta
{
    short inUse;
    struct block_meta *next;
    struct block_meta *prev;
    int len;
};

struct heap_meta
{
    void *start;
    void *end;
    int len;
    void (*free_hook)(void *ptr);
} BlockMeta;

void *my_malloc(size_t size);
void my_free(void *ptr);
int initMalloc();
#ifdef DEBUG 
void print_heap();
#endif