# 🖥️ AWS Compute — Category 2: Complete Interview Guide

> **Target Audience:** DevOps / SRE / Platform / Cloud Engineers  
> **Difficulty:** Beginner → Advanced  
> **Topics Covered:** EC2, Pricing Models, ASG, Launch Templates, ELB, Placement Groups, IMDSv2, Spot Instances

---

## 📋 Table of Contents

1. [2.1 EC2 — Instance Types, AMIs, Key Pairs, User Data](#21-ec2--instance-types-amis-key-pairs-user-data)
2. [2.2 EC2 Pricing Models](#22-ec2-pricing-models)
3. [2.3 Auto Scaling Groups (ASG)](#23-auto-scaling-groups-asg)
4. [2.4 Launch Templates vs Launch Configurations](#24-launch-templates-vs-launch-configurations)
5. [2.5 Elastic Load Balancing — ALB, NLB, CLB, GWLB](#25-elastic-load-balancing--alb-nlb-clb-gwlb)
6. [2.6 EC2 Placement Groups](#26-ec2-placement-groups)
7. [2.7 EC2 Instance Metadata & IMDSv2](#27-ec2-instance-metadata--imdsv2)
8. [2.8 Spot Instances — Interruption Handling, Spot Fleets, Diversification](#28-spot-instances--interruption-handling-spot-fleets-diversification)

---

---

# 2.1 EC2 — Instance Types, AMIs, Key Pairs, User Data

---

## 🟢 What It Is in Simple Terms

EC2 (Elastic Compute Cloud) is AWS's virtual machine service. You rent a computer in AWS's data center, choose its size, operating system, and software, and it's ready in minutes. Everything else in AWS — containers, databases, load balancers — either runs ON EC2 or was built to replace it.

---

## 🔍 Why It Exists / What Problem It Solves

Before cloud, companies bought physical servers. That meant:

- 6–12 week lead times to provision hardware
- Paying for peak capacity even during off-peak hours
- No way to scale instantly during traffic spikes

EC2 solved this by virtualizing compute — you get a slice of a physical host, billed by the second, disposable at will.

---

## ⚙️ How It Works Internally

```
Physical Host (Nitro Hypervisor)
├── EC2 Instance A (your VM)
├── EC2 Instance B (another customer's VM)
└── EC2 Instance C (another customer's VM)

AWS Nitro System:
┌─────────────────────────────────────┐
│         Nitro Hypervisor            │  ← Lightweight, near bare-metal perf
│  ┌──────────┐  ┌──────────────────┐ │
│  │ Nitro    │  │ Nitro Security   │ │
│  │ Cards    │  │ Chip             │ │
│  │(Network/ │  │(Hardware root of │ │
│  │ Storage) │  │ trust)           │ │
│  └──────────┘  └──────────────────┘ │
└─────────────────────────────────────┘
```

AWS uses the **Nitro hypervisor** — it offloads network and storage virtualization to dedicated hardware cards, giving EC2 instances near bare-metal performance. This is why newer instance types (C5, M5, R5+) are faster than older ones (C3, M3).

---

## 🧩 Key Components

### Instance Type Families

```
Family  Purpose                    Examples
──────────────────────────────────────────────────────
t       Burstable (dev/test)       t3.micro, t3.medium
m       General purpose            m6i.large, m7g.xlarge
c       Compute optimized          c6i.2xlarge, c7g.4xlarge
r       Memory optimized           r6i.8xlarge, r7g.16xlarge
i       Storage optimized (NVMe)   i3.xlarge, i4i.2xlarge
p/g     GPU (ML/graphics)          p4d.24xlarge, g5.xlarge
hpc     High perf computing        hpc6a.48xlarge
```

### Instance Size Naming Convention

```
    m   6   i  .  2  x  large
    │   │   │     │  │    │
    │   │   │     │  └────┴── Size modifier
    │   │   │     └────────── # of units (1x, 2x, 4x...)
    │   │   └──────────────── Processor (i=Intel, a=AMD, g=Graviton)
    │   └──────────────────── Generation (higher = newer/better)
    └──────────────────────── Family (m=general purpose)
```

> ⚠️ **Interview Gotcha:** `t3` instances use **CPU Credits**. They earn credits when idle and spend them when bursting. If you run out of credits in `standard` mode, performance drops. In `unlimited` mode you get charged extra. This trips up many candidates.

---

### AMIs (Amazon Machine Images)

An AMI is a snapshot of an OS + software configuration used to launch EC2 instances.

```
AMI contains:
├── Root volume snapshot (OS, installed packages)
├── Block device mappings (which EBS volumes to attach)
├── Launch permissions (who can use this AMI)
└── Architecture (x86_64 or arm64)

AMI Types:
├── AWS-provided    → Amazon Linux 2, Ubuntu, Windows Server
├── AWS Marketplace → Pre-configured (e.g., Nginx Plus, Splunk)
├── Community       → Shared by other AWS users (use with caution)
└── Your own        → Golden AMIs baked by your team
```

**Golden AMI Pattern** (very common in production):

```
Base OS → Install agents (CW, SSM, etc.)
       → Harden (CIS benchmarks)
       → Run Packer
       → Output: Your Golden AMI
       → ASG uses this AMI for all instances
```

---

### Key Pairs

```
How SSH key pairs work with EC2:

Your machine          AWS
─────────             ────────────────────────────
Private Key    ←→     Public Key stored in ~/.ssh/authorized_keys
(you keep it)         (injected at boot via cloud-init)

ssh -i my-key.pem ec2-user@<public-ip>
```

> ⚠️ **Gotcha:** AWS stores only the public key. If you lose your private key, you CANNOT recover it. For prod, most teams use **SSM Session Manager** instead of SSH — no key pair needed, no open port 22.

---

### User Data

Script that runs **once** at first boot (via cloud-init):

```bash
#!/bin/bash
# This runs as root at instance launch
yum update -y
yum install -y nginx
systemctl enable nginx
systemctl start nginx
echo "Hello from $(hostname)" > /var/www/html/index.html
```

```
Instance Launch Timeline:
0s   → Hypervisor allocates VM
~10s → cloud-init starts
~15s → User data script executes
~60s → Instance health checks pass
~90s → Instance "InService" in ASG
```

> ⚠️ **Gotcha:** User data runs as **root**. It runs only on first boot by default. If your script fails, the instance still launches — EC2 doesn't roll back. Debugging: check `/var/log/cloud-init-output.log`

---

## 💬 Short Crisp Interview Answer

*"EC2 is AWS's virtual machine service built on the Nitro hypervisor. You choose an instance family based on your workload — compute, memory, storage, or GPU optimized — and a size. AMIs are the blueprint — they contain the OS and pre-installed software. User data lets you bootstrap instances on first boot. In production, we typically build golden AMIs with our agents pre-installed and use SSM Session Manager instead of key pairs for access."*

---

## 🔬 Deep Dive Version

*"EC2 runs on AWS's Nitro system which offloads network and storage I/O to dedicated hardware cards, giving near bare-metal performance. Instance types follow a naming convention — family, generation, processor variant, size. t-family instances are special — they use a CPU credit model for bursting. AMIs are region-specific but can be copied cross-region. For production, the golden AMI pattern with Packer is standard — you bake all agents, hardening, and config into the AMI so instances are immutable and launch fast. User data is a one-time bootstrap script but for idempotent configuration management, you'd layer in SSM State Manager or Ansible on top."*

---

## 🏭 Real World Production Example

```
Team: Platform Engineering at a fintech company

Problem: Dev teams spinning up EC2s with inconsistent configs,
         missing security agents, different OS versions.

Solution: Golden AMI Pipeline

  ┌──────────┐    ┌─────────┐    ┌──────────────┐    ┌─────────┐
  │ Base AMI │───▶│ Packer  │───▶│ Golden AMI   │───▶│  ASG    │
  │(AmazonLX)│    │ Script  │    │(hardened+    │    │Launch   │
  └──────────┘    └─────────┘    │ agents baked)│    │Template)│
                                 └──────────────┘    └─────────┘

Packer script installs:
- CloudWatch Agent
- SSM Agent
- Datadog Agent
- CIS hardening scripts
- Company CA certificates

Result:
- All instances identical at launch
- No SSH, no key pairs — SSM only
- AMI rebuilt weekly with latest patches
- New AMI triggers ASG instance refresh
```

---

## ❓ Common Interview Questions & Strong Answers

**Q: What's the difference between stopping and terminating an EC2 instance?**

> Stopping preserves the EBS root volume and the instance's private IP (in a VPC). RAM is lost, the host may change. Terminating deletes the instance and, by default, deletes the root EBS volume. The key gotcha: if `DeleteOnTermination` is false for the root volume, the EBS persists and you keep paying.

**Q: Can you change the instance type of a running EC2?**

> No — you must stop it first, then change the instance type, then start it. The instance may land on a different physical host. The private IP stays the same (VPC), but the public IP changes unless you're using an Elastic IP.

**Q: How does EC2 instance metadata work?**

> Every instance can query `http://169.254.169.254/latest/meta-data/` to get its own metadata — instance ID, AZ, IAM role credentials, public IP, etc. IMDSv2 is the secure version — it requires a session token obtained via a PUT request first, preventing SSRF attacks from stealing credentials.

---

## ⚠️ Tricky Edge Cases / Gotchas

| Gotcha | Detail |
|--------|--------|
| t3 CPU credits | Standard mode = throttled when credits run out. Unlimited = surprise bill |
| AMI is region-locked | You must copy AMI to use in another region |
| User data size limit | 16 KB max. Use S3 + curl for larger scripts |
| Key pairs ≠ IAM | SSH key pair controls OS access, IAM role controls AWS API access. They're separate |
| Stopped instance billing | You don't pay for compute when stopped, but you still pay for EBS and Elastic IPs |
| Instance store | Some instance types have ephemeral local NVMe. Data is LOST on stop/terminate |

---

## 🔗 Connections to Other AWS Concepts

```
EC2 connects to:
├── IAM          → Instance Profiles give EC2 AWS API permissions
├── VPC          → EC2 lives in a subnet, gets a security group
├── EBS          → Block storage attached to EC2
├── ASG          → EC2 fleet management, scaling
├── ALB/NLB      → Traffic distribution to EC2 instances
├── SSM          → Remote access, patching, config management
├── CloudWatch   → Metrics, logs from EC2
├── AMI          → Blueprint for EC2
└── Nitro        → Underlying hypervisor giving performance
```

---

---

# 2.2 EC2 Pricing Models

---

## 🟢 What It Is in Simple Terms

AWS gives you 4 ways to pay for EC2. Pick the wrong one and you'll massively overpay. Pick the right one and you can cut your compute bill by 70–90%.

---

## ⚙️ How Each Model Works

```
┌─────────────────┬──────────┬──────────────┬────────────────────────┐
│ Model           │ Discount │ Commitment   │ Best For               │
├─────────────────┼──────────┼──────────────┼────────────────────────┤
│ On-Demand       │ 0%       │ None         │ Unpredictable workloads│
│ Reserved (1yr)  │ ~40%     │ 1 year       │ Steady-state baseline  │
│ Reserved (3yr)  │ ~60%     │ 3 years      │ Long-term baseline     │
│ Savings Plans   │ ~66%     │ 1 or 3 years │ Flexible baseline      │
│ Spot            │ ~70-90%  │ None         │ Fault-tolerant/batch   │
└─────────────────┴──────────┴──────────────┴────────────────────────┘
```

---

### On-Demand

- Pay by the second (minimum 60 seconds)
- No commitment, highest price
- Use for: spiky traffic, dev/test, new applications you can't predict

---

### Reserved Instances (RIs)

```
3 payment options:
├── All Upfront     → Biggest discount, pay everything now
├── Partial Upfront → Pay some now, rest monthly
└── No Upfront      → Pay monthly, smallest discount

2 scope options:
├── Regional RI → Applies to any AZ in the region (flexible)
└── Zonal RI    → Applies to specific AZ (+ capacity reservation)

Standard RI    → Cannot change instance family (m5 stays m5)
Convertible RI → Can exchange for different family/OS (more flexible, less discount)
```

> ⚠️ **Gotcha:** RIs don't "attach" to instances. They're a billing construct. AWS automatically applies RI discounts to matching running instances. You can have 10 RIs and 0 running instances — you're still paying for the RIs.

---

### Savings Plans

Newer, more flexible alternative to RIs:

```
Compute Savings Plan:
└── Commit to $/hour spend (e.g., $10/hr)
    └── Applies to ANY EC2 instance family, region, size, OS
    └── Also applies to Fargate and Lambda
    └── Most flexible — recommended over RIs for most teams

EC2 Instance Savings Plan:
└── Commit to specific instance family in a region (e.g., m5 in us-east-1)
    └── Higher discount than Compute SP (~66% vs ~60%)
    └── Can change size, AZ, OS within family
```

---

### Spot Instances

```
How Spot pricing works:

AWS has spare capacity → offers it at 70-90% discount
Your Spot instance runs → until AWS needs capacity back
AWS needs capacity     → 2-minute warning then termination

Spot Instance States:
open → running → interrupted (2-min notice) → terminated/stopped/hibernated
```

---

## 💬 Short Crisp Interview Answer

*"AWS has four EC2 pricing models. On-Demand is full price, no commitment — good for unpredictable workloads. Reserved Instances or Savings Plans give 40–66% off in exchange for a 1 or 3 year commitment — you use these for your steady-state baseline. Spot instances use spare AWS capacity at 70–90% off but can be interrupted with 2 minutes notice — ideal for batch jobs, stateless workers, and fault-tolerant workloads. In production, a typical strategy is: Savings Plans for baseline, On-Demand for buffer, and Spot for burst or batch."*

---

## 🏭 Real World Production Example

```
Strategy: "3-tier compute cost optimization"

Your workload: Web app, always needs minimum 10 instances,
               sometimes needs up to 50 during business hours,
               runs nightly batch jobs.

Solution:
┌──────────────────────────────────────────────────────┐
│  10 instances  → Compute Savings Plan (always on)    │
│  +15 instances → On-Demand (business hour buffer)    │
│  +25 instances → Spot (nightly batch processing)     │
└──────────────────────────────────────────────────────┘

Cost savings vs all On-Demand:
- Savings Plan: saves ~60% on 10 instances
- Spot batch: saves ~80% on nightly jobs
- Net result: 40-50% overall bill reduction
```

---

## ❓ Common Interview Questions

**Q: What happens to your Spot instance when AWS interrupts it?**

> You get a 2-minute warning via instance metadata at `latest/meta-data/spot/termination-time` and via EventBridge. Your app should handle this gracefully — checkpoint state, drain connections, deregister from load balancer. ASGs with mixed instance policies handle this automatically.

**Q: Can you use Reserved Instances across accounts?**

> Yes — in AWS Organizations, RIs and Savings Plans can be shared across accounts via the management account's billing settings. You can also sell unused Standard RIs on the AWS Marketplace.

**Q: Savings Plans vs Reserved Instances — which do you recommend?**

> Compute Savings Plans in almost all cases. They're more flexible — they apply across families, regions, and even Fargate/Lambda. The only reason to choose RIs is if you need capacity reservations in a specific AZ (zonal RIs), or if you're on a very specific instance family long-term and want maximum discount.

---

## ⚠️ Gotchas

| Gotcha | Detail |
|--------|--------|
| RI billing trap | Unused RIs still cost money — you pay whether or not you run instances |
| Spot + stateful apps | Never run databases or stateful apps on Spot without interruption handling |
| Savings Plans stack | Your SP covers usage up to committed amount; excess is On-Demand |
| Convertible RI exchange | You can exchange but the new RI must be equal or greater value |
| Spot price ≠ bid price anymore | AWS moved to market pricing — you pay current Spot price, not your bid |

---

---

# 2.3 Auto Scaling Groups (ASG)

---

## 🟢 What It Is in Simple Terms

An ASG is a fleet manager for EC2 instances. You tell it: "I always want between 2 and 20 instances, target 70% CPU, add/remove instances automatically." ASG handles the rest — launching, terminating, replacing unhealthy instances, and integrating with load balancers.

---

## ⚙️ How It Works Internally

```
ASG Architecture:

                    ┌─────────────────────────┐
                    │    Auto Scaling Group    │
                    │  Min: 2  Max: 20         │
                    │  Desired: 5              │
                    └──────────┬──────────────┘
                               │ manages
              ┌────────────────┼────────────────┐
              ▼                ▼                 ▼
         ┌────────┐       ┌────────┐       ┌────────┐
         │  EC2   │       │  EC2   │       │  EC2   │
         │  i-1   │       │  i-2   │       │  i-3   │
         │  AZ-a  │       │  AZ-b  │       │  AZ-c  │
         └────────┘       └────────┘       └────────┘

ASG Health Check Loop (every 5 min default):
┌──────────────────────────────────────────────┐
│ 1. Check each instance (EC2 or ELB health)   │
│ 2. If unhealthy → terminate → launch new     │
│ 3. Check scaling policies                    │
│ 4. If scale-out triggered → launch instances │
│ 5. If scale-in triggered → terminate (oldest │
│    launch config OR closest to billing hour) │
└──────────────────────────────────────────────┘
```

---

## 🧩 Key Components

### Scaling Policies

```
3 Types of Scaling Policies:

1. TARGET TRACKING (recommended, simplest)
   ─────────────────────────────────────────
   "Keep average CPU at 50%"
   ASG does the math — adds/removes to hit target
   Built-in metrics: CPU, network, ALB request count per target

2. STEP SCALING (more control)
   ─────────────────────────────────────────
   "If CPU 60-80%  → add 1 instance
    If CPU 80-100% → add 3 instances
    If CPU < 40%   → remove 1 instance"
   Good for non-linear workloads

3. SIMPLE SCALING (legacy, avoid)
   ─────────────────────────────────────────
   "If alarm triggers → add 2, wait cooldown, re-evaluate"
   Slow — waits full cooldown between steps
```

**Target Tracking CLI Example:**

```bash
aws autoscaling put-scaling-policy \
  --policy-name cpu-target-tracking \
  --auto-scaling-group-name my-asg \
  --policy-type TargetTrackingScaling \
  --target-tracking-configuration '{
    "PredefinedMetricSpecification": {
      "PredefinedMetricType": "ASGAverageCPUUtilization"
    },
    "TargetValue": 50.0
  }'
```

---

### Cooldown Periods

```
Problem Cooldown Solves:
New instances launch → metrics look better immediately
→ Without cooldown, ASG would immediately scale back in
→ New instances never finish warming up!

Default Cooldown: 300 seconds (5 min)

Timeline:
0s   → Scale-out triggered (CPU 80%)
0s   → New instance starts launching
90s  → Instance InService
90s  → Cooldown starts (300s)
390s → Cooldown ends → ASG evaluates metrics again

⚠️ Key insight: Cooldown applies to Simple Scaling only.
Target Tracking and Step Scaling use "instance warmup"
period instead of cooldown.
```

---

### ⚠️ Lifecycle Hooks (Frequently Asked)

```
Normal ASG flow:
Pending → InService → Terminating → Terminated

With Lifecycle Hooks:

Scale OUT:
Pending → [Pending:Wait] → [Pending:Proceed] → InService
               │
               └── Your hook fires here!
                   - Register with load balancer
                   - Pull config from S3
                   - Run smoke tests
                   - Max wait: 48 hours

Scale IN:
InService → [Terminating:Wait] → [Terminating:Proceed] → Terminated
                  │
                  └── Your hook fires here!
                      - Drain connections
                      - Ship final logs
                      - Deregister from service discovery
                      - Take final snapshot

How hooks work:
1. ASG puts instance in Wait state
2. Sends notification to SNS/SQS/EventBridge
3. Your Lambda/script runs
4. Calls CompleteLifecycleAction (CONTINUE or ABANDON)
5. If no response in heartbeat timeout → default action
```

```bash
# Create a lifecycle hook for scale-in
aws autoscaling put-lifecycle-hook \
  --lifecycle-hook-name drain-connections \
  --auto-scaling-group-name my-asg \
  --lifecycle-transition autoscaling:EC2_INSTANCE_TERMINATING \
  --notification-target-arn arn:aws:sqs:us-east-1:123:my-queue \
  --role-arn arn:aws:iam::123:role/asg-hook-role \
  --heartbeat-timeout 300 \
  --default-result CONTINUE

# Complete lifecycle action from your script
aws autoscaling complete-lifecycle-action \
  --lifecycle-hook-name drain-connections \
  --auto-scaling-group-name my-asg \
  --lifecycle-action-result CONTINUE \
  --instance-id i-1234567890abcdef0
```

---

### Instance Refresh

Used for rolling updates (e.g., deploying a new AMI):

```bash
aws autoscaling start-instance-refresh \
  --auto-scaling-group-name my-asg \
  --preferences '{
    "MinHealthyPercentage": 80,
    "InstanceWarmup": 120
  }'
```

ASG replaces instances a percentage at a time, ensuring minimum healthy percentage is maintained. Much better than terminate-all-and-relaunch.

---

## 💬 Short Crisp Interview Answer

*"An ASG manages a fleet of EC2 instances automatically — maintaining desired capacity, replacing unhealthy instances, and scaling in/out based on policies. There are three scaling policy types: target tracking is simplest and recommended — you set a target metric and ASG does the math. Step scaling gives more control for non-linear loads. Lifecycle hooks are critical in production — they let you pause instance launch or termination to run custom logic like draining connections or registering with service discovery."*

---

## 🏭 Real World Production Example

```
Problem: Node.js API servers taking 4 minutes to warm up JVM cache.
         ASG was scaling out, declaring instances healthy before warm,
         sending live traffic to cold instances = 500 errors.

Solution: Lifecycle Hook + Custom Warmup

Scale-out lifecycle hook:
1. Instance launches → enters Pending:Wait
2. Hook calls Lambda
3. Lambda polls /health endpoint every 10s
4. When /health returns {"cache": "warm"} → CompleteLifecycleAction(CONTINUE)
5. Only then does ALB get the instance

Result: Zero 500 errors from cold instances.
        Slightly slower scale-out but zero errors in prod.
```

---

## ⚠️ Gotchas

| Gotcha | Detail |
|--------|--------|
| Health check type | Default is EC2 health check (just "is the VM running"). Set to ELB to check actual app health |
| Termination policy | Default terminates oldest launch config first, then closest to billing hour |
| AZ rebalancing | ASG auto-balances across AZs even without scaling events — can terminate instances unexpectedly |
| Scale-in protection | Individual instances can be protected from scale-in — useful for "leader" instances |
| Desired < Min | You can't set Desired below Min. Common Terraform bug |
| Cooldown vs warmup | Cooldown = pause after scaling. Warmup = time new instance counts toward metrics |

---

---

# 2.4 Launch Templates vs Launch Configurations

---

## 🟢 What It Is in Simple Terms

Both define "what kind of EC2 instance to launch" — the blueprint for your ASG. Launch Templates are the modern replacement. Launch Configurations are legacy and AWS has stopped adding features to them.

---

## ⚙️ Key Differences

```
┌─────────────────────────┬──────────────────┬─────────────────────┐
│ Feature                 │ Launch Config    │ Launch Template     │
├─────────────────────────┼──────────────────┼─────────────────────┤
│ Versioning              │ ❌ None           │ ✅ Yes (v1, v2, v3) │
│ Spot + On-Demand mix    │ ❌ No             │ ✅ Yes              │
│ Multiple instance types │ ❌ No             │ ✅ Yes              │
│ T2/T3 Unlimited         │ ❌ No             │ ✅ Yes              │
│ Dedicated Hosts         │ ❌ No             │ ✅ Yes              │
│ Capacity Reservations   │ ❌ No             │ ✅ Yes              │
│ AWS recommendation      │ ⚠️ Legacy         │ ✅ Use this         │
└─────────────────────────┴──────────────────┴─────────────────────┘
```

---

## AWS CLI — Create a Launch Template

```bash
aws ec2 create-launch-template \
  --launch-template-name my-web-lt \
  --version-description "v1 - initial" \
  --launch-template-data '{
    "ImageId": "ami-0abcdef1234567890",
    "InstanceType": "m6i.large",
    "KeyName": "my-keypair",
    "SecurityGroupIds": ["sg-12345678"],
    "IamInstanceProfile": {
      "Arn": "arn:aws:iam::123456789:instance-profile/my-role"
    },
    "UserData": "IyEvYmluL2Jhc2gKeXVtIHVwZGF0ZSAteQ==",
    "MetadataOptions": {
      "HttpTokens": "required",
      "HttpEndpoint": "enabled"
    },
    "TagSpecifications": [{
      "ResourceType": "instance",
      "Tags": [{"Key": "Environment", "Value": "prod"}]
    }]
  }'
```

> ⚠️ **Key Interview Point:** Launch Templates support **mixed instance policies** — you can specify a base instance type + overrides, letting ASG use m6i.large OR m6a.large OR m5.large, mixing Spot and On-Demand in one ASG. This is critical for Spot diversification.

---

## 💬 Short Interview Answer

*"Launch Templates are the modern, versioned replacement for Launch Configurations. The critical advantage is versioning — you can have v1, v2, v3 and roll back instantly. They also support mixed instance policies, letting a single ASG run multiple instance types and mix Spot with On-Demand. Launch Configurations are legacy — AWS hasn't added features to them in years. Always use Launch Templates."*

---

---

# 2.5 Elastic Load Balancing — ALB, NLB, CLB, GWLB

---

## 🟢 What It Is in Simple Terms

A load balancer sits in front of your servers and distributes incoming traffic across them. It also health-checks your instances and stops sending traffic to unhealthy ones. AWS has 4 types — each operating at different layers of the network stack.

---

## ⚙️ How It Works Internally

```
Internet → Load Balancer → Target Group → EC2/ECS/Lambda

                    ┌──────────────────────────┐
                    │      Load Balancer        │
                    │  (Multi-AZ, managed)      │
                    └─────────────┬────────────┘
                                  │
                         ┌────────▼────────┐
                         │  Target Group   │
                         │  Health Checks  │
                         └────┬────┬───────┘
                              │    │
                         ┌────▼┐  ┌▼────┐
                         │ EC2 │  │ EC2 │
                         │ AZ-a│  │ AZ-b│
                         └─────┘  └─────┘
```

---

## 🧩 The 4 Load Balancer Types

### ALB — Application Load Balancer (Layer 7)

```
Operates at: HTTP/HTTPS layer
Key feature: Content-based routing

Routing capabilities:
├── Path-based:    /api/* → service-A,  /web/* → service-B
├── Host-based:    api.example.com → api-TG
├── Header-based:  X-Custom-Header: mobile → mobile-TG
├── Query string:  ?version=2 → v2-TG
├── Method-based:  POST → write-TG, GET → read-TG
└── IP-based:      Source IP CIDR conditions

Target types:
├── Instance  → EC2 instance ID
├── IP        → Any IP (even on-prem via Direct Connect)
└── Lambda    → Serverless targets

Sticky sessions: Cookie-based (AWSALB cookie)
WebSocket:       ✅ Supported
gRPC:            ✅ Supported
```

**ALB Connection Flow:**

```
HTTPS request flow:
1. Client → ALB:443 (TLS terminated at ALB)
2. ALB decrypts, inspects HTTP headers
3. ALB evaluates listener rules in priority order
4. ALB selects target group
5. ALB picks target (round-robin or least-outstanding-requests)
6. ALB forwards request to target on HTTP (or HTTPS end-to-end)
7. Response flows back

SSL/TLS:
├── ACM cert on ALB (free cert, auto-renewed)
├── SNI support → multiple certs per ALB (for multi-domain)
└── Security policy → choose TLS 1.2 minimum, cipher suites
```

---

### NLB — Network Load Balancer (Layer 4)

```
Operates at: TCP/UDP/TLS layer
Key feature: Ultra-low latency, millions of RPS, static IP

Key differences from ALB:
├── No content inspection — just TCP bytes
├── Preserves source IP (ALB replaces it with LB IP)
├── One static IP per AZ (assignable Elastic IP)
├── Can handle 1M+ connections/sec
├── Sub-millisecond latency
└── Supports PrivateLink

Use cases:
├── Gaming (UDP)
├── IoT (MQTT)
├── Financial systems (ultra-low latency)
├── PrivateLink services (MUST use NLB)
└── When you need whitelisting by static IP
```

> ⚠️ **Gotcha:** NLB itself doesn't have security groups (classic). You control access via security groups on targets. Since NLB preserves source IP, your EC2 security groups see the real client IP. With ALB, EC2 sees the ALB's IP, so you open SG to ALB's SG, not the internet.

---

### CLB — Classic Load Balancer (Legacy)

```
Operates at: Layer 4 + Layer 7 (limited)
Status: LEGACY — do not use for new workloads

Interview answer:
"CLB is the old generation, doesn't support path-based routing,
 doesn't have target groups, has fewer features.
 Always use ALB or NLB."
```

---

### GWLB — Gateway Load Balancer (Layer 3)

```
Operates at: Network layer (IP packets)
Use case: Network security appliances (firewalls, IDS/IPS)

Traffic flow:
Internet → GWLB → Firewall Appliance (inspect/filter) → GWLB → App

Uses GENEVE protocol (port 6081)
Deploys as a VPC endpoint service

When you'd see this:
"We need to route all traffic through a Palo Alto firewall
 before it reaches our application"
→ GWLB + Palo Alto fleet behind it
```

---

## 💬 Short Crisp Interview Answer

*"AWS has 4 load balancer types. ALB operates at Layer 7 — it understands HTTP and can route based on path, host headers, query strings, and more. It's the right choice for microservices and web apps. NLB operates at Layer 4 — it's ultra-high performance, handles millions of connections, preserves the source IP, and supports static IPs per AZ — ideal for gaming, financial systems, and PrivateLink. CLB is legacy. GWLB is for routing traffic through third-party security appliances like firewalls."*

---

## 🏭 Real World Production Example

```
Microservices API Gateway pattern:

          ┌─────────────────────────────────┐
          │         ALB (single entry)       │
          └─┬──────────────┬────────────────┘
            │              │
     /api/users/*    /api/orders/*   /api/payments/*
            │              │                │
     ┌──────▼──┐    ┌──────▼──┐    ┌───────▼─┐
     │  Users  │    │ Orders  │    │Payments │
     │ Service │    │ Service │    │ Service │
     │  ECS    │    │  ECS    │    │  ECS    │
     └─────────┘    └─────────┘    └─────────┘

One ALB, one DNS name, routes to 3 different ECS services.
Each service auto-scales independently.
ALB health checks each Target Group separately.
```

---

## ⚠️ Gotchas

| Gotcha | Detail |
|--------|--------|
| ALB source IP | EC2 sees ALB's private IP, not client's. Use X-Forwarded-For header for real IP |
| NLB source IP | EC2 sees real client IP — open security group accordingly |
| Cross-zone load balancing | ALB: on by default. NLB: off by default (costs $$ when on) |
| Idle timeout | ALB default 60s. Long-running requests need this increased |
| Deregistration delay | 300s default — LB keeps sending traffic to deregistering target for 300s. Reduce for fast deployments |
| Health check grace period | On ASG, give instances time before health checks start |

---

---

# 2.6 EC2 Placement Groups

---

## 🟢 What It Is in Simple Terms

Placement Groups tell AWS HOW to physically place your EC2 instances relative to each other. Sometimes you want them on the same physical hardware for speed. Sometimes you want them as far apart as possible for resilience.

---

## 🧩 Three Types

### 1. Cluster Placement Group

```
Goal: Maximum network performance between instances

Physical layout:
┌─────────────────────────────────┐
│     Single Rack, Single AZ      │
│  ┌──────┐ ┌──────┐ ┌──────┐   │
│  │ EC2  │ │ EC2  │ │ EC2  │   │
│  └──────┘ └──────┘ └──────┘   │
└─────────────────────────────────┘

Network: Up to 100 Gbps between instances
Latency: Single-digit microseconds

Use cases:
├── HPC (tightly coupled MPI jobs)
├── Big data analytics (Spark/Hadoop with huge shuffles)
└── Machine learning training (GPU clusters)

⚠️ Risk: If rack fails, ALL instances fail together
⚠️ Risk: May get "insufficient capacity" if you try to add
          instances later — launch all instances at once
```

---

### 2. Spread Placement Group

```
Goal: Maximum isolation / resilience

Physical layout:
┌──────┐   ┌──────┐   ┌──────┐
│Rack 1│   │Rack 2│   │Rack 3│
│ EC2  │   │ EC2  │   │ EC2  │
└──────┘   └──────┘   └──────┘
(Different racks, different hardware, different power)

Limit: MAX 7 instances per AZ per placement group
Can span AZs

Use cases:
├── Small critical HA clusters (ZooKeeper, etcd)
├── Primary + standby databases
└── Any workload where simultaneous failure is unacceptable
```

---

### 3. Partition Placement Group

```
Goal: Balance between performance and resilience
      for large distributed systems

Physical layout:
┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│ Partition 1  │  │ Partition 2  │  │ Partition 3  │
│ (own racks,  │  │ (own racks,  │  │ (own racks,  │
│  own power)  │  │  own power)  │  │  own power)  │
│  EC2 EC2 EC2 │  │  EC2 EC2 EC2 │  │  EC2 EC2 EC2 │
└──────────────┘  └──────────────┘  └──────────────┘

Up to 7 partitions per AZ
Hundreds of instances per partition
Instances in same partition may share hardware
Instances in different partitions NEVER share hardware

Partitions visible via instance metadata:
curl http://169.254.169.254/latest/meta-data/placement/partition-number

Use cases:
├── HDFS (put DataNodes in different partitions)
├── Cassandra (put replicas in different partitions)
└── Kafka (spread brokers across partitions)
```

---

## 💬 Short Interview Answer

*"EC2 Placement Groups control physical placement of instances. Cluster packs instances onto the same rack for maximum bandwidth and minimum latency — used for HPC and ML training but all instances share the same failure domain. Spread puts each instance on separate hardware — maximum resilience, limited to 7 instances per AZ. Partition is the middle ground for large distributed systems like Cassandra or HDFS — you define partitions, each with their own racks and power, and place replica sets in different partitions so a hardware failure only affects one partition."*

---

## ⚠️ Gotchas

| Gotcha | Detail |
|--------|--------|
| Cluster = one AZ only | Can't span AZs. If AZ goes down, everything goes down |
| Can't merge PGs | You can't merge two placement groups |
| Existing instances | You can't add an existing running instance to a PG — must stop it first |
| Capacity errors | Cluster PG can fail to launch if AWS can't fit all instances on adjacent hardware — launch all at once |

---

---

# 2.7 EC2 Instance Metadata & IMDSv2

---

## 🟢 What It Is in Simple Terms

Every EC2 instance can ask "who am I?" by querying a special IP address: `169.254.169.254`. This returns data about the instance — its ID, AZ, IAM credentials, public IP, etc. IMDSv2 is the secure version that requires a session token first.

---

## ⚙️ How It Works

### IMDSv1 — INSECURE (Legacy)

```
Simple GET request, no auth required:

curl http://169.254.169.254/latest/meta-data/instance-id
→ i-0abc123def456789

The SSRF attack problem:
┌──────────────────────────────────────────────────────────────┐
│ Attacker finds SSRF vulnerability in your web app            │
│ Sends request: GET http://169.254.169.254/latest/meta-data/  │
│                    iam/security-credentials/my-role          │
│ Gets back: AccessKeyId, SecretAccessKey, Token               │
│ Now attacker has full IAM role permissions!                  │
└──────────────────────────────────────────────────────────────┘
This is how the Capital One breach (2019) happened.
```

---

### IMDSv2 — SECURE (Required)

```
Two-step process:

Step 1: Get a session token (PUT request required)
curl -X PUT "http://169.254.169.254/latest/api/token" \
     -H "X-aws-ec2-metadata-token-ttl-seconds: 21600"
→ Returns: TOKEN_VALUE

Step 2: Use token in all metadata requests
curl -H "X-aws-ec2-metadata-token: TOKEN_VALUE" \
     http://169.254.169.254/latest/meta-data/instance-id

Why SSRF can't exploit IMDSv2:
SSRF attacks typically follow redirects and use GET.
IMDSv2 requires a PUT first → SSRF libraries can't do this.
→ Attacker cannot get the token → cannot get credentials.
```

---

### Useful Metadata Paths

```bash
BASE=http://169.254.169.254/latest
TOKEN=$(curl -X PUT "$BASE/api/token" -H "X-aws-ec2-metadata-token-ttl-seconds: 21600")
H="X-aws-ec2-metadata-token: $TOKEN"

# Instance identity
curl -H "$H" $BASE/meta-data/instance-id
curl -H "$H" $BASE/meta-data/instance-type
curl -H "$H" $BASE/meta-data/placement/region
curl -H "$H" $BASE/meta-data/placement/availability-zone

# Networking
curl -H "$H" $BASE/meta-data/local-ipv4
curl -H "$H" $BASE/meta-data/public-ipv4

# IAM credentials (rotated automatically by AWS)
curl -H "$H" $BASE/meta-data/iam/security-credentials/my-role

# Spot interruption notice (check every 5s on Spot instances)
curl -H "$H" $BASE/meta-data/spot/termination-time
# Returns 404 if not interrupted, returns time if 2-min warning fired

# User data
curl -H "$H" $BASE/user-data
```

---

### Enforce IMDSv2 in Launch Template

```json
{
  "MetadataOptions": {
    "HttpTokens": "required",
    "HttpEndpoint": "enabled",
    "HttpPutResponseHopLimit": 1
  }
}
```

> ⚠️ **Hop Limit Gotcha:** If you're running containers on EC2 and the container needs metadata, set `HttpPutResponseHopLimit: 2`. With limit 1, the PUT token request from inside a container doesn't reach the metadata service due to the extra network hop.

---

## 💬 Short Interview Answer

*"EC2 instance metadata is available at 169.254.169.254 and lets an instance discover its own instance ID, AZ, IAM credentials, and more at runtime. IMDSv2 is the secure version — it requires a session token obtained via a PUT request before any metadata can be fetched. This prevents SSRF attacks from stealing IAM credentials, which is how the Capital One breach happened using the old IMDSv1. In production, we enforce IMDSv2 via the Launch Template's MetadataOptions and an SCP that denies launching instances without it."*

---

## ⚠️ Gotchas

| Gotcha | Detail |
|--------|--------|
| Hop limit for ECS/K8s | Set to 2 if containers need metadata access |
| IMDSv2 enforcement | Set via Launch Template AND via SCP at org level |
| IAM creds auto-rotate | Credentials from metadata rotate before expiry. Never cache them long-term |
| Instance identity document | `/latest/dynamic/instance-identity/document` — signed JSON you can verify to prove you're on a real EC2 |

---

---

# 2.8 Spot Instances — Interruption Handling, Spot Fleets, Diversification

---

## 🟢 What It Is in Simple Terms

Spot instances are unused EC2 capacity that AWS sells at a steep discount. The catch: AWS can reclaim them with 2 minutes notice. Done right, Spot can power production workloads at a fraction of the cost.

---

## ⚙️ How Spot Works Internally

```
AWS has spare physical capacity in every AZ at all times.
Rather than leave it idle, AWS sells it as Spot.

Spot Price:
├── Changes based on supply/demand (but rarely spikes now)
├── Typically 70-90% below On-Demand
└── You pay current Spot price, not a "bid" (AWS changed this)

Interruption trigger:
├── AWS needs capacity back (someone launched On-Demand/Reserved)
├── Spot price exceeds your max price (if you set one)
└── AWS gives 2-minute warning via:
    ├── Instance metadata: /meta-data/spot/termination-time
    ├── EventBridge event: EC2 Spot Instance Interruption Warning
    └── CloudWatch event
```

---

## 🧩 Spot Fleet & EC2 Fleet

```
Problem: Relying on one instance type/AZ = gets interrupted together

Solution: Spot Fleet (diversification)

Spot Fleet config example:
{
  "TargetCapacity": 100,
  "AllocationStrategy": "capacity-optimized",
  "LaunchSpecifications": [
    {"InstanceType": "m5.xlarge",  "SubnetId": "subnet-az1"},
    {"InstanceType": "m5a.xlarge", "SubnetId": "subnet-az1"},
    {"InstanceType": "m6i.xlarge", "SubnetId": "subnet-az2"},
    {"InstanceType": "m4.xlarge",  "SubnetId": "subnet-az2"},
    {"InstanceType": "c5.2xlarge", "SubnetId": "subnet-az3"}
  ]
}

Allocation strategies:
├── capacity-optimized       → launch from pools with most available
│                              capacity (lowest interruption risk) ← RECOMMENDED
├── lowest-price             → cheapest option (higher interruption risk)
├── diversified              → spread evenly across all pools
└── price-capacity-optimized → balance of price and capacity (newer)
```

---

## 🛡️ Interruption Handling Pattern

```bash
#!/bin/bash
# Spot interruption handler — run every 5 seconds on instance
while true; do
  TERMINATION=$(curl -sf \
    -H "X-aws-ec2-metadata-token: $TOKEN" \
    http://169.254.169.254/latest/meta-data/spot/termination-time \
    2>/dev/null)

  if [ -n "$TERMINATION" ]; then
    echo "Spot interruption at: $TERMINATION"

    # 1. Stop accepting new work
    # 2. Checkpoint current progress to S3
    # 3. Drain active connections
    # 4. Deregister from load balancer
    # 5. Complete ASG lifecycle hook

    aws autoscaling complete-lifecycle-action \
      --lifecycle-action-result CONTINUE \
      --instance-id $(curl -sf .../instance-id) \
      --lifecycle-hook-name spot-interruption-hook \
      --auto-scaling-group-name my-asg

    break
  fi
  sleep 5
done
```

---

## 🔧 ASG Mixed Instances Policy (Production Pattern)

```json
{
  "AutoScalingGroupName": "my-mixed-asg",
  "MixedInstancesPolicy": {
    "InstancesDistribution": {
      "OnDemandBaseCapacity": 2,
      "OnDemandPercentageAboveBaseCapacity": 20,
      "SpotAllocationStrategy": "capacity-optimized"
    },
    "LaunchTemplate": {
      "LaunchTemplateSpecification": {
        "LaunchTemplateName": "my-lt",
        "Version": "$Latest"
      },
      "Overrides": [
        {"InstanceType": "m6i.xlarge"},
        {"InstanceType": "m6a.xlarge"},
        {"InstanceType": "m5.xlarge"},
        {"InstanceType": "m5a.xlarge"},
        {"InstanceType": "c6i.2xlarge"}
      ]
    }
  }
}
```

This keeps 2 On-Demand always running as a baseline, fills the rest 80% Spot / 20% On-Demand, across 5 instance types for maximum capacity pool diversification.

---

## 💬 Short Crisp Interview Answer

*"Spot Instances are spare AWS capacity offered at 70–90% discount, but AWS can interrupt them with 2 minutes notice. The key to using Spot in production is diversification — never rely on a single instance type or AZ. Use ASG Mixed Instance Policies with 5+ instance types across multiple AZs. Use the capacity-optimized allocation strategy to minimize interruptions. Design your application to handle interruptions gracefully — checkpoint state to S3, drain connections on the 2-minute warning. For stateless workloads like web servers or batch processing, you can run 80% Spot with 20% On-Demand as baseline and get reliable, cheap compute."*

---

## 🏭 Real World Production Example

```
ML Training Cluster at an AI startup:

Problem: Training jobs take 8-24 hours on p3.8xlarge instances.
         On-Demand cost: $12.24/hr × 20 instances × 16 hrs = $3,916

Solution:
├── Use Spot p3.8xlarge: ~$2.50/hr = $800 (80% savings!)
├── Checkpoint model weights to S3 every 30 minutes
├── If interrupted: job resumes from last checkpoint
├── Use 3 instance types: p3.8xlarge, p3.16xlarge, g4dn.12xlarge
│   (all equivalent GPU compute, spread across capacity pools)
├── Use capacity-optimized strategy
└── SQS job queue: interrupted job returns to queue, retried

Result:
├── Cost: $800 instead of $3,916
├── Average interruption: 1-2 per 16hr job
├── Max checkpoint loss: 30 minutes of training
└── Total extra time due to interruptions: ~1 hour
```

---

## ⚠️ Gotchas

| Gotcha | Detail |
|--------|--------|
| Spot ≠ unreliable | With proper diversification, interruption rates are low (< 5% per hour) |
| Spot for stateful apps | Only if you handle interruption perfectly — checkpoint and resume |
| EBS on Spot | EBS volumes survive Spot interruption if `DeleteOnTermination: false`. Data is safe |
| Spot blocks (deprecated) | Used to offer 1-6hr guaranteed slots. AWS deprecated this in 2021 |
| Reserved + Spot myth | RI discount applies to On-Demand matching instances, not Spot |
| Spot in EKS | Use Karpenter or Cluster Autoscaler with Spot nodegroups — Karpenter is better at multi-type diversification |

---

---

# 🔗 Category 2 — Full Connections Map

```
COMPUTE (EC2) connects to everything:

EC2 Instances
├── IAM Instance Profile    → AWS API permissions
├── VPC/Subnets/SGs         → Network isolation
├── EBS/EFS/Instance Store  → Storage
├── AMI                     → Boot image (Golden AMI pattern)
├── ASG                     → Fleet management + scaling
│   ├── Launch Templates    → Instance config (versioned)
│   ├── Scaling Policies    → Target tracking / step
│   ├── Lifecycle Hooks     → Custom launch/terminate logic
│   └── Instance Refresh    → Rolling AMI updates
├── ALB/NLB                 → Traffic distribution
│   └── Target Groups       → Health check + routing
├── Placement Groups        → Physical placement strategy
├── Spot Fleet              → Cost optimization + diversification
├── CloudWatch              → Metrics and alarms driving ASG
├── SSM                     → Patch, access, config
├── KMS                     → EBS encryption
└── IMDSv2                  → Secure metadata access
```

---

## 📌 Quick Reference — Interview Cheat Sheet

| Topic | Key Number / Fact |
|-------|-------------------|
| Spot discount | 70–90% off On-Demand |
| Spot warning | 2 minutes before interruption |
| Savings Plans discount | Up to 66% off |
| ASG default cooldown | 300 seconds |
| Spread PG limit | 7 instances per AZ |
| Partition PG limit | 7 partitions per AZ |
| User data size limit | 16 KB |
| ALB idle timeout default | 60 seconds |
| ALB deregistration delay | 300 seconds default |
| IMDSv2 token TTL max | 21600 seconds (6 hours) |
| NLB cross-zone LB | Off by default (costs extra) |
| ALB cross-zone LB | On by default |
| t3 CPU credit mode | Standard (throttle) or Unlimited (charged) |
| Launch Template versions | Unlimited, with Default and Latest pointers |

---

*Guide prepared for DevOps / SRE / Platform Engineer interview preparation.*  
*Excluded topics: CodeBuild, CodePipeline, CloudFormation.*
