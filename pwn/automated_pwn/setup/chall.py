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

fakeFunction = ""
for i in range(0,random.randint(1,100)):
    fakeFunction = fakeFunction + """
     void loseFunction"""+ str(i) + """()
    {
        printf("Cool");
        exit(0);
    }
    """
binaries = [
    {
        "code": """
    #include <stdio.h>
    #include <stdlib.h>
    #include <string.h>
    #include <ctype.h>

    """ + fakeFunction + """
    void winFunction()
    {
        printf("Cool");
        exit(0);
    }
    int main(int argc, char **argv)
    {
        char name[256];
        printf("What is your name my friend:\\n");
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
    """ + fakeFunction + """
    void winFunction()
    {
        printf("Cool");
        exit(0);
    }
    int main(int argc, char **argv)
    {
        char name[0xff];
        printf("What is your name:\\n");
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

successCounter = 0
for i in range(0, len(binaries)):
    b64Prog = createProg(binaries[i])

    print("Base64 code:")
    print(b64Prog.decode())
    print("Base64 code end")
    payload = input("Enter your payload:")
    payload = payload.encode('utf8','surrogateescape')
    output, returncode = runTemp(payload)
    os.remove("./temp")
    # print("Exit code: {} Output {}".format(returncode, output))
    if returncode == 0:
        successCounter = successCounter + 1
        print("exploit success")
    else:
        print("exploit fail")
        break
    # output, returncode = runB64(b64Prog, progInput)
if successCounter == len(binaries):
    f = open("flag.txt", "r")
    flag = f.read()
    f.close()
    print(flag)
else:
    print("No flag for you")
