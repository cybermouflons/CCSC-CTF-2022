CC=clang++
CFLAGS=-fstack-protector-all -Wl,-z,now -Wl,-z,relro -fPIE -pie -fvisibility=default -flto -fsanitize=cfi -fsanitize-cfi-cross-dso

.PHONY: ctf debug

ctf:
		$(CC) $(CFLAGS) chall.cpp -o chall
		strip -s chall

debug:
		$(CC) $(CFLAGS) -g chall.cpp -o chall
