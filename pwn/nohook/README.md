# nohook
**Category:** pwn

**Author:** s3nn__

## Description
No hooks, no problem! I know that new situations can be intimidating. You’re lookin’ around and it’s all scary and different, but y’know, meeting them head-on, charging into ‘em like a bull — that’s how we grow as pwners.


## Solution
<details>
 <summary>Reveal Spoiler</summary>

There are two vulnerabilities: a read-after-free and an off-by-null byte overflow. libc2.34 is used, compiled tcache support. Players need to exploit the two vulnerabilities to create overlapping chunks as an arbitrary write primitive which can be used to leak the stack and overwrite a return address.

A solution that uses the House of Einherjar is provided in [sol.py](./sol/sol.py). Use the following:

Run against local docker container<br>
<code>
	python3.7 sol.py R LHOST
</code>

Run against CyberRanges (IP might change in [sol.py](./sol/sol.py))<br>
<code>
	python3.7 sol.py R
</code>

Run against local binary<br>
<code>
	python3.7 sol.py
</code>

</details>
