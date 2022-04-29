#include <time.h>
#include <stdio.h>
#include <fcntl.h>
#include <errno.h>
#include <unistd.h>
#include <string.h>
#include <stdlib.h>
#include <stdint.h>

// Function prototypes
void show_usage(void);
void print_stderr(const char *);
ssize_t write_full(int, const void *, size_t);
uint8_t transform(uint8_t);

int main(int argc, char *argv[])
{

    // check arguments
    if (argc != 3) {
        show_usage();
        exit(EXIT_FAILURE);
    }

    // open input file
    errno = 0;
    int ifd = open(argv[1], O_RDONLY);
    if (ifd < 0) {
        perror("open");
        exit(EXIT_FAILURE);
    }

    // open output file
    if (strcmp(argv[1], argv[2]) == 0) {
        print_stderr("Output file can't be the same as input.\n");
        exit(EXIT_FAILURE);
    }
    
    errno = 0;
    int ofd = open(argv[2], O_CREAT | O_WRONLY | O_TRUNC, S_IRUSR | S_IWUSR);
    if (ofd < 0) {
        perror("open");
        exit(EXIT_FAILURE);
    }

    // encrypt
    int c;
    ssize_t nread;

    // init seed
    (void)srand(time(NULL));

    do {

        errno = 0;
        nread = read(ifd, &c, 1);

        if (nread == 0) { break; }

        // byte transformation
        c = transform(c);

        write_full(ofd, &c, 1);

    } while (1);

    // close input fd
    errno = 0;
    if (close(ifd) < 0) {
        perror("close");
        exit(EXIT_FAILURE);
    }
    
    // close output fd
    errno = 0;
    if (close(ofd) < 0) {
        perror("close");
        exit(EXIT_FAILURE);
    }
    return 0;
}

void show_usage(void)
{
    const char msg[] = "Usage: chall01 <input> <output>\n";
    write_full(STDERR_FILENO, msg, strlen(msg));
}

void print_stderr(const char *msg)
{
    write_full(STDERR_FILENO, msg, strlen(msg));
}

ssize_t write_full(int fd, const void *buf, size_t size)
{
    ssize_t nwritten = 0;
    while (size > 0) {
        do {
            errno = 0;
            nwritten = write(fd, buf, size);
        } while ((nwritten < 0) && (errno == EINTR || errno == EAGAIN));

        if (nwritten < 0) {
            perror("write_full");
            return nwritten;
        }

        size -= nwritten;
        buf += nwritten;
    }
    return 0;
}

uint8_t transform(uint8_t c)
{
    return c ^ rand();
}
