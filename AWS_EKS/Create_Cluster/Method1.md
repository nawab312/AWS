### Create an IAM Role for EKS ###
- eks-trust-policy.json
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": { "Service": "eks.amazonaws.com" },
            "Action": "sts:AssumeRole"
        }
    ]
}
```

- Create an IAM Role for EKS Control Plane**
```bash
aws iam create-role --role-name eksClusterRole --assume-role-policy-document file://eks-trust-policy.json
```

- Now attach required policies:
```bash
aws iam attach-role-policy --role-name eksClusterRole --policy-arn arn:aws:iam::aws:policy/AmazonEKSClusterPolicy
aws iam attach-role-policy --role-name eksClusterRole --policy-arn arn:aws:iam::aws:policy/AmazonEKSServicePolicy
```

**Why do we need this IAM role?**
- The reason for creating an IAM role for EKS (Elastic Kubernetes Service) is to grant the necessary permissions to the EKS control plane (the EKS service itself) so it can interact with other AWS resources on behalf of your Kubernetes cluster.
- `AmazonEKSClusterPolicy`: This policy allows EKS to create and manage resources such as the VPC, subnets, security groups, and other networking components required for the cluster.
- `AmazonEKSServicePolicy`: This policy allows EKS to interact with other AWS services like EC2, CloudWatch, IAM, and more, which are necessary for the cluster's operation.
- The trust policy (`eks-trust-policy.json`) is important because it defines who (or what) can assume the role. In this case, you're allowing the EKS service (`eks.amazonaws.com`) to assume the IAM role


### Create an EKS Cluster ###

```bash
eksctl create cluster --name my-eks-cluster --region us-east-1 --version 1.28 --nodegroup-name worker-nodes --node-type t3.medium --nodes 2 --nodes-min 1 --nodes-max 3 --managed
```
- After the Cluster is Created check AWS Console

![image](https://github.com/user-attachments/assets/a714a375-af61-4228-b5ba-8d04ad380643)

- This Security Group will Automatically get Created. `EKS created security group applied to ENI that is attached to EKS Control Plane master nodes, as well as any managed workloads.`
![image](https://github.com/user-attachments/assets/f67bb857-2775-48c3-9d58-858df287168b)

- Inbound and Outbound Rules of Security Group that is Created
![image](https://github.com/user-attachments/assets/4c60de31-9392-4bd9-9c98-76b636df66a6)

### Configure `kubectl` for EKS ###

```bash
aws eks update-kubeconfig --region us-east-1 --name my-eks-cluster
```

### Delete EKS Cluster ###

- Delete CloudFormation Stack
```bash
aws cloudformation delete-stack --region us-east-1 --stack-name eksctl-my-eks-cluster-cluster
```





