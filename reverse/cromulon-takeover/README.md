
**Category**: Reversing/Pwn

**Author**: neo

## Description

Rick is trying to build a server to let people send
their songs to the Cromulons. If they really like your
song, they might even reward you with a part of the flag.
Make sure the checksum of your packets is correct though,
you definitely don't wanna anger the Cromulons! I heard
they are so powerful they can make your brain leak out
of your ears...

<details>
<summary>Reveal Spoiler</summary>
The checksum calculation function has a 1-byte leak
when the size of the packet is odd. Contentants need
to
</details>
