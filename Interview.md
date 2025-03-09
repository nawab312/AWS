`How would you secure a multi-tier architecture in AWS?`

To secure a multi-tier architecture in AWS, I would follow security best practices across each layer of the architecture 

**Network Security (VPC Configuration)**

- Private Subnets: I would place the application and database layers in private subnets
- Public Subnets: The presentation layer (frontend) can be in public subnets, as it needs to be accessed from the internet. I would use NAT gateways to enable outbound internet access for resources in private subnets.
- Security Groups & NACL

**Access Control and Identity Management**

- Ensuring only authorized entities can access resources is critical. I would implement AWS Identity and Access Management (IAM) and AWS Cognito for identity and access management.
  
**Web Application Layer Security (Presentation Layer)**
- The frontend tier often interacts with users over the internet, so securing this layer is vital.
- Application Load Balancer (ALB): I would use an Application Load Balancer (ALB) to distribute traffic to EC2 instances or containerized services, ensuring high availability.
- AWS WAF (Web Application Firewall): To protect the web tier, I would deploy AWS WAF in front of the ALB. WAF protects against common web exploits like SQL injection, cross-site scripting (XSS), and DDoS attacks.
- SSL/TLS Encryption: I would ensure that all traffic between clients and the ALB is encrypted using SSL/TLS

**Application Layer Security**
- The application tier processes business logic and may interact with the database layer. Securing this tier involves controlling access and minimizing attack surfaces.
- Private Communication: I would ensure that the application servers in private subnets can communicate with the database tier using internal IPs and are not exposed to the internet.
- **Environment Variables and Secrets Management:** Store sensitive configuration settings, such as database credentials, in **AWS Secrets Manager**

**Database Layer Security (Data Layer)**
- **Encryption:** I would enable encryption at rest using **AWS KMS (Key Management Service)** to protect the data stored in services like **Amazon RDS, Amazon DynamoDB, or Amazon S3**.
- **Encryption in Transit:** I would also ensure that data is encrypted in transit using TLS/SSL when connecting to the database.
- **VPC Peering:** To restrict access to the database, I would configure **VPC peering** or **VPC endpoints** to ensure only authorized application instances in the private subnets can access the database.

**Logging and Monitoring**
- **AWS CloudTrail:** I would enable AWS CloudTrail to log API activity across the environment, helping detect unauthorized or suspicious activities.
- **Amazon CloudWatch:** I would configure Amazon CloudWatch to monitor performance metrics and set up alarms for anomalous activity, such as high CPU usage, unusual traffic patterns, or errors.
- **AWS GuardDuty:** I would enable AWS GuardDuty for threat detection and monitoring of potential malicious activity within the environment
- **VPC Flow Logs:** I would enable VPC Flow Logs to capture and monitor network traffic in and out of the VPC, which helps with identifying potential security issues.

**Backup and Disaster Recovery**

**DDoS Protection**
- **AWS Shield:** For protection against DDoS attacks, I would enable AWS Shield Standard, which is automatically included with AWS services like ALB and CloudFront.

**Compliance and Auditing**
- To ensure compliance with security standards (e.g., GDPR, HIPAA), I would leverage AWS’s compliance programs and services
- **AWS Config:** I would use AWS Config to track changes to the AWS resources and to ensure the environment stays in a compliant state.

`Can you share some AWS cost optimization techniques you have implemented in your organization?`

**Right-Sizing EC2 Instances**
- We analyzed *EC2 utilization* using *AWS Compute Optimizer* and CloudWatch metrics.
- Many instances were over-provisioned, so we:
  - Downsized underutilized instances (e.g., `m5.large → t3.medium`).
  - Used Auto Scaling Groups to scale dynamically based on demand.

**Implementing Reserved Instances & Savings Plans**
- Instead of using On-Demand EC2, we purchased *Reserved Instances (RIs)* and *Compute Savings Plans* for predictable workloads.
- For non-flexible workloads, we used *1-year Convertible RIs*, allowing modification based on future needs.
- For dynamic workloads, we leveraged *Spot Instances* for batch processing jobs.

**Storage Cost Optimization (S3, EBS, and EFS)**
- S3 Lifecycle Policies:
  - Moved infrequently accessed data from *S3 Standard* to *S3 Intelligent-Tiering* and *Glacier*.
  - Enabled *S3 Object Expiration* to delete unused logs automatically.
- EBS Volume Optimization:
  - Identified *idle/unattached EBS* volumes using *AWS Trusted Advisor* and deleted them.
  - Used gp3 instead of gp2, which provides the same performance at a lower cost.
 
**Using AWS Lambda for Serverless Workloads**
- Instead of running *EC2 instances for cron jobs*  we replaced them with AWS Lambda functions.
- Optimized Lambda memory allocation based on execution time.
- Used *Provisioned Concurrency* only when necessary.
