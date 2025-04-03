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

---

### EBS Snapshots ###
An Amazon EBS Snapshot is a point-in-time (Captures the exact state of data at a specific moment, allowing restoration to that precise time.) backup of an Amazon Elastic Block Store (EBS) volume. Snapshots are incremental, meaning that only the changed blocks since the last snapshot are saved, reducing storage costs and improving efficiency. Key Concepts:
- Incremental Backups – Only changed data blocks are saved after the first full snapshot.
- Stored in Amazon S3 (internally) – EBS Snapshots are stored in S3 but are not visible in the S3 console.
- Restoration to Volumes – Snapshots can be used to create a new EBS volume in any AWS Region.
- Cross-Region & Cross-Account Sharing – Snapshots can be copied across regions and shared with other AWS accounts.
- Automated Snapshots – AWS Backup and Data Lifecycle Manager (DLM) can automate snapshot creation and deletion.

---

*How does the incremental nature of EBS snapshots reduce storage costs, and what impact does this have on restoring snapshots?*

The incremental nature of EBS snapshots means that after the first full backup, only changed data blocks are stored in subsequent snapshots. This reduces storage costs by avoiding duplicate data storage. When restoring a snapshot, AWS reconstructs the volume by retrieving data from the latest snapshot and any previous ones as needed. This can slightly impact restoration speed, but AWS optimizes it using **Fast Snapshot Restore (FSR)** for quicker access. Understanding Incremental Snapshots

Assume you have a 100 GB EBS volume and take snapshots over time as follows:
- Snapshot 1 (Full Backup)
  - The first snapshot is always a full backup.
  - It stores all 100 GB of data.
  - Total storage used so far: 100 GB
- Snapshot 2 (Incremental)
  - Let's say 10 GB of data changed since Snapshot 1.
  - AWS only stores the changed 10 GB.
  - Total storage used so far: 100 GB + 10 GB = 110 GB
- Snapshot 3 (Incremental)
  - Another 5 GB of data changes.
  - Only the changed 5 GB is stored.
  - Total storage used so far: 110 GB + 5 GB = 115 GB
 
What Happens During Restoration?
- If you restore Snapshot 3, AWS reconstructs the volume using:
  - Snapshot 1 (Base: 100 GB)
  - Snapshot 2 (Changes: +10 GB)
  - Snapshot 3 (Changes: +5 GB)
- Total data restored = 100 GB (Base) + 10 GB + 5 GB = 100 GB

---

*What Happens When You Delete an EBS Snapshot with Dependent Snapshots?*

Deleting a Snapshot with Dependencies
- If you delete a snapshot with newer snapshots still existing, AWS does not delete the actual data blocks that are still referenced by later snapshots.
- Instead, AWS only removes the metadata pointing to that snapshot.
- The dependent snapshots remain fully restorable because they still reference the needed data from earlier snapshots.

Deleting the Last Snapshot
- If you delete the last remaining snapshot, all data is permanently lost because no more references exist.

Example Scenario

Snapshots Created Over Time (100 GB Volume)
- Snapshot 1 (Full Backup) → 100 GB
- Snapshot 2 (Incremental) → 10 GB changed
- Snapshot 3 (Incremental) → 5 GB changed

What Happens When You Delete Snapshot 2?
- The 10 GB of changed blocks will not be deleted if Snapshot 3 still references them.
- AWS ensures Snapshot 3 remains usable by keeping the necessary data from Snapshot 2.
- Only the metadata for Snapshot 2 is deleted.

What Happens When You Delete Snapshot 3?
- If Snapshot 3 contained unique changed blocks that are not referenced in any other snapshot, AWS deletes them.
- Can I restore to the exact state of Snapshot 3?
  - No, since its metadata is deleted, you cannot restore the volume exactly as it was at Snapshot 3.

---

*What Happens Internally When You Copy an Encrypted EBS Snapshot to Another Region?*
- Data Decryption & Re-encryption
  - AWS decrypts the snapshot in the source region using the original KMS key.
  - The snapshot data is then securely transferred over AWS’s internal network.
  - In the destination region, AWS re-encrypts the snapshot using a KMS key of your choice (can be the same or a new key).
- Handling of KMS Encryption Keys
  - Cross-region KMS keys are not shared: The original KMS key does not move across regions.
  - You must specify a KMS key in the destination region (either an existing one or create a new one).
  - AWS re-encrypts the snapshot using this new KMS key.
- New Snapshot in Destination Region
  - After encryption, AWS creates a new snapshot ID in the destination region.
  - The copied snapshot retains the same data but is now encrypted with the new region’s KMS key.
  - The copied snapshot can now be used to create volumes in the new region.
 
---

*Why Does Restoring an EBS Volume from a Snapshot Take a Long Time?*

When you restore an EBS volume from a snapshot, AWS **lazily loads** data from Amazon S3 to the volume on demand. This means:
- The first read/write operations on blocks not yet loaded can be slow.
- AWS fetches data from the snapshot stored in S3, causing high latency for initial requests.

How to Speed Up Restoration & Improve I/O Performance?

Use Fast Snapshot Restore (FSR) (Best AWS Feature)
- AWS Feature: Fast Snapshot Restore (FSR) pre-warms the snapshot so that all data is immediately available on the volume.
- FSR eliminates lazy loading by preloading data before the volume is attached.

---
