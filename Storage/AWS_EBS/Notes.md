- Amazon Elastic Block Store (EBS) is a highly available, scalable, and durable **block storage** service used with Amazon EC2. It provides persistent storage that remains intact even when the associated EC2 instance is stopped or terminated
- **Block Storage** – EBS provides block-level storage (like traditional hard drives or SSDs) that is attached to EC2 instances.
- **Persistence** – Unlike EC2 instance store, EBS volumes retain data even if the instance is stopped or terminated.
- **Durability** – Data is replicated within an Availability Zone (AZ) to prevent data loss.
- **Elasticity** – Volumes can be resized dynamically without downtime (Elastic Volumes feature).

**IOPS (Input/Output Operations Per Second)**
- The number of read/write operations that an EBS volume can handle per second.
- Measures how many operations can be performed.
- Unit: Operations per second.
- Use Case: Workloads that require low latency and frequent small reads/writes, such as databases (MySQL, PostgreSQL, MongoDB, etc.).

**Throughput**
- The amount of data transferred (read/write) per second.
- Measures how fast data is transferred.
- Unit: MB/s (Megabytes per second).
- Use Case: Workloads that involve large sequential data transfers, such as big data analytics, log processing, and video streaming.

### EBS Volume Types ###

**General Purpose SSD (gp3, gp2)**
- **gp3**
  - The gp3 volume is the latest generation of general-purpose SSDs and offers cost-effective storage with high performance.
  - It is suitable for a broad range of workloads, including system boot volumes, small-to-medium-sized databases, development environments, and applications requiring low-latency access.
  - Offers baseline performance of 3,000 IOPS and can scale up to 16,000 IOPS.
  - Throughput of up to 1,000 MB/s
- **gp2 (Older Generation):**
  - gp2 is the previous generation of general-purpose SSDs. While still widely used, it is being phased out in favor of the more efficient gp3
  - Provides 3 IOPS per GB of provisioned storage, with a maximum of 16,000 IOPS and 250 MB/s throughput

**Provisioned IOPS SSD (io2, io1)**
- **io2**
  - io2 is a high-performance SSD designed for I/O-intensive applications that require extremely high input/output operations per second (IOPS), such as large databases, high-performance computing (HPC), and critical business applications.
  - Provisioned IOPS of up to 64,000 IOPS per volume.
  - Throughput of up to 1,000 MB/s.
  - Use Case: *Large relational databases (e.g., Oracle, SQL Server)*, *NoSQL databases (e.g., MongoDB, Cassandra)*
  - Cost: Higher cost due to provisioned IOPS and high durability features.

**Throughput Optimized HDD (st1)**
- The st1 volume is designed for *workloads requiring high throughput rather than high IOPS*.
- This is ideal for large- scale, sequential workloads like big data analytics, log processing, and data warehousing.

**Cold HDD (sc1)**
- The sc1 volume is the lowest-cost storage option for infrequently accessed data.
- This is designed for cold storage or archival purposes where data is accessed only occasionally

![image](https://github.com/user-attachments/assets/37acef63-0142-4f52-bdc5-5f567e004898)
