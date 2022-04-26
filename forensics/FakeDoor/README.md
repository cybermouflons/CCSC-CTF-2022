# FakeDoor

**Category**: Forensics

**Author**: icyDux

## Description
Rick was furious when he heard that his naïve nephew Morty clicked on a phishing e-mail about Real Fake Doors. Fortunately, Rick had managed to take a memory snapshot before Morty's computer was fully infected. Help Rick to find out what happened.


## Points

100

<details>
<summary>Reveal Spoiler</summary>
	
	1. Linux_lsof plugin shows that the backd000r process has an opened file named s3cr3t.

	2. Linux_volshell plugin should be used to determine the inode number of the opened file.

	3. Run the following commands in the volshell:
		- cc(pid=1685)
		- for fd in self._proc.lsof():
		- dt(fd[0]) (find the f_inode of s3cr3t)
	5. Dump the s3cr3t file using: volatility -f dump.mem --profile=LinuxDebian_3_16_0-11-amd64_profilex64 linux_find_file --inode=0xffff88007a5010a0 -O s3cr3t

</details>
