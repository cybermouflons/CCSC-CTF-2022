# FakeDoor

**Category**: Forensics

**Author**: icyDux

## Description
Rick was furious when he heard that his naïve nephew Morty clicked on a phishing e-mail about Real Fake Doors. Fortunately, Rick had managed to take a memory snapshot before Morty's computer was fully infected. Help Rick to find out what happened.


## Points

100

<details>
<summary>Reveal Spoiler</summary>
Linux_lsof plugin shows that the backd000r process has an opened file named s3cr3t.
Linux_Volshell plugin should be used to determine the inode number of the opened file.
Run the following commands in the volshell:
	cc(pid=1378)
	for fd in self._proc.lsof():
		//where fd is a tuple where the first entry is a linux_file object
		dt(fd[0])->f_inode is the inode number of the s3cr3t file
Dump the s3cr3t file using: volatility -f dump.mem --profile=LinuxDebian_3_16_0-11-amd64_profilex64 linux_find_file --inode=0xffff88001a785850 -O s3cr3t

</details>
