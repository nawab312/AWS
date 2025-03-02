**Amazon EFS** is a *cloud-native file storage service* that is accessible via the standard file system interface (like NFS - Network File System). It is ideal for applications that require shared access to files or persistent storage, particularly when multiple instances or resources need to access the same data concurrently. This makes EFS suitable for applications, websites, or services that need to share files among various compute resources.
- **Scalability:** EFS automatically scales your storage up or down as you add or remove files, meaning you only pay for the storage you use without needing to worry about provisioning
- **Regional Scope (Multi-AZ)** is the default behavior for EFS when you create it within a VPC. The file system will automatically be designed to span multiple AZs for high availability, unless otherwise specified.
![image](https://github.com/user-attachments/assets/7ca01162-36be-40df-82a9-0dd13b21ba3a)

- **Concurrent Access:** Multiple Amazon EC2 instances or other resources can access the EFS file system at the same time. It is designed for high-throughput workloads and is ideal for applications that require shared file storage.
- **Performance Modes:** EFS offers different performance modes to optimize for your specific use case:
  - **General Purpose Mode:** This is the default mode, providing low latency and high throughput for workloads that need consistent performance.
  - **Max I/O Mode:** This mode is designed for scale-out workloads that require high throughput and can tolerate slightly higher latencies.
- **Data Encryption:** EFS supports encryption of data at rest and in transit. You can configure encryption using AWS Key Management Service (KMS) for data at rest and use TLS for encrypting data in transit.

![image](https://github.com/user-attachments/assets/f51db425-22c5-4c83-9d3f-6d4685e00e2e)

- **Use Cases for EFS**
  - **Shared File Storage for Web Servers:** If you are running a fleet of web servers that need access to the same content, such as images, videos, or logs, EFS provides a simple, scalable solution for storing and serving these files.
  - **Big Data and Analytics:** EFS is ideal for workloads that require shared storage for large datasets. For example, if multiple instances are processing big data jobs or running analytics, EFS allows them to access the same data.
  - **Database Storage:** While EFS is not ideal for traditional relational databases (which typically use block storage like Amazon EBS), it can be used for shared file storage in some NoSQL database scenarios or for storing backups and logs.
  - **Home Directories:** EFS can be used to provide shared home directories for EC2 instances, allowing users and applications to store and access files easily.
 
- **Performance Considerations**
  - **Throughput:** Throughput Mode determines the rate at which your file system can read and write data. EFS offers two primary throughput modes:
    - **Bursting Throughput Mode:** Throughput is tied to the amount of data stored in the file system, meaning it automatically scales as your storage grows. This mode works well for most general-purpose workloads that don't require consistent, high-throughput performance.
    - **Enhanced Throughput Mode:** Offers two options: Elastic and Provisioned. **Elastic Throughput (default under Enhanced)** Automatically adjusts to meet your performance needs, providing scalable throughput as your storage grows. It works in a way similar to Bursting Throughput, but with more flexibility for high-performance workloads. **Provisioned Throughput** You can set the throughput independently of the file system size. This is useful for workloads that require consistent and predictable performance, such as high-performance applications or databases, where you need guaranteed throughput regardless of the data stored
  - **Latency:** EFS is optimized for low-latency access, but performance may vary depending on the size of your data and the mode you use. The General Purpose mode offers low-latency, while Max I/O mode may have slightly higher latency but supports larger workloads.
![image](https://github.com/user-attachments/assets/55e11a23-914c-41b3-b126-8ef98e3f8f39)


- **EFS Storage Classes**
  - **EFS Standard** This storage class is designed for frequently accessed files. It is ideal for use cases where data needs to be accessed continuously or on-demand, such as web applications, content management systems, or user home directories.Provides low-latency and high-throughput access to files
  - **EFS Infrequent Access (IA)** This storage class is designed for files that are accessed less frequently but still need to be available when required. Files in this class cost less to store compared to EFS Standard. There is a charge for data retrieval
  - **EFS Archive Storage Class** is designed for long-term archival storage of files that are rarely accessed, but still need to be retained for compliance, backup, or other purposes. For Transition files to Archive **Throughput Mode must be Elastic**

- **EFS Lifecycle Management**
  - Allows you to automatically move files between storage classes based on how frequently they are accessed,
  - **Lifecycle Policies:** With lifecycle management, you can create policies that automatically move files to the EFS Infrequent Access (IA) storage class after they have not been accessed for a certain number of days.
  - **Transitioning Data:** Once a file hasn't been accessed for a specified period (e.g., 30 days), it will be moved to the IA storage class without requiring any manual action. When a file is accessed again, it will automatically be moved back to the EFS Standard class to ensure quicker access.

![image](https://github.com/user-attachments/assets/df624e64-bf11-44da-bb03-b36eb6112d4d)

- **Mount targets** are network endpoints that allow your Amazon EC2 instances, on-premises servers, or other resources to access an EFS file system.
  - Imagine you have an EFS file system for storing shared data across several EC2 instances in different availability zones. To ensure that each EC2 instance can access the file system, you create a mount target in each availability zone. Each mount target is associated with an IP address in the corresponding subnet, and your EC2 instances use those mount points to mount the file system and read/write data.

- **EFS Access Point** is a managed entry point that controls how applications access an Amazon EFS file system. It simplifies permissions by enforcing user/group IDs and restricting access to specific directories
  - Imagine you have a shared storage (EFS) used by multiple applications. One app needs access to `/data/app1`, and another app needs `/data/app2`. Instead of giving full access to the entire EFS, you create separate Access Points for each app, restricting them to their specific directories.

---

**Why You Don't Need a Kubernetes Service Account for Pods to Access AWS EFS**
- EFS Works Over NFS, Not AWS API
  - Unlike S3 or DynamoDB, which require authentication via IAM roles, EFS uses NFS (Network File System). NFS doesn’t rely on IAM authentication but instead: Uses Security Groups for network-level access. Uses POSIX permissions for file-level access.
- EFS Mounts are Handled by the EFS CSI Driver
  - Kubernetes uses the AWS EFS CSI Driver (`efs.csi.aws.com`) to mount EFS. The driver runs as a DaemonSet on worker nodes and automatically manages mounts.
- When Would You Need a Service Account?
  - If You are dynamically creating EFS file systems or access points from inside the pod.
  - If You are managing EFS lifecycle policies via AWS APIs.

