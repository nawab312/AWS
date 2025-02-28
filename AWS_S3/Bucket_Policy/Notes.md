- Bucket policy in AWS is a **resource-based access control policy** that defines who can access the objects within an Amazon S3 and what actions they can perform. These are JSON Documents
- A **Resource-Based Access Control (RBAC)** policy defines permissions based on the resources themselves, specifying which users or entities can access specific resources and what actions they are allowed to perform on those resources.

### Key Concepts ###
- **Statement:** A list of one or more permission statements.
- **Sid (Optional):** A unique identifier for the statement (used for referencing purposes).
- **Resources:** The resources in a bucket policy are typically Amazon S3 bucket(s) and the objects within it. A bucket policy can be used to grant permissions to the bucket itself or objects stored in it.
- **Principals:** A principal is an entity that can access the resources. The principal can be an AWS account, an IAM (Identity and Access Management) user, an IAM role, or even anonymous users (everyone, which is less secure).
- **Actions:** These define what operations the principal can perform on the resources. Examples of S3 actions are:
  - `s3:GetObject`: Allows getting (reading) objects.
  - `s3:PutObject`: Allows uploading (writing) objects
  - `s3:DeleteObject`: Allows deleting objects.
- **Conditions:** Bucket policies support conditions that allow you to define access controls based on specific factors like the source IP address, the time of access, or whether the request is made using HTTPS.
- **Effect:** Each statement in the bucket policy has an Effect field, which can either be Allow or Deny. Allow grants permission, while Deny explicitly denies permission regardless of other policies.

**Allow Access Only from Specific IP Address:**
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "ExampleStatement1",
      "Effect": "Allow",
      "Principal": "*",
      "Action": "s3:GetObject",
      "Resource": "arn:aws:s3:::my-bucket/*",
      "Condition": {
        "IpAddress": {
          "aws:SourceIp": "192.0.2.0/24"
        }
      }
    }
  ]
}
```
**Deny Access to All Except a Specific User: This policy denies access to all users except a specific IAM user `(arn:aws:iam::123456789012:user/specific-user)`.**
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "DenyAllExceptSpecificUser",
      "Effect": "Deny",
      "Principal": "*",
      "Action": "s3:GetObject",
      "Resource": "arn:aws:s3:::my-bucket/*",
      "Condition": {
        "StringNotEquals": {
          "aws:PrincipalARN": "arn:aws:iam::123456789012:user/specific-user"
        }
      }
    }
  ]
}
```

**Allow an AWS Account to List Bucket Contents: This policy allows a specific AWS account (in this case, account ID `123456789012`) to list the contents of the bucket but denies all other actions.**
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "AllowListingOfBucket",
      "Effect": "Allow",
      "Principal": "arn:aws:iam::123456789012:root",
      "Action": "s3:ListBucket",
      "Resource": "arn:aws:s3:::my-bucket"
    }
  ]
}
```

- **Use IAM Policies in Combination:** Bucket policies are effective for granting broad permissions (e.g., cross-account access), but use IAM policies for more granular, user-specific access control.
