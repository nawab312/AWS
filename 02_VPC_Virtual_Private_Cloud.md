# Topic 2: VPC — Virtual Private Cloud (Deep Dive)

---

## WHY Does VPC Exist? What Problem Does It Solve?

When AWS first launched, every EC2 instance you created was thrown into a flat, shared network with every other AWS customer's instances. Your database server was technically reachable from someone else's EC2 instance if they knew the IP. Security was bolt-on — you used security groups and hoped for the best. There was no concept of network isolation at the infrastructure level.

This is the equivalent of renting office space in a building where every tenant shares the same open floor plan, the same hallways, and the same doors. Your filing cabinets are in the same room as everyone else's. You put a lock on your cabinet, but anyone can walk up to it and try the lock.

VPC solves this by giving you **your own private, isolated section of the AWS network**. When you create a VPC, AWS carves out a virtual network that exists exclusively for your account. You define the IP address space. You define the subnets. You define what can talk to what. You decide what has internet access and what doesn't. Nothing gets in or out unless you explicitly allow it.

The real-world analogy is that you stopped renting a desk in an open co-working space and instead leased your own floor in the building. You control the doors, the internal layout, the phone lines, and who gets a visitor badge. Other tenants cannot even see your floor exists.

For your work specifically: **every EKS cluster lives inside a VPC**. Your worker nodes are EC2 instances inside subnets inside a VPC. Your RDS databases live in private subnets inside a VPC. Your load balancers sit at the edge of a VPC. When a pod can't reach a database, when a node can't pull an image, when an ingress isn't routing traffic — the answer almost always lives somewhere in the VPC layer. You cannot debug any of this without understanding VPC cold.

---

## The Big Picture — VPC Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        AWS ACCOUNT                                       │
│                                                                          │
│  ┌───────────────────────────────────────────────────────────────────┐  │
│  │                    VPC  10.0.0.0/16                                │  │
│  │                                                                   │  │
│  │   AVAILABILITY ZONE A          AVAILABILITY ZONE B               │  │
│  │  ┌─────────────────────┐      ┌─────────────────────┐            │  │
│  │  │  PUBLIC SUBNET      │      │  PUBLIC SUBNET      │            │  │
│  │  │  10.0.1.0/24        │      │  10.0.2.0/24        │            │  │
│  │  │                     │      │                     │            │  │
│  │  │  [NAT Gateway]      │      │  [NAT Gateway]      │            │  │
│  │  │  [Load Balancer]    │      │  [Load Balancer]    │            │  │
│  │  └──────────┬──────────┘      └──────────┬──────────┘            │  │
│  │             │                            │                        │  │
│  │  ┌──────────▼──────────┐      ┌──────────▼──────────┐            │  │
│  │  │  PRIVATE SUBNET     │      │  PRIVATE SUBNET     │            │  │
│  │  │  10.0.3.0/24        │      │  10.0.4.0/24        │            │  │
│  │  │                     │      │                     │            │  │
│  │  │  [EKS Worker Nodes] │      │  [EKS Worker Nodes] │            │  │
│  │  │  [App Pods]         │      │  [App Pods]         │            │  │
│  │  └──────────┬──────────┘      └──────────┬──────────┘            │  │
│  │             │                            │                        │  │
│  │  ┌──────────▼──────────┐      ┌──────────▼──────────┐            │  │
│  │  │  ISOLATED SUBNET    │      │  ISOLATED SUBNET    │            │  │
│  │  │  10.0.5.0/24        │      │  10.0.6.0/24        │            │  │
│  │  │                     │      │                     │            │  │
│  │  │  [RDS Database]     │      │  [RDS Replica]      │            │  │
│  │  │  [ElastiCache]      │      │  [ElastiCache]      │            │  │
│  │  └─────────────────────┘      └─────────────────────┘            │  │
│  │                                                                   │  │
│  └───────────────────────────────────────────────────────────────────┘  │
│                          │                                               │
│                 ┌────────▼────────┐                                      │
│                 │ INTERNET GATEWAY│                                      │
│                 └────────┬────────┘                                      │
└──────────────────────────┼──────────────────────────────────────────────┘
                           │
                      INTERNET
```

Every component you will ever deploy on AWS lives somewhere in this picture. Understanding where each component sits, how traffic flows between layers, and what controls that flow — that is VPC mastery.

---

## CIDR Blocks — The Language of IP Addressing in VPC

Before anything else you need to be comfortable reading CIDR notation because it appears everywhere in VPC configuration and interviews.

CIDR (Classless Inter-Domain Routing) notation expresses an IP address range as a base address plus a prefix length. The prefix length tells you how many bits are fixed (the network part) and how many bits are free (the host part).

```
10.0.0.0/16

10.0.0.0   = the base address
/16        = the first 16 bits are fixed (10.0 is locked)
             the remaining 16 bits are free
             2^16 = 65,536 possible IP addresses

10.0.0.0/24

/24        = the first 24 bits are fixed (10.0.0 is locked)
             the remaining 8 bits are free
             2^8 = 256 possible IP addresses
             (AWS reserves 5, so 251 usable)

10.0.0.0/28

/28        = 28 bits fixed, 4 bits free
             2^4 = 16 IP addresses (11 usable after AWS reserves 5)
             This is the smallest subnet AWS allows
```

The real-world analogy: think of the VPC CIDR as a city's phone number area code — `10.0` is your city prefix. Subnets are like neighborhoods within that city, each with their own exchange number — `10.0.1`, `10.0.2`. Individual EC2 instances are specific phone numbers — `10.0.1.45`.

**AWS reserves 5 IP addresses in every subnet:**

```
For subnet 10.0.1.0/24:

10.0.1.0   → Network address (reserved)
10.0.1.1   → AWS VPC router (reserved)
10.0.1.2   → AWS DNS server (reserved)
10.0.1.3   → AWS future use (reserved)
10.0.1.255 → Broadcast address (reserved)

Usable range: 10.0.1.4 through 10.0.1.254 = 251 addresses
```

This matters when you're sizing subnets for EKS. Each pod gets an IP address from the subnet (with the VPC CNI plugin). If you create a `/24` subnet and run 251 pods on a node group in that subnet, you run out of IPs. More on this in the EKS-specific section.

---

## The Core VPC Components — Built Bottom Up

### Internet Gateway (IGW)

The Internet Gateway is a horizontally scaled, redundant, highly available VPC component that allows communication between your VPC and the internet. It performs NAT for instances that have public IP addresses.

Think of it as the main entrance door to your office building. Without it, no one from outside can get in, and no one from inside can get out to the internet.

One VPC can have only one IGW attached. The IGW itself never fails — AWS manages its availability. You attach it to a VPC and it's done.

```
Internet ←──→ Internet Gateway ←──→ Public Subnet Resources
```

### Route Tables

A route table is a set of rules (routes) that determine where network traffic is directed. Every subnet must be associated with exactly one route table. The route table says: "if traffic is destined for this IP range, send it here."

```
PUBLIC SUBNET Route Table:
┌─────────────────┬──────────────────┐
│  Destination    │  Target          │
├─────────────────┼──────────────────┤
│  10.0.0.0/16    │  local           │  ← All VPC traffic stays local
│  0.0.0.0/0      │  igw-xxxxxxxx    │  ← All other traffic → Internet
└─────────────────┴──────────────────┘

PRIVATE SUBNET Route Table:
┌─────────────────┬──────────────────┐
│  Destination    │  Target          │
├─────────────────┼──────────────────┤
│  10.0.0.0/16    │  local           │  ← All VPC traffic stays local
│  0.0.0.0/0      │  nat-xxxxxxxx    │  ← All other traffic → NAT GW
└─────────────────┴──────────────────┘

ISOLATED SUBNET Route Table:
┌─────────────────┬──────────────────┐
│  Destination    │  Target          │
├─────────────────┼──────────────────┤
│  10.0.0.0/16    │  local           │  ← ONLY local VPC traffic
│                 │                  │  ← No internet route at all
└─────────────────┴──────────────────┘
```

This is the most important concept to understand about public vs private subnets: **the only difference between a public subnet and a private subnet is the route table**. A public subnet has a route `0.0.0.0/0 → IGW`. A private subnet does not. That's it. The subnet itself has no inherent "public" or "private" property — it's entirely defined by where the default route points.

### NAT Gateway

Private subnet resources (your EKS worker nodes, your application pods) often need to reach the internet for outbound traffic — pulling container images from Docker Hub, calling external APIs, downloading OS patches. But you don't want them to have public IPs or be directly reachable from the internet.

The NAT (Network Address Translation) Gateway solves this. It sits in the **public subnet**, has a public IP (called an Elastic IP), and allows resources in private subnets to initiate outbound connections to the internet while preventing the internet from initiating inbound connections to those resources.

```
EKS Pod (10.0.3.45)
       │
       │ "I need to reach api.github.com"
       ▼
Private Subnet Route Table
       │ 0.0.0.0/0 → NAT Gateway
       ▼
NAT Gateway (in public subnet, has Elastic IP 54.x.x.x)
       │ Translates source IP: 10.0.3.45 → 54.x.x.x
       ▼
Internet Gateway
       │
       ▼
api.github.com
       │
       │ Response comes back to 54.x.x.x
       ▼
NAT Gateway translates back to 10.0.3.45
       │
       ▼
EKS Pod receives response
```

**Critical production point:** NAT Gateways are per-AZ. For high availability, you need one NAT Gateway per AZ, and each private subnet in an AZ should route to the NAT Gateway in the same AZ. If you route all private subnets through a single NAT Gateway in one AZ and that AZ goes down, all your private subnet resources lose internet access. This is also a cost consideration — NAT Gateway charges per GB of data processed, and cross-AZ traffic costs extra.

### Subnets

A subnet is a range of IP addresses within your VPC, confined to a single Availability Zone. You cannot span a subnet across multiple AZs. This is a hard rule in AWS.

There are three tiers of subnets in a well-architected deployment:

**Public subnets** — resources here have public IPs and are directly reachable from the internet (if security groups allow). Your load balancers, NAT Gateways, and bastion hosts live here.

**Private subnets** — resources here have no public IPs. They can reach the internet via NAT Gateway for outbound traffic but cannot be reached from the internet directly. Your EKS worker nodes, application servers, and internal services live here.

**Isolated subnets** — no internet access at all, in either direction. No NAT Gateway route. Your databases, caches, and most sensitive data stores live here. They can only be reached by other resources within the VPC.

### Security Groups

A Security Group is a **stateful** virtual firewall that controls inbound and outbound traffic at the **resource level** (EC2 instance, RDS instance, EKS node, Lambda function, etc.).

Stateful means: if you allow inbound traffic on port 443, the response traffic is automatically allowed outbound without needing an explicit outbound rule. AWS tracks the connection state.

```
Security Group: eks-worker-nodes-sg
┌──────────────────────────────────────────────────────┐
│  INBOUND RULES                                       │
├───────────┬──────────┬───────────────────────────────┤
│  Protocol │  Port    │  Source                       │
├───────────┼──────────┼───────────────────────────────┤
│  TCP      │  443     │  eks-control-plane-sg         │  ← API server → kubelet
│  TCP      │  10250   │  eks-control-plane-sg         │  ← API server → kubelet
│  All      │  All     │  eks-worker-nodes-sg          │  ← Node to node comms
├───────────┴──────────┴───────────────────────────────┤
│  OUTBOUND RULES                                      │
├───────────┬──────────┬───────────────────────────────┤
│  Protocol │  Port    │  Destination                  │
├───────────┼──────────┼───────────────────────────────┤
│  All      │  All     │  0.0.0.0/0                    │  ← Allow all outbound
└───────────┴──────────┴───────────────────────────────┘
```

A critical point about Security Groups: **they can reference other security groups as sources/destinations**, not just IP ranges. This is extremely powerful. Instead of hardcoding IP addresses, you say "allow traffic from any resource that has the `rds-clients-sg` security group attached." When you add a new EKS node, it automatically gets the right access to RDS because it has the right security group — no IP management needed.

### Network ACLs (NACLs)

NACLs are **stateless** firewalls that operate at the **subnet level**. Stateless means return traffic must be explicitly allowed — you need both an inbound rule allowing the request and an outbound rule allowing the response.

NACLs evaluate rules in order from lowest to highest number and stop at the first match. They are the last line of defense and the first line for blocking known bad IP ranges across an entire subnet.

```
NACL vs Security Group — Key Differences:

┌─────────────────────┬────────────────────┬────────────────────┐
│  Feature            │  Security Group    │  NACL              │
├─────────────────────┼────────────────────┼────────────────────┤
│  Level              │  Resource          │  Subnet            │
│  State              │  Stateful          │  Stateless         │
│  Rules              │  Allow only        │  Allow + Deny      │
│  Rule evaluation    │  All rules         │  In order, stop    │
│  Default            │  Deny all inbound  │  Allow all         │
│  Use case           │  Fine-grained      │  Broad subnet      │
│                     │  per-resource      │  level blocking    │
└─────────────────────┴────────────────────┴────────────────────┘
```

In practice, most teams rely heavily on Security Groups and treat NACLs as a coarse tool for subnet-level blocking. If you need to block a specific IP range from an entire subnet (DDoS mitigation, blocking a known bad actor), NACLs are the right tool.

---

## Traffic Flow — How a Request Gets from the Internet to Your EKS Pod

This is the most important flow to understand for interviews. Trace every hop:

```
USER'S BROWSER
      │
      │ HTTPS request to your-app.com
      ▼
ROUTE 53
      │ Resolves your-app.com → ALB DNS name
      ▼
INTERNET GATEWAY
      │ Inbound traffic enters the VPC
      ▼
APPLICATION LOAD BALANCER
      │ Lives in PUBLIC subnets across multiple AZs
      │ Security Group: allow 443 inbound from 0.0.0.0/0
      │ Terminates TLS
      │ Routes based on host/path rules
      ▼
AWS LOAD BALANCER CONTROLLER
      │ (Running as a pod inside EKS)
      │ Watches Ingress objects and configures ALB rules
      ▼
TARGET GROUP
      │ Points to EKS worker node IPs + NodePort
      │ OR directly to pod IPs (IP mode)
      ▼
EKS WORKER NODE (in PRIVATE subnet)
      │ Security Group: allow traffic from ALB security group
      │ kube-proxy forwards to the right pod
      ▼
APPLICATION POD
      │ Receives the request
      │ Pod IP is from the private subnet CIDR
      │ (VPC CNI assigns real VPC IPs to pods)
      ▼
RESPONSE travels back the same path in reverse
```

Every arrow in this diagram is a place where something can go wrong, and every step is controlled by a combination of route tables, security groups, NACLs, and IAM policies.

---

## VPC for EKS — The Deep Connection

This is where your existing Kubernetes knowledge maps directly to VPC concepts. Let me show you exactly what EKS does at the VPC layer.

### The VPC CNI Plugin — Why EKS Pods Get Real VPC IPs

Most Kubernetes networking plugins (Calico, Flannel, Cilium in overlay mode) use an overlay network — pods get IPs from a separate address space that's overlaid on top of the node network using tunnels. The pod IPs are not real network IPs that other VPC resources know about.

EKS uses the **AWS VPC CNI plugin**, which does something fundamentally different: **every pod gets a real IP address directly from the VPC subnet**. There is no overlay. Pod IPs are routable within the VPC the same way EC2 instance IPs are.

```
WITHOUT VPC CNI (overlay):                WITH VPC CNI (EKS default):

Node IP: 10.0.3.10                         Node IP: 10.0.3.10
Pod IPs: 192.168.1.x (overlay network)     Pod IPs: 10.0.3.45, 10.0.3.46, 10.0.3.47
         not real VPC IPs                            REAL VPC IPs from subnet CIDR
         need tunneling to reach                     directly routable in the VPC
         other VPC resources                         RDS can see pod IPs directly
```

This has profound implications:

**The good:** Pods can communicate directly with any VPC resource (RDS, ElastiCache, other services) using their real IPs. Security groups can reference pod IPs. No tunneling overhead.

**The trade-off:** Each pod consumes a real VPC IP address. Each EC2 instance type has a limit on how many network interfaces and IP addresses it can hold. A `t3.medium` can hold a maximum of 3 network interfaces × 6 IPs each = 18 IPs, minus 1 per interface for the node itself = 15 pods maximum per node. If you're running large clusters with many small pods, IP exhaustion becomes a real operational concern.

```bash
# Check how many IPs your node type supports
# Formula: (number of ENIs) × (IPs per ENI - 1)
# t3.medium: 3 ENIs × 6 IPs = 18 - 3 = 15 max pods

# Check current IP usage in your cluster
kubectl get nodes -o custom-columns=\
'NAME:.metadata.name,MAX_PODS:.status.allocatable.pods'

# Check VPC CNI configuration
kubectl describe daemonset aws-node -n kube-system

# Check available IPs in a subnet
aws ec2 describe-subnets \
  --subnet-ids subnet-xxxxxxxx \
  --query 'Subnets[0].AvailableIpAddressCount'
```

### Subnet Sizing for EKS — Production Reality

A very common mistake when setting up EKS is creating subnets that are too small. Here is how to think about sizing:

```
For a production EKS cluster:

EKS Worker Node Subnets (Private):
- Plan for: nodes + pods per node
- A /24 gives you 251 IPs
- A t3.xlarge supports max 44 pods, needs 44 IPs
- 251 / 44 ≈ 5 nodes per subnet before IP exhaustion
- For large clusters, use /21 or /22 subnets
- RECOMMENDATION: Use /21 (2048 IPs) for worker node subnets

EKS Control Plane Subnets (Private):
- AWS managed control plane ENIs land here
- /28 is the minimum AWS requires (11 usable IPs)
- Use /28 per AZ for control plane subnets

Load Balancer Subnets (Public):
- ALBs need at least 8 free IPs per AZ
- /27 (32 IPs) per AZ is safe
- Or share with NAT Gateway in /24
```

### The Required Subnet Tags for EKS

EKS and the AWS Load Balancer Controller use subnet tags to discover which subnets to use. Missing these tags is a very common production issue:

```bash
# Tag public subnets for external load balancers (internet-facing ALB/NLB)
aws ec2 create-tags \
  --resources subnet-public-az-a subnet-public-az-b \
  --tags \
    Key=kubernetes.io/cluster/my-cluster,Value=shared \
    Key=kubernetes.io/role/elb,Value=1

# Tag private subnets for internal load balancers AND for EKS worker nodes
aws ec2 create-tags \
  --resources subnet-private-az-a subnet-private-az-b \
  --tags \
    Key=kubernetes.io/cluster/my-cluster,Value=shared \
    Key=kubernetes.io/role/internal-elb,Value=1
```

Without the `kubernetes.io/role/elb=1` tag on public subnets, the AWS Load Balancer Controller cannot find where to deploy internet-facing load balancers and your Ingress objects will never get an ALB provisioned. This is one of the most common "why isn't my Ingress getting an address" issues.

### EKS Security Group Architecture

EKS creates and manages several security groups. Understanding which is which is important for debugging:

```
┌─────────────────────────────────────────────────────────────────┐
│                    EKS SECURITY GROUPS                           │
│                                                                  │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │  CLUSTER SECURITY GROUP (created by EKS automatically) │    │
│  │  Applied to: Control plane ENIs + Worker nodes         │    │
│  │  Purpose: Allow all traffic between control plane      │    │
│  │           and worker nodes                             │    │
│  └─────────────────────────────────────────────────────────┘    │
│                                                                  │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │  CONTROL PLANE SECURITY GROUP (you can specify this)   │    │
│  │  Applied to: EKS managed ENIs in your VPC              │    │
│  │  Purpose: Control who can reach the K8s API server     │    │
│  └─────────────────────────────────────────────────────────┘    │
│                                                                  │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │  NODE GROUP SECURITY GROUP (you manage this)            │    │
│  │  Applied to: EC2 worker nodes                          │    │
│  │  Purpose: Control inbound to nodes from ALB,           │    │
│  │           inter-node traffic, pod-to-pod across nodes  │    │
│  └─────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────┘
```

---

## VPC Endpoints — Keeping Traffic Off the Internet

This is a senior-level topic that comes up constantly in Platform Engineering and SRE interviews. The question is: your EKS pods need to talk to S3, ECR, Secrets Manager, CloudWatch. By default, that traffic leaves your VPC, goes out through the NAT Gateway, hits the public internet, and comes back to the AWS service endpoint. This means:

- You pay NAT Gateway data processing fees for every byte
- Traffic traverses the public internet (security concern)
- You need NAT Gateway running at all times for these calls to work

VPC Endpoints solve this by creating a **private connection between your VPC and AWS services** that never leaves the Amazon network.

```
WITHOUT VPC Endpoint:                    WITH VPC Endpoint:

EKS Pod                                  EKS Pod
  │                                        │
  │ s3:GetObject                           │ s3:GetObject
  ▼                                        ▼
Private Subnet                           Private Subnet
  │                                        │
  ▼                                        ▼
NAT Gateway ──→ Internet ──→ S3          VPC Endpoint ──→ S3
  (costs money, public internet)           (free for Gateway type,
                                           stays in AWS network,
                                           no NAT needed)
```

There are two types of VPC Endpoints:

**Gateway Endpoints** — For S3 and DynamoDB only. They are free. They work by adding a route to your route table that points S3/DynamoDB traffic to the endpoint instead of the NAT Gateway. No network interface is created.

**Interface Endpoints (PrivateLink)** — For all other AWS services (ECR, Secrets Manager, CloudWatch, STS, SSM, etc.). These create an Elastic Network Interface (ENI) in your subnet with a private IP. They cost money (hourly + per GB). But for high-throughput services like ECR (pulling images) they pay for themselves quickly by eliminating NAT costs.

```bash
# Create a Gateway endpoint for S3
aws ec2 create-vpc-endpoint \
  --vpc-id vpc-xxxxxxxx \
  --service-name com.amazonaws.us-east-1.s3 \
  --vpc-endpoint-type Gateway \
  --route-table-ids rtb-private-az-a rtb-private-az-b

# This automatically adds a route to your route table:
# pl-xxxxxxxx (S3 prefix list) → vpce-xxxxxxxx
```

```bash
# Create Interface endpoints for EKS-critical services
# These are the ones you almost always need for a private EKS cluster:

# ECR API (for image metadata)
aws ec2 create-vpc-endpoint \
  --vpc-id vpc-xxxxxxxx \
  --service-name com.amazonaws.us-east-1.ecr.api \
  --vpc-endpoint-type Interface \
  --subnet-ids subnet-private-az-a subnet-private-az-b \
  --security-group-ids sg-vpc-endpoints

# ECR Docker (for image layer pulls)
aws ec2 create-vpc-endpoint \
  --vpc-id vpc-xxxxxxxx \
  --service-name com.amazonaws.us-east-1.ecr.dkr \
  --vpc-endpoint-type Interface \
  --subnet-ids subnet-private-az-a subnet-private-az-b \
  --security-group-ids sg-vpc-endpoints

# S3 (for ECR image layers stored in S3) — use Gateway type
aws ec2 create-vpc-endpoint \
  --vpc-id vpc-xxxxxxxx \
  --service-name com.amazonaws.us-east-1.s3 \
  --vpc-endpoint-type Gateway \
  --route-table-ids rtb-private-az-a rtb-private-az-b

# CloudWatch Logs (for container log shipping)
aws ec2 create-vpc-endpoint \
  --vpc-id vpc-xxxxxxxx \
  --service-name com.amazonaws.us-east-1.logs \
  --vpc-endpoint-type Interface \
  --subnet-ids subnet-private-az-a subnet-private-az-b \
  --security-group-ids sg-vpc-endpoints

# STS (for IRSA token exchange)
aws ec2 create-vpc-endpoint \
  --vpc-id vpc-xxxxxxxx \
  --service-name com.amazonaws.us-east-1.sts \
  --vpc-endpoint-type Interface \
  --subnet-ids subnet-private-az-a subnet-private-az-b \
  --security-group-ids sg-vpc-endpoints
```

### Fully Private EKS Cluster

For highly regulated environments, you can run EKS with the API server endpoint set to private-only. This means `kubectl` and all node-to-control-plane traffic stays entirely within the VPC.

```bash
# Create a fully private EKS cluster
aws eks create-cluster \
  --name private-cluster \
  --resources-vpc-config \
    subnetIds=subnet-private-az-a,subnet-private-az-b,\
endpointConfigPrivateAccess=true,\
endpointConfigPublicAccess=false

# For a private cluster, you MUST have these VPC endpoints:
# - com.amazonaws.region.ec2
# - com.amazonaws.region.ecr.api
# - com.amazonaws.region.ecr.dkr
# - com.amazonaws.region.s3 (Gateway)
# - com.amazonaws.region.logs
# - com.amazonaws.region.sts
# Without these, nodes cannot join the cluster and
# pods cannot pull images
```

---

## Real CLI Commands for VPC Operations

```bash
# ── DISCOVERY ─────────────────────────────────────────────────────

# List all VPCs in your account
aws ec2 describe-vpcs \
  --query 'Vpcs[*].{ID:VpcId,CIDR:CidrBlock,Name:Tags[?Key==`Name`]|[0].Value}' \
  --output table

# List all subnets in a VPC with their AZ and available IPs
aws ec2 describe-subnets \
  --filters Name=vpc-id,Values=vpc-xxxxxxxx \
  --query 'Subnets[*].{ID:SubnetId,AZ:AvailabilityZone,
            CIDR:CidrBlock,FreeIPs:AvailableIpAddressCount,
            Name:Tags[?Key==`Name`]|[0].Value}' \
  --output table

# List route tables and their routes
aws ec2 describe-route-tables \
  --filters Name=vpc-id,Values=vpc-xxxxxxxx \
  --query 'RouteTables[*].{ID:RouteTableId,
            Routes:Routes[*].{Dest:DestinationCidrBlock,Target:GatewayId}}' \
  --output json

# List security groups with their rules
aws ec2 describe-security-groups \
  --filters Name=vpc-id,Values=vpc-xxxxxxxx \
  --query 'SecurityGroups[*].{ID:GroupId,Name:GroupName}' \
  --output table

# ── TROUBLESHOOTING ────────────────────────────────────────────────

# Check if a security group is blocking traffic (describe its rules)
aws ec2 describe-security-groups \
  --group-ids sg-xxxxxxxx \
  --query 'SecurityGroups[0].IpPermissions'

# Find which security groups are attached to an EC2/EKS node
aws ec2 describe-instances \
  --instance-ids i-xxxxxxxx \
  --query 'Reservations[0].Instances[0].SecurityGroups'

# Check VPC Flow Logs for traffic (if enabled)
aws logs filter-log-events \
  --log-group-name /aws/vpc/flowlogs \
  --filter-pattern "REJECT" \
  --start-time $(date -d '1 hour ago' +%s000)

# Test connectivity between resources using VPC Reachability Analyzer
aws ec2 start-network-insights-analysis \
  --network-insights-path-id nip-xxxxxxxx

# ── VPC FLOW LOGS ──────────────────────────────────────────────────

# Enable VPC Flow Logs to CloudWatch (essential for debugging)
aws ec2 create-flow-logs \
  --resource-type VPC \
  --resource-ids vpc-xxxxxxxx \
  --traffic-type ALL \
  --log-destination-type cloud-watch-logs \
  --log-group-name /aws/vpc/flowlogs \
  --deliver-logs-permission-arn arn:aws:iam::123456789012:role/flow-logs-role
```

---

## Console Walkthrough — Key VPC Actions in the AWS Console

**To see your full VPC topology:**
`VPC → Your VPCs → [select VPC] → Resource map tab` — this gives you a visual diagram of all subnets, route tables, gateways, and their connections. This is the fastest way to audit a VPC in an interview scenario.

**To debug routing:**
`VPC → Route Tables → [select route table] → Routes tab` shows all routes. `Subnet associations tab` shows which subnets use this route table. If a subnet has no internet access, this is the first place to check.

**To debug security group rules:**
`EC2 → Security Groups → [select SG] → Inbound rules / Outbound rules` — check if the expected port and source are present. `Network interfaces tab` shows which resources have this SG attached.

**To use Reachability Analyzer (gold for debugging):**
`VPC → Reachability Analyzer → Create and analyze path` — specify source (EC2 instance, ENI) and destination (EC2, RDS endpoint, etc.) with port. AWS will trace the entire path and tell you exactly where connectivity is being blocked — route table, security group, NACL, or missing peering. This saves hours of debugging.

**To check VPC Flow Logs:**
`VPC → Your VPCs → [select VPC] → Flow logs tab` — shows if flow logs are enabled. For active debugging: `CloudWatch → Log groups → /aws/vpc/flowlogs → search for your IP or REJECT entries`.

---

## Terraform — Building a Production VPC for EKS

```hcl
# ── variables.tf ────────────────────────────────────────────────────

variable "cluster_name" {
  default = "production"
}

# ── main.tf ─────────────────────────────────────────────────────────

locals {
  azs            = ["us-east-1a", "us-east-1b", "us-east-1c"]
  public_cidrs   = ["10.0.1.0/24", "10.0.2.0/24", "10.0.3.0/24"]
  private_cidrs  = ["10.0.11.0/21", "10.0.19.0/21", "10.0.27.0/21"]
  isolated_cidrs = ["10.0.101.0/24", "10.0.102.0/24", "10.0.103.0/24"]
}

# VPC
resource "aws_vpc" "main" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_hostnames = true   # Required for EKS
  enable_dns_support   = true   # Required for EKS

  tags = {
    Name = "${var.cluster_name}-vpc"
    "kubernetes.io/cluster/${var.cluster_name}" = "shared"
  }
}

# Internet Gateway
resource "aws_internet_gateway" "main" {
  vpc_id = aws_vpc.main.id
  tags   = { Name = "${var.cluster_name}-igw" }
}

# Public Subnets
resource "aws_subnet" "public" {
  count                   = 3
  vpc_id                  = aws_vpc.main.id
  cidr_block              = local.public_cidrs[count.index]
  availability_zone       = local.azs[count.index]
  map_public_ip_on_launch = true

  tags = {
    Name = "${var.cluster_name}-public-${local.azs[count.index]}"
    "kubernetes.io/cluster/${var.cluster_name}" = "shared"
    "kubernetes.io/role/elb"                    = "1"
  }
}

# Private Subnets (EKS worker nodes + pods)
resource "aws_subnet" "private" {
  count             = 3
  vpc_id            = aws_vpc.main.id
  cidr_block        = local.private_cidrs[count.index]
  availability_zone = local.azs[count.index]

  tags = {
    Name = "${var.cluster_name}-private-${local.azs[count.index]}"
    "kubernetes.io/cluster/${var.cluster_name}" = "shared"
    "kubernetes.io/role/internal-elb"           = "1"
  }
}

# Isolated Subnets (RDS, ElastiCache)
resource "aws_subnet" "isolated" {
  count             = 3
  vpc_id            = aws_vpc.main.id
  cidr_block        = local.isolated_cidrs[count.index]
  availability_zone = local.azs[count.index]

  tags = {
    Name = "${var.cluster_name}-isolated-${local.azs[count.index]}"
  }
}

# Elastic IPs for NAT Gateways
resource "aws_eip" "nat" {
  count  = 3
  domain = "vpc"
  tags   = { Name = "${var.cluster_name}-nat-eip-${count.index}" }
}

# NAT Gateways — one per AZ for HA
resource "aws_nat_gateway" "main" {
  count         = 3
  allocation_id = aws_eip.nat[count.index].id
  subnet_id     = aws_subnet.public[count.index].id
  tags          = { Name = "${var.cluster_name}-nat-${local.azs[count.index]}" }
  depends_on    = [aws_internet_gateway.main]
}

# Public Route Table
resource "aws_route_table" "public" {
  vpc_id = aws_vpc.main.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.main.id
  }

  tags = { Name = "${var.cluster_name}-public-rt" }
}

resource "aws_route_table_association" "public" {
  count          = 3
  subnet_id      = aws_subnet.public[count.index].id
  route_table_id = aws_route_table.public.id
}

# Private Route Tables — one per AZ pointing to local NAT GW
resource "aws_route_table" "private" {
  count  = 3
  vpc_id = aws_vpc.main.id

  route {
    cidr_block     = "0.0.0.0/0"
    nat_gateway_id = aws_nat_gateway.main[count.index].id
  }

  tags = { Name = "${var.cluster_name}-private-rt-${local.azs[count.index]}" }
}

resource "aws_route_table_association" "private" {
  count          = 3
  subnet_id      = aws_subnet.private[count.index].id
  route_table_id = aws_route_table.private[count.index].id
}

# S3 Gateway Endpoint (free, essential for ECR image pulls)
resource "aws_vpc_endpoint" "s3" {
  vpc_id            = aws_vpc.main.id
  service_name      = "com.amazonaws.us-east-1.s3"
  vpc_endpoint_type = "Gateway"
  route_table_ids   = aws_route_table.private[*].id

  tags = { Name = "${var.cluster_name}-s3-endpoint" }
}
```

---

## Common Failure Scenarios and How to Debug Them

### Scenario 1: EKS Pods Cannot Pull Images from ECR

Symptoms: Pods stuck in `ImagePullBackOff` or `ErrImagePull`. This is one of the most common EKS issues.

```bash
# Step 1: Describe the pod to see the exact error
kubectl describe pod my-pod -n my-namespace
# Look for: "Failed to pull image" and the specific error message

# Step 2: Check if the node has internet access (if not using VPC endpoints)
# SSH to node or use SSM Session Manager
curl -I https://123456789012.dkr.ecr.us-east-1.amazonaws.com
# If this times out: routing problem (NAT GW or VPC endpoint issue)

# Step 3: Check if NAT Gateway is healthy
aws ec2 describe-nat-gateways \
  --filter Name=vpc-id,Values=vpc-xxxxxxxx \
  --query 'NatGateways[*].{ID:NatGatewayId,State:State}'

# Step 4: Check if ECR VPC endpoints exist (if using private cluster)
aws ec2 describe-vpc-endpoints \
  --filters Name=vpc-id,Values=vpc-xxxxxxxx \
  --query 'VpcEndpoints[*].{Service:ServiceName,State:State}'
# Look for: ecr.api, ecr.dkr, s3

# Step 5: Check the node's IAM role has ECR pull permissions
aws iam list-attached-role-policies \
  --role-name eks-node-group-role
# Must have: AmazonEC2ContainerRegistryReadOnly

# Step 6: Check security group on VPC endpoints allows HTTPS from nodes
aws ec2 describe-security-groups \
  --group-ids sg-vpc-endpoint \
  --query 'SecurityGroups[0].IpPermissions'
# Must allow: TCP 443 from node security group
```

### Scenario 2: Pod Cannot Connect to RDS Database

Symptoms: Application pod gets connection timeout trying to reach the RDS endpoint.

```bash
# Step 1: Get the RDS endpoint and security group
aws rds describe-db-instances \
  --db-instance-identifier my-db \
  --query 'DBInstances[0].{Endpoint:Endpoint.Address,
            Port:Endpoint.Port,SG:VpcSecurityGroups}'

# Step 2: Check if pod's node security group is allowed in RDS security group
aws ec2 describe-security-groups \
  --group-ids sg-rds-xxxx \
  --query 'SecurityGroups[0].IpPermissions'
# Must have: TCP 5432 (postgres) or 3306 (mysql)
# from: node security group OR pod CIDR

# Step 3: Check if RDS is in the right subnet (isolated/private)
aws rds describe-db-subnet-groups \
  --db-subnet-group-name my-db-subnet-group

# Step 4: Test connectivity from inside a pod
kubectl run -it debug --image=nicolaka/netshoot --restart=Never -- \
  nc -zv my-db.xxxxx.us-east-1.rds.amazonaws.com 5432
# If this times out: security group is blocking
# If "Connection refused": wrong port or RDS is not listening

# Step 5: Use VPC Reachability Analyzer
aws ec2 create-network-insights-path \
  --source eni-node-xxxxx \
  --destination eni-rds-xxxxx \
  --protocol TCP \
  --destination-port 5432
aws ec2 start-network-insights-analysis \
  --network-insights-path-id nip-xxxxxxxx
# This will tell you EXACTLY which SG rule or route is blocking
```

### Scenario 3: Ingress Not Getting an External IP / ALB Not Provisioned

Symptoms: `kubectl get ingress` shows `ADDRESS` as empty even after several minutes.

```bash
# Step 1: Check AWS Load Balancer Controller logs
kubectl logs -n kube-system \
  -l app.kubernetes.io/name=aws-load-balancer-controller

# Common errors:
# "no matching subnet" → missing subnet tags
# "unable to resolve service" → service doesn't exist
# "AccessDenied" → LBC IAM role missing permissions

# Step 2: Check subnet tags
aws ec2 describe-subnets \
  --subnet-ids subnet-public-az-a \
  --query 'Subnets[0].Tags'
# Must have: kubernetes.io/role/elb=1

# Step 3: Check the ingress annotations
kubectl describe ingress my-ingress -n my-namespace
# Look for: kubernetes.io/ingress.class: alb
# Or: ingressClassName: alb in spec

# Step 4: Check if LBC has the right IAM permissions (IRSA)
kubectl describe sa aws-load-balancer-controller -n kube-system
# Look for: eks.amazonaws.com/role-arn annotation

# Step 5: Check if the ALB security group is allowing traffic
# The LBC creates an SG for the ALB automatically
# Check it allows 80/443 from 0.0.0.0/0 (or your desired CIDR)
```

### Scenario 4: VPC Flow Logs Showing REJECT — Debugging Unknown Traffic Drops

```bash
# VPC Flow Log format:
# version account-id interface-id srcaddr dstaddr srcport dstport
# protocol packets bytes start end action log-status

# Search for REJECT entries for a specific destination IP
aws logs filter-log-events \
  --log-group-name /aws/vpc/flowlogs \
  --filter-pattern '[version, account, eni, source, destination="10.0.3.45",
                     srcport, destport="5432", protocol="6", ...]' \
  --start-time $(date -d '30 minutes ago' +%s000)

# Interpret a flow log entry:
# 2 123456789012 eni-xxx 10.0.1.10 10.0.5.45 54231 5432 6 1 40 ... REJECT OK
#                                                              ^TCP  ^       ^BLOCKED
# This tells you: source 10.0.1.10 tried to reach 10.0.5.45:5432
# and was REJECTED — look at the security group on the destination
```

---

## How This Connects to the Rest of Your Learning Path

IAM touches every single topic that comes after this. Here's specifically what you're building toward:

**EC2 & Auto Scaling (Topic 3):** EC2 instances live inside VPC subnets. Launch templates specify which subnet and security group. Auto Scaling Groups span multiple AZs using your private subnets.

**EKS AWS Layer (Topic 4):** Everything EKS does at the network layer is VPC — the CNI plugin, node group subnet placement, control plane ENIs, endpoint access mode, cluster security group. This topic is the prerequisite for all EKS networking.

**Load Balancing (Topic 7):** ALBs live in public subnets, target groups point to private subnet resources. The AWS Load Balancer Controller reads your VPC subnet tags to know where to deploy. All of that only makes sense after understanding VPC.

**RDS (Topic 11):** RDS lives in isolated subnets. DB subnet groups span multiple AZs. Security groups control which EKS pods can reach the database. All VPC concepts.

**Networking Deep Dive (Topic 12):** Transit Gateway, VPC Peering, PrivateLink — all of these are extensions of VPC. You need this topic mastered before that one makes sense.

**Security (Topic 13):** VPC Flow Logs feed into CloudWatch and GuardDuty for threat detection. NACLs are part of the defense-in-depth security model. Security groups are the primary network security control.

---

## Interview Cheat Sheet

| Question | Crisp Answer |
|----------|-------------|
| What is the difference between a public and private subnet? | The only difference is the route table. A public subnet has a route `0.0.0.0/0 → IGW`. A private subnet routes `0.0.0.0/0 → NAT Gateway`. The subnet itself has no inherent public/private property. |
| What is the difference between a Security Group and a NACL? | Security Groups are stateful, resource-level, allow-only firewalls evaluated all at once. NACLs are stateless, subnet-level, allow+deny firewalls evaluated in rule order. Security Groups are the primary control; NACLs are for coarse subnet-level blocking. |
| What does stateful mean for a Security Group? | Return traffic for an allowed connection is automatically permitted without needing an explicit outbound rule. AWS tracks connection state. |
| Why does EKS use the VPC CNI plugin? | So pods get real VPC IP addresses routable within the VPC — no overlay network, no tunneling. Pods can communicate directly with RDS, ElastiCache, and other VPC resources. |
| What is IP exhaustion in EKS and how do you prevent it? | Each pod consumes a VPC IP. EC2 instances have limits on IPs per ENI. Prevent it by using large subnets (/21 or bigger) for worker nodes, enabling prefix delegation in VPC CNI, or using custom networking. |
| What are VPC Endpoints and why do you use them? | Private connections between your VPC and AWS services that never traverse the public internet. Saves NAT Gateway costs, improves security, and is required for fully private EKS clusters. |
| What subnet tags are required for EKS load balancers? | Public subnets need `kubernetes.io/role/elb=1` for internet-facing ALBs. Private subnets need `kubernetes.io/role/internal-elb=1` for internal load balancers. Both need `kubernetes.io/cluster/<name>=shared`. |
| How do you give private subnet resources outbound internet access? | NAT Gateway in a public subnet. Private subnet route table has `0.0.0.0/0 → NAT Gateway`. For HA, one NAT Gateway per AZ. |
| What is the minimum subnet size AWS allows? | /28 — giving 16 IP addresses, 11 usable after AWS reserves 5. |
| How would you debug a pod that cannot connect to RDS? | Check security group on RDS allows traffic from node/pod SG on the DB port. Check the pod is in a subnet that can route to the isolated subnet. Use `nc -zv` from inside the pod to test. Use VPC Reachability Analyzer for definitive path analysis. |
| What happens if you only have one NAT Gateway across multiple AZs? | If that NAT Gateway's AZ goes down, all private subnet resources in other AZs lose outbound internet access. Always deploy one NAT Gateway per AZ for production. |
| What VPC endpoints does a fully private EKS cluster require? | ec2, ecr.api, ecr.dkr, s3 (Gateway), logs, sts — at minimum. Without these, nodes cannot join the cluster and pods cannot pull images from ECR. |
| What is VPC Flow Logs and when do you use it? | Flow Logs capture metadata about all IP traffic in/out of your VPC. Use it to debug REJECT entries (security group/NACL blocks), audit traffic patterns, and feed security tools like GuardDuty. |
| How does a Security Group reference another Security Group as a source? | Instead of specifying a CIDR, you specify the security group ID as the source. Any resource with that SG attached is automatically allowed — no IP management needed. This is the right pattern for EKS-to-RDS access control. |
