**Elastic Compute Cloud (EC2)** is a web service that provides resizable compute capacity in the cloud. Allows you to launch virtual machines (VMs) with different configurations.

- Commands: https://github.com/nawab312/AWS/blob/main/Compute/EC2/Commands.md

**EC2 Instance Types**
- General Purpose: Balanced CPU, memory, and networking (e.g., T3, M5).
- Compute Optimized: High-performance CPU for intensive tasks (e.g., C5, C6i).
- Memory Optimized: Large RAM for in-memory databases (e.g., R5, X1).
- Storage Optimized: High IOPS storage for big data (e.g., I3, D2).
- Accelerated Computing: GPU-based workloads (e.g., P4, G5).

**EC2 Pricing Models**
- On-Demand: Pay as you go, no commitments (flexibility, but costly).
- Reserved Instances (RI): Up to 75% savings with long-term commitment (1 or 3 years).
- Spot Instances: Up to 90% cheaper but can be terminated anytime.
- Savings Plans: Flexible alternative to RIs with cost savings.
- Dedicated Hosts: Physical servers for compliance needs.

**Key Components of EC2**
- AMI (Amazon Machine Image): Pre-configured OS and software stack for launching instances
- Instance Types: Determines the hardware configuration (vCPU, RAM, storage).
- Security Groups: Acts as a virtual firewall for controlling inbound/outbound traffic.
- Elastic Block Store (EBS): Persistent storage that can be attached to instances.
- Elastic IP (EIP): Static, public IP address that you can assign to instances.
- Key Pairs: SSH authentication for secure access to instances.
- IAM Roles: Grant permissions to instances without storing credentials.

**EC2 Storage Options**
- Instance Store: Temporary storage (lost when the instance stops).
- EBS: Persistent block storage (snapshots available for backup).
- EFS (Elastic File System): Managed file storage for multiple EC2 instances.

**EC2 Placement Groups** are a way to control the placement of instances within a specific availability zone (AZ) to meet the requirements of your application. 
Placement groups enable you to manage how your EC2 instances are physically located on underlying hardware, which can help improve performance, fault tolerance, and scalability. 
There are three types of placement groups in AWS:
- **Cluster Placement Group**
  - Purpose: Used to launch instances close to each other within a single Availability Zone (AZ) for low-latency, high- throughput communication
  - Use Case: Ideal for applications that require high-performance computing (HPC) (that rely on fast data transfer between instances), like big data processing, scientific simulations, or gaming workloads, where network performance and low latency are critical.
  - Key Features:
    - All instances in the group are placed physically close to each other.
    - Ensures low-latency communication between instances.
    - It’s important to note that instances in a cluster placement group may share the same underlying hardware, so there's a risk of hardware failure affecting all instances in the group.
  ![image](https://github.com/user-attachments/assets/ac2361d3-1d5e-418a-ba84-2082c603ccb1)
- **Spread Placement Group**
  - Distributes instances across multiple distinct underlying hardware to reduce the risk of correlated failures, ensuring high availability.
  - Use Case: Suitable for applications that require high availability but are not dependent on low-latency communication between instances
  - Key Features:
    - Instances are spread across different physical hardware within the same AZ.
    - Can have up to 7 running instances per AZ in a spread placement group.
  ![image](https://github.com/user-attachments/assets/0078b87f-e09c-4a9e-bdd1-fc2510af3e53)
- **Partition Placement Group**
  - Purpose: Divides the instances into logical groups (partitions) within a single AZ or across multiple AZs, ensuring that the instances in each partition do not share the same underlying hardware.
  - Key Features:
    - Instances are grouped into partitions, and each partition is placed on distinct hardware
    - Instances in different partitions don’t share the same underlying hardware, providing fault isolation.
  ![image](https://github.com/user-attachments/assets/aa18713a-065b-46ff-9718-a896b3727776)



