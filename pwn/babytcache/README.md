# babytcache
**Category:** pwn

**Author:** s3nn__

**Author Difficulty:** Easy

## Description
Morty's first heap challenge !

## Points
dynamic

## Solution
<details>
 <summary>Reveal Spoiler</summary>

There is a double-free vulnerability in the binary; libc2.28 is used, compiled with tcache support. Players are given a libc leak and just need to exploit the double-free vulnerability to carry out a tcachebin dup to achieve code execution by overwriting one of the malloc hooks.

Players are also provided with the source code and the binary is setup to use the same version of libc as the remote, with debug symbols present; this limits the setup and reverse engineering efforts for new players as this challenge is meant to introduce players to one of the most foundatinal concepts regarding glibc heap exploitation.

A solution that performs the above steps is provided in [sol.py](./sol/sol.py)
Use the following:

Run against local docker container<br>
<code>
	python3.7 sol.py LR
</code>

Run against CyberRanges (IP might change in [sol.py](./sol/sol.py))<br>
<code>
	python3.7 sol.py R HOST=<cyberranges_ip>
</code>

Run against local binary<br>
<code>
	python3.7 sol.py
</code>

</details>
