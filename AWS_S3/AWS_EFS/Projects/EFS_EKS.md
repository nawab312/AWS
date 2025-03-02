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
```

### Step 3: Deploy the EFS CSI Driver in EKS ###
- Install the **EFS CSI driver** to allow Kubernetes pods to mount EFS.
```bash
kubectl apply -k "github.com/kubernetes-sigs/aws-efs-csi-driver/deploy/kubernetes/overlays/stable/ecr/"
```

- Verify the **CSI driver installation:**
```bash
kubectl get pods -n kube-system | grep efs
```
```bash
#Output

efs-csi-controller-7bcc75ddff-krspm   3/3     Running   0          30s
efs-csi-controller-7bcc75ddff-zwcb6   3/3     Running   0          30s
efs-csi-node-8b5dk                    3/3     Running   0          30s
efs-csi-node-pf5jt                    3/3     Running   0          30s
```

### Step 4: Configure EFS Access Points for Different Workloads ###
- Create **EFS Access Points** for:
    - **Session state storage (Read/Write access).**
    - **Transaction logs (Read/Write access).**
    - **Reports service (Read-Only access).**
```bash
aws efs create-access-point --file-system-id fs-0a5d41af9211be4c2 --posix-user Uid=1000,Gid=1000 --root-directory '{"Path": "/session-data", "CreationInfo": {"OwnerUid": 1000, "OwnerGid": 1000, "Permissions": "755"}}'
aws efs create-access-point --file-system-id fs-0a5d41af9211be4c2 --posix-user Uid=1001,Gid=1001 --root-directory '{"Path": "/transaction-logs", "CreationInfo": {"OwnerUid": 1001, "OwnerGid": 1001, "Permissions": "755"}}'
aws efs create-access-point --file-system-id fs-0a5d41af9211be4c2 --posix-user Uid=1002,Gid=1002 --root-directory '{"Path": "/reports", "CreationInfo": {"OwnerUid": 1002, "OwnerGid": 1002, "Permissions": "555"}}'
```
![image](https://github.com/user-attachments/assets/16be8eab-a67f-4f22-a953-4dd0de40e3af)


### Step 5: Define Kubernetes Storage Classes & Persistent Volumes ###
- Create a **StorageClass** for Amazon EFS.
```yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: efs-sc
provisioner: efs.csi.aws.com
```

- Create a **PersistentVolume (PV)** for EFS.
```yaml
apiVersion: v1
kind: PersistentVolume
metadata:
  name: efs-pv
spec:
  capacity:
    storage: 5Gi
  accessModes:
    - ReadWriteMany
  persistentVolumeReclaimPolicy: Retain
  storageClassName: efs-sc
  csi:
    driver: efs.csi.aws.com
    volumeHandle: fs-0a5d41af9211be4c2
```

- Create a **PersistentVolumeClaim (PVC)**.
```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: efs-pvc
spec:
  accessModes:
    - ReadWriteMany
  storageClassName: efs-sc
  resources:
    requests:
      storage: 5Gi
```

```bash
kubectl apply -f storage-class.yaml
kubectl apply -f pv.yaml
kubectl apply -f pvc.yaml
```

```bash
kubectl get pv
NAME     CAPACITY   ACCESS MODES   RECLAIM POLICY   STATUS   CLAIM             STORAGECLASS   REASON   AGE
efs-pv   5Gi        RWX            Retain           Bound    default/efs-pvc   efs-sc

kubectl get pvc
NAME      STATUS   VOLUME   CAPACITY   ACCESS MODES   STORAGECLASS   AGE
efs-pvc   Bound    efs-pv   5Gi        RWX            efs-sc         8s
```

### Step 6: Deploy Microservices with EFS Storage ###
- Example deployment for Session Service using EFS PVC:
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: session-service
spec:
  replicas: 2
  selector:
    matchLabels:
      app: session-service
  template:
    metadata:
      labels:
        app: session-service
    spec:
      containers:
        - name: session-service
          image: nginx
          volumeMounts:
            - name: efs-storage
              mountPath: /mnt/session-data
      volumes:
        - name: efs-storage
          persistentVolumeClaim:
            claimName: efs-pvc
```
Repeat for transaction logs service and reporting service.

### Step 7: Configure IAM Permissions & Security ###
- Attach an **IAM policy** to allow EKS worker nodes to access EFS.
```json
{
	"Version": "2012-10-17",
	"Statement": [
		{
			"Effect": "Allow",
			"Action": [
				"elasticfilesystem:ClientMount",
				"elasticfilesystem:ClientWrite",
				"elasticfilesystem:ClientRootAccess"
			],
			"Resource": "arn:aws:elasticfilesystem:us-east-1:961341511681:file-system/fs-0a5d41af9211be4c2"
		}
	]
}
```

### Step 8: To verify if your session-service is correctly accessing AWS EFS ###
```bash
kubectl exec -it session-service-75bbfcf478-f9bdw -- /bin/bash
```

```bash
df -h | grep /mnt/session-data
127.0.0.1:/     8.0E     0  8.0E   0% /mnt/session-data
```

```bash
touch /mnt/session-data/testfile.txt
echo "Hello from session-service" > /mnt/session-data/testfile.txt
```


