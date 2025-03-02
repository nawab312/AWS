## Project: AWS EFS Implementation with Amazon EKS ##
**Objectives:**
- Deploy Amazon EKS and configure Amazon EFS as shared storage.
- Optimize Performance, Cost, and Security.
- Implement Fine-grained access control for different workloads.

---

### Step 1: Set Up Amazon EKS Cluster ###
- Create an **EKS Cluster** with at least **two worker nodes** across multiple AZs.
Follow this: https://github.com/nawab312/AWS/blob/main/AWS_EKS/Create_Cluster/Method1.md

### Step 2: Create an Amazon EFS File System ###
- Create an Amazon EFS file system in the same VPC as EKS.
```bash
aws efs create-file-system --region us-east-1 --performance-mode generalPurpose --throughput-mode bursting --encrypted
```
```bash
#Output
"FileSystemId": "fs-0a5d41af9211be4c2"
```

### Step 2: Create EFS Mount Targets ###
To allow **EKS worker nodes** to access the **EFS file system**, we create **mount targets** in **each subnet**.

- **Get the Subnet IDs of Your EKS Cluster**
```bash
aws eks describe-cluster --name my-eks-cluster --query "cluster.resourcesVpcConfig.subnetIds"
```
```bash
#Output
[
    "subnet-02e501cea315eb5a2",
    "subnet-09d781cd70121affa",
    "subnet-09737f74c8ac11cc5",
    "subnet-00a0c7e5ee0a1a570"
]
```

- **Create Security Group for EFS:** We must allow **NFS traffic (port 2049)** between EFS and EKS worker nodes.
```bash
aws ec2 create-security-group --group-name EFS-SG --description "Security Group for EFS" --vpc-id vpc-057c7710c1218cc95
```
```bash
#Output
{
    "GroupId": "sg-0f1c8d24461c3a960"
}
```
  - Allow NFS(2049 Port)
```bash
# source-group should be Security Groups of EKS Nodes
aws ec2 authorize-security-group-ingress --group-id sg-0f1c8d24461c3a960 --protocol tcp --port 2049 --source-group sg-04e66565c5bd4943f
```

- Create Mount Targets: For each subnet, run:
```bash
aws efs create-mount-target --file-system-id fs-0a5d41af9211be4c2 --subnet-id subnet-02e501cea315eb5a2 --security-groups sg-0f1c8d24461c3a960
aws efs create-mount-target --file-system-id fs-0a5d41af9211be4c2 --subnet-id subnet-09d781cd70121affa --security-groups sg-0f1c8d24461c3a960
aws efs create-mount-target --file-system-id fs-0a5d41af9211be4c2 --subnet-id subnet-09737f74c8ac11cc5 --security-groups sg-0f1c8d24461c3a960
aws efs create-mount-target --file-system-id fs-0a5d41af9211be4c2 --subnet-id subnet-00a0c7e5ee0a1a570 --security-groups sg-0f1c8d24461c3a960
```

