# Total Rickvenge
**Category:** pwn, script

**Author:** condiom

## Description
The only friends we got is Rick and Morty, Morty! We gotta take revenge on those parasites, Morty. <br/>
Giving them a taste of their own BURRRP their own medicine. We gotta impose the impostors, Morty.


## Solution
<details>
 <summary>Reveal Spoiler</summary>

There are two binaries given in random order to the user after he connects to the service:
1. Buffer overflow return address.<br/>
The goal is to override the return address with realRick(we need to find iAmRealRick{X} function that exits(0))

2. Format string vulnerability<br/>
The goal is to override puts GOT function with realMorty(we need to find iAmRealMorty{X} function that exits(0))

A solution that performs the above steps is provided in [sol.py](./sol/sol.py). Use the following:

Run against local docker container<br>
<code>
    python3.7 sol.py
</code>

Run against CyberRanges (IP might change in [sol.py](./sol/sol.py))<br>
<code>
    python3.7 sol.py R
</code>


</details>