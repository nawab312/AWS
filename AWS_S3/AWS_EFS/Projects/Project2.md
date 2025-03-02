You are a **DevOps Engineer** working for a banking client that wants to migrate their legacy monolithic application to a containerized microservices architecture on Amazon EKS.
The application needs **shared storage** for:
- **Session state data** (to maintain user sessions across multiple pods).
- **Transaction logs** (to ensure financial data integrity and compliance).
- **Report generation files** (processed by multiple services concurrently).

Your team decides to implement **Amazon EFS** as the **shared storage** solution. However, after deployment, you encounter the following challenges:
- High latency and slow performance when transaction logs are being written.
- Intermittent read/write failures from some microservices.
- Inconsistent access to files across multiple Availability Zones (AZs).
- EFS costs are higher than expected due to unexpected throughput usage.
- Security concerns since multiple applications have access to EFS, and compliance policies require fine-grained access control.

**Challenge:**
- How would you **properly configure Amazon EFS for high availability and performance** in an EKS environment?
- What **performance and throughput mode** would you choose for different workloads (session state, logs, reports)?
- How would you **troubleshoot intermittent read/write failures** in EKS pods using EFS?
- What strategies would you implement to **optimize AWS EFS costs** while maintaining reliability?
- How would you implement **fine-grained access control** to ensure only authorized microservices can access specific files in EFS?

- Your banking client now requires that the **reporting microservice should have read-only access**, while the **transaction processing microservice should have read/write access** to the same EFS file system. How would you enforce this using AWS EFS access points and IAM policies?

---

**EFS Configuration for High Availability & Performance:**
- Use **Regional EFS** across multiple AZs.
- Mount EFS using the **EFS CSI Driver for Kubernetes**.

**Performance Mode Selection:**
- **General Purpose mode** for session data (low latency).
- **Max I/O mode** for transaction logs and large-scale reports.

**Throughput Mode Selection:**
- **Bursting Throughput** for unpredictable workloads.
- **Provisioned Throughput** if consistent performance is needed.

**Troubleshooting Read/Write Failures:**
- Ensure **Security Groups allow NFS (port 2049)** between EKS worker nodes and EFS.
- Check **IAM roles and Kubernetes RBAC** for correct permissions.

**Cost Optimization Strategies:**
- **Enable EFS Intelligent-Tiering** for cost-efficient storage management. Use **Lifecycle policies** to move infrequent files to Infrequent Access storage.
- Deploy **EFS in the same AZ as worker nodes** to reduce cross-AZ transfer costs.

**Security & Access Control:**
- Use **AWS IAM + EFS Access Points** to define role-based access for microservices.
- Encrypt data at rest with **AWS KMS** and enforce **TLS encryption** for in-transit security.

