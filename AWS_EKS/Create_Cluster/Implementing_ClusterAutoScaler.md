**Creating EKS Cluster**
```bash
eksctl create cluster --name my-eks-cluster --region us-east-1 --version 1.28 --nodegroup-name worker-nodes --node-type t3.medium --nodes 1 --nodes-min 1 --nodes-max 3 --managed
```

### Create an IAM Role for Cluster Autoscaler ###
**Create ClusterAutoScaler Policy**
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "autoscaling:DescribeAutoScalingGroups",
                "autoscaling:DescribeAutoScalingInstances",
                "autoscaling:DescribeTags",
                "autoscaling:SetDesiredCapacity",
                "autoscaling:TerminateInstanceInAutoScalingGroup",
                "ec2:DescribeInstances",
                "ec2:DescribeInstanceTypes",
                "ec2:DescribeLaunchTemplateVersions"
            ],
            "Resource": "*"
        }
    ]
}
```

**Create EKSClusterAutoscalerRole**
- Get the *OIDC Provider* of your EKS Cluster
  ```bash
  aws eks describe-cluster --name sid-eks-cluster --query "cluster.identity.oidc.issuer" --output text
  https://oidc.eks.us-east-1.amazonaws.com/id/1751DF70F3AD7C7BC7B1E97C0D20C039
  ```
- ```bash
  eksctl utils associate-iam-oidc-provider --region us-east-1 --cluster sid-eks-cluster --approve
  2025-03-20 20:09:21 [ℹ]  will create IAM Open ID Connect provider for cluster "sid-eks-cluster" in "us-east-1"
  2025-03-20 20:09:23 [✔]  created IAM Open ID Connect provider for cluster "sid-eks-cluster" in "us-east-1"
  ```
- ```bash
  aws iam list-open-id-connect-providers | grep 1751DF70F3AD7C7BC7B1E97C0D20C039
  "Arn": "arn:aws:iam::961341511681:oidc-provider/oidc.eks.us-east-1.amazonaws.com/id/1751DF70F3AD7C7BC7B1E97C0D20C039"
  ```
- Create a Custom Trust Policy
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": {
                "Federated": "arn:aws:iam::961341511681:oidc-provider/oidc.eks.us-east-1.amazonaws.com/id/1751DF70F3AD7C7BC7B1E97C0D20C039"
            },
            "Action": "sts:AssumeRoleWithWebIdentity",
            "Condition": {
                "StringEquals": {
                    "oidc.eks.us-east-1.amazonaws.com/id/1751DF70F3AD7C7BC7B1E97C0D20C039:sub": "system:serviceaccount:kube-system:cluster-autoscaler"
                }
            }
        }
    ]
}
```
- Attach `ClusterAutoScaler` Policy to the `EKSClusterAutoscalerRole` Role

### Deploy Cluster Autoscaler Using Helm ###
**Add the Helm Repository**
```bash
helm repo add autoscaler https://kubernetes.github.io/autoscaler
helm repo update
```

**Install Cluster Autoscaler**
```bash
helm install cluster-autoscaler autoscaler/cluster-autoscaler --namespace kube-system \
  --set autoDiscovery.clusterName=sid-eks-cluster \
  --set awsRegion=us-east-1 \
  --set rbac.create=true \
  --set rbac.serviceAccount.create=true \
  --set rbac.serviceAccount.name=cluster-autoscaler
```

**Annotate the ServiceAccount**
- ```bash
  kubectl annotate serviceaccount cluster-autoscaler -n kube-system eks.amazonaws.com/role-arn=arn:aws:iam::961341511681:role/EKSClusterAutoscalerRole
  ```
- ```yaml
  kubectl get serviceaccount cluster-autoscaler -n kube-system -o yaml
  apiVersion: v1
  automountServiceAccountToken: true
  kind: ServiceAccount
  metadata:
    annotations:
      eks.amazonaws.com/role-arn: arn:aws:iam::961341511681:role/EKSClusterAutoscalerRole
      meta.helm.sh/release-name: cluster-autoscaler
      meta.helm.sh/release-namespace: kube-system
    creationTimestamp: "2025-03-20T14:24:31Z"
    labels:
      app.kubernetes.io/instance: cluster-autoscaler
      app.kubernetes.io/managed-by: Helm
      app.kubernetes.io/name: aws-cluster-autoscaler
      helm.sh/chart: cluster-autoscaler-9.46.3
    name: cluster-autoscaler
    namespace: kube-system
    resourceVersion: "6815"
    uid: a23aa725-1a0f-449e-8cf8-aeb3c47ba928
  ```

**Check Cluster AutoScaler Pod**
```bash
kubectl get pods -n kube-system | grep cluster-autoscaler
NAME                                                         READY   STATUS    RESTARTS   AGE
cluster-autoscaler-aws-cluster-autoscaler-5798c89bfd-nw57p   1/1     Running   0          9m43s
```

**Create a High-Resource Nginx Deployment**
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-high-load
  namespace: default
spec:
  replicas: 3  # Increase if needed
  selector:
    matchLabels:
      app: nginx-high-load
  template:
    metadata:
      labels:
        app: nginx-high-load
    spec:
      containers:
        - name: nginx
          image: nginx
          resources:
            requests:
              cpu: "700m"   # Request 0.7 CPU
              memory: "700Mi" # Request 700Mi memory
            limits:
              cpu: "1000m"  # Limit to 1 CPU
              memory: "1000Mi" # Limit to 1GB memory
```

**Verify the New Node**
- After a few minutes, check if new nodes have been added:
  ```bash
  kubectl get nodes
  NAME                            STATUS   ROLES    AGE   VERSION
  ip-192-168-14-86.ec2.internal   Ready    <none>   49s   v1.28.15-eks-aeac579
  ip-192-168-40-39.ec2.internal   Ready    <none>   49m   v1.28.15-eks-aeac579
  ```
- 1 More Node was Added 49s Before

