AWS Certificate Manager (ACM) is a service that helps you easily provision, manage, and deploy **SSL/TLS certificates** for securing your AWS applications and services. We use ACM to secure websites, APIs, and internal applications running on AWS services like **Elastic Load Balancer (ELB)**, **CloudFront** and **API Gateway**. SSL/TLS certificates  encrypt data transmitted between users and applications, ensuring secure communication. **Automates certificate renewal**, reducing the risk of expired certificates.

AWS ACM supports two types of certificates:
- **Public SSL/TLS Certificates** – Issued by AWS ACM for use with AWS services only (e.g., ELB, CloudFront, API Gateway).
- **Private SSL/TLS Certificates** – Created using AWS Private CA for internal applications, including hybrid cloud setups.

### Request a Certificate ###

**Step1) Certificate Type**

<img width="1481" height="235" alt="image" src="https://github.com/user-attachments/assets/c3c2dcf3-125c-487e-af9f-5a06602953f5" />

**Step2) Request Public Certificate**

<img width="1475" height="639" alt="image" src="https://github.com/user-attachments/assets/d525e409-e1af-4d35-9751-5d85f069ae75" />

<img width="1333" height="212" alt="image" src="https://github.com/user-attachments/assets/a0fdb4d6-a8b2-4a0b-b804-da9bcf28a871" />

- After requesting for certificate ACM will give you a CNAME record that you must add in Route53 for validation.

- **FQDN :** FQDN (Fully Qualified Domain Name) is the complete domain name of a system, uniquely identifying it within the Domain Name System (DNS) hierarchy. Example `www.example.com`
    - Hostname – Identifies a specific machine (e.g., www, mail, api).
    - Domain Name – Represents the organization or website (e.g., example.com).
    - Top-Level Domain (TLD) – Defines the highest level of the domain structure (e.g., .com, .org, .net).
 
- **Validation Methods in AWS ACM :** When requesting an SSL/TLS certificate in AWS Certificate Manager (ACM), AWS needs to verify that you own or control the domain. This is done through domain validation, which has two methods:
    - *DNS Validation (Recommended)*: AWS provides a CNAME record that must be added to your domain’s DNS settings. ACM continuously checks for this record, and once found, it validates the domain. The certificate is issued and will automatically renew as long as the CNAME remains in place. This is how to do it
      - Go to Route53 → hosted zone for your domain.
      - Create the CNAME record exactly as ACM instructs.
      - Once the record propagates, ACM will automatically validate the certificate. Status will change from Pending validation → Issued.
    - *Email Validation*: ACM sends a validation email to domain-related addresses: `admin@example.com` or `administrator@example.com` etc. The recipient must click a link to approve the request.

- **Key Algorithm :** refers to the cryptographic algorithm used to generate the *private key* for an SSL/TLS certificate. This key is crucial for secure encryption and decryption in HTTPS communication.

- **Attach the certificate to your ALB**
  - Go to EC2 → Load Balancers → select your ALB.
  - Click on the Listeners tab → you need an HTTPS listener (443).
    - If you don’t have one, click “Add listener → HTTPS 443”.
  - Under Default SSL certificate, choose “From ACM” → select the certificate you just created.
  - Configure security policy (TLS versions, ciphers)—you can use AWS defaults.
  - Set the Target group (your backend EC2/ECS/EKS instances) → save.
