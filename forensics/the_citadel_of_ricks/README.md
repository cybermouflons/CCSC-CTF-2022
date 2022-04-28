# The Citadel of Ricks
**Category:** forensics

**Author:** R3D

## Description
The Citadel came under the authoritarian rule of President Morty (Evil Morty) who, after being elected President of The Citadel, committed a series of unprecedented purges against the de facto ruling Shadow Council and other personal political enemies. His number one enemy, Rick now lives in a dimension unknown even to his grandson Morty.  

Mr. Meeseeks which was summoned by Morty, intercepted some network traffic between the Ricks on the run. Can you help Mr.Meeseeks complete his task and Morty to find his grandpa?

## Points
N/A

## Solution
<details>
 <summary>Reveal Spoiler</summary>
    ```tshark -r portal.pcapng -Y 'http.request.method == "POST"' -T fields -e http.file_data > results.txt ```
    ```while read p; do printf "\x$(printf %x ${#p})"; done < results.txt```


A solution that performs the above is provided in [solution](./sol/solution)

</details>
