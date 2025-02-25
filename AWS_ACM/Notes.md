AWS Certificate Manager (ACM) is a service that helps you easily provision, manage, and deploy **SSL/TLS certificates** for securing your AWS applications and services. We use ACM to secure websites, APIs, and internal applications running on AWS services like **Elastic Load Balancer (ELB)**, **CloudFront** and **API Gateway**. SSL/TLS certificates  encrypt data transmitted between users and applications, ensuring secure communication. **Automates certificate renewal**, reducing the risk of expired certificates.

AWS ACM supports two types of certificates:
- **Public SSL/TLS Certificates** – Issued by AWS ACM for use with AWS services only (e.g., ELB, CloudFront, API Gateway).
- **Private SSL/TLS Certificates** – Created using AWS Private CA for internal applications, including hybrid cloud setups.

### Request a Certificate ###

**Step1) Certificate Type**

![Certificate Type](https://github.com/nawab312/AWS/blob/main/AWS_ACM/Images/Certificate_Type.png)

**Step2) Request Public Certificate**

![Request Public Certificate](https://github.com/nawab312/AWS/blob/main/AWS_ACM/Images/Request_Public_Certificate.png)

- **FQDN :** FQDN (Fully Qualified Domain Name) is the complete domain name of a system, uniquely identifying it within the Domain Name System (DNS) hierarchy. Example `www.example.com`
    - Hostname – Identifies a specific machine (e.g., www, mail, api).
    - Domain Name – Represents the organization or website (e.g., example.com).
    - Top-Level Domain (TLD) – Defines the highest level of the domain structure (e.g., .com, .org, .net). 
