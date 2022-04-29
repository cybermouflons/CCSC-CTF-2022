# rickrop
**Category:** pwn

**Author:** s3nn__

**Author Difficulty:** Easy / Medium

## Description
Rick ROPs with style. Guaranteed to have the most fun you've had with this specific type of challenge.

## Points
dynamic

## Solution
<details>
 <summary>Reveal Spoiler</summary>

Simple format string bug; source code + docker setup is provided to limit reverse engineering. The binary is statically-compiled with all protections. The players get two passes to exploit the format string:
- They can use the first to leak a binary address to resolve the binary base, and a stack address to calculate the return address of the vulnerable echo() function as well as the the input buffer (that's also on the stack)
- They can use the second to hijack the flow of execution by overwriting the return address of the echo() function 

Since there are no one gadgets and library functions present, they need to pivot the stack somewhere and write a ROP chain to get a shell or read the flag.

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
