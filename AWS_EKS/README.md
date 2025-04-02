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

---

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

---

**RBAC in Kubernetes/EKS**
In EKS (Elastic Kubernetes Service), RBAC allows you to define roles and permissions based on Kubernetes roles (which specify what actions can be done on which resources) and Kubernetes users/groups (which represent who is allowed to perform those actions). Key RBAC Components:
- Role and ClusterRole:
  - Role: Defines a set of permissions within a specific namespace.
  - ClusterRole: Defines a set of permissions across the entire cluster (i.e., cluster-wide permissions).
- RoleBinding and ClusterRoleBinding:
  - RoleBinding: Associates a Role with a user, group, or service account within a specific namespace.
  - ClusterRoleBinding: Associates a ClusterRole with a user, group, or service account across the entire cluster.
- Subjects: The entities (users, groups, or service accounts) that the role is being assigned to. These are the entities that can perform the actions defined in the Role or ClusterRole.

Step-by-Step: How RBAC Works in EKS
- Define Roles (Role or ClusterRole):
  - Roles specify what actions a user can perform on which resources. These resources can include Pods, Services, Deployments, Namespaces, etc.
  - Roles define actions using verbs (e.g., `get`, `list`, `create`, `delete`, `update`) on specific resources (e.g., `pods`, `services`).
- Create RoleBindings or ClusterRoleBindings:
  - After defining a Role or ClusterRole, you bind it to a user, group, or service account using a RoleBinding or ClusterRoleBinding.
  - The binding tells Kubernetes who (the subjects) can perform what actions (based on the Role or ClusterRole)
 
Example 1: Role and RoleBinding (Namespace-Level Permissions)
- Let's say you want to give a user read-only access to Pods in a specific namespace.

Step 1: Create a Role (Read-Only Access)
```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  namespace: mynamespace  # The namespace where this role applies
  name: pod-reader
rules:
- apiGroups: [""]
  resources: ["pods"]  # Resources this role applies to (in this case, Pods)
  verbs: ["get", "list"]  # Allowed actions
```

Step 2: Create a RoleBinding (Bind the Role to a User)
```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: pod-reader-binding
  namespace: mynamespace
subjects:
- kind: User
  name: john_doe  # The user you want to grant access to
  apiGroup: rbac.authorization.k8s.io
roleRef:
  kind: Role
  name: pod-reader  # The Role we created earlier
  apiGroup: rbac.authorization.k8s.io
```

*Mapping IAM Roles to Kubernetes RBAC Groups in aws-auth ConfigMap:*
The aws-auth ConfigMap plays a critical role in managing security and access control in Amazon EKS (Elastic Kubernetes Service). It defines the AWS IAM (Identity and Access Management) roles and users that are granted access to the Kubernetes cluster. Here's how it contributes to security and access control:
- Associating IAM Roles/Users with Kubernetes RBAC (Role-Based Access Control) Users:  The `aws-auth` ConfigMap maps IAM users and roles to Kubernetes RBAC groups. This mapping allows IAM users and roles to interact with the Kubernetes cluster with specific permissions, governed by Kubernetes RBAC rules.
  - For example, an IAM role can be mapped to a Kubernetes group like `system:masters`, which grants administrative privileges within the Kubernetes cluster. Similarly, roles can be mapped to custom RBAC roles, limiting access to specific namespaces, resources, or actions.
- Controlled Access to the Cluster: The ConfigMap provides a clear, auditable way to control which IAM entities (users or roles) have access to the Kubernetes cluster. Only the IAM entities explicitly listed in the `aws-auth` ConfigMap can access the cluster, enforcing strict access controls. This is vital for security as it ensures that unauthorized users cannot gain access to sensitive resources.

```yaml
apiVersion: v1
data:
  mapRoles: |
    - rolearn: arn:aws:iam::123456789012:role/eks-admin
      username: eks-admin
      groups:
        - system:masters  # This grants admin-level access
  mapUsers: |
    - userarn: arn:aws:iam::123456789012:user/john_doe
      username: john_doe
      groups:
        - developers  # This could be a custom group you create
kind: ConfigMap
metadata:
  name: aws-auth
  namespace: kube-system
```
