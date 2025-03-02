Your company is running a web application that requires a **shared file system** for multiple EC2 instances across **multiple Availability Zones (AZs)** in a **highly available and scalable** manner.
- The application writes logs and user-generated content to the shared storage.
- You notice that during high traffic periods, **read latency increases significantly**, affecting the performance of the application.
- The security team has also raised concerns about ensuring that only specific instances can access the file system.

Question:
- How will you design the EFS setup to optimize performance for high traffic and minimize latency?
- How will you enforce access control to ensure only specific instances can mount and access EFS?
- What cost optimization strategies can be applied while ensuring availability and performance?

---

## AWS EFS Hands-on Project: High Availability, Performance Optimization & Security ##
### Project Overview ###
- A **highly available** and **scalable** EFS setup for 2 EC2 instances across 2 Availability Zones (AZs).
- Optimize **performance** to reduce latency during high traffic.
- Implement **security** controls to allow only specific instances to access the EFS.
- Apply **cost optimization strategies** based on workload patterns.
- **Prerequisites** 2 EC2 Instances in 2 AZs (us-east-1a, us-east-1b)

![image](https://github.com/user-attachments/assets/1c6a90cf-39e5-4b2a-96ae-3294108e8f51)


### Step 1: Setup AWS EFS ###
- Go to **AWS Console → EFS → Create File System**.
- Create a security group for EFS.
  - Open the AWS Console → Go to EC2 → Security Groups. Click Create Security Group.
  - **Add an Inbound Rule** to allow NFS access: Type: `NFS`, Protocol: `TCP`, Port Range: `2049`, Source: `EC2 instance IPs`
- Attach the Security Group to AWS EFS
  - Go to **EFS** → Select your file system. Go to **Network** → Click on each **Mount Target**. Click **Manage Security Groups**. Attach the **EFS Security Group** (`nfs-sg`).

![image](https://github.com/user-attachments/assets/4096c5ce-b542-45c9-bc31-0cf4fb884c30)

- Check if EFS is accessible from EC2: `telnet <EFS-DNS-Name> 2049`

### Step2: Launch EC2 Instances and Mount EFS ###
```bash
sudo apt update
sudo apt install nfs-common -y
sudo mkdir /mnt/efs
sudo mount -t nfs4 <efs-dns-name>:/ /mnt/efs
```
- **Automate Mounting** on **Reboot** Add this entry to `/etc/fstab`:
```bash
fs-xxxxxx:/ /mnt/efs efs defaults,_netdev 0 0
```

### Step4: Performance Optimization ###
- Switch to **Max I/O Performance Mode**
```bash
aws efs update-file-system --file-system-id fs-xxxxxx --performance-mode maxIO
```

- Enable **EFS Caching (for high read performance)**
```bash
sudo mount -t nfserver=4.1, nconnect=4 fs-xxxxxx.efs.region.amazonaws.com:/ /mnt/efs
```



