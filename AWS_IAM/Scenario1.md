###Scenario###
Your company has a multi-account AWS environment managed via AWS Organizations. You have a centralized security account that manages IAM roles and permissions for all other accounts (Dev, Staging, and Production).
A developer in the **Dev account** needs temporary access to an **S3 bucket in the Production account** to analyze logs. The security team has strict compliance policies and does not allow direct IAM user access across accounts.

Your Task:
- How would you set up cross-account access using IAM roles while following security best practices?

---

- Create an **IAM policy** in the Production account granting read-only access to the specific S3 bucket:
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "s3:GetObject",
        "s3:ListBucket"
      ],
      "Resource": [
        "arn:aws:s3:::prod-logs-bucket",
        "arn:aws:s3:::prod-logs-bucket/*"
      ]
    }
  ]
}
```

- Create an **IAM Role** in the **Production Account** (Role: `S3ReadOnlyRole`). Attach the above IAM policy to the role `S3ReadOnlyRole`

- Update the **trust policy** to allow the **developer's IAM principal** in the Dev account to assume this role:
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "AWS": "arn:aws:iam::DEV_ACCOUNT_ID:user/developer-user"
      },
      "Action": "sts:AssumeRole",
      "Condition": {
        "StringEquals": {
          "aws:PrincipalOrgID": "o-xxxxxxxxxx"
        }
      }
    }
  ]
}
```

- The **developer in the Dev account** needs permission to assume the `S3ReadOnlyRole` in the **Production account**. Attach this IAM policy to the developer’s IAM user in the Dev account:
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": "sts:AssumeRole",
      "Resource": "arn:aws:iam::PROD_ACCOUNT_ID:role/S3ReadOnlyRole"
    }
  ]
}
```
 

