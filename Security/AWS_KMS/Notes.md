AWS Key Management Service (KMS) is a fully managed encryption service that allows you to create, manage, and control cryptographic keys used to encrypt data across AWS services and applications. It integrates with AWS services like S3, RDS, and Lambda, providing centralized key management with fine-grained access control.This reduces direct API calls to KMS, improving performance and security.

AWS KMS supports two types of cryptographic keys:
- **Symmetric Keys**– A single key is used for both encryption and decryption. These are commonly used for data encryption and integrate with AWS services like S3, RDS, and Lambda. AWS KMS stores and manages these keys securely.
- **Asymmetric Keys** – A key pair consisting of a public key (used for encryption or verification) and a private key (used for decryption or signing). These are used for digital signatures, secure communication, and cryptographic operations outside AWS services.

AWS KMS supports different key usages depending on the key type:
- **Encrypt and Decrypt (Symmetric & Asymmetric Keys)**
  - Symmetric Keys: Used for encrypting and decrypting data with the same key (AES-256).
  - Asymmetric Keys: The public key encrypts, and the private key decrypts (RSA or ECC).
- **Sign and Verify (Asymmetric Keys)**
  - The private key signs a message or document to ensure authenticity.
  - The public key verifies the signature, ensuring the data’s integrity.
  - Used in digital signatures (e.g., RSA, ECDSA).
- **Key Agreement (Asymmetric Keys - ECC)**
  - Used in cryptographic protocols where two parties generate a shared secret key without directly exchanging it.
  - Supports Elliptic Curve Diffie-Hellman (ECDH) for secure key exchange.
- **Generate and Verify HMAC (Symmetric Keys)**
  - Generates a cryptographic hash-based message authentication code (HMAC) to ensure message integrity and authenticity.
  - Used for API authentication, data integrity verification, and secure communications.

- **KMS Key Policy** is a set of permissions that define who can use and manage an AWS KMS key. Key Elements of a KMS Key Policy:
  - Principal: Specifies who (which IAM users, roles, or AWS services) can perform actions on the key.
  - Actions: Defines what operations are allowed, such as `Encrypt`, `Decrypt`, `GenerateDataKey`, `CreateGrant`, and `DescribeKey`.
  - Resources: Defines the scope of the resource to which the policy applies (the KMS key itself).
  - Condition: Optional, specifies when the policy should be applied (for example, based on IP address or time of day).
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "AWS": "arn:aws:iam::123456789012:user/YourUserName"
      },
      "Action": [
        "kms:Encrypt",
        "kms:Decrypt"
      ],
      "Resource": "*"
    }
  ]
}
```

### Scenario 1 ###
Your company stores sensitive customer data in Amazon S3, and encryption is required to meet compliance requirements. The security team wants to ensure that only authorized applications can decrypt the data while also maintaining an audit trail of key usage.
You are asked to design an encryption strategy using AWS KMS. How would you implement this, and which key type and key policies would you use?

Follow-up Questions:
- Would you choose symmetric or asymmetric keys for this use case? Why?
- How would you enforce least privilege access using KMS key policies?
- How can you track and audit key usage in AWS KMS?
- How does envelope encryption enhance security in this scenario?

To encrypt sensitive customer data in Amazon S3 while ensuring only authorized applications can decrypt it, we would use **AWS KMS with a symmetric Customer Managed Key** (CMK).

**Choosing the Right Key Type**
- Symmetric CMK (AES-256) is ideal because it integrates natively with S3 Server-Side Encryption (SSE-KMS).
- Asymmetric keys are not required since we only need encryption and decryption within AWS services.
**Implementing Encryption with AWS KMS**
- Enable SSE-KMS on the S3 bucket, specifying the Customer Managed Key (CMK).
- When objects are uploaded, S3 automatically encrypts them using KMS.
- Authorized applications use `KMS Decrypt` permissions to access the data.
**Enforcing Least Privilege Access with Key Policies**
- Define a KMS key policy granting access only to specific IAM roles or applications.
**Tracking and Auditing Key Usage**
- Enable AWS CloudTrail to log every KMS API call.
- Monitor logs to see who accessed the key, when, and from where.
- Set up AWS CloudWatch Alarms for unusual activity, such as unauthorized decryption attempts.
**Enhancing Security with Envelope Encryption**
- Instead of encrypting data directly with the KMS key, generate *Data Keys* using `GenerateDataKey()`.
- Encrypt data locally with the data key, then encrypt the data key with KMS.
- This reduces direct API calls to KMS, improving performance and security.

