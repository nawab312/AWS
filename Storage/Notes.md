**AWS Storage** refers to a set of cloud-based storage services that provide scalable, durable, and cost-effective solutions for different storage needs. AWS offers object storage, block storage, file storage, backup solutions, and hybrid cloud storage.

### AWS S3 vs EFS vs EBS - Use Cases & Differences ###
- **Amazon S3 (Object Storage)** https://github.com/nawab312/AWS/blob/main/Storage/AWS_S3/Notes.md
  - Stores objects (files, images, videos, backups).
  - Scalable & highly durable (11 nines durability).
  - Accessible via HTTP(S) – not tied to EC2.
  - Use Cases
    - Data lakes & big data analytics (store massive datasets)
    - Backup & disaster recovery (store backups from RDS, EBS, DynamoDB
    - Static website hosting (host HTML, CSS, JS files)
    - Media storage & streaming (videos, images, audio)
    - Machine learning datasets (store training data)
   
- **Amazon EFS (File Storage)** https://github.com/nawab312/AWS/blob/main/Storage/AWS_EFS/Notes.md
  - *Managed NFS (Network File System)* that multiple EC2 instances can access.
  - *Scales automatically* based on storage needs.
  - Provides *low-latency access* for shared file systems.
  - Supports *POSIX permissions* (ideal for Linux-based workloads).
  - Use Cases
    - Shared file storage (multiple EC2 instances access the same files)
    - Eg: You have a *web application* running on multiple EC2 instances in an *Auto Scaling Group*. The application needs a *shared storage system* to store *user-uploaded images, logs, or configuration files* that all instances can access.
    - Web applications (storing logs, configuration files)
    - Machine learning & big data processing (shared datasets)
    - Development & CI/CD environments (shared project files)
    - Eg: A DevOps team is working on a microservices-based application.
      - Multiple *developers* and *CI/CD* pipelines need access to the same project files.
      - The *Jenkins CI/CD* server needs shared storage to *cache dependencies, store build artifacts, and share logs* across multiple build agents.
      - *Solution:* Use Amazon EFS as a shared storage for project files and CI/CD build artifacts.
     
  - **Amazon EBS (Block Storage)** https://github.com/nawab312/AWS/blob/main/Storage/AWS_EBS/Notes.md
    - *Attached to EC2 instances*, like a hard drive for VMs.
    - Provides *low-latency, high-performance* block storage.
    - Requires *manual scaling* (pre-allocated storage size).
    - Supports *snapshots* (backups stored in S3).
    - Use Cases
      - Databases (RDS, MySQL, PostgreSQL, MongoDB, etc.)
      - Boot volumes for EC2 instances
      - High-performance applications (SAP, Oracle, gaming servers)
      - Big data analytics requiring low latency
     
![image](https://github.com/user-attachments/assets/73d0f56b-c34f-4112-af5e-0f00426c9c35)
