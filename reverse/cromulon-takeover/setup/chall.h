#include <stdint.h>

#define CORRECT_PASS_STR "Correct password! You can have a flag letter: "

#define WRONG_PASS_BUFLEN strlen(WRONG_PASS_STR) + sizeof(struct packet_hdr)

#define PKT_SIZE 200
#define PASS_LEN 16
#define MAX_LISTEN 10
#define CORRECT_CHECKSUM 0

#define ECHO_PROTO 0x50
#define ECHO_REPLY_PROTO 0x51
#define FLAG_PROTO 0x80
#define FLAG_REPLY_PROTO 0x81
#define WRONG_CHECKSUM_PROTO 0x30
#define WRONG_PASS_PROTO 0x31
#define WRONG_PROTO_PROTO 0x32
#define WRONG_IDX_PROTO 0x33
#define CORRECT_PASS_PROTO 0x21

#define FLAG_LETTER_REPEAT 0x20
#define CORRECT_PASS_BUFLEN strlen(CORRECT_PASS_STR) + FLAG_LETTER_REPEAT + sizeof(struct packet_hdr)

struct packet_hdr {

  uint16_t proto;
  uint8_t repeats;
  uint8_t data_len;
  uint16_t checksum;

} __attribute__((packed));
