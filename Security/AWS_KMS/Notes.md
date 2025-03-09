AWS Key Management Service (KMS) is a fully managed encryption service that allows you to create, manage, and control cryptographic keys used to encrypt data across AWS services and applications. It integrates with AWS services like S3, RDS, and Lambda, providing centralized key management with fine-grained access control.

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



