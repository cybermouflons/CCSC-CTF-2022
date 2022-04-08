all: dynamicNoPie

dynamicNoPie: clean pwnDynamicNoPie cleanObj libCopy
dynamic: clean pwnDynamic cleanObj libCopy
static: clean pwnStatic cleanObj libCopy

libCopy:
	cp setup/libc.so.6 public/libc.so.6

pwnDynamicNoPie: heapAllocator.so 
	gcc -o public/pwn setup/pwn.c -L./public -l:heapAllocator.so -no-pie
	gcc -o setup/pwn setup/pwn.c -L./public -l:heapAllocator.so -no-pie

pwnDynamic: heapAllocator.so 
	gcc -o public/pwn setup/pwn.c -L./public -l:heapAllocator.so
	gcc -o setup/pwn setup/pwn.c -L./public -l:heapAllocator.so

pwnStatic: heapAllocator.a
	gcc -O -c setup/pwn.c -o public/pwn.o -Wunused-result
	gcc -o public/pwn public/pwn.o -L./public -l:heapAllocator.a
	gcc -o setup/pwn public/pwn.o -L./public -l:heapAllocator.a

heapAllocator.so: heapAllocatorDynamic.o
	gcc -shared -o public/heapAllocator.so public/heapAllocator.o
	gcc -shared -o setup/heapAllocator.so public/heapAllocator.o

heapAllocator.a: heapAllocatorStatic.o
	ar rcs public/heapAllocator.a public/heapAllocator.o
	ar rcs setup/heapAllocator.a public/heapAllocator.o

heapAllocatorDynamic.o:
	gcc -c -fpic setup/heapAllocator.c -o public/heapAllocator.o

heapAllocatorStatic.o:
	gcc -O -c setup/heapAllocator.c -o public/heapAllocator.o

libTest: 
	gcc -O setup/heapAllocator.c -o public/heapAllocator -D DEBUG

libs: heapAllocator.so heapAllocator.a

clean:
	rm -f public/*
	rm -f setup/*.so setup/*.a
	rm -f setup/pwn

cleanObj:
	rm -f public/*.o public/*.gch
	rm -f setup/*.o public/*.gch