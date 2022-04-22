# Meeseeks and Destroy
**Category:** pwn

**Author:** condiom

## Description
Rick: This is a Meeseeks box. Let me show you how it works. You press this. <br />
(meeseeks spawns)<br />
Meeseeks: I'm Mr. Meeseeks! Look at me!<br />
Rick: You make a request. Mr. Meeseeks, open Jerry's stupid mayonnaise jar.<br />
Meeseeks: Yes, siree!<br />
(Meeseeks grabs mayonnaise jar as Rick explains.)<br />
Rick: The Meeseeks fulfills the request.<br />
(Meeseeks opens jar and hands to jerry.)<br />
Meeseeks: All done!<br />
Jerry: [amazed] Wow!<br />
Rick: And then it stops existing.<br />
(Meeseeks vanishes into particles in air.)<br />



## Solution
<details>
 <summary>Reveal Spoiler</summary>

A custom implementation of a heap memory management library has been created. <br />
There is a buffer overflow vulnerability when creating  Mr. Meeseeks that allows you to override the metadata of the next chunk of memory.<br />
Goal is to trick the custom library into giving you a chunk that point to the GOT and leak a memory adress libc without breaking the execution flow.</br> 
Then overide the the custom library myfree GOT with the system function and call it with the "bin/sh" string to get a shell  

A solution that performs the above steps is provided in [sol.py](./sol/sol.py). Use the following:

Run against local docker container<br>
<code>
	python3.7 sol.py R LHOST
</code>

Run against CyberRanges (IP might change in [sol.py](./sol/sol.py))<br>
<code>
	python3.7 sol.py R
</code>


</details>