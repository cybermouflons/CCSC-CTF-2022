#include <stdio.h>
#include <time.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <sys/stat.h>
#include <errno.h>

int try_decrypt(long, char *, char *, size_t);

int main(int argc, char *argv[])
{
    // return code
    int ret = 0; 
    int found = 0;
    char dec[] = "CCSC2022";  // known plaintext
    size_t dec_len = strlen(dec) - 1;
    char buf[dec_len];

    if (argc != 2) {
        fprintf(stderr, "Usage: solve <input-file>\n");
        return -1;
    }

    // open encrypted file
    errno = 0;
    FILE *fin = fopen(argv[1], "rb");
    if (NULL == fin) {
        perror("fopen");
        return EXIT_FAILURE;
    }

    // find modification time in seconds
    struct stat st;
    errno = 0;
    ret = lstat(argv[1], &st);
    if (ret < 0) {
        perror("lstat");
        ret = EXIT_FAILURE;
        goto err;
    }

    // read first len bytes (known plaintext length)
    fread(buf, sizeof(char), dec_len, fin);
    if (ferror(fin) != 0) {
        perror("fread");
        ret = EXIT_FAILURE;
        goto err;
    }

    // modification time in seconds
    long seed_start = st.st_mtim.tv_sec;
    printf("[#] Trying seed: %lu\n", seed_start);

    found = try_decrypt(seed_start, buf, dec, dec_len);
    if (found) {
        // initialize PRNG
        (void)srand(seed_start);
      
        // decrypt
        int c;
        (void)rewind(fin);
        while (fread(&c, sizeof(char), 1, fin) != 0) {
            c ^= (char)rand();
            putchar(c);
        }
    }

err:
    fclose(fin);
    return ret;
}

int try_decrypt(long seed, char *enc, char *dec, size_t len)
{

    (void)srand(seed);

    char c;
    for (size_t i = 0; i < len; i++) {
        c = enc[i] ^ (char)rand();
        if (dec[i] != c) { return 0; }
    }

    return 1;
}
