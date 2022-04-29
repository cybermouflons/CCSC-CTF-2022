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
$o = unserialize($_GET['universe']);

$title = "CCSC 2022";

$header = <<< EOF
  <table bgcolor="#000000" width="100%" border="0" 
    cellspacing="0" cellpadding="0">
    <tr>
      <td><center><h1 style="color: red;">{$title}</h1></center></td>
    </tr>
  </table>
EOF;


$leftcolumn = <<< EOF
  <center><h3 style="color: red;">M3nu</h2>
  <br/><a href="index.php">H0m3</a>
  <br/><a href="info.php">1nf0</a>
  <br/><a href="s3r1al1z3.php">F1l3</a>
  <br/></center>
EOF;


$content = <<< EOF
  <p>
    "The universe is basically a good hint. It leeds to escape. It creates files to idiot's servers just to hack them." - Rick
EOF;


$mainbody = <<< EOF
  <table width="100%" border="0" cellspacing="0"
    cellpadding="0" id="full">
    <tr valign="top">
      <td nowrap bgcolor="#000000" width="125px">
        {$leftcolumn}
      </td>
      <td>
        <center>
        {$content}
	</center>
	</td>
    </tr>
  </table>
EOF;


$footer = <<< EOF
  <table width="100%" bgcolor="#000000" border="0" 
    cellspacing="0" cellpadding="0">
    <tr>
      <td><p style="color: red;" align="center"><i>Created by Kotsios - 2022</i></td>
    </tr>
  </table>
EOF;


$style = <<< EOF
  <style type="text/css">
      html, body {
      background: url(bg.jpg) no-repeat center center fixed;
      background-size: cover;
      margin: 0;
      padding: 0;
      border: none;
    }
    #full { height: 100%; }
  </style>
EOF;


$html = <<< EOF
  <html>
  <head>
    <title>{$title}</title>
    {$style}
  </head>
  <body>
    {$header}
    {$mainbody}
    {$footer}
  </body>
  </html>
EOF;

echo $html;

?>
