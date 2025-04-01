### Scenario ###
Your company runs a critical application on **Amazon EC2** that stores **sensitive customer data in an Amazon S3 bucket**. The security team has given the following security requirements:
- **The EC2 instances should have read/write access to the S3 bucket** but must **NOT** be able to delete objects.
- **No IAM users or roles should be able to access the S3 bucket directly** except the **EC2 instances** running **in a specific VPC** (`vpc-12345678`).
- The **EC2 instances should only access the S3 bucket using temporary credentials** (IAM roles), not static credentials.
- A **security guardrail** should be in place to **prevent accidental misconfigurations,** ensuring that no one modifies or weakens these security restrictions.

---

**IAM Role for EC2 Instances**
- Since EC2 instances should access S3 using temporary credentials, we need an **IAM Role** with **Amazon EC2 as a trusted entity**.
- Attach this policy to an IAM Role that is assigned to EC2 instances:
- The `Deny` statement ensures that even if another policy grants `DeleteObject`, it will still be blocked due to IAM's **explicit deny rule**.

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "s3:GetObject",
        "s3:PutObject"
      ],
      "Resource": "arn:aws:s3:::secure-customer-data/*"
    },
    {
      "Effect": "Deny",
      "Action": "s3:DeleteObject",
      "Resource": "arn:aws:s3:::secure-customer-data/*"
    }
  ]
}
```

**S3 Bucket Policy to Restrict Direct Access**
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "AWS": "arn:aws:iam::ACCOUNT_ID:role/EC2S3AccessRole"
      },
      "Action": ["s3:GetObject", "s3:PutObject"],
      "Resource": "arn:aws:s3:::secure-customer-data/*",
      "Condition": {
        "StringEquals": {
          "aws:SourceVpc": "vpc-12345678"
        }
      }
    },
    {
      "Effect": "Deny",
      "Principal": "*",
      "Action": "s3:*",
      "Resource": "arn:aws:s3:::secure-customer-data/*",
      "Condition": {
        "StringNotEquals": {
          "aws:SourceVpc": "vpc-12345678"
        }
      }
    }
  ]
}
```

**IAM Guardrails to Prevent Policy Changes**
- To **prevent unauthorized changes** to the S3 policy or IAM role, use **Service Control Policies (SCPs)** or **IAM Conditions**.
- Deny `iam:UpdateRolePolicy`
- Blocks modification of IAM policies & S3 bucket policies, except for a specific **Security Admin role**.
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Deny",
      "Action": [
        "iam:UpdateRolePolicy",
        "s3:PutBucketPolicy",
        "s3:DeleteBucketPolicy"
      ],
      "Resource": "*",
      "Condition": {
        "StringNotEquals": {
          "aws:PrincipalArn": "arn:aws:iam::ACCOUNT_ID:role/SecurityAdmin"
        }
      }
    }
  ]
}
```
