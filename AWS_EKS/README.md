### Multi-AZ High Availability in Amazon EKS ###
Ensuring high availability (HA) in Amazon EKS means designing a fault-tolerant Kubernetes architecture that can withstand failures in AWS Availability Zones (AZs) and continue running smoothly.

**Understanding Multi-AZ in EKS**

*Control Plane HA (Managed by AWS)*
- Amazon EKS automatically deploys and manages the Kubernetes control plane across multiple Availability Zones.
- The control plane components (API server, etcd, controllers) are redundant across AZs.
- AWS provides automatic failover if an AZ goes down.

*Worker Nodes (Self-Managed HA)*
- You are responsible for deploying worker nodes across multiple AZs.
- Using an Auto Scaling Group (ASG) ensures that nodes are evenly distributed.
- Amazon EBS volumes are AZ-specific, so if a node with an EBS volume fails, a new pod in another AZ might not have access to the data.

**Strategies for Multi-AZ High Availability**

*Deploying EKS Worker Nodes Across Multiple AZs*
- Define an Auto Scaling Group (ASG) spanning multiple AZs.
- Use a Multi-AZ Node Group with subnets in different AZs.
- Ensure your EKS cluster can tolerate node failures by distributing workloads across AZs.
```yaml
nodeGroups:
  - name: my-node-group
    instanceTypes: ["m5.large"]
    desiredCapacity: 3
    minSize: 3
    maxSize: 6
    subnets:
      - subnet-az1
      - subnet-az2
      - subnet-az3
```

*Using Kubernetes Pod Spreading Techniques*
- Prevents multiple replicas from being scheduled in the same AZ.
```yaml
affinity:
  podAntiAffinity:
    requiredDuringSchedulingIgnoredDuringExecution:
      - labelSelector:
          matchExpressions:
            - key: app
              operator: In
              values:
                - my-app
        topologyKey: "topology.kubernetes.io/zone"
```
- Kubernetes Topology Spread Constraints. Ensures pods are evenly distributed across AZs.
```yaml
topologySpreadConstraints:
  - maxSkew: 1
    topologyKey: "topology.kubernetes.io/zone"
    whenUnsatisfiable: ScheduleAnyway
    labelSelector:
      matchLabels:
        app: my-app
```

*Load Balancing for Multi-AZ HA*
- Use the AWS Load Balancer Controller to expose services across multiple AZs.
- Best Practice: ALBs and NLBs should be deployed with cross-zone load balancing enabled.
```yaml
service:
  type: LoadBalancer
  annotations:
    service.beta.kubernetes.io/aws-load-balancer-cross-zone-load-balancing-enabled: "true"
```

*High Availability for Persistent Storage*
- Since Amazon EBS volumes are AZ-specific, use Amazon EFS or S3 for multi-AZ persistent storage.
- Best Practices:
  - EFS (Elastic File System): Multi-AZ shared storage for stateful apps.
  - S3: Store application assets, logs, and backups in a durable, multi-AZ location.

*Disaster Recovery & Failover Strategy*
- Use AWS Route 53 for global traffic routing between clusters.
- Backup & Restore with Velero for cluster recovery in case of failure.

### Kubernetes Security ###

**Service Accounts**
- Service Accounts in EKS provide an identity for Pods, allowing them to authenticate with the Kubernetes API and interact with AWS services
- EKS allows you to associate AWS IAM roles with Kubernetes Service Accounts using IAM Roles for Service Accounts (IRSA)
- This enables Pods to access AWS resources securely without embedding AWS credentials in the application code
- When a Pod uses the Service Account, it automatically receives temporary AWS credentials through the associated IAM role, allowing it to interact with AWS services like S3, DynamoDB, etc

![image](https://github.com/user-attachments/assets/1eeca5ea-e652-4c31-884c-3f44929b38b2) ![image](https://github.com/user-attachments/assets/5d260bef-06fd-4356-9030-81b10067fff7)

**OIDC(Open ID Connect)**
OpenID Connect is an authentication protocol that allows clients to verify the identity of users or service accounts through an identity provider (IdP) using OAuth 2.0. OIDC provider for the cluster is used to authenticate requests to the Kubernetes API
and to facilitate the integration of IAM roles with Kubernetes Service Accounts.

![image](https://github.com/user-attachments/assets/b548eb8c-cd18-40da-85d6-bb7fc3961d9e)

