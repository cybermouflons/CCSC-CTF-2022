# Supersingular Finite Curve
**Category:** crypto

**Author:** _Rok0'sBasilisk_

## Description

In response to the Central Finite Curve, evil Morty is forming the Supersingular Finite Curve. This is a portion of the multiverse, where Mortys dominate over Ricks. Not sure if Morty's smart enough to complete this.. his maths may be out of order...

## Solution
<details>
 <summary>Reveal Spoiler</summary>

Challenge provides params on a supersingular curve. Supersingular curves are know to have a small embedding degree. Curves with small embedding degrees are vulnerable to MOV attack which maps the ECDLP to DLP in a finite field that is easier to solve.

Review [setup.ipynb](setup/setup.ipynb) for a working solution. Note that you need a Jupyter Sage kernel for that to run. 

Use [run_jupyter.sh](setup/run_jupyter.sh) to run one.
</details>