#include "chall.h"

#include <stdint.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <stdio.h>
#include <math.h>
#include <pthread.h>
#include <arpa/inet.h>
#include <sys/socket.h>
#include <sys/types.h>
#include <sys/random.h>
#include <netdb.h>
#include <asm-generic/socket.h>
#include <netinet/in.h>

static const char flag[] =    "CCSC{r1ck_f0rg0t_t0_p4d_ag41n!!}";
/* static const char flag[] = "CCSC{redactedredactedredactedre}"; */
static const char echo_msg[] = "The Cromulons said: Show me what you got! ";

static uint16_t calculate_checksum(uint16_t *data, uint8_t len)
{
    uint16_t sum = 0;
    uint8_t  overflows = 0;
    uint16_t *cur = data;

    int counter = len;
    while (counter > 0) {
        if (__builtin_add_overflow(sum, *cur, &sum)) {
            overflows++;
        }
        cur++;
        counter -= 2;
    }

    sum += overflows;
    sum = ~sum;
    return sum;
}

static int recv_all(int sock, char *dest, int to_receive)
{
    int remaining = to_receive;
    int received;
    int tot_received = 0;
    char *buffer = dest;

    while (remaining > 0) {

        if ((received = recv(sock, buffer, remaining, 0)) < 0) {
            perror("recv");
            return -1;
        }

        if (received == 0) {
            return 0;
        }

        remaining -= received;
        buffer += received;
        tot_received += received;

    }

    return tot_received;
}

static int send_all(int sock, char *src, int to_send)
{
    int remaining = to_send;
    int tot_sent = 0;
    int sent;
    char *buffer = src;

    while (remaining > 0) {

        if ((sent = send(sock, src, remaining, 0)) < 0) {
            perror("send");
            return sent;
        }
        remaining -= sent;
        buffer += sent;
        tot_sent += sent;
    }

    return tot_sent;
}

static int validate_checksum(char *pkt, uint8_t data_len)
{
    uint16_t checksum;

    checksum = calculate_checksum((uint16_t *) pkt, data_len + sizeof(struct packet_hdr));

    if (checksum == CORRECT_CHECKSUM) {
        return 0;
    }

    return -1;
}

static int check_passphrase(char *pass, char *guess, uint8_t data_len)
{
    uint8_t correct;

    if (data_len != PASS_LEN) {
        return 0;
    }

    correct = 1;
    for (int i = 0; i < PASS_LEN; i++) {
        correct &= pass[i] == guess[i];
    }

    return correct;
}

static int send_letter(int sock, char *buf)
{
    int ret;
    int pass_strlen;
    char pkt[CORRECT_PASS_BUFLEN];
    uint16_t checksum;
    int flag_len;

    struct packet_hdr *packet_hdr;

    memset(&pkt, 0, CORRECT_PASS_BUFLEN);
    packet_hdr = (struct packet_hdr*) pkt;
    pass_strlen = strlen(CORRECT_PASS_STR);
    flag_len = strlen(flag);

    packet_hdr->repeats = 1;
    packet_hdr->data_len = pass_strlen + FLAG_LETTER_REPEAT;
    packet_hdr->proto = htons(CORRECT_PASS_PROTO);

    memcpy(pkt + sizeof(struct packet_hdr), CORRECT_PASS_STR, pass_strlen);
    memcpy(pkt + sizeof(struct packet_hdr) + pass_strlen, buf, FLAG_LETTER_REPEAT);

    checksum = calculate_checksum((uint16_t *) pkt, CORRECT_PASS_BUFLEN);
    packet_hdr->checksum = checksum;

    ret = send_all(sock, pkt, CORRECT_PASS_BUFLEN);

    return ret;
}

static int send_hdr_packet(int sock, uint8_t proto)
{
    int ret;
    uint16_t checksum;

    struct packet_hdr packet_hdr;

    memset(&packet_hdr, 0, sizeof(struct packet_hdr));

    packet_hdr.repeats = 0;
    packet_hdr.data_len = 0;
    packet_hdr.proto = htons(proto);

    checksum = calculate_checksum((uint16_t *) &packet_hdr, sizeof(struct packet_hdr));
    packet_hdr.checksum = checksum;

    ret = send_all(sock, (char *) &packet_hdr, sizeof(struct packet_hdr));

    return ret;
}

static int get_flag(char *pkt, int client_sock)
{
    struct packet_hdr *packet_hdr;
    char *buf;
    char *cli_pass;
    char passphrase[PASS_LEN];
    int ret;
    uint8_t letter_idx;

    packet_hdr = (struct packet_hdr *) pkt;

    letter_idx = packet_hdr->repeats;

    if (letter_idx >= strlen(flag)) {
        ret = send_hdr_packet(client_sock, WRONG_IDX_PROTO);
        if (ret < 0) {
            return -1;
        }
    }

    cli_pass = pkt + sizeof(struct packet_hdr);

    ret = getrandom(passphrase, PASS_LEN, 0);

    if (ret < 0) {
        perror("getrandom");
        return -1;
    }

    buf = malloc(FLAG_LETTER_REPEAT);

    if (buf == NULL) {
        perror("Malloc error");
        return -1;
    }

    for (int i = 0; i < FLAG_LETTER_REPEAT; i++) {
        memcpy(buf + i, &flag[letter_idx], 1);
    }

    ret = check_passphrase(passphrase, cli_pass, packet_hdr->data_len);
    if (ret == 1) {
        ret = send_letter(client_sock, buf);
        if (ret < 0) {
            goto cleanup;
        }
    } else {
        ret = send_hdr_packet(client_sock, WRONG_PASS_PROTO);
        if (ret < 0) {
            goto cleanup;
        }
    }

cleanup:
    free(buf);
    return ret;
}

// Echo back data repeat times
static int echo_back(char *pkt, int client_sock)
{

    struct packet_hdr *packet_hdr;
    int buflen;
    int data_len;
    int echo_len;
    int msg_len;
    char *buf;
    char *data;
    char *echo_buf;
    uint16_t checksum;

    packet_hdr = (struct packet_hdr *) pkt;
    data = pkt + sizeof(struct packet_hdr);

    msg_len = strlen(echo_msg);
    data_len = packet_hdr->data_len;
    echo_len = data_len * packet_hdr->repeats;
    buflen = msg_len + echo_len + sizeof(struct packet_hdr);

    buf = malloc(buflen);
    if (buf == NULL) {
        perror("Malloc error");
        return -1;
    }

    memset(buf, 0, buflen);

    packet_hdr = (struct packet_hdr *) buf;
    packet_hdr->proto = htons(ECHO_PROTO);
    packet_hdr->data_len = msg_len + echo_len;
    packet_hdr->repeats = 0;

    checksum = calculate_checksum((uint16_t *) buf, buflen);
    packet_hdr->checksum = checksum;

    memcpy(buf + sizeof(struct packet_hdr), echo_msg, strlen(echo_msg));

    echo_buf = buf + sizeof(struct packet_hdr) + strlen(echo_msg);
    for (int i = 0; i < echo_len; i += data_len) {
        memcpy(echo_buf + i, data, data_len);
    }

    if ((send_all(client_sock, buf, buflen)) != buflen) {
        perror("send_all()");
        free(buf);
        return -1;
    }

    free(buf);
    return 0;
}

static int setup(char *port)
{
    struct addrinfo hints;
    struct addrinfo *server_info;
    int retval;
    int sock;
    int yes = 1;

    memset((void *) &hints, 0, sizeof(struct addrinfo));
    hints.ai_family = AF_INET;
    hints.ai_socktype = SOCK_STREAM; // TCP socket
    hints.ai_flags = AI_PASSIVE;

    if ((retval = getaddrinfo(NULL, port, &hints, &server_info)) != 0) {
        perror("getaddrinfo");
        exit(1);
    }

    if ((sock = socket(server_info->ai_family,
                       server_info->ai_socktype, server_info->ai_protocol)) < 0) {
        perror("socket");
        exit(1);
    }

    if ((retval = setsockopt(sock,
                             SOL_SOCKET, SO_REUSEADDR, &yes, sizeof yes)) < 0) {
        perror("setsockopt");
        exit(1);
    }

    if ((retval = bind(sock, server_info->ai_addr, server_info->ai_addrlen)) < 0) {
        perror("bind");
        exit(1);
    }

    if ((retval = listen(sock, MAX_LISTEN)) < 0) {
        perror("listen");
        exit(1);
    }

    freeaddrinfo(server_info);

    return sock;
}

static void *handle_client(void *data)
{
    uint8_t data_len;
    uint16_t proto;
    int ret;
    struct packet_hdr *packet_hdr;
    char pkt[sizeof(struct packet_hdr) + 0x100];
    char *pkt_heap;
    int alloc_size;

    int client_sock = *(int *) data;

    while (1) {

        ret = recv_all(client_sock, (char *) &pkt, sizeof(struct packet_hdr));

        if (ret == 0) {
            continue;
        }

        if (ret != sizeof(struct packet_hdr)) {
            perror("Error while receiving data");
            goto cleanup;
        }

        packet_hdr = (struct packet_hdr*) pkt;
        data_len = packet_hdr->data_len;

        ret = recv_all(client_sock, pkt + sizeof(struct packet_hdr), data_len);
        if (ret != data_len) {
            perror("Error while receiving data");
            goto cleanup;
        }

        alloc_size = data_len + sizeof(struct packet_hdr);
        pkt_heap = malloc(alloc_size);
        memcpy(pkt_heap, pkt, alloc_size);

        ret = validate_checksum(pkt_heap, data_len);

        if (ret < 0) {
            ret = send_hdr_packet(client_sock, WRONG_CHECKSUM_PROTO);
            if (ret < 0) {
                goto cleanup;
            }
            free(pkt_heap);
            continue;
        }

        proto = ntohs(packet_hdr->proto);

        if (proto == ECHO_PROTO) {
            ret = echo_back(pkt_heap, client_sock);
            if (ret < 0) {
                goto cleanup;
            }
        } else if (proto == FLAG_PROTO) {
            ret = get_flag(pkt_heap, client_sock);
            if (ret < 0) {
                goto cleanup;
            }
        } else {
            send_hdr_packet(client_sock, WRONG_PROTO_PROTO);
        }
        free(pkt_heap);

    }

    cleanup:
        close(client_sock);
        pthread_exit(NULL);
}

static void serve(int listen_sock)
{
    int client_sock;
    struct sockaddr_in client_addr;
    pthread_t thread;
    socklen_t addr_len;
    int retval;

    while (1) {

        addr_len = sizeof(client_addr);
        if ((client_sock = accept(listen_sock, (struct sockaddr*) &client_addr, &addr_len)) < 0) {
            perror("accept");
            continue;
        }

        if ((retval = pthread_create(&thread, NULL, handle_client, (void *)&client_sock)) < 0) {
            perror("pthread_create");
            continue;
        }

    }

}

int main(int argc, char *argv[])
{
    int sock;
    char *port;

    if (argc < 2) {
        puts("Usage: ./server LPORT");
    }

    port = argv[1];
    sock = setup(port);

    serve(sock);

    return 0;
}
