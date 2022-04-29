#include <stdio.h>
#include <sys/types.h>
#include <unistd.h>

#define BUF_SIZE 32
#define FLAG_MAX_SIZE 128

void secret() {
    FILE *fp;
    char buf[FLAG_MAX_SIZE] = "";
    printf("You found the secret!\n");

    fp = fopen("flag.txt","r");
    fread(buf, sizeof(char), FLAG_MAX_SIZE, fp);
    fclose(fp);
    printf("%s\n", buf);
}

int vuln() {
    char buf[BUF_SIZE];
    printf("Please provide an input\n");
    read(0, buf, BUF_SIZE*sizeof(char*));
    printf("ok\n");
    return 0;
}

int main()
{
    int pid = 0;
    char* input;
    int status = 0;

    // disable buffering
    setbuf(stdout, 0);

    printf("This software was designed so that it survives crashes\n");
    printf("Should I make you a fork?\n");

    while (1) {
        gets(input);
        printf("I'll make you one anyway :p\n");

        if ((pid = fork()) < 0) {
            // Handle fork error
            printf("Failed to fork\n");
        }
        else if (pid == 0) {
            // Child process
            vuln();
            return 0;
        }
        else {
            // Parent process
            wait(&status);
            printf("xxx\n");
            if (status != 0) {
                printf("feeew... This could have crashed the entire process\n");
                printf("Good thing we have this super robust mechanism\n");
            }
            printf("Should I make you another fork?\n");
        }

    }
  
    printf("How did you get here??!\n");
    secret();
    return 0;
}
