- Amazon S3 (Simple Storage Service) is an **object storage** service offered by AWS that provides scalability, security, durability, and high availability for storing and retrieving any amount of data from anywhere on the web. Stores objects (files, metadata, and permissions).
- An **S3 bucket** is a logical container in Amazon S3 that stores objects (files, metadata, and permissions).
  - Each bucket has a globally unique name.
  - Objects inside the bucket are stored as **key-value** pairs.
  - You can configure access policies, versioning, logging, and lifecycle rules for a bucket.
- Maximum size of a single object in Amazon S3 is **5 TB**. Multipart Upload allows uploading a **single object** as multiple parts, each up to **5 GB** in size. The minimum part size (except the last part) is **5 MB**. You can upload up to **10,000 parts per object**, enabling files up to 5 TB in size.
- You can create up to **100 S3 buckets per AWS account**. However, this limit can be increased up to **1,000 buckets per account** by requesting a quota increase from AWS. 
 
### Different S3 Storage Class ###
- **S3 Standard**: Frequently accessed data
- **S3 Intelligent-Tiering:** Use Case: Unknown or changing access patterns. Performance: Same as S3 Standard. Moves objects between frequent and infrequent tiers based on access. Slightly higher than Standard but optimizes automatically
- **S3 Standard-Infrequent Access (S3 Standard-IA):** Use Case: Infrequently accessed data but requires quick retrieval. Performance: Same as S3 Standard. Cost: Lower than Standard but charges for retrieval
- **S3 One Zone-Infrequent Access (S3 One Zone-IA)** Use Case: Infrequently accessed data, but doesn’t require multi-AZ resilience. Performance: Same as Standard. Cost: Cheaper than Standard-IA but stores data in only one AZ
- **S3 Glacier Instant Retrieval:** Use Case: Archive storage with milliseconds retrieval. Performance: Low latency retrieval. Cost: Lower than S3 Standard-IA but charges per GB retrieval
- **S3 Glacier Deep Archive:** Use Case: Long-term archival (years), lowest-cost storage. Retrieval Time: Standard: 12 hours, Bulk: 48 hours. Cost: Lowest among all S3 storage classes

![image](https://github.com/user-attachments/assets/835b3645-9024-4d44-93c3-16e8d1085789)

How does Amazon S3 ensure data **Durability** and **Availability**?
- Amazon S3 achieves 99.999999999% (11 nines) durability, meaning data loss probability is extremely low. This is achieved through:
  - When you upload an object to S3 (except for **One Zone-IA**), Amazon S3 automatically replicates it across at **least 3 Availability Zones (AZs)** in the region.
  - **S3 Versioning** allows multiple versions of an object, preventing accidental deletions or overwrites.
  - **Cross-Region Replication (CRR)** for Extra Protection
- Amazon S3 provides high availability by ensuring objects are always accessible when needed. This is achieved through:
  - Data is stored across multiple AZs, so even if one AZ goes down, S3 can serve the data from other locations.
  - S3 uses **load balancers** to distribute requests evenly across storage infrastructure, preventing bottlenecks. Requests are **automatically rerouted** to healthy nodes if failures occur.
 
**S3 Bucket Policy** https://github.com/nawab312/AWS/tree/main/Storage/AWS_S3/Bucket_Policy

**Track S3 Bucket Access with CloudTrail** https://github.com/nawab312/AWS/blob/main/Storage/AWS_S3/CloudTrail_S3.md
