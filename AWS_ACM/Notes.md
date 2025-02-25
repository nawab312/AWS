AWS Certificate Manager (ACM) is a service that helps you easily provision, manage, and deploy **SSL/TLS certificates** for securing your AWS applications and services. We use ACM to secure websites, APIs, and internal applications running on AWS services like **Elastic Load Balancer (ELB)**, **CloudFront** and **API Gateway**. SSL/TLS certificates  encrypt data transmitted between users and applications, ensuring secure communication. **Automates certificate renewal**, reducing the risk of expired certificates.

AWS ACM supports two types of certificates:
- **Public SSL/TLS Certificates** – Issued by AWS ACM for use with AWS services only (e.g., ELB, CloudFront, API Gateway).
- **Private SSL/TLS Certificates** – Created using AWS Private CA for internal applications, including hybrid cloud setups.
