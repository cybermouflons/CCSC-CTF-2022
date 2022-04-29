.PHONY: all
.PHONY: clean
.PHONY: solution

CC=gcc
CFLAGS=-static -s

encryptor.bin: encryptor.c
	mkdir -p ../public
	$(CC) $(CFLAGS) -o ../public/$@ $<

all: clean encryptor.bin
	../public/encryptor.bin flag.txt ../public/flag.enc

clean:
	rm -f *.bin flag.enc
