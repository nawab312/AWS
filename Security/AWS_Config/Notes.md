AWS Config is a continuous monitoring service that tracks AWS resource configurations, records changes, and evaluates compliance against security best practices.

**Key Features of AWS Config**
- Resource Inventory & Change Tracking
  - Continuously records configuration changes in AWS resources (e.g., EC2, IAM, S3, RDS).
  - Maintains a history of resource configurations.
- Compliance & Security Auditing
  - Uses AWS Config Rules to check compliance (e.g., ensuring S3 buckets are private).
  - Helps with governance and audit trails for security assessments.
- Operational Troubleshooting
  - Detects unintended changes in infrastructure.
  - Helps diagnose root causes of issues (e.g., why a security group was modified).
- Multi-Account & Multi-Region Support
  - Supports centralized monitoring using AWS Organizations.

**How AWS Config Works**
- Enable AWS Config in a region.
- AWS Config discovers resources and starts recording configurations.
- It stores configuration snapshots and logs changes to Amazon S3 & AWS CloudTrail.
- AWS Config Rules check if resources comply with policies.
- Non-compliant changes trigger notifications (SNS, EventBridge, Lambda for automation).

**AWS Config Use Cases**
- Compliance Monitoring
  - Ensure IAM roles do not have overly permissive policies.
  - Verify that EC2 instances are using approved AMIs.
- Security Auditing
  - Track changes to VPC Security Groups.
  - Ensure S3 Buckets have encryption enabled.
- Cost Optimization
  - Detect unattached EBS volumes or unused elastic IPs.
  - Identify underutilized resources.
 
**AWS Config Rules**

AWS Config uses managed and custom rules to check resource compliance.

Examples of AWS Managed Rules
- `s3-bucket-public-read-prohibited` Ensures no S3 bucket allows public read access.
- `iam-user-mfa-enabled` Checks if IAM users have MFA enabled.
- `ec2-instance-no-public-ip` Ensures EC2 instances do not have public IP addresses.

Custom AWS Config Rules
- Use AWS Lambda to define custom logic.
- Example: A rule to check if EBS volumes are encrypted.
