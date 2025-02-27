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
