### Scenario ###
Your company has two AWS accounts:
- Dev Account (Account ID: 111111111111)
- Prod Account (Account ID: 222222222222)

You need to allow developers in the Dev Account to assume an IAM role in the Prod Account to perform read-only operations on an S3 bucket (`prod-logs-bucket`).
Requirements:
- The role should only be assumable by a specific IAM group (`DevOpsTeam`) in the Dev Account.
- The role should restrict access to objects only with the prefix `logs`/ in `prod-logs-bucket`.
- The access should only be granted when developers assume the role from a specific corporate IP range (`203.0.113.0/24`).
- The access should be revoked after 6 hours of assuming the role.

---

**Trust Policy (in the Prod Account)**
- This allows only the `DevOpsTeam` group in the **Dev Account** to assume the role. It enforces:
  - Access only from a specific corporate IP range (`203.0.113.0/24`)
  - The Dev Account must be part of a known AWS Organization (`o-xxxxxxxxxx`)
 
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "AWS": "arn:aws:iam::111111111111:group/DevOpsTeam"
      },
      "Action": "sts:AssumeRole",
      "Condition": {
        "StringEquals": {
          "aws:PrincipalOrgID": "o-xxxxxxxxxx"
        },
        "IpAddress": {
          "aws:SourceIp": "203.0.113.0/24"
        }
      }
    }
  ]
}
```

**Permissions Policy (Attached to the Role in Prod Account)**

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
        "arn:aws:s3:::prod-logs-bucket/logs/*"
      ]
    }
  ]
}
```

**Session Duration Restriction (Enforced via IAM Role settings)**
```bash
aws iam update-role --role-name ProdReadOnlyRole --max-session-duration 21600
```

**What Happens if a Developer Tries to Access the S3 Bucket Directly?**
- If a developer in the Dev Account tries to access prod-logs-bucket **without assuming the role**, they will be denied.

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": "sts:AssumeRole",
      "Resource": "arn:aws:iam::PROD_ACCOUNT_ID:role/ProdReadOnlyRole"
    }
  ]
}
