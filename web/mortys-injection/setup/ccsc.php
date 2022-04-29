<?php

$cmd2 = escapeshellcmd($_GET["name"]);
$cmd = escapeshellcmd($_GET["surname"]);

if(isset($cmd2)){
system($cmd." ".$cmd2);
}
if(strcmp($cmd2,'Morty')==0){
$content = <<< EOF
  <p>
"Nobody exists on purpose. Nobody belongs anywhere. We’re all going to die. Come watch TV." — Morty
EOF;
}
if(strcmp($cmd2,'Ricky')==0){
$content = <<< EOF
  <p>
"I don’t like it here, Morty. I can’t abide bureaucracy. I don’t like being told where to go and what to do. I consider it a violation. Did you get those seeds all the way up your butt?" — Rick
EOF;
}

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
  <br/><a href="ccsc.php?name=Morty&surname=Ricky">Morty</a>
  <br/><a href="ccsc.php?name=Ricky&surname=Morty">Ricky</a>
  <br/><a href="index.php">Back</a>
  <br/></center>
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
      background: url(weldone.jpg) no-repeat center center fixed;
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
