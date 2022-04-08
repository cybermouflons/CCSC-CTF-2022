#include <sys/mman.h>
#include <stdio.h>
#include "heapAllocator.h"

short init = 0;
struct heap_meta *h_meta;
struct block_meta *fb_meta;

int initMalloc()
{
    if (init == 1)
        return 0;
    
    h_meta = (struct heap_meta *)mmap(NULL, memory_size, PROT_READ | PROT_WRITE, MAP_PRIVATE | MAP_ANONYMOUS,  0, 0);
    if(h_meta == MAP_FAILED){
        printf("Mapping Failed\n");
        return -1;
    }
    h_meta->free_hook = NULL;
    h_meta->start = h_meta + sizeof(struct heap_meta);
    h_meta->end = h_meta + memory_size - sizeof(struct heap_meta);
    h_meta->len = h_meta->end - h_meta->start;
    fb_meta = (struct block_meta *)h_meta->start;
    fb_meta->inUse = 0;
    fb_meta->next = NULL;
    fb_meta->prev = NULL;
    fb_meta->len = h_meta->len;
    init = 1;
    return 1;
}

void *my_malloc(size_t size)
{
    if(initMalloc() == -1){
        return NULL;
    }
    if (min_block_size > size)
    {
        size = min_block_size;
    }
    size += sizeof(struct block_meta);
    struct block_meta *currentBlock = fb_meta;
    struct block_meta *prevBlock = NULL;
    struct block_meta *nextBlock = currentBlock->next;
    while (nextBlock != NULL)
    {
        if (currentBlock->inUse == 1 || currentBlock->len < size)
        {
            prevBlock = currentBlock;
            currentBlock = currentBlock->next;
            nextBlock = currentBlock->next;
            continue;
        }
        break;
    }
    if (nextBlock == NULL || (currentBlock->len >= size + sizeof(struct block_meta) + min_block_size & currentBlock->inUse == 0))
    {
        currentBlock->next = size + (void *)currentBlock;
        currentBlock->next->inUse = 0;
        currentBlock->next->len = currentBlock->len - size;
        currentBlock->next->prev = currentBlock;
        currentBlock->next->next = nextBlock;
    }
    
    if(currentBlock->inUse == 0){
        currentBlock->inUse = 1;
        currentBlock->len = size - sizeof(struct block_meta);
    }
    currentBlock = currentBlock + 1;
    // printf("Malloc:    %p\n", currentBlock);
    return (void *)(currentBlock);
}
void my_free(void *ptr)
{
    if (h_meta->free_hook != NULL)
    {
        h_meta->free_hook(ptr);
    }
    struct block_meta *currentBlock = (struct block_meta *)(ptr - sizeof(struct block_meta));
    currentBlock->inUse = 0;
    currentBlock->len = currentBlock->len + sizeof(struct block_meta);
    if(currentBlock->next != NULL){
        if(currentBlock->next->inUse != 1){
            currentBlock->len = currentBlock->len + currentBlock->next->len;
            currentBlock->next = currentBlock->next->next;
            if(currentBlock->next != NULL){
                currentBlock->next->prev = currentBlock;
            }
        }
    }
    if(currentBlock->prev != NULL){
        if(currentBlock->prev->inUse != 1){
            currentBlock->prev->len = currentBlock->prev->len + currentBlock->len;
            currentBlock->prev->next = currentBlock->next;
            if(currentBlock->next != NULL){
                currentBlock->next->prev = currentBlock->prev;
            }
        }
    }
    // printf("Free:      %p\n", currentBlock);
    return;
}

#ifdef DEBUG 
void print_heap_block(void *ptr, short align)
{

    struct block_meta *block = (struct block_meta *)ptr;
    if (align)
    {
        block = block - sizeof(struct block_meta);
    }
    printf("Address:   %p\n", block);
    printf("In Use:    %d\n", block->inUse);
    printf("Next:      %p\n", block->next);
    printf("Prev:      %p\n", block->prev);
    printf("Len:       %d\n", block->len);
}

void print_all_heap_blocks()
{
    struct block_meta *currentBlock = fb_meta;
    int id = 0;
    while (currentBlock != NULL)
    {
        printf("\nBlock %d:\n", id);
        print_heap_block(currentBlock, 0);
        currentBlock = currentBlock->next;
        id++;
    }
}
void print_heap()
{
    if(initMalloc() == -1){
        return;
    }
    printf("=========Heap Start=========\n");
    printf("Heap:      %p\n", h_meta);
    printf("Start:     %p\n", h_meta->start);
    printf("End:       %p\n", h_meta->end);
    printf("Len:       0x%x\n", h_meta->len);
    printf("Block size:%ld\n", sizeof(struct block_meta));
    if (h_meta->free_hook != NULL)
    {
        printf("Free hook: %p\n", h_meta->free_hook);
    }
    printf("Heap init block state:\n");
    print_all_heap_blocks();
    printf("========= Heap End  =========\n\n");
}
int main()
{
    print_heap();
    char *test = (char *)my_malloc(0x50);
    printf("=========Malloc 1=========\n");
    print_all_heap_blocks();
    char *test2 = (char *)my_malloc(0x20);
    printf("\n=========Malloc 2=========\n");
    print_all_heap_blocks();
    my_free(test);
    printf("\n=========Free 1=========\n");
    print_all_heap_blocks();
    my_free(test2);
    printf("\n=========Free 2=========\n");
    print_all_heap_blocks();
    char *test3 = (char *)my_malloc(0x10);
    printf("\n=========Malloc 3=========\n");
    print_all_heap_blocks();
    char *test4 = (char *)my_malloc(0x10);
    printf("\n=========Malloc 4=========\n");
    print_all_heap_blocks();
    char *test5 = (char *)my_malloc(0x10);
    printf("\n=========Malloc 5=========\n");
    print_all_heap_blocks();
    my_free(test3);
    printf("\n=========Free 3=========\n");
    print_all_heap_blocks();
    char *test6 = (char *)my_malloc(0x10);
    printf("\n=========Malloc 6=========\n");
    print_all_heap_blocks();
    char *test7 = (char *)my_malloc(0x10);
    printf("\n=========Malloc 7=========\n");
    print_all_heap_blocks();
    h_meta->free_hook = &testHook;
    my_free(test7);
}
#endif
