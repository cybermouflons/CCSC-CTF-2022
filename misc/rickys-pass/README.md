# Ricky's Pass
**Category:** misc

**Author:** kotsios

## Description

Ricky's Pass is a mess. Ricky stored his secret data inside the qr code files. Can you help Morty and Jerry to leak Ricky's data? Jerry believes that the first step is to research the implementation of the qr code because Ricky is not an idiot. On the other hand, Morty believes that Ricky is the most stupid man in the world.

## Solution
<details>
 <summary>Reveal Spoiler</summary>
 
 Inherently, QR codes has a standard UNSED bit.
The participants have to research and find the position of the unused bit and implement a script to found the flag.

To automate the process, a script like the one below can be used:
```bash
#!/bin/bash


cd qrcode/ # Replace this with the folder which contains the qrcodes

flag=""
for i in {1..632}; do
	if grep -q "x=\"12mm\" y=\"17mm\"" qr$i.html; then
		flag="$flag 1"
	else
		flag="$flag 0"
	fi
done

flag_no_spaces=`echo $flag | sed 's/ //g'`
last=`echo $flag_no_spaces | perl -lpe '$_=pack"B*",$_'`
echo $last
```

</details>
