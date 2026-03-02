**Elastic Compute Cloud (EC2)** is a web service that provides resizable compute capacity in the cloud. Allows you to launch virtual machines (VMs) with different configurations.
- Commands: https://github.com/nawab312/AWS/blob/main/Compute/EC2/Commands.md

**EC2 Instance Types**
- General Purpose: Balanced CPU, memory, and networking (e.g., T3, M5).
- Compute Optimized: High-performance CPU for intensive tasks (e.g., C5, C6i).
- Memory Optimized: Large RAM for in-memory databases (e.g., R5, X1).
- Storage Optimized: High IOPS storage for big data (e.g., I3, D2).
- Accelerated Computing: GPU-based workloads (e.g., P4, G5).

**Graviton Instance**
- Graviton instances are EC2 instances powered by AWS-designed *ARM-based processors* (AWS Graviton chips), instead of traditional Intel/AMD x86 CPUs.
- They are used in instance families like: `t4g` `m6g` `c6g` `r6g`
- The “g” at the end means Graviton.
- Why Use Graviton?
  - Better Price/Performance: ~20–40% better price-performance compared to similar x86 instances.
  - Lower Cost: Graviton instances are generally cheaper than equivalent x86 types.
- When It Can Be a Problem:
  - Your application binary is compiled for x86
  - You use old Docker images built for amd64

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

**ENI**
- An ENI (Elastic Network Interface) in Amazon Web Services is basically:
  - The network card attached to your EC2 instance
  - It holds: Private IP, Public IP, Security groups, MAC address

**Golden AMI**
- A pre-configured, standardized machine image that contains the OS, required software, security patches, configurations, and sometimes even application code — used as the approved template to launch new EC2 instances.
- Why “Golden”?
  - Because: It is hardened, It is tested, It follows security standards, It is approved by the organization, It ensures consistency

**EC2 Storage Options**
- Instance Store: Temporary storage (lost when the instance stops).
- EBS: Persistent block storage (snapshots available for backup).
- EFS (Elastic File System): Managed file storage for multiple EC2 instances.

**EC2 Placement Groups** are a way to control the placement of instances within a specific availability zone (AZ) to meet the requirements of your application. 
Placement groups enable you to manage how your EC2 instances are physically located on underlying hardware, which can help improve performance, fault tolerance, and scalability. 
There are three types of placement groups in AWS:
- *Cluster Placement Group*
  - Purpose: Used to launch instances close to each other within a single Availability Zone (AZ) for low-latency, high- throughput communication
  - Use Case: Ideal for applications that require high-performance computing (HPC) (that rely on fast data transfer between instances), like big data processing, scientific simulations, or gaming workloads, where network performance and low latency are critical.
  - Key Features:
    - All instances in the group are placed physically close to each other.
    - Ensures low-latency communication between instances.
    - It’s important to note that instances in a cluster placement group may share the same underlying hardware, so there's a risk of hardware failure affecting all instances in the group.
  ![image](https://github.com/user-attachments/assets/ac2361d3-1d5e-418a-ba84-2082c603ccb1)
- *Spread Placement Group*
  - Distributes instances across multiple distinct underlying hardware to reduce the risk of correlated failures, ensuring high availability.
  - Use Case: Suitable for applications that require high availability but are not dependent on low-latency communication between instances
  - Key Features:
    - Instances are spread across different physical hardware within the same AZ.
    - Can have up to 7 running instances per AZ in a spread placement group.
  ![image](https://github.com/user-attachments/assets/0078b87f-e09c-4a9e-bdd1-fc2510af3e53)
- *Partition Placement Group*
  - Purpose: Divides the instances into logical groups (partitions) within a single AZ or across multiple AZs, ensuring that the instances in each partition do not share the same underlying hardware.
  - Key Features:
    - Instances are grouped into partitions, and each partition is placed on distinct hardware
    - Instances in different partitions don’t share the same underlying hardware, providing fault isolation.
  ![image](https://github.com/user-attachments/assets/aa18713a-065b-46ff-9718-a896b3727776)

**DNS Resolution**
The `/etc/resolv.conf` file in an EC2 instance (or any Linux system) is used to configure DNS (Domain Name System) resolution. It tells the instance which DNS servers to use to convert domain names (like google.com) into IP addresses.

Your EC2 instance needs to resolve domain names for various tasks, such as:
- Connecting to external APIs (e.g., `api.example.com`)
- Updating software (e.g., `yum update`, `apt update`)
- Accessing AWS services via domain names (e.g., `s3.amazonaws.com`)

```bash
cat /etc/resolv.conf
nameserver 169.254.169.253
options edns0
```

`169.254.169.253` is a special *AWS Internal DNS Resolver* that works inside a VPC.

**EC2 Health Checks**

*EC2 Console: 2/2 Checks*
- System Status Check
  - AWS checks its own infrastructure (host hardware, Hypervisor, networking at AWS side, etc.)
  - Failures here mean AWS has a problem (rare, but happens)
- Instance Status Checks
  - Can AWS reach your instance’s network stack
  - Is the instance responding to ARP?
    - ARP (Address Resolution Protocol) is a Layer 2 networking protocol used to map an IP address → MAC address inside the same subnet. Without ARP, machines in the same network cannot talk to each other.
    - When one server wants to send traffic to `10.0.1.25`, it knows the IP address. But Ethernet communication requires a MAC address, not an IP.
  - Has the OS booted properly?
  - Is the kernel responsive?
  - If this fails, it usually means:
    - OS kernel panic, Boot failure, Corrupted filesystem, Network misconfiguration, Instance stuck during startup
  - Instance status check verifies the OS-level reachability of my EC2 instance. It does not validate application health or resource utilization — for that we rely on CloudWatch metrics and load balancer health checks.

---

**If I lose the private key (.pem) for an EC2 instance. How can I access my EC2**

Case 1 — If You Have SSM Enabled
- If:
  - Instance has IAM role attached
  - SSM Agent installed
  - Outbound internet/NAT access
- You can connect via AWS Systems Manager Session Manager — no SSH key needed.

Case 2 — No SSM, No Key (Linux Instance)
- You must use the volume-detach method:
  - Stop the EC2 instance.
  - Detach the root EBS volume.
  - Attach it to another EC2 instance as secondary volume.
  - Mount the volume.
  - Edit
    ```bash
    /home/ec2-user/.ssh/authorized_keys
    ```
  - Add your new public key.
  - Detach volume.
  - Reattach to original instance.
  - Start instance.

---









