.PHONY: all
.PHONY: clean

CC=gcc
CFLAGS=-static -s

solver.bin: solver.c
	$(CC) -o $@ $<

all: clean solver.bin
	./solver.bin ../public/flag.enc

clean:
	rm -rf *.bin