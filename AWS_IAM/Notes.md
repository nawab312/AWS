AWS Identity and Access Management (IAM) is a service provided by Amazon Web Services (AWS) that helps securely manage access to AWS resources. It allows you to define who (users or groups) can access specific resources and what actions they are allowed to perform on those resources. 

### IAM Users ###
IAM user is an entity that you create in AWS to represent a person or application that interacts with AWS services and resources. Each IAM user has a unique name and can have specific permissions attached to it, such as full access to certain services or only the ability to read certain resources.
- **Credentials:** IAM users can have credentials like passwords for AWS Management Console access, and access keys (access key ID and secret access key) for programmatic access via AWS CLI or SDKs.
- **Permissions:** These define what the IAM user can do (e.g., create EC2 instances, view S3 buckets, etc.). Permissions are granted via **policies**.

### IAM Groups ###
An IAM group is a collection of IAM users. You can assign permissions to a group rather than to individual users. This makes it easier to manage permissions for multiple users with similar roles, such as an "Admin" group, a "Developer" group, or a "Read-Only" group.
- **Group Membership:** A user can be a member of one or more IAM groups. By attaching policies to groups, you manage the access permissions for all the users in that group.
- **Inheritance:** Any permissions assigned to the group are inherited by the IAM users in that group.

### IAM Roles ###
An IAM role is an AWS identity with specific permissions that can be assumed by users or services. Unlike users, roles are not tied to a specific person or entity but are meant to be assumed temporarily. This is useful for granting permissions to services or users that need temporary access.
- **Temporary Security Credentials:** When a role is assumed, temporary credentials are issued to the requester, allowing them to perform actions according to the role's permissions.
- **Use Cases:** IAM roles are commonly used in scenarios like granting EC2 instances permission to access S3 buckets or allowing cross-account access between AWS accounts.

![image](https://github.com/user-attachments/assets/655684e2-8ee5-4a2b-b47e-22b289732bf1)

![image](https://github.com/user-attachments/assets/5210df11-2c0e-456b-9b2b-ddfddeefed1a)


![image](https://github.com/user-attachments/assets/6bee1127-9d27-46e4-a0f1-cee42cfb291b)


### IAM Policies ###
IAM policies are documents that define permissions and are written in JSON format. They specify what actions are allowed or denied on specific AWS resources.
- **Principal** in an IAM policy refers to the entity that is allowed or denied access to AWS resources
  - **IAM Users:** Individual users defined within AWS IAM. `"Principal": {"AWS": "arn:aws:iam::123456789012:user/JohnDoe"}`
  - **IAM Roles:** Entities that can assume a set of permissions, which can be assumed by users, services, or other AWS resources. `"Principal": {"AWS": "arn:aws:iam::123456789012:role/EC2Role"}`
  - **AWS Services:** Some AWS services can be principals, such as when you give an S3 bucket permission to be accessed by Lambda or EC2. `"Principal": {"Service": "lambda.amazonaws.com"}`
  - **AWS Account:** A specific AWS account can also be a principal, allowing resources to be accessed by any user within that account. `"Principal": {"AWS": "arn:aws:iam::123456789012:root"}`

**Automating IAM Policy Enforcement to Avoid Security Misconfigurations:**
- *IAM Access Analyzer* continuously analyzes IAM policies and resource-based policies to identify policies that allow unintended access. You can automate the use of Access Analyzer to identify security risks in your IAM policies, including over-permissioned roles or users.
- Use *AWS Config* to create custom compliance rules that can automatically check if your IAM policies and roles comply with your security best practices. For example, ensure that IAM policies are not overly permissive or that MFA is enforced for users with administrative access.
### IAM Trust Policies ###
A Trust Policy is a JSON document that defines which entities (users, roles, or AWS services) are allowed to assume an IAM role. Trust policies are attached to IAM roles and specify the **trusted principals** that can assume the role. This is useful in scenarios like granting cross-account access or allowing AWS services to assume roles. Trust Policy Structure
- **Principal:** Defines which AWS user, role, service, or account can assume the role.
- **Action:** Specifies the `sts:AssumeRole` action, which allows the entity to assume the role.
- **Condition (Optional):** Specifies additional constraints for assuming the role (e.g., restricting based on source IP or MFA).
- Example Trust Policy for Cross-Account Access
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": {
                "AWS": "arn:aws:iam::111122223333:root"
            },
            "Action": "sts:AssumeRole",
            "Condition": {
                "StringEquals": {
                    "sts:ExternalId": "12345"
                }
            }
        }
    ]
}
```
- Example Trust Policy for an AWS Service (EC2): This policy allows the Amazon EC2 service to assume the role, enabling EC2 instances to use the associated permissions.
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": {
                "Service": "ec2.amazonaws.com"
            },
            "Action": "sts:AssumeRole"
        }
    ]
}
```

### IAM Permissions Boundaries ###
Permissions boundaries define the maximum permissions that an IAM user or role can have

### IAM Federation ###
IAM federation allows users from external identity providers (e.g., corporate Active Directory, or a third-party service like Google) to access AWS resources without needing an AWS-specific user account. This is particularly useful for organizations that want to manage user identities in a centralized identity provider.
- **SAML Federation:** You can use Security Assertion Markup Language (SAML) to federate identities from enterprise identity providers.
- **Web Identity Federation:** Allows federated access using external providers like Facebook or Amazon Cognito.

### Multi-Factor Authentication (MFA) ###
MFA is an added layer of security that requires users to provide two forms of identification: something they know (like a password) and something they have (such as a hardware or software token).

### AWS Organizations and Service Control Policies (SCPs) ###
In larger organizations with multiple AWS accounts, AWS Organizations helps manage multiple AWS accounts centrally. It allows you to organize accounts into organizational units (OUs) and apply policies that control the actions available across all accounts in an organization.
- **SCPs:** Service Control Policies are a set of policies that specify what actions are allowed or denied **across the organization’s accounts**. `Resource` in this case is `*` SCPs act as a guardrail and limit permissions granted by individual IAM policies.

**How does AWS IAM enforce least privilege access in a multi-account setup?**
- *AWS Organizations and Service Control Policies (SCPs)*: SCPs allow centralized control over permissions across all accounts, ensuring that accounts can only access the services they need, enforcing the least privilege principle.
- *IAM Roles for Cross-Account Access*: IAM roles are used for granting access between accounts, allowing users or services to assume roles with the least permissions necessary for tasks.
- *Granular IAM Policies*: IAM policies are defined to grant only the permissions required for users and roles in each account, limiting access to only the resources they need.
- *Resource-Based Policies*: Resource-based policies, such as those for S3 or Lambda, ensure that access to resources is controlled at the resource level, allowing cross-account access only as needed.
- *Permission Boundaries*: Permission boundaries allow you to set maximum permissions for IAM roles, ensuring that even if a role is granted broad permissions, it can only act within the boundaries defined.
- Use **IAM Access Analyzer** to identify and mitigate excessive or unintended access. It helps you review resource access across AWS accounts and ensures that only the right entities can access your resources.

**AWS Services for Tracking and Auditing User Activity:**

To track and audit user activity across AWS accounts, the following services can be very helpful:
- *AWS CloudTrail* provides a comprehensive audit trail of all API calls made within your AWS environment, capturing detailed information about every request. You can enable CloudTrail across all accounts within AWS Organizations and store logs centrally in a secure S3 bucket for audit and compliance purposes.
- *AWS Config* helps track configuration changes and provides a detailed history of configuration states. It can be used to ensure that resources are properly configured, and changes are logged for auditing purposes.
- *Amazon GuardDuty* is a threat detection service that can help identify unusual activity in your AWS environment. It helps detect malicious or unauthorized behavior, including unexpected access to sensitive data or the use of privileged IAM roles.
- *AWS Security Hub* aggregates security findings from various AWS services (such as GuardDuty, Inspector, and Macie), helping you centrally manage and monitor the security posture of your AWS accounts.

### Access Advisor ###
IAM Access Advisor helps to identify which permissions are being used by IAM users, groups, and roles. This allows you to review access patterns and potentially reduce unnecessary permissions, following the principle of least privilege.

### Access Keys ###
AWS Access Keys are a pair of credentials used to authenticate and authorize API requests made to AWS. These keys consist of:
- *Access Key ID:* A unique identifier for the AWS user or role making the request.
- *Secret Access Key:* A secret password used to sign the request, ensuring it comes from the authorized user.
The combination of the Access Key ID and Secret Access Key is used to authenticate requests to AWS services programmatically. These keys are essential for operations like accessing S3, EC2, or Lambda programmatically via AWS SDKs, CLI, or APIs.

**What are the best practices for securing access keys in AWS environments?**
- *Use IAM Roles Instead of Access Keys:* Prefer assigning IAM roles to EC2 instances, Lambda functions, and other AWS services instead of embedding access keys. Roles are more secure and automatically managed.
- *Enable Multi-Factor Authentication (MFA):* Require MFA for sensitive operations and access keys to provide an extra layer of security.
- *Rotate Access Keys Regularly*
- *Use Least Privilege Principle*
- *Avoid Hardcoding Access Keys:* Never hardcode access keys directly into application code. Use environment variables or AWS Secrets Manager to securely manage them.

---

**Cross Account Scenarios**
- https://github.com/nawab312/AWS/blob/main/AWS_IAM/Scenario1.md
- https://github.com/nawab312/AWS/blob/main/AWS_IAM/Scenario2.md

**Secure EC2 Access to S3 with IAM**
- https://github.com/nawab312/AWS/blob/main/AWS_IAM/Scenario3.md

