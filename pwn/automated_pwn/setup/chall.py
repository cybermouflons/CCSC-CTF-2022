import random
from base64 import b64encode, b64decode
from subprocess import run, PIPE
import os

def createProg(binary):
    f = open("temp.c", "w")
    f.write(binary["code"])
    f.close()

    cmd = 'gcc {}  -o temp -xc temp.c'.format(binary["gccFlags"])
    run(cmd.split())

    f = open("temp", "rb")
    b64Prog = b64encode(f.read())
    f.close()
    os.remove("./temp.c")
    return b64Prog


def runTemp(progInput):
    print(progInput)
    p = run(['./temp'], stdout=PIPE,
            input=progInput)
    return p.stdout, p.returncode


def runB64(b64Prog, progInput):
    binary = b64decode(b64Prog)
    f = open("temp", "wb")
    f.write(binary)
    f.close()

    p = run(['./temp'], stdout=PIPE,
            input=str(progInput)+'\n', encoding='ascii')
    return p.stdout, p.returncode

MAX_FUNCTIONS = 10
rick = random.randint(0,MAX_FUNCTIONS-1)
notRick = ""
for i in range(0,MAX_FUNCTIONS):
    if i == rick:
        notRick += """
        void iAmRealRick"""+ str(i) + """()
        {
            printf("Thank you for saving me");
            exit(0);
        }
        """
    else:
        notRick = notRick + """
        void iAmRealRick"""+ str(i) + """()
        {
            printf("Sucker");
            exit(1);
        }
        """
morty = random.randint(0,MAX_FUNCTIONS-1)
notMorty = ""
for i in range(0,MAX_FUNCTIONS):
    if i == morty:
        notMorty = notMorty + """
        void iAmRealMorty"""+ str(i) + """()
        {
            printf("Thank you for saving me");
            exit(0);
        } 
        """
    else:
        notMorty = notMorty + """
        void iAmRealMorty"""+ str(i) + """()
        {
            printf("Sucker");
            exit(1);
        }
        """
binaries = [
    {
        "code": """
    #include <stdio.h>
    #include <stdlib.h>
    #include <string.h>
    #include <ctype.h>

    """ + notRick + """
    int main(int argc, char **argv)
    {
        char name[256];
        printf("Hi am Rick. Who are you?\\n");
        scanf("%s", name);
        printf("Hello %s \\n",name);
        return 1;
    }
""",
        "gccFlags": "-no-pie -fno-pie -fno-stack-protector"
    },
    {
        "code": """
    #include <stdio.h>
    #include <stdlib.h>
    #include <string.h>
    #include <ctype.h>
    """ + notMorty + """
    int main(int argc, char **argv)
    {
        char name[0xff];
        printf("Hi am Morty. Who are you?\\n");
        int t = read(0, name, 0xff);
        if(name[t-1] == '\\n'){
            name[t-1] = '\\0';
        }
        name[t] = '\\0';
        printf("Hello ");
        printf(name);
        printf(" \\n");
        return 1;
    }
    """,
        "gccFlags": "-no-pie -fno-pie -Wno-format-security -Wno-implicit-function-declaration"
    }
]

# binaries = binaries[1:]

random.shuffle(binaries)

print("Please help me defeat the parasites and find the real Rick and Morty.")
print("We were able to intercept this communications between parasites.")
print("It seems that we can run them through a machine with an input.")
print("Can you help me find the correct input?")

successCounter = 0
for i in range(0, len(binaries)):
    b64Prog = createProg(binaries[i])

    print("Message:")
    print(b64Prog.decode())
    print("Message end")
    payload = input("Enter your input:")
    payload = payload.encode('utf8','surrogateescape')
    output, returncode = runTemp(payload)
    os.remove("./temp")
    if returncode == 0:
        successCounter = successCounter + 1
        print("Thank you kind friend. It seems we killed a parasite family. I hope you are not a parasite too")
    else:
        print("Input failed. The parasites killed Morty and Rick and now they are rule all the world")
        break
if successCounter == len(binaries):
    f = open("flag.txt", "r")
    flag = f.read()
    f.close()
    print(flag)
else:
    print("No flag for you")
