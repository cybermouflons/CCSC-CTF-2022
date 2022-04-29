#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <openssl/rc4.h>
#include <netdb.h>
#include <netinet/in.h>
#include <sys/socket.h>
#include <sys/types.h>

const unsigned char flag[] = {
  0x99, 0x7e, 0x0f, 0x75, 0xf6, 0xd3, 0xe8, 0xca, 0x2f, 0xe5, 0xb0, 0xe9,
  0x5f, 0x70, 0x31, 0xee, 0x51, 0xcb, 0x35, 0x52, 0xf4, 0x47, 0x84, 0x74,
  0xc7, 0x9b, 0xa3, 0x49, 0x93, 0x1b, 0x2f, 0x4f, 0x26, 0x19, 0x2f, 0x64,
  0x1e
};


const unsigned char x[] = {
  0x01, 0x00, 0x00, 0x00, 0x00, 0x01, 0x01, 0x00, 0x01, 0x01, 0x01, 0x00,
  0x01, 0x01, 0x00, 0x00, 0x00, 0x01, 0x01, 0x01, 0x01, 0x00, 0x00, 0x00,
  0x00, 0x00, 0x01, 0x01, 0x01, 0x01, 0x00, 0x01, 0x01, 0x01, 0x01, 0x01,
  0x00, 0x01, 0x00, 0x01, 0x01, 0x00, 0x00, 0x01, 0x01, 0x00, 0x01, 0x00,
  0x00, 0x00, 0x01, 0x00, 0x00, 0x00, 0x00, 0x01, 0x01, 0x00, 0x00, 0x00,
  0x01, 0x00, 0x01, 0x00
};

const char welcome[] = "You have to wait two minutes before you send the weights\n";
const char message[] = "Please send the weights\n";

void decrypt(unsigned char *w,unsigned char *out){
	RC4_KEY rc4_key;
	unsigned long long *y = calloc(8,sizeof(unsigned long long));
	unsigned char key_data[8];
	unsigned long long k=0;

        memset(&key_data,0x0,8);


	for (int i = 0 ; i < 8 ; i++){
		for (int z = 0 ; z < 8 ; z++){
			y[i] |= (unsigned long long)x[(i*8)+z] << (7-z)*8;
		}
		k += (y[i]*w[i]);
	}
	memcpy(&key_data,&k,8);
	RC4_set_key(&rc4_key,8,&key_data);
	RC4(&rc4_key,37,&flag,out);
}

int main()
{
	int sockfd, connfd, len;
	struct sockaddr_in servaddr, cli;
        unsigned char out[38];
        unsigned char *w = calloc(8,sizeof(unsigned char));

	// socket create and verification
	sockfd = socket(AF_INET, SOCK_STREAM, 0);
	if (sockfd == -1) {
		exit(0);
	}
	bzero(&servaddr, sizeof(servaddr));

	// assign IP, PORT
	servaddr.sin_family = AF_INET;
	servaddr.sin_addr.s_addr = htonl(INADDR_ANY);
	servaddr.sin_port = htons(10002);

    	// Binding newly created socket to given IP and verification
	if ((bind(sockfd, (struct sockaddr_in*)&servaddr, sizeof(servaddr))) != 0) {
		exit(0);
	}
	// Now server is ready to listen and verification
	if ((listen(sockfd, 5)) != 0) {
		exit(0);
	}
	len = sizeof(struct sockaddr_in); 

	for (;;){
		connfd = accept(sockfd, (struct sockaddr_in*)&cli,&len);
		if (connfd < 0) {
			exit(0);
		}
		memset(&out,0x0,38);
		memset(w,0x0,8);
		write(connfd,welcome,sizeof(welcome)-1);
		sleep(120);
		read(connfd,w,0x8);
		decrypt(w,&out);
		write(connfd,out,sizeof(out));
		close(connfd);
	}
	close(sockfd);
}
