Question 1:
You're on-call and receive an alert: a production EC2 instance behind an ALB is showing as "unhealthy" in the target group, but when you SSH into the instance, the application appears to be running fine on port 8080. The health check is configured for HTTP on port 80.
Walk me through your diagnosis — what's wrong and how do you confirm it?

Document Name: Interview.md
📌 Top-Level Heading: Section 2: EC2
🔖 Sub-heading: Scenario 2.1 — The Instance That Won't Stay Healthy Behind an ALB


Question 2:
Your team is running a DynamoDB table with 1,000 Write Capacity Units provisioned. CloudWatch shows average consumed WCUs sitting at around 600 — well under the limit. But your application is throwing ProvisionedThroughputExceededException errors during peak hours.
What is happening, and how do you fix it?

Document Name: Interview.md
📌 Top-Level Heading: # Section 3: Databases
🔖 Sub-heading: ## Scenario 3.3 — DynamoDB Throttling Despite Provisioned Capacity Looking Fine


Question 3:
You have a Lambda function running inside a VPC in a private subnet. It needs to call S3 and DynamoDB. Your team notices the NAT Gateway data processing bill has spiked significantly since this Lambda was deployed.
What is causing this and how do you fix it?

📄 Document Name: 11_Cost_Optimization.md
📌 Top-Level Heading: # 11.6 Data Transfer Costs — The Hidden AWS Bill Killer
🔖 Sub-heading: ## 🧩 NAT Gateway Cost OptimizationAlso cross-references:📄 03_Networking_VPC.md
📌 Top-Level Heading: # 3.4 VPC Endpoints — Interface vs Gateway
🔖 Sub-heading: ## 🧩 Gateway Endpoints (Free!)


Question 4:
A junior engineer on your team runs aws kms schedule-key-deletion on a KMS key with a 7-day pending window. Within hours, your application starts throwing errors — RDS can't read encrypted snapshots, S3 objects return KMS.DisabledException, and EBS volumes fail to mount on new instances.
What happened, and what is your immediate recovery step?

📄 Document Name: Interview.md
📌 Top-Level Heading: # Section 4: Security
🔖 Sub-heading: ## Scenario 4.5 — KMS Key Deletion Is Causing Cascading Failures Across Services


Question 5:
Your microservice in us-east-1 is calling a partner API also hosted on AWS in us-east-1. Both are in separate VPCs with overlapping CIDRs (both using 10.0.0.0/16). Your security team mandates that only the specific partner API endpoint is accessible — not their entire VPC. Traffic must never touch the internet.
What architecture do you use and why can't you use VPC Peering here?

📄 Document Name: Interview2.md
📌 Top-Level Heading: # Scenario 1 — Multi-Account VPC-to-VPC Secure Communication
🔖 Sub-heading: ## SolutionAlso cross-references:📄 03_Networking_VPC.md
📌 # 3.7 PrivateLink
🔖 ## 🧩 Use Cases


Question 6:
You're designing a system where EC2 instances in private subnets need to be patched, accessed for debugging, and have their logs shipped to CloudWatch — all without opening port 22 or using a bastion host.
What AWS service enables this, what are the specific capabilities you'd use, and what are the VPC requirements if these instances have no internet access?

Document Name: 10_Infrastructure_Automation.md
📌 Top-Level Heading: # 10.1 Systems Manager — Session Manager, Parameter Store, Run Command
🔖 Sub-heading: ## 🧩 Session Manager and ## 🧩 Run CommandAlso cross-references:📄 10_Infrastructure_Automation.md
📌 # 10.2 SSM — Patch Manager, Inventory, State Manager


Question 7:
Your team uses Terraform to manage production infrastructure across multiple AWS accounts. A new engineer joins and runs terraform apply from their laptop at the same time another engineer is running it from the CI/CD pipeline. Both are targeting the same environment.
What problem does this cause, how does Terraform prevent it, and what is the exact AWS infrastructure required to implement this correctly?

📄 Document Name: 10_Infrastructure_Automation.md
📌 Top-Level Heading: # 10.3 Terraform on AWS — State Management with S3 + DynamoDB
🔖 Sub-heading: ## 🔍 Why Remote State Exists / What Problem It Solves


Question 8:
Your RDS MySQL primary has one read replica. The ReplicaLag CloudWatch metric is slowly climbing and sometimes reaches 600 seconds. Users running reports say data is 5-10 minutes stale.
What are the likely causes and how do you fix each one?

📄 Document Name: Interview.md
📌 Top-Level Heading: # Section 3: Databases
🔖 Sub-heading: ## Scenario 3.1 — RDS Read Replica Is Falling Behind and Reads Are Stale


Question 9:
You're building a global e-commerce platform. Indian users must be served from ap-south-1 and European users from eu-west-1. Both regions must be fully active. If one region fails, 100% of traffic must automatically shift to the surviving region within 30 seconds — with no manual DNS changes.
What is your global routing solution, and why do you choose it over Route 53 latency-based routing?

📄 Document Name: Interview2.md
📌 Top-Level Heading: # Scenario 6 — Multi-Region Active-Active Architecture with Global Routing
🔖 Sub-heading: ## Solution and ## Alternatives ConsideredAlso cross-references:📄 12_Architecture_Patterns.md
📌 # 12.1 Multi-Region Active-Active vs Active-Passive
🔖 ## 🧩 Active-Active Architecture


Question 10:
Your company has a Direct Connect connection as the primary path to AWS, with a Site-to-Site VPN as backup. During a scheduled Direct Connect maintenance window, traffic must automatically fail over to VPN. Your application maintains long-lived TCP sessions (30+ minutes) between on-premises servers and RDS in the VPC.
Two specific concerns:

How do you achieve failover in under 30 seconds?
How do you ensure existing TCP sessions survive the path change?

📄 Document Name: Interview2.md
📌 Top-Level Heading: # Scenario 9 — Direct Connect Failover to VPN Without Dropping Sessions
🔖 Sub-heading: ## Solution


Question 11 (revised):
Your team performs a blue/green deployment by manually shifting ALB traffic from the blue target group to the green target group. The traffic switch completes, but for about 90 seconds afterward users are still hitting errors. You confirm the green instances are healthy.
What is causing the post-cutover errors and how do you fix them?

📄 Document Name: 12_Architecture_Patterns.md
📌 Top-Level Heading: # 12.5 Zero-Downtime Deployments — Blue/Green, Canary on AWS
🔖 Sub-heading: ## 🧩 Deployment Strategy 2 — Blue/GreenAlso cross-references:📄 02_Compute.md
📌 # 2.5 Elastic Load Balancing — ALB, NLB, CLB, GWLB
🔖 ## 🧩 Target Groups — Deep Dive → Deregistration delay section


Question 12:
You have 50 developer IAM users in your AWS account. You want to allow developers to create IAM roles for their Lambda functions themselves — without being able to escalate their own privileges by creating an admin role.
What IAM mechanism prevents this privilege escalation, and how does it work?

📄 Document Name: 08_Security_Compliance.md
📌 Top-Level Heading: # 8.1 IAM Deep Dive — Trust Policies, Permission Boundaries, SCPs
🔖 Sub-heading: ## 🧩 Permission BoundariesAlso cross-references:📄 01_AWS_Core_Fundamentals.md
📌 # 1.2 IAM — Users, Groups, Roles, Policies
🔖 ## 🧩 Least Privilege in Practice


Question 13:
Your EKS cluster has pods that need to call AWS services — specifically, certain pods need S3 access and others need DynamoDB access. A colleague suggests attaching broad S3 and DynamoDB permissions to the EC2 node's IAM role so all pods can access what they need.
Why is this a bad idea, and what is the correct AWS-native solution?

📄 Document Name: 05_Containers_Serverless.md
📌 Top-Level Heading: # 5.6 EKS — Networking (VPC CNI), IRSA, Cluster Autoscaler vs Karpenter
🔖 Sub-heading: ## 🧩 IRSA — IAM Roles for Service Accounts


Question 14:
Your team runs a high-traffic API on Lambda behind API Gateway. During peak hours, some users are experiencing noticeably higher latency on their first request — sometimes 2-3 seconds — while subsequent requests are fast. Non-peak hours show no complaints.
What is causing this, what are your options to fix it, and which option would you choose for a Java-based Lambda?

📄 Document Name: 05_Containers_Serverless.md
📌 Top-Level Heading: # 5.7 Lambda — Cold Starts, Provisioned Concurrency, SnapStart
🔖 Sub-heading: ## 🧩 Cold Start Deep Dive, ## 🧩 Provisioned Concurrency, ## 🧩 Lambda SnapStart


Question 15:
You're reviewing your AWS bill and notice NAT Gateway data processing charges are unexpectedly high. After investigation you find that inter-AZ traffic is a significant contributor — not just internet egress.
Explain exactly how inter-AZ traffic generates NAT Gateway costs, what the per-GB charges are, and what architectural fix prevents this specific problem.

📄 Document Name: 11_Cost_Optimization.md
📌 Top-Level Heading: # 11.6 Data Transfer Costs — The Hidden AWS Bill Killer
🔖 Sub-heading: ## 🧩 Inter-AZ Traffic Optimization and ## 🧩 NAT Gateway Cost OptimizationAlso cross-references:📄 03_Networking_VPC.md
📌 # 3.1 VPC Fundamentals — Subnets, Route Tables, IGW, NAT
🔖 ## 🧩 NAT Gateway


Question 16:
You're designing a multi-account AWS Organization. Your security team wants to ensure that no account in the organization can disable GuardDuty, delete CloudTrail trails, or launch EC2 instances outside of approved regions (us-east-1, eu-west-1, ap-south-1) — even if an account's root user attempts it.
What mechanism enforces this, where do you apply it, and what is the specific gotcha when writing the region restriction policy?

📄 Document Name: 08_Security_Compliance.md
📌 Top-Level Heading: # 8.1 IAM Deep Dive — Trust Policies, Permission Boundaries, SCPs
🔖 Sub-heading: ## 🧩 SCPs — Service Control PoliciesAlso cross-references:📄 10_Infrastructure_Automation.md
📌 # 10.5 Service Control Policies — Guardrails at Org Level
🔖 ## 🧩 Production SCP Examples


Question 17:
Your team is migrating from gp2 to gp3 EBS volumes across your fleet. A colleague asks: "Why bother? gp2 already gives us 3 IOPS per GB — we have 1TB volumes so that's 3,000 IOPS, same as gp3 baseline."
Is your colleague correct? What are the actual differences between gp2 and gp3, and what is the hidden risk with gp2 that your colleague is missing?

📄 Document Name: 04_Storage.md
📌 Top-Level Heading: # 4.2 EBS — Volume Types, Snapshots, Encryption
🔖 Sub-heading: ## 🧩 Volume Types → ### gp3 vs gp2 — Critical Interview Topic


Question 18:
Your team runs a production Aurora PostgreSQL cluster. During a routine review, you notice the BufferCacheHitRatio metric sitting at 99% — excellent. But after a blue/green deployment where you cut traffic to a new Aurora cluster, this metric drops to 40% within 10 minutes and query latency doubles.
What happened, what is the immediate mitigation, and how do you prevent this in future deployments?

📄 Document Name: Interview.md
📌 Top-Level Heading: # Section 3: Databases
🔖 Sub-heading: ## Scenario 3.4 — Aurora Cluster Slows Down After a Blue-Green Deployment


Question 19:
You're architecting a system where 50+ microservices across 30 AWS accounts all need access to shared internal services — an internal DNS resolver, a container image registry mirror, and a secrets management service. All accounts have potentially overlapping CIDRs.
What architecture do you use, and how do you handle the overlapping CIDR constraint specifically?

📄 Document Name: Interview2.md 📌 Top-Level Heading: # Scenario 4 — Shared Services VPC Accessed by 50+ Spoke VPCs Securely at Scale 🔖 Sub-heading: ## Solution
Also cross-references:
📄 03_Networking_VPC.md 📌 # 3.3 VPC Peering & Transit Gateway 🔖 ## 🧩 VPC Peering Limitations — Non-Transitivity
📄 03_Networking_VPC.md 📌 # 3.7 PrivateLink


Question 20:
A developer on your team generates a presigned S3 URL for a private object and shares it with a customer. The URL is set to expire in 7 days. However, the customer reports the URL stopped working after only 2 hours.
What is the most likely cause, and how do you fix it?

📄 Document Name: 04_Storage.md
📌 Top-Level Heading: # 4.3 S3 — Lifecycle Policies, Replication, Presigned URLs
🔖 Sub-heading: ## 🧩 Presigned URLs


Question 21:
Your ECS Fargate tasks are failing to start. The error in the ECS console shows the task is stuck in PROVISIONING state and then moves to STOPPED with the error: CannotPullContainerError: failed to pull image.
The ECR repository exists, the image tag is correct, and the task definition references the right image URI. What do you investigate?

📄 Document Name: 05_Containers_Serverless.md
📌 Top-Level Heading: # 5.3 ECS Launch Types — EC2 vs Fargate
🔖 Sub-heading: ## 🧩 Fargate Launch Type — Deep DiveAlso cross-references:📄 05_Containers_Serverless.md
📌 # 5.1 ECS — Clusters, Tasks, Services, Task Definitions
🔖 ## 🧩 Key Components Deep Dive → Two IAM Roles section📄 03_Networking_VPC.md
📌 # 3.4 VPC Endpoints — Interface vs Gateway


Question 22:
Your team wants to implement automatic node scaling on EKS. A colleague suggests using Cluster Autoscaler. You recommend Karpenter instead.
Make the case for Karpenter over Cluster Autoscaler, and describe one specific scenario where Cluster Autoscaler would still be the right choice.

📄 Document Name: 05_Containers_Serverless.md
📌 Top-Level Heading: # 5.6 EKS — Networking (VPC CNI), IRSA, Cluster Autoscaler vs Karpenter
🔖 Sub-heading: ## 🧩 Cluster Autoscaler vs Karpenter


Question 23:
You enable S3 Cross-Region Replication (CRR) from a source bucket in us-east-1 to a destination bucket in eu-west-1. After enabling it, you notice that objects uploaded before replication was enabled are not appearing in the destination bucket. Additionally, a colleague reports that delete operations on the source bucket are also not being replicated.
Are these behaviors expected? Explain why, and how do you address both gaps.

📄 Document Name: 04_Storage.md
📌 Top-Level Heading: # 4.3 S3 — Lifecycle Policies, Replication, Presigned URLs
🔖 Sub-heading: ## 🧩 S3 Replication


Question 24:
Your Lambda function processes messages from an SQS queue. During an incident, you notice the same message is being processed multiple times — sometimes 3-4 times — causing duplicate records in your database.
What are the two root causes that explain this behavior, and how do you fix each one?

📄 Document Name: 05_Containers_Serverless.md
📌 Top-Level Heading: # 5.5 Lambda — Execution Model, Triggers, Layers, Concurrency
🔖 Sub-heading: ## 🧩 Triggers (Event Sources) → SQS trigger configuration section
📄 05_Containers_Serverless.md
📌 # 5.5 Lambda — Execution Model, Triggers, Layers, Concurrency
🔖 ## ⚠️ Tricky Edge Cases / Gotchas


Question 25:
Your team is running a multi-tenant SaaS application. Each tenant's data is stored in DynamoDB with tenantId as the partition key. You want to ensure that each IAM role can only access their own tenant's data — without creating a separate IAM role per tenant.
What IAM feature enables this, and how does it work with DynamoDB?

📄 Document Name: 08_Security_Compliance.md
📌 Top-Level Heading: # 8.7 IAM — ABAC, Session Policies
🔖 Sub-heading: ## 🧩 ABAC — Attribute-Based Access Control


Question 26:
Your team runs a CloudWatch alarm that monitors the ErrorRate metric for your API. The alarm is configured to trigger when ErrorRate > 5% for 3 consecutive evaluation periods of 5 minutes each.
During an incident, the error rate spikes to 80% for exactly 8 minutes then recovers. The on-call engineer receives no alert.
Why didn't the alarm fire, and how do you fix the configuration?

📄 Document Name: 07_Observability_Monitoring.md
📌 Top-Level Heading: # 7.3 CloudWatch Alarms — States, Actions, Composite Alarms
🔖 Sub-heading: ## 🧩 Alarm Configuration


Question 27:
Your organization runs 40+ AWS accounts under AWS Organizations. The security team wants a single pane of glass to see all security findings — GuardDuty threats, Inspector vulnerabilities, IAM Access Analyzer findings, and Macie sensitive data discoveries — across every account, normalized into one format.
What AWS service provides this, how do you enable it at scale across all accounts, and what is the normalized finding format it uses?

📄 Document Name: 08_Security_Compliance.md
📌 Top-Level Heading: # 8.4 GuardDuty, Security Hub, Inspector
🔖 Sub-heading: ## 🧩 AWS Security Hub


Question 28 (rephrased):
Your team wants to send 10% of API Gateway traffic to a new Lambda version and 90% to the current stable version — using only native Lambda features, no CodeDeploy.
What Lambda feature enables this traffic split, how do you configure it, and how do you implement automatic rollback based on error rate?

📄 Document Name: 12_Architecture_Patterns.md
📌 Top-Level Heading: # 12.5 Zero-Downtime Deployments — Blue/Green, Canary on AWS
🔖 Sub-heading: ## 🧩 Deployment Strategy 3 — CanaryAlso cross-references:📄 05_Containers_Serverless.md
📌 # 5.5 Lambda — Execution Model, Triggers, Layers, Concurrency


Question 29:
Your team stores all application secrets — database passwords, API keys, third-party credentials — in AWS Secrets Manager. A developer asks: "Why can't we just store everything in SSM Parameter Store SecureString instead? It's cheaper."
Make the case for when Secrets Manager is the right choice over Parameter Store, and when Parameter Store is actually sufficient.

📄 Document Name: 08_Security_Compliance.md 📌 Top-Level Heading: # 8.3 Secrets Manager vs Parameter Store 🔖 Sub-heading: ## ⚠️ Deep Comparison and ## 🧩 Secrets Manager — Rotation Deep Dive


Question 30:
Your Aurora PostgreSQL Global Database has a primary cluster in eu-west-1 and a secondary cluster in ap-south-1. The eu-west-1 region experiences a complete outage.
Walk through exactly what happens automatically, what requires manual intervention, and what the approximate RTO is for this scenario.

📄 Document Name: 06_Databases.md
📌 Top-Level Heading: # 6.4 Aurora — Architecture, Aurora Serverless, Global Database
🔖 Sub-heading: ## 🧩 Aurora Global DatabaseAlso cross-references:📄 12_Architecture_Patterns.md
📌 # 12.2 Disaster Recovery Strategies — RTO/RPO, Pilot Light, Warm Standby
🔖 ## 🧩 DR Strategy Summary


Question 31:
Your team is running Redis on ElastiCache in Cluster Mode. A developer complains that their MGET command fetching multiple keys is failing with a CROSSSLOT error, even though the same command works fine on their local Redis instance.
What is causing this error and how do you fix it without restructuring the entire caching layer?

📄 Document Name: 06_Databases.md
📌 Top-Level Heading: # 6.6 ElastiCache — Redis vs Memcached, Cluster Mode
🔖 Sub-heading: ## 🧩 Cluster Mode


Question 32:
Your team is building a data pipeline where objects uploaded to S3 must trigger a Lambda function for processing. A colleague sets up S3 Event Notifications directly to Lambda. You suggest using EventBridge instead.
What are the specific advantages of EventBridge over direct S3 → Lambda notifications, and in what scenario would direct S3 notifications still be the right choice?

📄 Document Name: 04_Storage.md
📌 Top-Level Heading: # 4.6 S3 — Event Notifications, S3 Select, Multipart Upload
🔖 Sub-heading: ## 🧩 S3 Event NotificationsAlso cross-references:📄 12_Architecture_Patterns.md
📌 # 12.4 Event-Driven Architecture on AWS
🔖 ## 🧩 Core EDA Patterns on AWS


Question 33:
Your team is designing a compliance reporting system. Regulations require that audit logs stored in S3 cannot be deleted or modified for 7 years — not even by the root account. A security audit also requires that any attempt to delete these logs must be blocked at the storage level, not just at the IAM level.
What S3 feature implements this, what are the two modes it operates in, and what is the one prerequisite that must be set at bucket creation?

📄 Document Name: 04_Storage.md
📌 Top-Level Heading: # 4.5 S3 Security — Bucket Policies, ACLs, Block Public Access, S3 Object Lock
🔖 Sub-heading: ## 🧩 S3 Object Lock ⚠️ (Critical for Compliance)


Question 34:
Your team enables AWS Config across all accounts in your organization. A security engineer asks: "We already have CloudTrail — what does Config add that CloudTrail doesn't give us?"
Explain the fundamental difference between what CloudTrail records and what AWS Config records, and give a concrete example showing why you need both.

📄 Document Name: 08_Security_Compliance.md
📌 Top-Level Heading: # 8.6 AWS Config — Rules, Conformance Packs, Remediation
🔖 Sub-heading: ## 🧩 AWS Config Core ConceptsAlso cross-references:📄 08_Security_Compliance.md
📌 # 8.9 VPC Flow Logs + CloudTrail + Athena (Security Audit Pattern)
🔖 ## 🧩 AWS CloudTrail


Question 35:
Your team is implementing observability for a high-traffic Lambda function processing 10 million invocations per day. You want to publish custom business metrics — order count, processing latency, failure reasons — without the overhead of calling cloudwatch:PutMetricData on every invocation.
What AWS-native solution solves this, how does it work, and what is the critical operational mistake that causes all metrics to be silently lost?

📄 Document Name: 07_Observability_Monitoring.md
📌 Top-Level Heading: # 7.6 CloudWatch Embedded Metric Format (EMF)
🔖 Sub-heading: ## 🧩 EMF Format and ## 🧩 EMF High-Cardinality Pattern


Q36 — EFS Mount Targets
How do EC2 instances in multiple AZs connect to EFS? What happens at the network layer when an EC2 instance in AZ-a mounts an EFS filesystem, and what security group configuration is required?
📄 04_Storage.md
📌 # 4.4 EFS — Use Cases, Performance Modes, Mount Targets
🔖 ## 🧩 Mount Targets & Security


Q37 — Lambda Concurrency Types
You have a critical payment Lambda and a reporting Lambda in the same account. The reporting Lambda occasionally spikes to 900 concurrent executions. What happens to the payment Lambda, and what are your three options to prevent this?
📄 05_Containers_Serverless.md
📌 # 5.5 Lambda — Execution Model, Triggers, Layers, Concurrency
🔖 ## 🧩 Concurrency



Q38 — DR Strategies RTO/RPO
Your CTO asks: "What's the difference between Pilot Light and Warm Standby? We need RTO under 30 minutes." Which do you recommend and why?
📄 12_Architecture_Patterns.md
📌 # 12.2 Disaster Recovery Strategies — RTO/RPO, Pilot Light, Warm Standby
🔖 ## 🧩 DR Strategy 2 — Pilot Light and ## 🧩 DR Strategy 3 — Warm Standby


Q39 — EBS Encryption In-Place
A compliance requirement mandates all EBS volumes must be encrypted. You have 50 running EC2 instances with unencrypted gp3 root volumes. How do you encrypt them without terminating the instances?
📄 04_Storage.md
📌 # 4.2 EBS — Volume Types, Snapshots, Encryption
🔖 ## 🧩 Encryption


Q40 — Savings Plans vs Reserved Instances
Your team runs: 20 m5.xlarge EC2 instances 24/7, 5 Lambda functions processing 50M invocations/day, and 3 RDS PostgreSQL instances. Which commitment purchasing options apply to each workload and which type of Savings Plan covers the most ground?
📄 11_Cost_Optimization.md
📌 # 11.2 Savings Plans vs Reserved Instances
🔖 ## 🧩 Savings Plans — Three Types and ## 🧩 Reserved Instances — Types and Options


Q41 — VPC CNI Pod DensityYour EKS cluster nodes are m5.large instances. Pods keep failing to schedule with "insufficient resources" even though CPU and memory look fine. You investigate and find the node has hit its maximum pod count. What is causing this limit, what is the exact calculation, and how do you fix it without changing instance type?📄 05_Containers_Serverless.md
📌 # 5.6 EKS — Networking (VPC CNI), IRSA, Cluster Autoscaler vs Karpenter
🔖 ## 🧩 VPC CNI — Pod Networking


Q42 — X-Ray Sampling
Your high-traffic API handles 50,000 requests/second. You enable X-Ray Active Tracing but your AWS bill spikes significantly due to X-Ray costs. You need to reduce costs while still catching errors and slow requests. How do you configure X-Ray sampling to achieve this?
📄 07_Observability_Monitoring.md
📌 # 7.5 AWS X-Ray — Tracing, Segments, Sampling
🔖 ## 🧩 Sampling

Q43 — Well-Architected FrameworkYou're reviewing a new microservice architecture. Walk through how you would evaluate it against the AWS Well-Architected Framework. Name all 6 pillars and for each give one specific AWS service or pattern that addresses it.📄 12_Architecture_Patterns.md
📌 # 12.3 Well-Architected Framework — 6 Pillars
🔖 ## 🧩 Pillar 1 through ## 🧩 Pillar 6 — Sustainability💡 Add to notes:
  

Q43 — Control Tower Account Factory
Your organization is growing rapidly — a new product team needs a fully secured AWS account with CloudTrail, GuardDuty, Config, and SSO access configured. Without Control Tower, this takes your platform team 3 days. How does Control Tower solve this, and what does a new account get automatically?
📄 10_Infrastructure_Automation.md
📌 # 10.6 AWS Control Tower — Landing Zones, Guardrails
🔖 ## 🧩 Account Factory

Q44 — Control Tower Account Factory
Your organization is growing rapidly — a new product team needs a new AWS account every 2 weeks. Without Control Tower, this takes 3 days of manual setup. How does Control Tower solve this, what is automatically provisioned in every new account, and what is the one thing Control Tower cannot do retroactively?
📄 10_Infrastructure_Automation.md
📌 # 10.6 AWS Control Tower — Landing Zones, Guardrails
🔖 ## 🧩 Account Factory and ## 🧩 Control Tower Landing Zone


Q45 — Composite Alarms
Your on-call team is suffering alert fatigue — they receive 50+ CloudWatch alarms per week, most of which are correlated (high CPU + high memory + high latency all firing simultaneously for the same root cause). How do you reduce this to a single meaningful alert, and what is the one thing composite alarms cannot do that individual metric alarms can?
📄 07_Observability_Monitoring.md
📌 # 7.3 CloudWatch Alarms — States, Actions, Composite Alarms
🔖 ## 🧩 Composite Alarms

Q46 — DynamoDB Streams and TTL
You use DynamoDB TTL to automatically expire user session items after 24 hours. A colleague notices that expired items are still being returned by Query operations up to 48 hours after their TTL timestamp. Additionally, your Lambda consuming DynamoDB Streams is receiving delete events for TTL-expired items — how do you distinguish these from user-initiated deletes?
📄 06_Databases.md
📌 # 6.5 DynamoDB — Capacity Modes, DAX, Streams, TTL
🔖 ## 🧩 DynamoDB Streams and ## 🧩 TTL — Time to Live


Q47 — S3 Intelligent-Tiering Gotchas
Your team decides to move all S3 objects to Intelligent-Tiering to "automatically optimize costs". A cost review 3 months later shows the bill actually increased for some buckets. What went wrong?
📄 11_Cost_Optimization.md
📌 # 11.5 S3 Intelligent-Tiering & Storage Cost Patterns
🔖 ## 🧩 S3 Intelligent-Tiering — Deep Dive


Q48 — SSM State Manager vs Run Command
Your team uses SSM Run Command to install the CloudWatch Agent on all EC2 instances. Three weeks later, a security scan shows 15% of instances don't have the agent running — some had it uninstalled accidentally, others are newly launched instances that missed the initial Run Command execution.
📄 10_Infrastructure_Automation.md
📌 # 10.2 SSM — Patch Manager, Inventory, State Manager
🔖 ## 🧩 State Manager


Q49 — Spot Mixed Instances Policy
Your team wants to migrate the web tier ASG to use Spot Instances to save costs. A colleague suggests using a single instance type (m5.xlarge) with Spot. You push back. What is the correct Spot strategy for a production web tier, what allocation strategy do you use and why, and how do you ensure minimum guaranteed capacity?
📄 11_Cost_Optimization.md
📌 # 11.4 Spot Strategy for Production Workloads
🔖 ## 🧩 Spot Strategies in Auto Scaling Groups


Q50 — RAM Resource Sharing
Your network team manages a Transit Gateway in a central networking account. 30 spoke accounts need to attach their VPCs to it. Without RAM, what would this require? With RAM, how does sharing work at the Organization level, and what happens when a new account joins the organization?
📄 10_Infrastructure_Automation.md
📌 # 10.7 Resource Access Manager (RAM)
🔖 ## 🧩 RAM in Practice — Transit Gateway Sharing


Q51 — KMS Envelope EncryptionYour application needs to encrypt 500MB files before storing them in S3. A developer suggests calling kms:Encrypt directly. Why won't this work, and what is the correct pattern?📄 08_Security_Compliance.md
📌 # 8.2 KMS — CMKs, Key Policies, Envelope Encryption
🔖 ## 🧩 Envelope Encryption


Q52 — IMDSv2 and SSRF ProtectionYour security team mandates IMDSv2 on all EC2 instances. A developer asks: "Why? What attack does IMDSv2 prevent that IMDSv1 doesn't?" Explain the attack, why IMDSv2 blocks it, and what the HttpPutResponseHopLimit setting does for containers.
📄 02_Compute.md
📌 # 2.7 EC2 Instance Metadata & IMDSv2
🔖 ## ⚙️ IMDSv2 — SECURE

Q53 — Route 53 Routing PoliciesYou have a global application. EU users must always be routed to eu-west-1 for GDPR compliance regardless of latency. US users should go to whichever region is fastest. If a region fails, traffic must automatically shift. Which Route 53 routing policies do you use for each requirement and why can't you use a single policy for all three?
📄 03_Networking_VPC.md
📌 # 3.5 Route 53 — Hosted Zones, Routing Policies
🔖 ## 🧩 Routing Policies ⚠️ (Most Interviewed Topic)


Q54 — RDS Proxy with Lambda
Your Lambda functions are causing "too many connections" errors on RDS PostgreSQL. The DBA says max_connections is set to 330 for the db.t3.medium instance. During peak load you have 500 concurrent Lambda executions. What is the root cause, what AWS service fixes it, and what additional benefit does it provide during RDS failover?
📄 06_Databases.md
📌 # 6.9 RDS Proxy — Connection Pooling, Use with Lambda
🔖 ## 🟢 What It Is and ## ⚙️ How RDS Proxy Works


Q55 — GuardDuty Incident Response
GuardDuty fires a HIGH severity finding: UnauthorizedAccess:IAMUser/MaliciousIPCaller. An IAM user's access key is making API calls from an Eastern European IP. Walk through your incident response in the correct order — what do you do first, second, and third, and what is the critical mistake teams make by doing Phase 3 before Phase 2?
📄 08_Security_Compliance.md
📌 # 8.4 GuardDuty, Security Hub, Inspector
🔖 ## 🧩 GuardDuty — Incident Response Playbook


Q56 — IAM Access AnalyzerYour security team wants to continuously monitor which S3 buckets, IAM roles, KMS keys, and Lambda functions are accessible from outside your AWS Organization — and get alerted automatically when new external access is introduced. What AWS tool provides this, what is a "zone of trust", and how does it differ from IAM Access Advisor?📄 08_Security_Compliance.md
📌 # 8.1 IAM Deep Dive — Trust Policies, Permission Boundaries, SCPs
🔖 ## 🧩 IAM Access Analyzer


Q57 — WAF and ShieldYour public-facing ALB is receiving a volumetric DDoS attack AND SQL injection attempts simultaneously. Walk through exactly which AWS services handle each threat, at which OSI layer, and what the difference is between Shield Standard and Shield Advanced in terms of what you get during an active attack.📄 08_Security_Compliance.md
📌 # 8.5 WAF & Shield
🔖 ## 🧩 AWS WAF and ## 🧩 AWS Shield


Q58 — CloudFront Behaviors and Cache InvalidationYour React SPA is served via CloudFront with S3 as origin. After a deployment, users are still seeing the old version of index.html but new JavaScript files load correctly. Why is this happening, and what is the correct long-term solution that avoids cache invalidation costs entirely?📄 03_Networking_VPC.md
📌 # 3.6 CloudFront — Distributions, Behaviors, Origins, Cache Invalidation
🔖 ## 🧩 Cache Policies & TTLs and ## 🧩 Cache Invalidation


Q59 — Aurora Serverless v2
Your team runs a SaaS application with highly variable database load — near-zero traffic overnight, heavy load during business hours. You're considering Aurora Serverless v2. What does it scale, what does it NOT scale to, and when would provisioned Aurora still be the better choice?
📄 06_Databases.md
📌 # 6.4 Aurora — Architecture, Aurora Serverless, Global Database
🔖 ## 🧩 Aurora Serverless v2


Q60 — Event-Driven Architecture Patterns
You're designing an order processing system. When an order is created, you need to: process payment, update inventory, send confirmation email, and update analytics — all independently and without the order service knowing about downstream consumers. A colleague suggests having the order service call each downstream service directly via HTTP.
Why is this wrong, what pattern do you use instead, and when would you use Step Functions orchestration over pure event choreography?
📄 12_Architecture_Patterns.md
📌 # 12.4 Event-Driven Architecture on AWS
🔖 ## 🧩 Core EDA Patterns on AWS and ## 🧩 Choreography vs Orchestration


Q61 — Trusted Advisor vs Compute OptimizerYour engineering manager asks you to reduce EC2 costs by identifying over-provisioned instances. You have access to both AWS Trusted Advisor and AWS Compute Optimizer. Which do you use for this specific task, what is the fundamental difference in how each makes its recommendation, and what must be installed on EC2 instances for Compute Optimizer to give accurate memory-based recommendations?📄 11_Cost_Optimization.md
📌 # 11.3 Trusted Advisor & Compute Optimizer
🔖 ## 🧩 AWS Trusted Advisor and ## 🧩 AWS Compute Optimizer


Q62 — Container Insights vs Lambda InsightsYour ECS cluster shows high CPU at the cluster level in CloudWatch, but you can't tell which specific task or container is responsible. Your Lambda functions show high duration but you can't tell if they're running out of memory or just slow. What AWS observability features give you per-container and per-invocation visibility, and how are they enabled?📄 07_Observability_Monitoring.md
📌 # 7.9 Container Insights & Lambda Insights
🔖 ## 🧩 Container Insights and ## 🧩 Lambda Insights


Q63 — CDK BootstrappingYour team adopts AWS CDK to manage infrastructure. A new engineer runs cdk deploy in a fresh AWS account and gets the error: "This stack uses assets, so the toolkit stack must be deployed to the environment." What is missing, what does bootstrapping create, and why must bootstrapping be run per account AND per region?📄 10_Infrastructure_Automation.md
📌 # 10.4 AWS CDK — Constructs, Stacks, Bootstrapping
🔖 ## 🧩 CDK Bootstrapping


Q64 — Expand-Contract DB Migration PatternYour team needs to rename a column in a production PostgreSQL RDS table from user_name to username during a zero-downtime blue/green deployment. Both old and new application versions will run simultaneously during the deployment window. A developer suggests: "Just rename the column and deploy — it'll be fine." Why is this wrong and what is the correct pattern?
📄 12_Architecture_Patterns.md
📌 # 12.5 Zero-Downtime Deployments — Blue/Green, Canary on AWS
🔖 ## 🧩 Database Migrations in Zero-Downtime Deployments


Q65 — Cost Anomaly Detection
Your AWS bill spikes unexpectedly by $42,000 in a single day. You had AWS Budgets configured with a monthly threshold alert at 80%. Why didn't Budgets catch this spike earlier, and what AWS service would have detected it within hours? How does that service determine what's "anomalous" without you setting a threshold?
📄 11_Cost_Optimization.md
📌 # 11.1 Cost Explorer, Budgets, Cost Anomaly Detection
🔖 ## 🧩 Cost Anomaly Detection


Q66 — EC2 Status Checks vs ELB vs ASG Health ChecksYour production EC2 instance passes both EC2 status checks but the ALB shows it as unhealthy. Meanwhile your ASG health check type is set to EC2 (default) so the ASG thinks the instance is healthy and doesn't replace it. Users are getting errors.Explain the three different health check systems, what each tests, and what ASG configuration change fixes this specific scenario.📄 02_Compute.md
📌 # 2.1 EC2 — Instance Types, AMIs, Key Pairs, User Data
🔖 ## 🧩 EC2 Status Checks — System vs Instance and ## How Status Checks Connect to ASG


Q67 — CloudWatch Logs InsightsDuring an incident your on-call engineer needs to answer three questions from Lambda logs within 2 minutes: (1) What is the P99 latency per API endpoint in the last hour? (2) Which user ID is generating the most errors? (3) How many cold starts occurred in the last 30 minutes?Write the Logs Insights queries for each and identify the cost consideration.📄 07_Observability_Monitoring.md
📌 # 7.2 CloudWatch Logs — Log Groups, Metric Filters, Insights
🔖 ## 🧩 CloudWatch Logs Insights


Q68 — ECS Lifecycle HooksYour ECS service runs a Node.js application that takes 90 seconds to warm up its in-memory cache before it can serve requests correctly. Without any special configuration, new tasks get traffic immediately after passing the ALB health check (which checks /health returning 200). Users get slow/incorrect responses for 90 seconds after each deployment.What ECS feature solves this, and what is the difference between solving it at the ECS layer vs the ALB layer?📄 05_Containers_Serverless.md
📌 # 5.1 ECS — Clusters, Tasks, Services, Task Definitions
🔖 ## 🧩 Services → Deployment types section and Lifecycle Hooks


Q69 — DynamoDB GSI vs LSIYou have a DynamoDB table storing orders with customerId as partition key and orderDate as sort key. You need two additional access patterns: (1) get all orders with status=SHIPPED across ALL customers, (2) get all orders for a specific customer sorted by totalAmount instead of orderDate.Which index type solves each requirement and why can't you use the same index type for both?📄 06_Databases.md
📌 # 6.2 DynamoDB — Tables, Items, Partition Keys, GSI/LSI
🔖 ## 🧩 Indexes — GSI and LSI


70 — SSM Patch Manager Maintenance WindowsYour organization has 500 EC2 instances across production and development environments. The security team mandates all instances must be patched within 72 hours of a critical CVE being published. Patching all 500 simultaneously would cause an outage. Design the patching strategy using SSM Patch Manager.📄 10_Infrastructure_Automation.md
📌 # 10.2 SSM — Patch Manager, Inventory, State Manager
🔖 ## 🧩 Patch Manager


Q71 — KMS Cross-Account AccessTeam A owns a KMS key in Account A used to encrypt S3 objects. Team B's application in Account B needs to decrypt those objects. A developer in Account B adds kms:Decrypt to their IAM role policy referencing Account A's key ARN. It still doesn't work. Why, and what are the exact two steps required?📄 08_Security_Compliance.md
📌 # 8.8 KMS — Multi-Region Keys, Cross-Account Access, Grants
🔖 ## 🧩 Cross-Account KMS Access


Q72 — VPC Flow Logs + Athena Security AuditAfter a security incident you need to answer: "Did the compromised EC2 instance (10.0.1.50) send any data to external IPs in the last 7 days?" You have VPC Flow Logs enabled and shipping to S3. What do Flow Logs capture, what don't they capture, and write the Athena query to answer this question efficiently.📄 08_Security_Compliance.md
📌 # 8.9 VPC Flow Logs + CloudTrail + Athena (Security Audit Pattern)
🔖 ## 🧩 VPC Flow Logs and ## 🧩 Athena Security Audit Pattern


Q73 — Macie for Sensitive DataYour company stores customer uploads in S3. A compliance audit requires you to prove that no PII (names, SSNs, credit card numbers) exists in your prod-uploads bucket. Your security team also wants to be automatically notified if PII is uploaded in future. What AWS service provides this, what does it scan, and what is the cost consideration for large buckets?📄 08_Security_Compliance.md
📌 # 8.10 Macie, Detective, Audit Manager
🔖 ## 🧩 Amazon Macie

Q74 — Step Functions OrchestrationYour order processing workflow has 6 steps: validate order → reserve inventory → charge payment → create shipment → send confirmation → update analytics. If payment fails, inventory must be released. If shipment creation fails, payment must be refunded.Why is pure event choreography (EventBridge + SQS) insufficient here, and what does Step Functions provide that solves this specifically?📄 12_Architecture_Patterns.md
📌 # 12.4 Event-Driven Architecture on AWS
🔖 ## 🧩 Choreography vs Orchestration


Q75 — Tag Policies and Cost AllocationYour CFO asks: "How much did the payments team spend on AWS last month, broken down by service?" You realize you cannot answer this question. What two things must be set up for this to work, what is the critical timing gotcha, and how do you prevent untagged resources from appearing as an unknown cost bucket in future?📄 10_Infrastructure_Automation.md
📌 # 10.8 Tag Policies & Cost Allocation
🔖 ## 🧩 Cost Allocation Tags and ## 🧩 Tag Policies (AWS Organizations)


Q76 — Placement GroupsYour HPC team runs a tightly coupled MPI simulation that requires maximum network bandwidth between 50 GPU instances. A separate team runs a 3-node ZooKeeper cluster that must survive any single hardware failure. A third team runs a 200-node Cassandra cluster where replicas must never share physical hardware within the same group.Which placement group type does each team need and what are the specific limits for each?📄 02_Compute.md
📌 # 2.6 EC2 Placement Groups
🔖 ## 🧩 Three Types


Q77 — NACLs Stateless + Ephemeral PortsYour security team adds a NACL to the public subnet allowing inbound HTTP (port 80) and HTTPS (port 443). After applying it, all HTTPS traffic works but HTTP requests time out silently. No security group changes were made. What is causing this and what is the exact fix?📄 03_Networking_VPC.md
📌 # 3.9 Network ACLs Deep Dive & Stateless vs Stateful
🔖 ## ⚙️ Stateless Deep Dive — Why It Matters


Q78 — DynamoDB DAXYour DynamoDB table serves a product catalog with 10,000 reads/second. 80% of reads are for the same 100 "featured products". Read latency is currently 5-10ms. Your team wants sub-millisecond reads for these hot items without changing the application's DynamoDB SDK calls.What solution fits, what does it NOT help with, and what happens to strongly consistent reads?📄 06_Databases.md
📌 # 6.5 DynamoDB — Capacity Modes, DAX, Streams, TTL
🔖 ## 🧩 DAX — DynamoDB Accelerator


Q79 — ElastiCache Eviction PoliciesYour ElastiCache Redis cluster is running at 95% memory utilization. New writes are failing with OOM command not allowed errors. You need to decide on an eviction policy. Your cache stores session data (must not be evicted), product catalog (can be evicted and re-fetched), and rate limiting counters (must not be evicted).Which eviction policy do you choose and why, and what is the correct architectural fix?📄 06_Databases.md
📌 # 6.6 ElastiCache — Redis vs Memcached, Cluster Mode
🔖 ## 🧩 Redis Key Features


Q80 — S3 Multipart Upload + Incomplete Upload CostsYour billing team notices S3 storage costs are higher than expected. The bucket stores large video files uploaded via multipart upload. Investigation shows the bucket contains 500GB of data you can see in the console, but you're being charged for 800GB. Where is the missing 300GB and how do you fix it permanently?📄 04_Storage.md
📌 # 4.6 S3 — Event Notifications, S3 Select, Multipart Upload
🔖 ## 🧩 Multipart Upload → incomplete multipart uploads section


Q81 — ECR Lifecycle PoliciesYour ECR repositories are growing unbounded. The prod-api repository has 2,000 images — most are old dev/PR builds that will never be used again. Your storage bill for ECR is $400/month. Design a lifecycle policy that: keeps the last 5 production images (tagged with v), deletes untagged images after 1 day, and removes dev/PR images (tagged dev- or pr-) older than 14 days.📄 05_Containers_Serverless.md
📌 # 5.2 ECR — Image Lifecycle, Scanning, Replication
🔖 ## 🧩 Image Lifecycle Policies

Q82 — Lambda LayersYour organization has 50 Lambda functions across 10 teams. Each function bundles the same 200MB set of dependencies (pandas, numpy, scikit-learn). Deployment packages are slow to upload and hitting the 250MB unzipped size limit. How do Lambda Layers solve this, what are the limits, and what is the critical operational gotcha when you update a layer?📄 05_Containers_Serverless.md
📌 # 5.5 Lambda — Execution Model, Triggers, Layers, Concurrency
🔖 ## 🧩 Lambda Layers

Q83 — EFS Performance Modes and Mount TargetsYour team is deploying a WordPress fleet behind an ASG. Media uploads must be shared across all instances. You configure EFS and mount it on your EC2 instances. Three weeks later you notice EFS costs are 10x higher than expected, and file operations on large media files are slower than anticipated.What performance mode and throughput mode should you have chosen, and what is causing the high cost?📄 04_Storage.md
📌 # 4.4 EFS — Use Cases, Performance Modes, Mount Targets
🔖 ## 🧩 Performance Modes and ## 🧩 Storage Classes & Lifecycl


Q84 — ASG Lifecycle Hooks + Instance RefreshYour ASG runs a Java application that takes 3 minutes to fully initialize. During a rolling deployment (Instance Refresh), new instances are marked healthy by the ALB after 30 seconds (the health check passes on /health) but the JVM isn't fully warmed up yet. Users get slow responses for 3 minutes after each batch of new instances join.What two mechanisms solve this at different layers, and what is Instance Refresh used for vs a scaling event?📄 02_Compute.md
📌 # 2.3 Auto Scaling Groups (ASG)
🔖 ## 🧩 Lifecycle Hooks (Frequently Asked) and ## Instance Refresh


Q85 — Route 53 Private Hosted Zones + Split-Horizon DNS
Your application runs in a VPC. Internally, api.company.com should resolve to the private IP 10.0.1.50. Externally (from the internet), api.company.com should resolve to the ALB's public DNS. You also have on-premises servers that need to resolve internal AWS service names like rds.internal.company.com.
What Route 53 features implement each requirement and what must be configured for on-premises DNS resolution to work?
📄 03_Networking_VPC.md
📌 # 3.5 Route 53 — Hosted Zones, Routing Policies
🔖 ## 🧩 Hosted Zones → Split-horizon DNS section


Q86 — Redshift Distribution StylesYour Redshift data warehouse has two large tables: sales (500M rows, frequently joined with customers) and customers (50M rows). Query performance is poor — the query planner shows massive data redistribution across nodes during joins. What distribution styles do you assign to each table and why, and what is the risk of using DISTKEY incorrectly?📄 06_Databases.md
📌 # 6.10 Redshift — Architecture, Distribution Styles, Sort Keys
🔖 ## 🧩 Distribution Styles


Q87 — KMS Multi-Region KeysYour application encrypts customer data in us-east-1 using a KMS CMK. For disaster recovery, you've set up an Aurora Global Database secondary in eu-west-1. During a failover test, the eu-west-1 application tier cannot decrypt data — it gets KMS.NotFoundException. What is the root cause and what KMS feature solves it without re-encrypting all data?📄 08_Security_Compliance.md
📌 # 8.8 KMS — Multi-Region Keys, Cross-Account Access, Grants
🔖 ## 🧩 Multi-Region Keys

Q88 — Session PoliciesA contractor needs temporary access to your production S3 bucket prod-reports for exactly 4 hours to download specific files from the Q4-2024/ prefix only. Your existing developer-role has broad S3 permissions across all buckets. How do you grant the contractor scoped access without creating a new IAM role or modifying existing policies?📄 08_Security_Compliance.md
📌 # 8.7 IAM — ABAC, Session Policies
🔖 ## 🧩 Session Policies


Q89 — AWS Config Auto-Remediation + Conformance PacksYour security team wants: (1) any EC2 Security Group with port 22 open to 0.0.0.0/0 to be automatically fixed within 5 minutes of creation, and (2) a single command to deploy 50+ security rules across all 40 accounts in your organization for PCI-DSS compliance.What AWS Config features implement each requirement and what is the critical warning about automatic remediation?📄 08_Security_Compliance.md
📌 # 8.6 AWS Config — Rules, Conformance Packs, Remediation
🔖 ## 🧩 Automated Remediation and ## 🧩 Conformance Packs

Q90 — CloudFront Origin Access Control (OAC)
Your React SPA is served from a private S3 bucket via CloudFront. A security scanner reports that users can bypass CloudFront and access S3 objects directly using the S3 bucket URL (https://my-bucket.s3.amazonaws.com/index.html). This bypasses your WAF rules attached to CloudFront. How do you fix this, and what is the difference between the legacy OAI approach and the modern OAC approach?
📄 03_Networking_VPC.md
📌 # 3.6 CloudFront — Distributions, Behaviors, Origins, Cache Invalidation
🔖 ## 🧩 CloudFront Security

Q91 — EKS Managed vs Self-Managed Node GroupsYour EKS cluster needs three different node configurations: standard application nodes (m6i.xlarge), GPU nodes for ML inference (g4dn.xlarge), and nodes with a custom kernel module for network packet processing. Which node group type do you use for each, and what is the key operational advantage of Managed Node Groups during a Kubernetes version upgrade?📄 05_Containers_Serverless.md
📌 # 5.4 EKS — Architecture, Node Groups, Managed vs Self-Managed
🔖 ## 🧩 Node Groups


Q92 — ECS Fargate Resource CombinationsA developer creates an ECS Fargate task definition with cpu: 256 (0.25 vCPU) and memory: 8192 (8GB). The task fails to register with the error "Invalid CPU or memory value specified." They then try cpu: 512 and memory: 8192 — same error. What is wrong and what is the valid combination?📄 05_Containers_Serverless.md
📌 # 5.9 Fargate — Resource Limits, Networking, Security
🔖 ## 🧩 Resource Limits

Q93 — CPU Steal TimeYour EC2 m5.large instance running a Node.js API shows 85% CPU utilization in CloudWatch but the application feels sluggish and throughput is much lower than expected. When you SSH in and run top, you see %us: 15%, %sy: 5%, %id: 68%, %st: 12%. What does the %st value mean, what causes it, and what are your options to fix it?📄 02_Compute.md
📌 # 2.1 EC2 — Instance Types, AMIs, Key Pairs, User Data
🔖 ## CPU Steal Time — the hidden performance thief


Q94 — T-Series CPU CreditsYour application runs on a t3.small instance. Performance is fine during the day but degrades significantly every night during a batch job that runs for 2 hours. CloudWatch shows CPU at 100% during the batch. The next morning, performance is slow for about 30 minutes before returning to normal. What is happening and what are your options?📄 02_Compute.md
📌 # 2.1 EC2 — Instance Types, AMIs, Key Pairs, User Data
🔖 ## Instance Type Families → t-family CPU credits section

Q95 — Launch Templates vs Launch ConfigurationsYour team is setting up a new ASG and a colleague uses a Launch Configuration. You recommend switching to a Launch Template instead. Your colleague asks: "They do the same thing — why does it matter?" Give three specific capabilities that Launch Templates have that Launch Configurations don't, and name one scenario where the difference is critical for cost optimization.📄 02_Compute.md
📌 # 2.4 Launch Templates vs Launch Configurations
🔖 ## ⚙️ Key Differences


Q96 — DynamoDB Single-Table Design PatternsYou're designing a DynamoDB schema for a multi-tenant SaaS application. You need to support these access patterns: (1) get user profile by userId, (2) get all orders for a user, (3) get a specific order, (4) get all products in a category. A colleague suggests four separate tables. Why is single-table design better here, and show the PK/SK structure that supports all four access patterns.📄 06_Databases.md
📌 # 6.8 DynamoDB — Hot Partition Problem, Adaptive Capacity, Design Patterns
🔖 ## 🧩 DynamoDB Design Patterns


Q97 — Egress-Only IGW + NAT Gateway vs NAT InstanceYour VPC has IPv6-enabled EC2 instances in private subnets that need to initiate outbound connections to the internet (for software updates) but must NOT be reachable from the internet. You also have a team asking about replacing NAT Gateway with a NAT Instance to save costs. Address both questions.📄 03_Networking_VPC.md
📌 # 3.10 Egress-Only IGW, NAT Gateway vs NAT Instance
🔖 ## 🟢 Egress-Only Internet Gateway and ## 🔧 NAT Gateway vs NAT Instance


Q98 — ADOT vs X-Ray SDK
Your organization is standardizing on OpenTelemetry for observability. Some teams use X-Ray SDK directly, others use ADOT. A new team asks: "Should we instrument our ECS services with X-Ray SDK or ADOT?" What is the fundamental difference, when is ADOT the right choice, and what does ADOT enable that X-Ray SDK cannot?
📄 07_Observability_Monitoring.md
📌 # 7.8 AWS Distro for OpenTelemetry (ADOT)
🔖 ## 🧩 ADOT vs X-Ray SDK vs CloudWatch Agent


Q99 — CloudWatch Contributor Insights
Your DynamoDB table is being throttled despite having sufficient provisioned capacity. You suspect a hot partition but don't know which partition keys are causing it. Your API Gateway is also receiving unusual traffic but you can't identify which users or IPs are responsible. What CloudWatch feature answers both questions automatically, and how does it differ from writing custom Logs Insights queries?
📄 07_Observability_Monitoring.md
📌 # 7.4 CloudWatch Dashboards & Contributor Insights
🔖 ## 🧩 Contributor Insights


Q100 — CloudWatch Metric Filters
Your application logs JSON to CloudWatch Logs. Each log line contains {"level":"ERROR","latency":145,"path":"/api/orders","userId":"user123"}. Your team wants: (1) a CloudWatch metric tracking error count per minute, and (2) a metric tracking actual latency values (not just counts) for P99 alarm. What are the limitations of Metric Filters for requirement 2, and what is the alternative?
📄 07_Observability_Monitoring.md
📌 # 7.2 CloudWatch Logs — Log Groups, Metric Filters, Insights
🔖 ## 🧩 Metric Filters


Q101 — ALB vs NLB: Source IP, Security Groups, Cross-ZoneA developer reports that after migrating from NLB to ALB, their EC2 application's IP-based rate limiting stopped working — it's now rate-limiting by the ALB's IP instead of the client's real IP. They also notice their EC2 security group rule referencing "the load balancer's SG" no longer works after switching back to NLB. Explain both behaviors and the correct fix for each.📄 02__Compute.md
📌 # 2.5 Elastic Load Balancing — ALB, NLB, CLB, GWLB
🔖 ## 🧩 ALB vs NLB — Security Group Behavior


Q102 — FSx Types: Windows vs Lustre vs ONTAPThree teams come to you with storage requirements: (1) a .NET team needs shared NTFS storage with Active Directory authentication for Windows EC2 instances, (2) an ML team needs a file system that can deliver 1 million IOPS for GPU training jobs with lazy loading from S3, (3) a database team needs a file system that supports NFS, SMB, AND iSCSI simultaneously with instant zero-copy clones for dev/test environments. Which FSx type for each, and why?📄 04_Storage.md
📌 # 4.8 FSx — Windows, Lustre, NetApp ONTAP
🔖 ### FSx for Windows File Server, ### FSx for Lustre, ### FSx for NetApp ONTAP

Q103 — Storage Gateway TypesYour company has three on-premises requirements: (1) a Linux NAS server that should transparently archive infrequently accessed files to S3 without application changes, (2) Windows backup software (Veeam) that currently writes to a physical tape library and must continue using the same backup procedures, (3) a VMware environment that needs a local iSCSI block device but wants AWS to hold the primary copy with on-prem as a cache. Which Storage Gateway type for each?📄 04_Storage.md
📌 # 4.9 Storage Gateway — Types and Use Cases
🔖 ## 🧩 Four Types

Q104 — CLI Credential Precedence + dry-runA developer runs aws s3 ls from their laptop and gets an AccessDenied error. They have a correct ~/.aws/credentials file with valid keys. Their colleague runs the exact same command from the same terminal and it works. Later, the developer runs aws ec2 run-instances --dry-run and gets a DryRunOperation error — they panic thinking something is wrong. Explain both situations.📄 01_AWS_Core_Fundamentals.md
📌 # 1.3 AWS CLI & SDK Basics
🔖 ## 🧩 CLI Installation and Configuration and ## 🧩 CLI Power User Techniques

Q105 — AZ Names vs AZ IDs + Consolidated BillingYour platform team shares a Transit Gateway from Account A with Account B. Both teams try to deploy resources into "us-east-1a" but end up in different physical AZs, causing unexpected latency. Separately, your finance team asks why Reserved Instances purchased in the management account apply discounts to workloads in member accounts, and whether member accounts can opt out. Explain both.📄 01_AWS_Core_Fundamentals.md
📌 # 1.1 AWS Global Infrastructure and # 1.4 AWS Organizations & Multi-account Strategy
🔖 ## 🧩 Availability Zones (AZs) and ## 🧩 Consolidated Billing

Q106 — ECS Task Role vs Execution RoleYour ECS Fargate task is failing at startup with two different errors at different times: sometimes "CannotPullContainerError: access denied to ECR", sometimes the container starts but immediately logs "AccessDenied calling dynamodb:PutItem". A junior engineer suggests "just attach AdministratorAccess to fix both". Explain why there are two separate errors, why AdministratorAccess is wrong, and what the minimal correct fix is for each.📄 05_Containers_Serverless.md
📌 # 5.1 ECS — Clusters, Tasks, Services, Task Definitions
🔖 ## Two IAM Roles in ECS — Critical Interview Topic

Q107 — Aurora Storage ArchitectureA colleague claims "Aurora Multi-AZ works just like RDS Multi-AZ — it keeps a synchronous standby in another AZ." Correct this misconception. Explain Aurora's actual storage architecture, why it can survive losing an entire AZ without data loss, and why Aurora failover is typically 4x faster than RDS Multi-AZ failover.📄 06_Databases.md
📌 # 6.7 Aurora — Storage Architecture, Fast Failover, Parallel Query
🔖 ## 🧩 Storage Architecture Deep Dive

Q108 — RDS Automated Backups vs SnapshotsA developer is about to run a major schema migration on a production RDS PostgreSQL database. They ask: "Should I take a manual snapshot or can I rely on automated backups? What's the difference?" After the migration, a data corruption bug is discovered 6 hours later. Walk through exactly how you recover, what the recovered database endpoint looks like, and what happens to the original instance.📄 06_Databases.md
📌 # 6.3 RDS — Parameter Groups, Option Groups, Automated Backups, Snapshots
🔖 ## 🧩 Automated Backups and ## 🧩 DB Snapshots


Q109 — CloudFront Behaviors + Cache Key + Signed URLsYour SPA (React app) is served via CloudFront backed by S3. After deploying a new version, users still see the old version for up to 24 hours. Separately, your premium video content in S3 must only be accessible to paying subscribers for a limited time. Address both requirements, and explain why versioned filenames are better than cache invalidation for the first problem.📄 03_Networking_VPC.md
📌 # 3.6 CloudFront — Distributions, Behaviors, Origins, Cache Invalidation
🔖 ## 🧩 Cache Policies & TTLs and ## 🧩 CloudFront Security


110 — VPC Peering Non-Transitivity + ExternalIdTwo separate questions your security team asks: (1) "We have VPC-A peered with VPC-B, and VPC-B peered with VPC-C. Can VPC-A reach VPC-C through VPC-B?" (2) "We're giving a third-party vendor access to our S3 bucket via cross-account role assumption. They claim their system is secure. What prevents their system from being tricked into accessing another customer's AWS resources using their same IAM role?" Answer both.📄 01_AWS_Core_Fundamentals.md
📌 # 1.2 IAM — Users, Groups, Roles, Policies
🔖 ## 🧩 IAM Roles — Deep Dive → ExternalId section📄 03_Networking_VPC.md
📌 # 3.3 VPC Peering & Transit Gateway
🔖 ## ⚠️ VPC Peering Limitations — Non-Transitivity


Q111 — GWLB + Centralized Egress InspectionYour security team mandates that ALL outbound internet traffic from 20 VPCs must pass through a fleet of third-party firewall appliances (Palo Alto) for deep packet inspection before reaching the internet. A colleague suggests putting the firewalls behind an ALB. Why won't ALB work here, and what is the correct AWS service? Walk through the packet flow from a private EC2 instance to the internet.📄 02__Compute.md
📌 # 2.5 Elastic Load Balancing — ALB, NLB, CLB, GWLB
🔖 ## 🧩 GWLB — Gateway Load Balancer (Layer 3)📄 10_Infrastructure_Automation.md
📌 # 10.5 Service Control Policies
🔖 ## 🧩 Production SCP Examples (centralized egress pattern)


Q112 — RDS Parameter GroupsYour PostgreSQL RDS instance is generating thousands of slow query log entries but they're not appearing in CloudWatch Logs. You also need to enable pg_stat_statements extension for query analysis. A colleague tries to modify the default parameter group but gets an error. Walk through all three issues and their fixes.📄 06_Databases.md
📌 # 6.3 RDS — Parameter Groups, Option Groups, Automated Backups, Snapshots
🔖 ## 🧩 Parameter Groups and ## 🧩 RDS Monitoring


Q113 — S3 Versioning + Delete MarkersA developer runs aws s3 rm s3://prod-bucket/important-file.csv on a versioning-enabled bucket and panics thinking the file is gone. Explain exactly what happened, how to recover the file, and then explain the difference between this scenario and when a file is truly unrecoverable. Also: your lifecycle policy expires objects after 90 days but old versions are accumulating and tripling storage costs — fix it.📄 04_Storage.md
📌 # 4.1 S3 — Buckets, Objects, Storage Classes, Versioning
🔖 ## 🧩 Versioning

Q114 — CloudWatch High-Resolution Metrics + Agent ProcstatYour team's SLA requires detecting Lambda throttling within 10 seconds of occurrence. Standard CloudWatch metrics won't meet this. Separately, you need to alert when your Nginx process on EC2 exceeds 2GB RAM usage and when it spawns more than 200 worker threads. What configuration achieves each requirement?📄 07_Observability_Monitoring.md
📌 # 7.1 CloudWatch Metrics — Namespaces, Dimensions, Resolution
🔖 ## 🧩 Resolution📄 07_Observability_Monitoring.md
📌 # 7.7 CloudWatch Agent — Custom Metrics, Procstat
🔖 ## 🧩 Procstat Plugin


Q115 — App Mesh / Service Mesh ConceptsYour microservices team has 15 services in ECS. They report: retries are implemented differently in each service (Go uses one library, Python another, Java another), mTLS between services is inconsistently enforced, and distributed tracing is missing for 6 services. A colleague suggests "we should standardize the retry library." Why is that the wrong solution, and what does AWS App Mesh provide that solves all three problems without changing application code?📄 05_Containers_Serverless.md
📌 # 5.8 App Mesh & Service Mesh Concepts
🔖 ## 🟢 What It Is in Simple Terms and ## ⚙️ How App Mesh Works


Q116 — ECS Fargate Networking Deep DiveYour ECS Fargate service is behind an ALB. A developer registers the service with target type instance and gets no healthy targets. After switching to target type ip, it works — but now they notice inter-AZ latency between the ALB and tasks. They also ask why Fargate tasks in a private subnet with assignPublicIp: DISABLED can still reach S3 but cannot reach external APIs without a NAT Gateway. Explain all three.📄 05_Containers_Serverless.md
📌 # 5.9 Fargate — Resource Limits, Networking, Security
🔖 ## 🧩 Fargate Networking


Q117 — S3 Lifecycle Transitions: Waterfall + Minimum Duration CostsYour team sets up a lifecycle policy that transitions objects to Glacier Flexible after 7 days and deletes them after 30 days. Finance reports the S3 bill is higher than expected. A second policy transitions objects from Standard directly to Glacier Deep Archive — this also generates unexpected costs. Identify all the mistakes and fix them.📄 04_Storage.md
📌 # 4.3 S3 — Lifecycle Policies, Replication, Presigned URLs
🔖 ## 🧩 Lifecycle Policies

Q118 — AWS DetectiveAfter a GuardDuty alert fires for UnauthorizedAccess:IAMUser/MaliciousIPCaller, your incident response runbook says "check blast radius in Detective." A junior engineer asks why you'd use Detective instead of just querying CloudTrail directly in Athena. Explain what Detective provides that Athena cannot, and what Detective needs to become useful.📄 08_Security_Compliance.md
📌 # 8.10 Macie, Detective, Audit Manager
🔖 ## 🧩 Amazon Detective


Q119 — Redshift Sort Keys + VACUUM
Your Redshift analytics queries on a 2TB sales table are slow. EXPLAIN shows full table scans despite the table having a sort key on sale_date. Your DBA says "just add more nodes." You suspect the sort key isn't being used effectively. What are the two likely causes, and why does Redshift require VACUUM while traditional databases don't?
📄 06_Databases.md
📌 # 6.10 Redshift — Architecture, Distribution Styles, Sort Keys
🔖 ## 🧩 Sort Keys

Q120 — IAM Groups Not Principals + CLI Pagination
Two quick production gotchas: (1) Your security team writes a bucket policy to grant read access to the "developers" IAM Group. It doesn't work despite being syntactically correct. Why? (2) A script running aws ec2 describe-instances in an account with 3,000 instances only returns 1,000 results and your automation silently processes incomplete data. Why does this happen and what are the two fixes?
📄 01_AWS_Core_Fundamentals.md
📌 # 1.2 IAM — Users, Groups, Roles, Policies
🔖 ## ⚠️ Tricky Edge Cases / Gotchas
📄 01_AWS_Core_Fundamentals.md
📌 # 1.3 AWS CLI & SDK Basics
🔖 ## 🧩 CLI Output Formats and Filtering and ## ⚠️ Tricky Edge Cases / Gotchas


Q121 — EBS RAID + io2 Block ExpressYour Oracle RAC database needs 256,000 IOPS on a single volume and must attach to 16 EC2 instances simultaneously. Your analytics team needs a scratch volume delivering 120,000 IOPS from two combined EBS volumes. What volume type and configuration for each, and why does AWS explicitly warn against RAID 5/6 on EBS?📄 04_Storage.md
📌 # 4.7 EBS — RAID Configurations, io2 Block Express

Q122 — Private API Gateway
Your internal API must be accessible from on-premises (via Direct Connect) and two specific VPCs, but completely blocked from the internet — even with valid API keys. A colleague suggests "just use WAF IP allowlisting on a public API." Why is that insufficient, and walk through the complete architecture using Private API Gateway including how resource policies enforce per-consumer access control.
📄 Interview2.md
📌 # Scenario 5 — Private API Gateway

Q123 — ECS EC2 vs Fargate DecisionYour team is migrating three workloads to ECS: (1) a GPU-based ML inference service, (2) 200 small microservices each needing 0.25 vCPU and 512MB RAM, (3) a batch job that runs for 10 minutes every hour and needs zero idle cost. Which launch type for each, and what is the one scenario where EC2 launch type is definitively cheaper than Fargate even without GPU?📄 05_Containers_Serverless.md
📌 # 5.3 ECS Launch Types — EC2 vs Fargate
🔖 ## 🧩 When to Choose Which


Q124 — Cross-Region DB + Aurora Global (Interview2 Sc 2)Your SaaS app runs in us-east-1. GDPR requires EU customer data stays in eu-west-1. The EU app tier needs writes to go to eu-west-1. Your US app tier needs read access to EU data with p99 < 50ms. A colleague suggests "just use a cross-region read replica." Why is that wrong, and what is the complete correct architecture including how you handle the physics problem of cross-region latency?📄 Interview2.md
📌 ## Scenario 2 — Application in Region A Accessing a Database in Region B

Q125 — On-Prem Migration + DMS + DX Zero-Downtime (Interview2 Sc 3)You're migrating a live Oracle database (500GB, 50K transactions/day) from on-premises Mumbai to Aurora PostgreSQL in ap-south-1. Downtime must be under 2 minutes. Walk through the complete migration architecture, the exact cutover sequence, and the three things that will silently break your cutover if not prepared in advance.📄 Interview2.md
📌 ## Scenario 3 — Hybrid Connectivity: On-Premises to AWS with Zero-Downtime Cutover


Q126 — Cross-Account S3 Pipeline + KMS Re-encryption (Interview2 Sc 7)Raw data lands in Account A's S3 (encrypted with KMS Key A). A Spark job in Account B must read it, process it, and write results to Account C's S3 (encrypted with KMS Key C). Account D's analysts need read-only access to Account C's results. Account A must be completely inaccessible to Account D. Walk through every IAM and KMS policy required, and name the single most commonly missed step that causes AccessDenied.📄 Interview2.md
📌 ## Scenario 7 — Cross-Account S3 Data Pipeline with Strict Security Boundaries


Q127 — Microservices Cross-Account PrivateLink + mTLS (Interview2 Sc 8)Order-service on EKS in Account A calls payment-service on EKS in Account B. Requirements: no internet, only payment-service exposed (not full VPC), payment-service IPs change as pods scale, mTLS enforced between services, <2ms network overhead. Walk through the complete architecture and explain why you cannot use a fixed IP approach.📄 Interview2.md
📌 ## Scenario 8 — Microservices Across Accounts Communicating Without Internet Exposure


Q128 — Lambda Cross-Account RDS Proxy via PrivateLink + IAM Auth (Interview2 Sc 11)A Lambda function in Account A (Application) needs to query an RDS PostgreSQL database in Account B (Database). Account B has no internet access, no VPC peering, and only RDS Proxy should be exposed — not the full VPC. IAM database authentication is required (no passwords). Walk through the complete architecture and explain the specific step that generates an IAM auth token that Account B's RDS Proxy will actually accept.📄 Interview2.md
📌 ## Scenario 11 — Database in a Locked-Down Account Accessed by Lambda in Another Account



