#include <stdio.h>
#include <sys/types.h>
#include <unistd.h>
#include <fcntl.h>
#include <dirent.h>

#define PASS_HASH 0x20
#define PASS_LEN 0x2000
#define BUF_LEN 0x100

#include "openssl/sha.h"
#include <string.h>


char* sha256(char* line, unsigned char* hash) {
    SHA256_CTX sha256;
    SHA256_Init(&sha256);
    SHA256_Update(&sha256, line, strlen(line));
    SHA256_Final(hash, &sha256);
    return hash;
}


int check_pass(char* password_hash) {
    char password[PASS_HASH];
    unsigned char input_hash[SHA256_DIGEST_LENGTH];
    unsigned char input_hash_hex[2*SHA256_DIGEST_LENGTH + 1] = "";

    // read password
    read(0, password, PASS_LEN);

    // hash password
    sha256(password, input_hash);

    for (int i = 0; i < SHA256_DIGEST_LENGTH; i++) {
        sprintf(input_hash_hex, "%s%02x", input_hash_hex, input_hash[i]);
    }
    return strcmp(password_hash, input_hash_hex) == 0;
}

int main() {
    FILE *fp;
    char password_hash[2*SHA256_DIGEST_LENGTH+1];
    char buf[BUF_LEN];

    DIR *dp;
    struct dirent *dir_entry;

    // disable buffering
    setbuf(stdout, 0);

    // open directory
    dp = opendir(".");

    // read password hash
    fp = fopen("password.txt","r");

    // load password hash
    fread(password_hash, sizeof(char), 2*SHA256_DIGEST_LENGTH, fp);
    password_hash[2*SHA256_DIGEST_LENGTH] = '\0';
    printf("%s\n", password_hash);

    // chroot into a jail
    printf("About to chroot for extra security of flag.txt");
    printf("\n");
    setuid(0);
    chroot("./jail");   // create jail
    chdir("./jail");    // get into the jail
    setuid(0xe4ff);     // swich to a VEEERY RANDOM uid

    // check login
    if (check_pass(password_hash)) {
        printf("Successful login\n");
        while ((dir_entry = readdir(dp)) != NULL) {
            printf("%s\n", dir_entry->d_name);
        }
    }

    // close descriptors
    fclose(fp);
    closedir(dp);

    return 0;
}
