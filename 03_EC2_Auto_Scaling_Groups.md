# Topic 3: EC2 & Auto Scaling Groups

---

## WHY Does EC2 Exist? What Problem Does It Solve?

Before cloud computing, if your application needed more compute capacity, you had to physically order servers, wait weeks for delivery, rack them in a data center, install the operating system, configure networking, and then finally run your application. If your traffic spike lasted two hours, you still owned that hardware for three to five years. If you underestimated capacity, your application fell over. If you overestimated, you wasted millions in capital expenditure sitting idle.

EC2 (Elastic Compute Cloud) solved this by making compute capacity a utility — like electricity. You need a server? You have one in 60 seconds. You need 500 servers for a Black Friday traffic spike? Done. Spike is over? Terminate them all and stop paying. The word **Elastic** in EC2 is the entire point — capacity stretches and shrinks with your actual need.

For your specific work: **when you create an EKS node group, every worker node in that group is an EC2 instance**. The Kubernetes scheduler places pods on these nodes. The Cluster Autoscaler adds and removes these nodes based on pod demand. When a node fails, EC2 and Auto Scaling work together to replace it. When you right-size your cluster, you are choosing EC2 instance types. You cannot understand EKS operations without understanding EC2 and Auto Scaling Groups deeply.

---

## The Big Picture — EC2 in the Context of EKS

```
┌──────────────────────────────────────────────────────────────────────┐
│                         AWS ACCOUNT / VPC                            │
│                                                                      │
│   ┌──────────────────────────────────────────────────────────────┐  │
│   │              AUTO SCALING GROUP (ASG)                        │  │
│   │         "I want between 2 and 20 EC2 instances"              │  │
│   │                                                              │  │
│   │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐         │  │
│   │  │  EC2 Node   │  │  EC2 Node   │  │  EC2 Node   │   ...   │  │
│   │  │  AZ-A       │  │  AZ-B       │  │  AZ-A       │         │  │
│   │  │             │  │             │  │             │         │  │
│   │  │ ┌─────────┐ │  │ ┌─────────┐ │  │ ┌─────────┐ │         │  │
│   │  │ │  Pod    │ │  │ │  Pod    │ │  │ │  Pod    │ │         │  │
│   │  │ │  Pod    │ │  │ │  Pod    │ │  │ │  Pod    │ │         │  │
│   │  │ │  Pod    │ │  │ │  Pod    │ │  │ │  Pod    │ │         │  │
│   │  │ └─────────┘ │  │ └─────────┘ │  │ └─────────┘ │         │  │
│   │  └─────────────┘  └─────────────┘  └─────────────┘         │  │
│   │         ▲                                                    │  │
│   │         │ Scale Out / Scale In                              │  │
│   │  ┌──────┴───────────────────┐                               │  │
│   │  │   CLUSTER AUTOSCALER     │                               │  │
│   │  │   (pod in kube-system)   │                               │  │
│   │  │   Watches: pending pods  │                               │  │
│   │  │   Triggers: ASG scaling  │                               │  │
│   │  └──────────────────────────┘                               │  │
│   └──────────────────────────────────────────────────────────────┘  │
│                                                                      │
│   LAUNCH TEMPLATE: "Each new EC2 instance should be this type,      │
│   use this AMI, have this IAM role, run this bootstrap script"       │
└──────────────────────────────────────────────────────────────────────┘
```

Every box labelled "EC2 Node" in this diagram is a real virtual machine running in AWS. The Auto Scaling Group is the control plane that manages how many of those boxes exist at any time. The Launch Template is the blueprint that describes exactly what each new box looks like when it's created.

---

## EC2 Instance Types — Choosing the Right Node for EKS

Instance types define the hardware profile of your EC2 instance — how much CPU, memory, network bandwidth, and storage it has. AWS organizes them into families based on their intended workload.

```
INSTANCE TYPE FORMAT:

   m   5   .   x  l  a  r  g  e
   │   │       └──────────────── Size
   │   └─────────────────────── Generation (higher = newer, better price/perf)
   └─────────────────────────── Family

FAMILIES:
┌──────────┬────────────────────────────────────────────────────┐
│  Family  │  Best For                                          │
├──────────┼────────────────────────────────────────────────────┤
│  m       │  General purpose. Balanced CPU/memory.             │
│          │  m5, m6i, m7i — default choice for EKS nodes      │
├──────────┼────────────────────────────────────────────────────┤
│  c       │  Compute optimized. High CPU, less memory.         │
│          │  c5, c6i — API servers, data processing pods       │
├──────────┼────────────────────────────────────────────────────┤
│  r       │  Memory optimized. High RAM.                       │
│          │  r5, r6i — caches, in-memory DBs, Java heaps      │
├──────────┼────────────────────────────────────────────────────┤
│  t       │  Burstable. Cheap baseline + burst credits.        │
│          │  t3.medium, t3.large — dev/test only, never prod  │
├──────────┼────────────────────────────────────────────────────┤
│  g / p   │  GPU instances. Machine learning workloads.        │
│          │  g4dn, p3 — ML training/inference pods            │
├──────────┼────────────────────────────────────────────────────┤
│  i       │  Storage optimized. Fast local NVMe SSDs.          │
│          │  i3, i4i — Kafka, Elasticsearch, Cassandra nodes  │
└──────────┴────────────────────────────────────────────────────┘

SIZE SCALE (within any family):
nano → micro → small → medium → large → xlarge → 2xlarge → 4xlarge
→ 8xlarge → 12xlarge → 16xlarge → 24xlarge → 48xlarge → metal
```

### Choosing Instance Types for EKS — Production Thinking

The most common mistake is treating all EKS nodes as identical. A senior engineer thinks about this differently:

**The Pod Density Calculation:** Each EC2 instance type has a maximum number of pods it can run due to ENI and IP limits from the VPC CNI plugin. The formula is `(number of ENIs × (IPs per ENI - 1)) + 2`.

```
Common EKS instance types and their max pods:

┌──────────────┬──────┬────────┬─────────┬──────────┬──────────┐
│  Instance    │  CPU │  RAM   │  ENIs   │  IPs/ENI │ Max Pods │
├──────────────┼──────┼────────┼─────────┼──────────┼──────────┤
│  t3.medium   │  2   │  4 GB  │    3    │    6     │    17    │
│  t3.large    │  2   │  8 GB  │    3    │    12    │    35    │
│  m5.large    │  2   │  8 GB  │    3    │    10    │    29    │
│  m5.xlarge   │  4   │  16 GB │    4    │    15    │    58    │
│  m5.2xlarge  │  8   │  32 GB │    4    │    15    │    58    │
│  m5.4xlarge  │  16  │  64 GB │    8    │    30    │    234   │
│  c5.xlarge   │  4   │  8 GB  │    4    │    15    │    58    │
│  r5.xlarge   │  4   │  32 GB │    4    │    15    │    58    │
└──────────────┴──────┴────────┴─────────┴──────────┴──────────┘
```

Notice that `m5.large` and `m5.2xlarge` have the same max pod count (58) because they have the same ENI configuration. If you're running many small pods and hitting the pod limit before hitting CPU/memory limits, you need a larger ENI-dense instance type or you need to enable prefix delegation in the VPC CNI.

**The Bin Packing Reality:** Kubernetes schedules pods onto nodes based on resource requests. If your pods request 0.5 CPU and 512Mi memory, and your nodes have 4 CPU and 16Gi memory, you can fit roughly 8 pods per node by CPU, or roughly 30 by memory — whichever limit you hit first becomes your bottleneck. Choosing the right instance type means understanding your pod resource profile first.

---

## EC2 Purchasing Options — This Is a Cost Optimization AND Reliability Topic

This comes up constantly in interviews because it directly impacts both cost and the resilience design of your EKS cluster.

### On-Demand Instances

You pay for compute by the second with no commitment. The instance runs until you stop or terminate it. This is the most expensive option but the most flexible. Use this for your core, stable baseline workload — the nodes that must never disappear.

### Reserved Instances and Savings Plans

You commit to a specific amount of compute usage for 1 or 3 years in exchange for up to 72% discount. The modern version of this is **Savings Plans** — more flexible than old Reserved Instances because they apply across instance families, sizes, and even regions in some cases.

Use Savings Plans to cover your baseline capacity — the minimum number of nodes you know you'll always be running.

### Spot Instances

This is the most important purchasing option for EKS at scale and the one interviewers love to ask about.

AWS has massive amounts of spare compute capacity sitting idle. They sell this capacity at a discount of up to 90% compared to On-Demand pricing. The catch: **AWS can reclaim Spot instances with a 2-minute warning** when they need that capacity back. This is called a Spot interruption.

```
SPOT INTERRUPTION FLOW:

AWS decides it needs capacity back
           │
           ▼
EC2 sends interruption notice to the instance
(appears in instance metadata at /latest/meta-data/spot/
termination-time AND as a CloudWatch event)
           │
           ▼
2-minute window begins
           │
           ▼
┌──────────────────────────────────────────────┐
│  What SHOULD happen (if you're prepared):    │
│  - Node lifecycle hook fires                 │
│  - Kubernetes drains the node gracefully     │
│  - Pods get rescheduled to other nodes       │
│  - ASG launches a replacement                │
└──────────────────────────────────────────────┘
           │
           ▼
Instance is terminated by AWS
```

**The production pattern for Spot with EKS:**

Use the **AWS Node Termination Handler** — a DaemonSet that runs on every node, watches for Spot interruption notices via the instance metadata service, and triggers a graceful drain before AWS pulls the plug.

```yaml
# AWS Node Termination Handler — deployed via Helm
# helm repo add eks https://aws.github.io/eks-charts
# helm install aws-node-termination-handler \
#   eks/aws-node-termination-handler \
#   --namespace kube-system

# What it does:
# 1. Polls instance metadata for interruption notices
# 2. When notice detected: cordons the node (no new pods)
# 3. Drains the node (evicts existing pods gracefully)
# 4. Pods reschedule on other nodes
# 5. Instance terminates 2 min after notice
```

**The Spot diversification strategy:** Never rely on a single Spot instance type. Spot capacity can dry up for a specific type in a specific AZ. Use multiple instance types in your node group so that if `m5.xlarge` Spot is unavailable, the ASG can launch `m5.2xlarge` or `m4.xlarge` Spot instead.

```
PRODUCTION NODE GROUP STRATEGY:

┌──────────────────────────────────────────────────────────────┐
│  ON-DEMAND Node Group (Baseline)                             │
│  Instance: m5.xlarge                                         │
│  Min: 3, Max: 6, Desired: 3                                  │
│  Purpose: Core workloads, system pods, stateful services     │
│  Taints: none                                                │
└──────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────┐
│  SPOT Node Group (Burst capacity)                            │
│  Instances: m5.xlarge, m5.2xlarge, m4.xlarge, c5.xlarge     │
│             (multiple types = higher availability)           │
│  Min: 0, Max: 50, Desired: 0                                 │
│  Purpose: Stateless, fault-tolerant workloads                │
│  Taints: spot=true:NoSchedule                                │
│  (only pods that tolerate spot get scheduled here)           │
└──────────────────────────────────────────────────────────────┘
```

---

## Launch Templates — The EC2 Node Blueprint

A Launch Template is the document that defines exactly what an EC2 instance looks like when it is created. When the Auto Scaling Group needs to launch a new node, it reads the Launch Template and creates an instance matching that specification exactly. Think of it as a cookie cutter — every node that gets created is stamped out from the same mold.

```bash
# Create a Launch Template for EKS nodes
aws ec2 create-launch-template \
  --launch-template-name eks-node-template \
  --version-description "EKS Node Group v1" \
  --launch-template-data '{
    "ImageId": "ami-0123456789abcdef0",
    "InstanceType": "m5.xlarge",
    "IamInstanceProfile": {
      "Arn": "arn:aws:iam::123456789012:instance-profile/eks-node-role"
    },
    "SecurityGroupIds": ["sg-eks-nodes"],
    "BlockDeviceMappings": [
      {
        "DeviceName": "/dev/xvda",
        "Ebs": {
          "VolumeSize": 50,
          "VolumeType": "gp3",
          "Iops": 3000,
          "Encrypted": true
        }
      }
    ],
    "MetadataOptions": {
      "HttpTokens": "required",
      "HttpPutResponseHopLimit": 2
    },
    "UserData": "BASE64_ENCODED_BOOTSTRAP_SCRIPT",
    "TagSpecifications": [
      {
        "ResourceType": "instance",
        "Tags": [
          {"Key": "Name", "Value": "eks-production-node"},
          {"Key": "kubernetes.io/cluster/my-cluster", "Value": "owned"}
        ]
      }
    ]
  }'
```

The `MetadataOptions` section is critical for security. Setting `HttpTokens: required` enforces IMDSv2 — the Instance Metadata Service version 2. IMDSv2 requires a session token to access instance metadata, which prevents Server Side Request Forgery (SSRF) attacks from being able to steal the instance's IAM credentials via the metadata endpoint. This is a security best practice that interviewers will ask about.

### The EKS Node Bootstrap Script

When a new EC2 instance starts as an EKS worker node, it needs to join the Kubernetes cluster. This happens via the bootstrap script in the UserData field of the Launch Template.

```bash
#!/bin/bash
# This runs on every new EKS node at first boot
# For Amazon Linux 2 EKS-optimized AMI:

/etc/eks/bootstrap.sh my-cluster \
  --b64-cluster-ca <BASE64_CLUSTER_CA> \
  --apiserver-endpoint https://XXXXX.gr7.us-east-1.eks.amazonaws.com \
  --kubelet-extra-args '--node-labels=role=worker,env=production \
                         --max-pods=58 \
                         --register-with-taints=spot=true:NoSchedule'

# What this script does:
# 1. Configures kubelet with the cluster API endpoint and CA
# 2. Starts kubelet service
# 3. kubelet registers the node with the API server
# 4. Node appears in kubectl get nodes as Ready
```

For managed node groups, EKS handles the bootstrap automatically — you don't write this script yourself. But for self-managed node groups and custom AMIs, this is exactly what runs.

---

## Auto Scaling Groups — The Node Lifecycle Manager

An Auto Scaling Group is the AWS service that ensures you always have the right number of EC2 instances running. It continuously monitors the health of instances, replaces failed ones, and adjusts capacity based on scaling policies or external signals.

```
AUTO SCALING GROUP LIFECYCLE:

                    ┌─────────────────┐
                    │    Pending      │  ← Instance is launching
                    │  (bootstrapping)│
                    └────────┬────────┘
                             │ Bootstrap completes
                             │ Joins EKS cluster
                             ▼
┌───────────────┐   ┌─────────────────┐   ┌───────────────────┐
│  Terminating  │   │    InService    │   │  Pending:Wait     │
│               │   │                 │   │  (Lifecycle Hook) │
│  Being        │   │  Running,       │   │  Custom logic     │
│  terminated   │   │  healthy,       │   │  before launch    │
│               │   │  serving pods   │   └───────────────────┘
└───────┬───────┘   └────────┬────────┘
        │                    │
        │            ┌───────▼────────┐
        │            │   Standby      │  ← Manually put aside
        │            └───────┬────────┘
        │                    │
        │            ┌───────▼────────┐
        └────────────│  Terminating:  │  ← Lifecycle Hook fires
                     │  Wait          │     drain node here
                     └───────┬────────┘
                             │ Complete lifecycle action
                             ▼
                         TERMINATED
```

### ASG Health Checks — EC2 vs ELB

The ASG needs to know whether each instance is healthy. It supports two types of health checks:

**EC2 Health Check (default):** Checks that the instance is running and passing the EC2 system status checks. This is a low-level check — it only knows the VM is up, not that your application is running. An instance where kubelet has crashed would still pass the EC2 health check.

**ELB Health Check:** Checks that the instance is passing the load balancer's health check. More meaningful for application-level health. When an instance fails ELB health checks, the ASG marks it unhealthy and replaces it.

For EKS specifically, the more sophisticated approach is to let Kubernetes node conditions drive replacement — the Cluster Autoscaler and Node Health Management handle the Kubernetes-aware decisions, while the ASG handles pure EC2 failures.

### ASG Scaling Policies

There are three types of scaling policies:

**Simple Scaling:** "When CPU > 70%, add 2 instances. Wait 300 seconds. Evaluate again." The cooldown period prevents thrashing — rapidly adding and removing instances in response to momentary spikes.

**Step Scaling:** More granular version of simple scaling. "When CPU is 70-80%, add 1 instance. When CPU is 80-90%, add 2 instances. When CPU > 90%, add 4 instances." Different response sizes for different alarm severities.

**Target Tracking Scaling:** The most modern approach. "Maintain average CPU at 50%." AWS automatically calculates how many instances to add or remove to maintain the target metric. This is like a thermostat — you set the desired temperature and AWS adjusts the heating and cooling automatically.

For EKS, you typically **do not use ASG scaling policies directly**. Instead, you use the **Cluster Autoscaler** or **Karpenter**, which drive the ASG externally based on Kubernetes-native signals (pending pods, node utilization). The ASG scaling policies are more relevant for non-EKS EC2 fleets.

---

## Cluster Autoscaler — How Kubernetes Drives ASG Scaling

This is where your Kubernetes knowledge connects directly to EC2 and ASG. The Cluster Autoscaler is a Kubernetes controller (runs as a Deployment in `kube-system`) that watches for two conditions and responds to each:

**Scale Out condition:** There are pods in `Pending` state because no existing node has enough available CPU or memory to schedule them.

**Scale In condition:** A node has been underutilized (below 50% of both CPU and memory requests) for more than 10 minutes, AND all the pods on that node can be safely moved to other nodes.

```
CLUSTER AUTOSCALER SCALE-OUT FLOW:

1. You deploy a new application or existing app scales up
         │
         ▼
2. Kubernetes scheduler tries to place new pods
   "No node has enough CPU/memory available"
   Pod enters Pending state
         │
         ▼
3. Cluster Autoscaler detects Pending pods
   Simulates: "If I add a node, would these pods schedule?"
   Answer: Yes → trigger scale out
         │
         ▼
4. Cluster Autoscaler calls AWS ASG API:
   aws autoscaling set-desired-capacity \
     --auto-scaling-group-name eks-node-asg \
     --desired-capacity 5  (was 4)
         │
         ▼
5. ASG launches new EC2 instance using Launch Template
   (takes ~2-3 minutes: EC2 boot + EKS bootstrap + node Ready)
         │
         ▼
6. New node appears in kubectl get nodes as Ready
         │
         ▼
7. Kubernetes scheduler places Pending pods on new node
         │
         ▼
8. Pods transition from Pending → ContainerCreating → Running
```

```
CLUSTER AUTOSCALER SCALE-IN FLOW:

1. Traffic decreases, pods scale down (HPA or manual)
         │
         ▼
2. Some nodes are now underutilized
   Cluster Autoscaler identifies: Node X has been
   below 50% utilization for 10+ minutes
         │
         ▼
3. Autoscaler checks: can all pods on Node X be
   moved to other nodes?
   - Not a DaemonSet pod? ✓
   - Not a pod with local storage? ✓
   - Not a pod with restrictive PodDisruptionBudget? ✓
         │
         ▼
4. Autoscaler cordons the node
   (kubectl cordon → no new pods scheduled here)
         │
         ▼
5. Autoscaler drains the node
   (kubectl drain → evicts all pods gracefully)
   Pods are rescheduled on other nodes
         │
         ▼
6. Autoscaler calls ASG to terminate this specific instance
         │
         ▼
7. ASG terminates EC2 instance
   Desired capacity decreases by 1
```

### Cluster Autoscaler Configuration

```yaml
# cluster-autoscaler deployment (key configuration)
apiVersion: apps/v1
kind: Deployment
metadata:
  name: cluster-autoscaler
  namespace: kube-system
spec:
  template:
    spec:
      serviceAccountName: cluster-autoscaler  # needs IRSA
      containers:
        - name: cluster-autoscaler
          image: registry.k8s.io/autoscaling/cluster-autoscaler:v1.28.0
          command:
            - ./cluster-autoscaler
            - --cloud-provider=aws
            - --node-group-auto-discovery=asg:tag=k8s.io/cluster-autoscaler/enabled,k8s.io/cluster-autoscaler/my-cluster
            - --balance-similar-node-groups      # balance nodes across AZs
            - --skip-nodes-with-system-pods=false
            - --scale-down-delay-after-add=10m   # wait 10min after scale-out before scaling in
            - --scale-down-unneeded-time=10m     # node must be unneeded for 10min before removal
            - --scale-down-utilization-threshold=0.5  # below 50% = candidate for removal
            - --max-graceful-termination-sec=600  # 10min to drain a node
          env:
            - name: AWS_REGION
              value: us-east-1
```

The `--node-group-auto-discovery` flag is key — instead of hardcoding ASG names, the Cluster Autoscaler finds all ASGs with specific tags. This means you can add new node groups and the autoscaler discovers them automatically.

```bash
# Required ASG tags for auto-discovery
aws autoscaling create-or-update-tags \
  --tags \
    ResourceId=my-asg,ResourceType=auto-scaling-group,\
Key=k8s.io/cluster-autoscaler/enabled,Value=true,PropagateAtLaunch=false \
    ResourceId=my-asg,ResourceType=auto-scaling-group,\
Key=k8s.io/cluster-autoscaler/my-cluster,Value=owned,PropagateAtLaunch=false
```

### IRSA for Cluster Autoscaler

The Cluster Autoscaler pod needs to call AWS ASG APIs. This is a perfect IRSA use case — connecting back to Topic 1:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "autoscaling:DescribeAutoScalingGroups",
        "autoscaling:DescribeAutoScalingInstances",
        "autoscaling:DescribeLaunchConfigurations",
        "autoscaling:DescribeScalingActivities",
        "autoscaling:SetDesiredCapacity",
        "autoscaling:TerminateInstanceInAutoScalingGroup",
        "ec2:DescribeLaunchTemplateVersions",
        "ec2:DescribeInstanceTypes"
      ],
      "Resource": "*"
    }
  ]
}
```

---

## Karpenter — The Modern Alternative to Cluster Autoscaler

No EC2/ASG topic in 2024-2025 is complete without covering Karpenter because interviewers at AWS-heavy shops will ask about it. Karpenter is an open-source, AWS-native node provisioner that takes a fundamentally different approach to scaling than the Cluster Autoscaler.

```
CLUSTER AUTOSCALER approach:
  Pending Pod → "Which existing node group can I expand?" →
  Expand the ASG → Wait for generic node → Pod schedules

KARPENTER approach:
  Pending Pod → "What does THIS pod actually need?" →
  Provision the EXACT right instance type directly →
  Pod schedules faster, on optimally-sized node
```

The key differences:

**Direct EC2 provisioning:** Karpenter bypasses ASGs entirely and provisions EC2 instances directly. This means it can launch ANY instance type, not just the ones predefined in a node group.

**Bin packing intelligence:** Karpenter looks at ALL pending pods together and finds the most cost-efficient instance type(s) that can run them. A Cluster Autoscaler just picks whichever node group fits.

**Faster scaling:** Karpenter typically launches nodes in under 60 seconds vs 2-3 minutes for Cluster Autoscaler + ASG.

**Consolidation:** Karpenter actively consolidates workloads — if two half-empty nodes can fit on one node, it proactively terminates the emptier node and repacks the pods.

```yaml
# Karpenter NodePool (replaces the concept of node groups)
apiVersion: karpenter.sh/v1beta1
kind: NodePool
metadata:
  name: default
spec:
  template:
    spec:
      requirements:
        - key: kubernetes.io/arch
          operator: In
          values: ["amd64"]
        - key: karpenter.sh/capacity-type
          operator: In
          values: ["spot", "on-demand"]    # try spot first
        - key: karpenter.k8s.aws/instance-category
          operator: In
          values: ["c", "m", "r"]          # multiple families
        - key: karpenter.k8s.aws/instance-generation
          operator: Gt
          values: ["2"]                    # only gen 3+
      nodeClassRef:
        apiVersion: karpenter.k8s.aws/v1beta1
        kind: EC2NodeClass
        name: default
  limits:
    cpu: 1000                              # max total CPU across all nodes
  disruption:
    consolidationPolicy: WhenUnderutilized # actively consolidate
    consolidateAfter: 30s

---
apiVersion: karpenter.k8s.aws/v1beta1
kind: EC2NodeClass
metadata:
  name: default
spec:
  amiFamily: AL2
  role: "eks-node-role"
  subnetSelectorTerms:
    - tags:
        kubernetes.io/cluster/my-cluster: owned
  securityGroupSelectorTerms:
    - tags:
        kubernetes.io/cluster/my-cluster: owned
```

---

## EC2 Instance Lifecycle Hooks — Graceful Node Shutdown

Lifecycle Hooks let you pause the ASG during launch or termination to run custom logic. For EKS, the termination hook is critical — it gives you time to drain a node before the EC2 instance is terminated.

```
WITHOUT Lifecycle Hook:
ASG decides to terminate node → EC2 immediately terminates → Pods get killed hard

WITH Lifecycle Hook:
ASG decides to terminate node
         │
         ▼
Instance enters "Terminating:Wait" state
(ASG pauses, instance still running)
         │
         ▼
Lambda function / EventBridge rule fires
Runs: kubectl drain node --ignore-daemonsets --delete-emptydir-data
         │
         ▼
All pods gracefully migrate to other nodes
         │
         ▼
Lambda completes lifecycle action:
aws autoscaling complete-lifecycle-action \
  --lifecycle-hook-name eks-node-drain \
  --auto-scaling-group-name my-asg \
  --lifecycle-action-result CONTINUE \
  --instance-id i-xxxxxxxx
         │
         ▼
ASG terminates the EC2 instance cleanly
```

```bash
# Create a lifecycle hook for graceful node termination
aws autoscaling put-lifecycle-hook \
  --lifecycle-hook-name eks-node-drain \
  --auto-scaling-group-name my-eks-asg \
  --lifecycle-transition autoscaling:EC2_INSTANCE_TERMINATING \
  --heartbeat-timeout 300 \
  --default-result CONTINUE
```

---

## Real CLI Commands for EC2 and ASG Operations

```bash
# ── EC2 INSTANCE OPERATIONS ───────────────────────────────────────

# List all EC2 instances with their state and type
aws ec2 describe-instances \
  --query 'Reservations[*].Instances[*].{
    ID:InstanceId,
    Type:InstanceType,
    State:State.Name,
    AZ:Placement.AvailabilityZone,
    IP:PrivateIpAddress,
    Name:Tags[?Key==`Name`]|[0].Value}' \
  --output table

# Get all EKS worker nodes (filter by cluster tag)
aws ec2 describe-instances \
  --filters \
    Name=tag:kubernetes.io/cluster/my-cluster,Values=owned \
    Name=instance-state-name,Values=running \
  --query 'Reservations[*].Instances[*].{
    ID:InstanceId,Type:InstanceType,IP:PrivateIpAddress}' \
  --output table

# Get instance metadata from within the instance
# (useful for debugging from inside a node)
curl http://169.254.169.254/latest/meta-data/instance-id
curl http://169.254.169.254/latest/meta-data/instance-type
curl http://169.254.169.254/latest/meta-data/placement/availability-zone

# IMDSv2 (when HttpTokens=required):
TOKEN=$(curl -X PUT "http://169.254.169.254/latest/api/token" \
  -H "X-aws-ec2-metadata-token-ttl-seconds: 21600")
curl -H "X-aws-ec2-metadata-token: $TOKEN" \
  http://169.254.169.254/latest/meta-data/instance-id

# Check Spot interruption notice (from inside instance)
curl -H "X-aws-ec2-metadata-token: $TOKEN" \
  http://169.254.169.254/latest/meta-data/spot/termination-time
# Returns 404 if no interruption pending
# Returns timestamp if interruption is coming

# ── ASG OPERATIONS ────────────────────────────────────────────────

# List all Auto Scaling Groups
aws autoscaling describe-auto-scaling-groups \
  --query 'AutoScalingGroups[*].{
    Name:AutoScalingGroupName,
    Min:MinSize,Max:MaxSize,Desired:DesiredCapacity,
    Instances:length(Instances)}' \
  --output table

# Manually scale an ASG (useful for testing)
aws autoscaling set-desired-capacity \
  --auto-scaling-group-name my-eks-asg \
  --desired-capacity 5

# Check scaling activity (what has the ASG been doing?)
aws autoscaling describe-scaling-activities \
  --auto-scaling-group-name my-eks-asg \
  --max-items 10

# Force terminate a specific instance and have ASG replace it
aws autoscaling terminate-instance-in-auto-scaling-group \
  --instance-id i-xxxxxxxx \
  --should-decrement-desired-capacity false

# Suspend ASG scaling (useful during maintenance)
aws autoscaling suspend-processes \
  --auto-scaling-group-name my-eks-asg \
  --scaling-processes Launch Terminate

# Resume ASG scaling
aws autoscaling resume-processes \
  --auto-scaling-group-name my-eks-asg \
  --scaling-processes Launch Terminate

# ── EKS NODE GROUP OPERATIONS ─────────────────────────────────────

# List EKS node groups
aws eks list-nodegroups --cluster-name my-cluster

# Describe a node group (shows ASG, instance types, status)
aws eks describe-nodegroup \
  --cluster-name my-cluster \
  --nodegroup-name my-nodegroup

# Update node group (rolling update of all nodes)
aws eks update-nodegroup-version \
  --cluster-name my-cluster \
  --nodegroup-name my-nodegroup \
  --release-version latest

# Scale a managed node group
aws eks update-nodegroup-config \
  --cluster-name my-cluster \
  --nodegroup-name my-nodegroup \
  --scaling-config minSize=2,maxSize=10,desiredSize=4
```

---

## Console Walkthrough — Key Actions in the AWS Console

**To view and manage EC2 instances:**
`EC2 → Instances → Instances` — filter by tag `kubernetes.io/cluster/<name>` to see all EKS nodes. Click any instance to see its instance type, AZ, security groups, IAM role, and networking details.

**To view Auto Scaling activity:**
`EC2 → Auto Scaling → Auto Scaling Groups → [select ASG] → Activity tab` — shows the complete history of scale-out and scale-in events with reasons. This is the first place to check when nodes are not launching as expected.

**To view and edit the Launch Template:**
`EC2 → Launch Templates → [select template]` — shows all configuration. To update: `Actions → Modify template (Create new version)`. Never edit the current version in place — always create a new version. Then update the ASG to use the new version.

**To check instance health in an ASG:**
`EC2 → Auto Scaling → Auto Scaling Groups → [select ASG] → Instance management tab` — shows each instance, its lifecycle state, and health status. Instances showing `Unhealthy` will be replaced automatically.

**To view EKS node groups:**
`EKS → Clusters → [cluster name] → Compute tab` — shows all node groups, their current node count, status, and the underlying ASG. This is the EKS-native view vs the raw ASG view.

---

## Terraform — Production EKS Node Group with Launch Template

```hcl
# IAM role for EKS worker nodes
resource "aws_iam_role" "eks_nodes" {
  name = "eks-node-role-${var.cluster_name}"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect    = "Allow"
      Principal = { Service = "ec2.amazonaws.com" }
      Action    = "sts:AssumeRole"
    }]
  })
}

# Required managed policies for EKS worker nodes
resource "aws_iam_role_policy_attachment" "eks_worker_node" {
  role       = aws_iam_role.eks_nodes.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonEKSWorkerNodePolicy"
}

resource "aws_iam_role_policy_attachment" "eks_cni" {
  role       = aws_iam_role.eks_nodes.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonEKS_CNI_Policy"
}

resource "aws_iam_role_policy_attachment" "ecr_read" {
  role       = aws_iam_role.eks_nodes.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonEC2ContainerRegistryReadOnly"
}

# Launch Template for EKS nodes
resource "aws_launch_template" "eks_nodes" {
  name_prefix   = "${var.cluster_name}-node-"
  image_id      = data.aws_ssm_parameter.eks_ami.value
  instance_type = "m5.xlarge"

  iam_instance_profile {
    arn = aws_iam_instance_profile.eks_nodes.arn
  }

  vpc_security_group_ids = [aws_security_group.eks_nodes.id]

  block_device_mappings {
    device_name = "/dev/xvda"
    ebs {
      volume_size           = 50
      volume_type           = "gp3"
      iops                  = 3000
      throughput            = 125
      encrypted             = true
      delete_on_termination = true
    }
  }

  metadata_options {
    http_endpoint               = "enabled"
    http_tokens                 = "required"   # IMDSv2 enforced
    http_put_response_hop_limit = 2            # needed for pods in containers
  }

  tag_specifications {
    resource_type = "instance"
    tags = {
      Name        = "${var.cluster_name}-node"
      Environment = var.environment
      "kubernetes.io/cluster/${var.cluster_name}" = "owned"
    }
  }

  lifecycle {
    create_before_destroy = true
  }
}

# Get latest EKS-optimized AMI via SSM Parameter Store
data "aws_ssm_parameter" "eks_ami" {
  name = "/aws/service/eks/optimized-ami/${var.eks_version}/amazon-linux-2/recommended/image_id"
}

# EKS Managed Node Group
resource "aws_eks_node_group" "main" {
  cluster_name    = aws_eks_cluster.main.name
  node_group_name = "main-nodes"
  node_role_arn   = aws_iam_role.eks_nodes.arn

  subnet_ids = aws_subnet.private[*].id

  scaling_config {
    min_size     = 2
    max_size     = 20
    desired_size = 3
  }

  update_config {
    max_unavailable_percentage = 25  # rolling update: 25% nodes at a time
  }

  launch_template {
    id      = aws_launch_template.eks_nodes.id
    version = aws_launch_template.eks_nodes.latest_version
  }

  # Force update when launch template changes
  lifecycle {
    ignore_changes = [scaling_config[0].desired_size]
  }

  tags = {
    "k8s.io/cluster-autoscaler/enabled"             = "true"
    "k8s.io/cluster-autoscaler/${var.cluster_name}" = "owned"
  }
}
```

---

## Common Failure Scenarios and How to Debug Them

### Scenario 1: "What happens when an EKS node fails?" — The Interview Classic

This is the most commonly asked EKS/EC2 scenario question. Walk through it step by step:

```
NODE FAILURE TIMELINE:

T+0:00  EC2 instance fails (hardware fault, OOM killer, kernel panic, etc.)

T+0:00  EC2 system status check FAILS
        ASG health check detects unhealthy instance

T+0:30  (approximately) kubelet on the failed node stops sending
        heartbeats to the Kubernetes API server

T+0:40  Kubernetes marks the node as "NotReady"
        All pods on the node show "Unknown" status

T+5:00  (default 5 minutes) Kubernetes node lifecycle controller
        starts evicting pods from the NotReady node
        (controlled by --pod-eviction-timeout, default 5m)
        Pods are recreated on remaining healthy nodes

T+5:00  ASG detects unhealthy instance (via EC2 health check)
        ASG terminates the unhealthy instance
        ASG launches a replacement EC2 instance

T+7:00  (approx) New EC2 instance boots, runs bootstrap script,
        joins EKS cluster as a new node
        New node appears as "Ready"

T+7:00  Kubernetes scheduler places pods on the new node
        System returns to full capacity

TOTAL IMPACT: ~5-7 minutes to full recovery
Pods may be running degraded (fewer replicas) during this window
```

**How to minimize impact:**

Set Pod Disruption Budgets so critical workloads always have minimum replicas. Set pod `requests` and `limits` accurately so the scheduler can pack pods onto remaining nodes. Run at least 3 replicas of critical services across multiple AZs. Use readiness probes so traffic isn't sent to pods still starting up on new nodes.

```yaml
# PodDisruptionBudget — ensures at least 2 replicas always running
apiVersion: policy/v1
kind: PodDisruptionBudget
metadata:
  name: my-app-pdb
spec:
  minAvailable: 2
  selector:
    matchLabels:
      app: my-app
```

### Scenario 2: Nodes Are Not Scaling Out — Pending Pods Stuck

```bash
# Step 1: Confirm pods are actually Pending
kubectl get pods --all-namespaces | grep Pending

# Step 2: Check WHY pods are Pending
kubectl describe pod pending-pod-name -n my-namespace
# Look for Events section — "0/3 nodes are available:
# 3 Insufficient memory." tells you the exact constraint

# Step 3: Check Cluster Autoscaler logs
kubectl logs -n kube-system \
  -l app=cluster-autoscaler --tail=100

# Common CA log messages and their meaning:
# "Scale-up: no feasible node group" → no node group can fit the pod
#   (check nodeSelector, taints/tolerations, resource requests)
# "Scale-up: pod didn't trigger scale-up, max node group size reached"
#   → ASG is at max capacity, increase maxSize
# "Not scaled up, exceeds maximum cluster size"
#   → cluster-wide limit hit in CA config

# Step 4: Check ASG max size
aws autoscaling describe-auto-scaling-groups \
  --auto-scaling-group-name my-eks-asg \
  --query 'AutoScalingGroups[0].{Max:MaxSize,Desired:DesiredCapacity}'

# Step 5: Check if ASG is trying to launch but failing
aws autoscaling describe-scaling-activities \
  --auto-scaling-group-name my-eks-asg \
  --max-items 5
# Look for: "Failed to launch instances" with reason

# Step 6: Common launch failure reasons:
# "InsufficientInstanceCapacity" → that instance type has no capacity in the AZ
#   Fix: use multiple instance types or AZs
# "Invalid IAM Instance Profile" → node IAM role issue
#   Fix: verify eks-node-role exists and has correct policies
# "The requested configuration is currently not supported"
#   → instance type not available in that AZ
```

### Scenario 3: Nodes Are Scaling In Too Aggressively — Pods Getting Evicted

```bash
# Symptom: pods keep getting evicted and rescheduled, causing disruption

# Step 1: Check if pods have proper PodDisruptionBudgets
kubectl get pdb --all-namespaces

# Step 2: Check Cluster Autoscaler scale-down settings
kubectl describe deployment cluster-autoscaler -n kube-system | grep -A 30 "Args:"
# Look for: --scale-down-unneeded-time (default 10m)
# If too short, nodes get removed too quickly
# Consider: --scale-down-unneeded-time=20m for stability

# Step 3: Annotate nodes to prevent scale-down
# (useful for nodes running stateful or critical pods)
kubectl annotate node my-node \
  cluster-autoscaler.kubernetes.io/scale-down-disabled=true

# Step 4: Check pod annotations — pods can opt out of eviction
# If a pod has this annotation, CA will not evict it:
kubectl annotate pod my-critical-pod \
  cluster-autoscaler.kubernetes.io/safe-to-evict=false
```

### Scenario 4: Spot Instance Interruption Causing Service Disruption

```bash
# Symptom: periodic service disruption every few hours as Spot instances
# get reclaimed and pods scramble to reschedule

# Step 1: Check if Node Termination Handler is installed
kubectl get daemonset -n kube-system | grep termination

# Step 2: Check NTH logs to see if it's catching interruptions
kubectl logs -n kube-system \
  -l app.kubernetes.io/name=aws-node-termination-handler \
  --tail=50

# Step 3: Verify Spot nodes have proper taints and
# only fault-tolerant pods run on them
kubectl get nodes --show-labels | grep spot
kubectl describe node spot-node-name | grep -A 10 Taints

# Step 4: Check that critical pods have anti-affinity to avoid
# all replicas landing on Spot nodes
# Example: ensure at least 1 replica on On-Demand

# Step 5: Check interruption rate in EC2 console
# EC2 → Spot Requests → Interruption history
# If a specific instance type in a specific AZ is
# interrupted often → add more instance type diversity
```

---

## How This Connects to the Rest of Your Learning Path

**EKS AWS Layer (Topic 4):** Everything you learned here — node groups, Launch Templates, ASG-driven scaling, bootstrap scripts, node IAM roles — gets expanded in the EKS topic which shows the full managed control plane picture.

**Load Balancing (Topic 7):** ALB Target Groups point to EC2 instances (or pod IPs). The ALB health check drives ASG health check in non-EKS scenarios. NodePort services expose EC2 node ports as targets.

**CloudWatch (Topic 9):** EC2 publishes metrics to CloudWatch (CPU, network, disk). CloudWatch Alarms can trigger ASG scaling policies. Container Insights collects node-level metrics for EKS.

**Cost Optimization (Topic 17):** Spot instances, Savings Plans, right-sizing node groups — all of this is the cost optimization layer built on top of EC2 and ASG. Karpenter is the modern tool that ties cost optimization directly into the scaling decision.

**High Availability (Topic 16):** Multi-AZ ASG configuration, node failure recovery timelines, PodDisruptionBudgets — the HA story for EKS is entirely built on how you configure EC2 and ASG across availability zones.

---

## Interview Cheat Sheet

| Question | Crisp Answer |
|----------|-------------|
| What happens when an EKS worker node fails? | EC2 health check detects failure. ASG marks instance unhealthy and launches a replacement. Kubernetes marks the node NotReady after missing heartbeats (~40s). After 5 minutes, pods are evicted and rescheduled on healthy nodes. New node joins in ~7 minutes. Total recovery ~5-7 min. |
| What is the difference between Cluster Autoscaler and Karpenter? | Cluster Autoscaler works with predefined ASG node groups — it scales existing groups up/down. Karpenter provisions EC2 instances directly, picks the optimal instance type per workload, is faster, and actively consolidates underutilized nodes. |
| What is a Launch Template and what does it contain? | A blueprint for EC2 instances — defines AMI, instance type, IAM role, security groups, EBS volumes, user data (bootstrap script), and metadata options. Used by ASGs to create identical instances. |
| What is a Spot instance and what is the risk? | Spare AWS capacity sold at up to 90% discount. AWS can reclaim with 2-minute notice (interruption). Mitigate with AWS Node Termination Handler for graceful drain, multiple instance types for capacity diversity. |
| Why is IMDSv2 important for EKS nodes? | IMDSv2 requires a session token for metadata requests, preventing SSRF attacks from stealing the node's IAM role credentials. Set `HttpTokens=required` and `HttpPutResponseHopLimit=2` (hop limit 2 needed for containerized workloads). |
| How does Cluster Autoscaler know which ASG to scale? | Via tag-based auto-discovery. ASGs tagged with `k8s.io/cluster-autoscaler/enabled=true` and `k8s.io/cluster-autoscaler/<cluster-name>=owned` are automatically discovered without hardcoding ASG names. |
| What prevents Cluster Autoscaler from scaling in a node? | PodDisruptionBudget violations, pods with `safe-to-evict=false` annotation, pods with local storage (emptyDir), DaemonSet pods, and node annotation `scale-down-disabled=true`. |
| What is an ASG Lifecycle Hook? | A pause mechanism that stops the ASG during launch or termination, allowing custom logic to run. For EKS, the termination hook is used to drain the node gracefully before EC2 terminates it. |
| What is the max pods limit per node and what determines it? | The VPC CNI limits pods to `(ENIs × (IPs per ENI - 1)) + 2`. A `m5.xlarge` has 4 ENIs × 15 IPs = 58 max pods. Increase with prefix delegation which gives 16 IPs per ENI slot. |
| What are the three required IAM policies for an EKS worker node? | `AmazonEKSWorkerNodePolicy` (node registration), `AmazonEKS_CNI_Policy` (VPC CNI networking), `AmazonEC2ContainerRegistryReadOnly` (pull images from ECR). |
| What is the difference between EC2 and ELB health checks on an ASG? | EC2 health check only checks if the VM is running. ELB health check checks if the application is responding. For EKS, Kubernetes node conditions are the primary health signal — EC2 health check handles bare VM failures. |
| How do you do a rolling update of all nodes in an EKS node group? | `aws eks update-nodegroup-version` triggers a rolling replacement. The `update_config.max_unavailable_percentage` controls how many nodes are replaced at once. Old nodes are drained before new ones launch. |
| What is Spot diversification and why does it matter? | Using multiple instance types and AZs in a Spot node group. If one instance type's Spot capacity is exhausted, the ASG falls back to another type. Without diversification, scale-out can fail during high-demand periods. |
| How does the ASG know the desired capacity after Cluster Autoscaler changes it? | The Cluster Autoscaler directly calls the ASG `SetDesiredCapacity` API. The ASG stores the desired capacity and maintains it. If an instance fails, ASG launches a replacement to maintain that desired count. |
