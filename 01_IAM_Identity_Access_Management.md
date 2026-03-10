# Topic 1: IAM — Identity & Access Management

---

## WHY Does IAM Exist? What Problem Does It Solve?

Imagine you're running a large company. You have hundreds of employees, dozens of departments, external contractors, and automated systems — all needing access to different resources. You wouldn't give every employee a master key to every room in the building. You'd give the security guard access to the front door, the accountant access to the finance room, and the developer access to the server room — and nothing more.

Before IAM existed, AWS had a simpler model — you had one root account with one set of credentials, and everything used those same credentials. That's the equivalent of giving every employee, every contractor, and every automated script the master key to your entire building. One leak and everything is compromised.

IAM solves this by answering three fundamental questions for every single action taken in AWS:

**Who are you? Can you prove it? And are you allowed to do this specific thing?**

Every API call in AWS — whether it's a human clicking in the console, a Jenkins pipeline pushing an image to ECR, a Kubernetes pod reading a secret, or a Lambda function writing to S3 — goes through IAM before anything happens. IAM is not a feature you opt into. It is the foundation that everything else sits on.

---

## The Big Picture — How IAM Fits Into AWS

```
                        ┌─────────────────────────────────────────┐
                        │              AWS CLOUD                   │
                        │                                          │
  ┌──────────┐          │   ┌─────────┐    ┌──────────────────┐   │
  │  Human   │──login──▶│   │   IAM   │───▶│  AWS Services    │   │
  │  User    │          │   │         │    │  (S3, EC2, EKS,  │   │
  └──────────┘          │   │ AuthN   │    │   RDS, ECR...)   │   │
                        │   │   +     │    └──────────────────┘   │
  ┌──────────┐          │   │ AuthZ   │                            │
  │ Jenkins  │──role───▶│   │         │    Every API call passes   │
  │ Pipeline │          │   │         │    through IAM first.      │
  └──────────┘          │   └─────────┘    No exceptions.          │
                        │        ▲                                  │
  ┌──────────┐          │        │                                  │
  │   EKS    │──IRSA───▶│        │                                  │
  │   Pod    │          │   Policies define                         │
  └──────────┘          │   WHAT is allowed                        │
                        └─────────────────────────────────────────┘
```

**AuthN** = Authentication — proving who you are (your identity)
**AuthZ** = Authorization — proving you are allowed to do something (your permissions)

IAM handles both. And it does this for every single interaction with AWS — humans, machines, services, and pods.

---

## The Core Building Blocks of IAM

Think of IAM as having four fundamental concepts. Everything else is built on these four.

### 1. IAM Users

An IAM User is a permanent identity created inside your AWS account. It represents a specific human or application. It has long-lived credentials — either a username/password for console access, or access key + secret key for programmatic access.

The real-world analogy is a physical employee ID card. It's tied to a specific person, it exists until you explicitly delete it, and if someone steals it, they have your identity permanently until you revoke it.

**In production, IAM Users are actually considered a legacy pattern for most use cases.** You should not create IAM Users for applications, pipelines, or services. You should use Roles for those. Users are mainly for human operators who need console access, and even then, most mature organizations use SSO (via IAM Identity Center) instead of individual IAM Users. But you need to understand Users because you'll find them everywhere in the wild and interviewers will ask about them.

### 2. IAM Groups

A Group is simply a collection of IAM Users. You attach policies to the Group, and all users in that group inherit those permissions. This is purely a management convenience — Groups have no identity of their own and cannot be used in resource policies or assumed by services.

The analogy is a job title or department. Instead of giving every developer permission individually, you put them all in a "Developers" group and manage permissions once.

### 3. IAM Roles

This is the most important concept in modern AWS. A Role is an identity that **does not belong to a specific person or thing permanently**. Instead, it is *assumed* temporarily. When an entity assumes a role, AWS gives it temporary credentials — an access key, a secret key, and a session token — that expire after a defined period (between 15 minutes and 12 hours).

The real-world analogy is a contractor badge. When a contractor comes to your office, you give them a temporary badge for the day. It has specific access for specific rooms. At the end of the day, it expires. You don't give them a permanent employee card.

This is fundamentally more secure because:
- Credentials are temporary — even if leaked, they expire
- You never store long-lived credentials in application code or config files
- The audit trail shows exactly when the role was assumed and by whom

**Roles are what your Jenkins pipelines, EKS pods, EC2 instances, Lambda functions, and cross-account deployments should always use. Never IAM Users for these.**

### 4. IAM Policies

A Policy is a JSON document that defines exactly what actions are allowed or denied, on which resources, and under what conditions. Policies are attached to Users, Groups, or Roles to grant them permissions.

Without a policy explicitly allowing something, it is denied by default. This is called **implicit deny** — AWS denies everything unless there is an explicit allow. And an explicit deny in any policy always overrides any allow, no matter where that allow comes from.

---

## The Anatomy of an IAM Policy

This is the most important JSON you'll read in AWS. Understanding every field is non-negotiable for interviews.

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "AllowS3ReadOnSpecificBucket",
      "Effect": "Allow",
      "Action": [
        "s3:GetObject",
        "s3:ListBucket"
      ],
      "Resource": [
        "arn:aws:s3:::my-production-bucket",
        "arn:aws:s3:::my-production-bucket/*"
      ],
      "Condition": {
        "StringEquals": {
          "aws:RequestedRegion": "us-east-1"
        }
      }
    }
  ]
}
```

Let me walk through every field because interviewers will ask about each one:

**Version** — Always `"2012-10-17"`. This is not a date you choose — it's the policy language version. Using the older `"2008-10-17"` disables certain features like policy variables. Always use `2012-10-17`.

**Statement** — An array of permission statements. One policy can have multiple statements.

**Sid** — Statement ID. Optional, but use it. It's a human-readable label for what this statement does. Makes debugging much easier when you have 20 statements in a policy.

**Effect** — Either `"Allow"` or `"Deny"`. This is binary. There is no "maybe."

**Action** — What API operations are being allowed or denied. These are in the format `"service:APIOperation"`. You can use wildcards — `"s3:*"` means all S3 actions. Being too broad here is the most common security mistake in production.

**Resource** — Which specific AWS resources this statement applies to. This is expressed as an ARN (Amazon Resource Name) — the unique identifier for any AWS resource. The `*` wildcard here means all resources of that type, which is almost always too broad for production.

**Condition** — Optional but powerful. Adds constraints like "only from this IP range", "only when MFA is enabled", "only in this region", "only for requests tagged with this value." Conditions are how you write fine-grained, production-grade policies.

---

## ARNs — The AWS Resource Naming System

Before going further you need to understand ARNs because they appear in every policy.

```
arn:aws:s3:::my-production-bucket
 │   │   │  │  └─ Resource identifier
 │   │   │  └──── Account ID (blank for global services like S3)
 │   │   └─────── Region (blank for global services like S3)
 │   └─────────── Service name
 └─────────────── Always "arn"

arn:aws:iam::123456789012:role/eks-node-role
 │   │   │    │             └─ Resource type/name
 │   │   │    └─────────────── AWS Account ID
 │   │   └──────────────────── IAM is global, no region
 │   └──────────────────────── Service: iam
 └──────────────────────────── arn

arn:aws:eks:us-east-1:123456789012:cluster/my-cluster
                 │         │                └─ Cluster name
                 │         └─────────────────── Account ID
                 └───────────────────────────── Region
```

The ARN is how AWS uniquely identifies every single resource across the entire AWS ecosystem. When you write a policy saying "allow access to this S3 bucket", you use the ARN to specify exactly which bucket. Wildcards in ARNs work like glob patterns — `arn:aws:s3:::my-bucket/*` means all objects inside `my-bucket`.

---

## Types of IAM Policies — This Is Where Most People Get Confused

There are several types of policies and they interact in ways that trip up even experienced engineers.

```
┌─────────────────────────────────────────────────────────────────┐
│                    POLICY TYPES                                  │
│                                                                  │
│  ┌─────────────────────┐    ┌─────────────────────────────────┐ │
│  │  IDENTITY-BASED     │    │  RESOURCE-BASED                 │ │
│  │  POLICIES           │    │  POLICIES                       │ │
│  │                     │    │                                 │ │
│  │  Attached TO a      │    │  Attached TO a resource         │ │
│  │  User, Role, Group  │    │  (S3 bucket, SQS queue,         │ │
│  │                     │    │   KMS key, Lambda...)           │ │
│  │  "What can THIS     │    │                                 │ │
│  │   identity do?"     │    │  "Who can access THIS           │ │
│  │                     │    │   resource?"                    │ │
│  └─────────────────────┘    └─────────────────────────────────┘ │
│                                                                  │
│  ┌─────────────────────┐    ┌─────────────────────────────────┐ │
│  │  AWS MANAGED        │    │  PERMISSIONS BOUNDARIES         │ │
│  │  POLICIES           │    │                                 │ │
│  │                     │    │  A guardrail — sets the         │ │
│  │  Pre-built by AWS.  │    │  MAXIMUM permissions an         │ │
│  │  E.g. ReadOnlyAccess│    │  identity can ever have,        │ │
│  │  AmazonS3FullAccess │    │  even if other policies         │ │
│  │                     │    │  grant more.                    │ │
│  │  Convenient but     │    │                                 │ │
│  │  often too broad    │    │  Used for delegated admin.      │ │
│  └─────────────────────┘    └─────────────────────────────────┘ │
│                                                                  │
│  ┌─────────────────────┐    ┌─────────────────────────────────┐ │
│  │  CUSTOMER MANAGED   │    │  SCPs — SERVICE CONTROL         │ │
│  │  POLICIES           │    │  POLICIES                       │ │
│  │                     │    │                                 │ │
│  │  Policies YOU write │    │  AWS Organizations level.       │ │
│  │  and manage.        │    │  Apply to entire accounts or    │ │
│  │  Reusable across    │    │  OUs. Even root cannot          │ │
│  │  multiple roles.    │    │  override these.                │ │
│  └─────────────────────┘    └─────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
```

### Identity-Based vs Resource-Based — The Cross-Account Key

This distinction is critical and comes up in senior interviews constantly.

**Identity-based policy** answers: "What is this identity allowed to do?"
**Resource-based policy** answers: "Who is allowed to touch this resource?"

For **same-account access**, you only need one of the two. Either give the role permission via an identity-based policy, or give the resource a resource-based policy — either works.

For **cross-account access**, you need BOTH. The role in Account A needs an identity-based policy saying "I'm allowed to access this resource in Account B." And the resource in Account B needs a resource-based policy saying "I trust Account A's role." Both doors need to be unlocked.

---

## How IAM Evaluation Works — The Decision Logic

This is one of the most tested concepts in senior AWS interviews. When an API call comes in, AWS evaluates all applicable policies in this exact order:

```
API Call Arrives
       │
       ▼
┌─────────────────────────────────────┐
│  1. Is there an explicit DENY       │
│     in any SCP (Org level)?         │──── YES ──▶ DENY (game over)
└─────────────────────────────────────┘
       │ NO
       ▼
┌─────────────────────────────────────┐
│  2. Is there an explicit DENY       │
│     in any Resource-Based Policy?  │──── YES ──▶ DENY
└─────────────────────────────────────┘
       │ NO
       ▼
┌─────────────────────────────────────┐
│  3. Is there an explicit DENY       │
│     in any Identity-Based Policy?  │──── YES ──▶ DENY
└─────────────────────────────────────┘
       │ NO
       ▼
┌─────────────────────────────────────┐
│  4. Is there an explicit ALLOW      │
│     in a Resource-Based Policy?    │──── YES ──▶ ALLOW
└─────────────────────────────────────┘
       │ NO
       ▼
┌─────────────────────────────────────┐
│  5. Is there an explicit ALLOW      │
│     in an Identity-Based Policy    │──── YES ──▶ ALLOW
│     AND within Permissions         │
│     Boundary (if set)?             │
└─────────────────────────────────────┘
       │ NO
       ▼
     DENY
  (implicit deny —
  the default)
```

The key rule to memorize: **Explicit DENY always wins. Everything is implicitly denied by default. You need an explicit ALLOW to do anything.**

---

## IAM Roles in Depth — Trust Policies

Every IAM Role has two separate policy documents that work together. Most people only think about one of them.

**The Trust Policy** (also called the assume-role policy) defines **who is allowed to assume this role**. This is the "who can pick up this contractor badge" document.

**The Permission Policy** defines **what this role is allowed to do** once assumed. This is the "what rooms can this badge open" document.

Both must be correct. A Jenkins pipeline can have every permission in AWS granted to it, but if the trust policy doesn't say "I trust Jenkins to assume me," it can't assume the role at all.

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "ec2.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
```

This trust policy says: "The EC2 service is allowed to assume this role." This is what you put on an Instance Profile so EC2 nodes can call AWS APIs.

For a cross-account scenario:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "AWS": "arn:aws:iam::JENKINS-ACCOUNT-ID:role/jenkins-pipeline-role"
      },
      "Action": "sts:AssumeRole",
      "Condition": {
        "StringEquals": {
          "sts:ExternalId": "unique-external-id-for-this-relationship"
        }
      }
    }
  ]
}
```

The `ExternalId` condition is a security best practice for cross-account role assumptions. It prevents the **confused deputy problem** — where a malicious third party tricks your account into assuming a role by pretending to be a legitimate requester.

---

## IRSA — IAM Roles for Service Accounts (Your EKS Connection)

This is where IAM connects directly to your Kubernetes knowledge, and this is one of the most important IAM concepts for EKS-focused roles.

**The Problem:** Your EKS pods need to call AWS APIs — reading from S3, writing to DynamoDB, publishing to SQS. How do you give them credentials securely? You cannot put an IAM User's access keys in a Kubernetes Secret — that's a static credential sitting in etcd, visible to anyone with cluster access, never rotating.

**The Old Bad Way (Node-Level IAM Role):** Attach an IAM role to the EC2 worker node. Every pod on that node inherits those permissions. A compromised pod gets the node's role. A noisy neighbor pod can make API calls with another team's permissions. This violates least privilege completely.

**The IRSA Way:** Each Kubernetes Service Account gets its own IAM Role. The pod uses its Kubernetes service account token to exchange for temporary AWS credentials via AWS STS. Each pod gets exactly the permissions it needs and nothing more. This is **workload-level identity** for AWS.

```
┌─────────────────────────────────────────────────────────────┐
│                    EKS CLUSTER                               │
│                                                              │
│  ┌──────────────────────────────────────────┐               │
│  │  Pod                                     │               │
│  │  ┌──────────────────────────────────┐    │               │
│  │  │  ServiceAccount: s3-reader-sa    │    │               │
│  │  │  annotation:                     │    │               │
│  │  │   eks.amazonaws.com/role-arn:    │    │               │
│  │  │   arn:aws:iam::123:role/s3-reader│    │               │
│  │  └──────────────────────────────────┘    │               │
│  │          │                               │               │
│  │          │ K8s OIDC token                │               │
│  └──────────┼───────────────────────────────┘               │
└─────────────┼───────────────────────────────────────────────┘
              │
              ▼
   ┌─────────────────────┐
   │  AWS STS            │
   │  AssumeRoleWith     │  "Here's my K8s OIDC token,
   │  WebIdentity        │   give me AWS credentials
   └──────────┬──────────┘   for this role"
              │
              │ Validates token against
              │ EKS OIDC Provider
              ▼
   ┌─────────────────────┐
   │  Temporary AWS      │
   │  Credentials        │  AccessKey + SecretKey
   │  (expire in 1hr)    │  + SessionToken
   └──────────┬──────────┘
              │
              ▼
   ┌─────────────────────┐
   │  AWS S3             │
   │  (with only the     │
   │   permissions the   │
   │   role has)         │
   └─────────────────────┘
```

### Setting Up IRSA — Real Production Steps

**Step 1: Create the OIDC Provider for your EKS cluster**

```bash
# Get your cluster's OIDC issuer URL
aws eks describe-cluster \
  --name my-cluster \
  --query "cluster.identity.oidc.issuer" \
  --output text

# Output: https://oidc.eks.us-east-1.amazonaws.com/id/EXAMPLED539D4633E53DE1B716D3041E

# Create the OIDC provider in IAM
eksctl utils associate-iam-oidc-provider \
  --cluster my-cluster \
  --approve

# Verify it was created
aws iam list-open-id-connect-providers
```

**Step 2: Create the IAM Role with a trust policy that references the OIDC provider**

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Federated": "arn:aws:iam::123456789012:oidc-provider/oidc.eks.us-east-1.amazonaws.com/id/EXAMPLED539D4633E53DE1B716D3041E"
      },
      "Action": "sts:AssumeRoleWithWebIdentity",
      "Condition": {
        "StringEquals": {
          "oidc.eks.us-east-1.amazonaws.com/id/EXAMPLED539D4633E53DE1B716D3041E:sub": "system:serviceaccount:production:s3-reader-sa",
          "oidc.eks.us-east-1.amazonaws.com/id/EXAMPLED539D4633E53DE1B716D3041E:aud": "sts.amazonaws.com"
        }
      }
    }
  ]
}
```

The `sub` condition is critical — it pins this role to a **specific namespace and service account name**. `system:serviceaccount:production:s3-reader-sa` means only the service account named `s3-reader-sa` in the `production` namespace can assume this role. No other pod can use it.

```bash
# Create the role
aws iam create-role \
  --role-name eks-s3-reader-role \
  --assume-role-policy-document file://trust-policy.json

# Attach the permission policy
aws iam attach-role-policy \
  --role-name eks-s3-reader-role \
  --policy-arn arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess
```

**Step 3: Create the Kubernetes Service Account with the annotation**

```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: s3-reader-sa
  namespace: production
  annotations:
    eks.amazonaws.com/role-arn: arn:aws:iam::123456789012:role/eks-s3-reader-role
```

**Step 4: Reference the service account in your pod/deployment**

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-app
  namespace: production
spec:
  template:
    spec:
      serviceAccountName: s3-reader-sa   # <── This is all you need
      containers:
        - name: app
          image: my-app:latest
          # AWS SDK inside the container automatically picks up
          # the injected credentials — no hardcoded keys anywhere
```

When the pod starts, the EKS pod identity webhook automatically mounts two things into the container:
- A projected service account token at `/var/run/secrets/eks.amazonaws.com/serviceaccount/token`
- Two environment variables: `AWS_WEB_IDENTITY_TOKEN_FILE` and `AWS_ROLE_ARN`

The AWS SDK reads these automatically and handles the STS token exchange transparently. Your application code just calls `boto3.client('s3')` or `new AWS.S3()` and it works — no credentials to manage.

---

## The aws-auth ConfigMap — The Other IAM/EKS Bridge

While IRSA handles pod-level AWS access, the `aws-auth` ConfigMap handles the opposite direction: **who can access the Kubernetes API** (kubectl commands) using their AWS identity.

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: aws-auth
  namespace: kube-system
data:
  mapRoles: |
    - rolearn: arn:aws:iam::123456789012:role/eks-node-group-role
      username: system:node:{{EC2PrivateDNSName}}
      groups:
        - system:bootstrappers
        - system:nodes
    - rolearn: arn:aws:iam::123456789012:role/developer-role
      username: developer
      groups:
        - eks-developers-group
  mapUsers: |
    - userarn: arn:aws:iam::123456789012:user/alice
      username: alice
      groups:
        - system:masters
```

This ConfigMap maps AWS IAM identities to Kubernetes RBAC users and groups. The node group role mapping is created automatically by EKS so nodes can join the cluster. The developer role mapping is what lets your engineers run `kubectl` commands using their AWS credentials.

**This is a critical failure point.** If you add a new node group with a different IAM role and forget to add it to `aws-auth`, your nodes will be stuck in `NotReady` state and you'll see `Unauthorized` errors in the kubelet logs.

---

## Common IAM CLI Commands You'll Use Daily

```bash
# Get the current identity (who am I right now?)
aws sts get-caller-identity

# Output:
# {
#   "UserId": "AROA...",
#   "Account": "123456789012",
#   "Arn": "arn:aws:iam::123456789012:assumed-role/developer-role/session-name"
# }

# List all roles
aws iam list-roles --query 'Roles[*].[RoleName,Arn]' --output table

# Get a role's trust policy
aws iam get-role --role-name my-role \
  --query 'Role.AssumeRolePolicyDocument'

# List policies attached to a role
aws iam list-attached-role-policies --role-name my-role

# Simulate what a role can do (policy simulator via CLI)
aws iam simulate-principal-policy \
  --policy-source-arn arn:aws:iam::123456789012:role/my-role \
  --action-names s3:GetObject \
  --resource-arns arn:aws:s3:::my-bucket/*

# Assume a role manually (for testing/debugging)
aws sts assume-role \
  --role-arn arn:aws:iam::123456789012:role/target-role \
  --role-session-name debug-session

# Create an IAM role from a trust policy file
aws iam create-role \
  --role-name my-new-role \
  --assume-role-policy-document file://trust-policy.json

# Create and attach an inline policy to a role
aws iam put-role-policy \
  --role-name my-new-role \
  --policy-name my-inline-policy \
  --policy-document file://permissions.json
```

---

## Console Walkthrough — Key IAM Actions in the AWS Console

For interviews and day-to-day work, here's how to navigate IAM in the console:

**To create a Role:**
`IAM → Roles → Create Role → Select trusted entity type` (AWS Service / AWS Account / Web Identity / SAML) `→ Select service (e.g. EC2) → Attach permission policies → Name the role → Create`

**To view what a role can do:**
`IAM → Roles → [click role name] → Permissions tab` shows all attached policies. `Trust relationships tab` shows the trust policy. `Access Advisor tab` (this is gold) shows the last time each service was actually used — critical for least-privilege cleanup.

**To debug an access denied:**
`IAM → Policy Simulator` (in the left nav under "Tools") → Select a role → Select service and action → Simulate. It tells you exactly which policy allowed or denied the action.

**To view IAM activity and last used:**
`IAM → Users/Roles → [entity] → Last activity column` shows when credentials were last used. If an IAM User hasn't been used in 90 days, it should be disabled or deleted.

---

## Common Failure Scenarios and How to Debug Them

### Scenario 1: `AccessDenied` — The Most Common Error in AWS

```
An error occurred (AccessDenied) when calling the GetObject 
operation: User: arn:aws:sts::123456789012:assumed-role/
my-pod-role/session is not authorized to perform: 
s3:GetObject on resource: arn:aws:s3:::my-bucket/path/to/file
```

**How to debug:**

First, read the error message carefully. AWS usually tells you exactly which identity is failing (`assumed-role/my-pod-role`) and exactly what action is failing (`s3:GetObject`) and on what resource.

```bash
# Step 1: Check if the role even exists and has the policy you think it has
aws iam list-attached-role-policies --role-name my-pod-role
aws iam list-role-policies --role-name my-pod-role  # inline policies

# Step 2: Check the actual policy document
aws iam get-role-policy --role-name my-pod-role --policy-name my-policy

# Step 3: Use the policy simulator
aws iam simulate-principal-policy \
  --policy-source-arn arn:aws:iam::123456789012:role/my-pod-role \
  --action-names s3:GetObject \
  --resource-arns arn:aws:s3:::my-bucket/path/to/file

# Step 4: Check if the S3 bucket has a bucket policy denying access
aws s3api get-bucket-policy --bucket my-bucket

# Step 5: Check if there's an SCP at the org level blocking this
# (you need org admin access for this)
aws organizations list-policies-for-target \
  --target-id YOUR-ACCOUNT-ID \
  --filter SERVICE_CONTROL_POLICY
```

The most common causes in order: wrong resource ARN in the policy (forgot the `/*` for bucket objects), resource-based policy is denying, SCP is blocking at org level, or the role simply doesn't have the policy attached.

### Scenario 2: IRSA Not Working — Pod Gets `NoCredentialProviders`

Your pod is trying to call AWS but says it can't find credentials.

```bash
# Step 1: Check if the pod has the right environment variables
kubectl exec -it my-pod -n production -- env | grep AWS
# Should show:
# AWS_ROLE_ARN=arn:aws:iam::123:role/my-role
# AWS_WEB_IDENTITY_TOKEN_FILE=/var/run/secrets/...

# Step 2: Check if the service account has the annotation
kubectl describe sa s3-reader-sa -n production
# Look for: eks.amazonaws.com/role-arn annotation

# Step 3: Check if the OIDC provider exists
aws iam list-open-id-connect-providers

# Step 4: Verify the trust policy condition matches exactly
# The namespace and service account name in the condition must match
# what exists in your cluster
aws iam get-role --role-name my-role \
  --query 'Role.AssumeRolePolicyDocument'

# Step 5: Test the token exchange manually from inside the pod
kubectl exec -it my-pod -n production -- \
  aws sts assume-role-with-web-identity \
  --role-arn $AWS_ROLE_ARN \
  --role-session-name test \
  --web-identity-token $(cat $AWS_WEB_IDENTITY_TOKEN_FILE)
```

The most common cause is a mismatch between the namespace/service account name in the IAM trust policy condition and what actually exists in the cluster. Typos in the `sub` condition are incredibly common.

### Scenario 3: New EKS Nodes Not Joining the Cluster

Symptoms: Node group is healthy in the EKS console, but `kubectl get nodes` shows nothing new, and the autoscaler or manual scaling doesn't bring nodes to Ready.

```bash
# Check the aws-auth configmap
kubectl describe configmap aws-auth -n kube-system

# Check if the new node group's IAM role ARN is in mapRoles
# If it's NOT there, nodes can't authenticate to the API server

# Fix: Add the new role to aws-auth
kubectl edit configmap aws-auth -n kube-system
# Add under mapRoles:
# - rolearn: arn:aws:iam::123:role/new-node-group-role
#   username: system:node:{{EC2PrivateDNSName}}
#   groups:
#     - system:bootstrappers
#     - system:nodes

# For managed node groups, eksctl can do this automatically:
eksctl create nodegroup --cluster my-cluster --managed
# eksctl automatically updates aws-auth for managed node groups
```

---

## Least Privilege in Practice — How Senior Engineers Actually Write Policies

In an interview, when they ask "how do you implement least privilege," this is the answer they want:

You start permissive and use the **IAM Access Analyzer** and the **Access Advisor** tab to tighten over time. Here's a real production approach:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "AllowSpecificBucketListAndRead",
      "Effect": "Allow",
      "Action": [
        "s3:ListBucket",
        "s3:GetObject"
      ],
      "Resource": [
        "arn:aws:s3:::my-app-artifacts-prod",
        "arn:aws:s3:::my-app-artifacts-prod/releases/*"
      ],
      "Condition": {
        "StringEquals": {
          "aws:RequestedRegion": "us-east-1"
        },
        "Bool": {
          "aws:SecureTransport": "true"
        }
      }
    },
    {
      "Sid": "DenyNonTLSRequests",
      "Effect": "Deny",
      "Action": "s3:*",
      "Resource": [
        "arn:aws:s3:::my-app-artifacts-prod",
        "arn:aws:s3:::my-app-artifacts-prod/*"
      ],
      "Condition": {
        "Bool": {
          "aws:SecureTransport": "false"
        }
      }
    }
  ]
}
```

Notice the specifics: exact bucket name (not `*`), exact path prefix (not `/*` on the whole bucket), region-locked, TLS required, explicit TLS deny as a belt-and-suspenders. This is what a production policy looks like.

---

## Terraform — Managing IAM as Code

Since you'll be managing IAM in production via IaC:

```hcl
# Create an IAM role for an EKS pod (IRSA pattern)
data "aws_iam_policy_document" "irsa_trust" {
  statement {
    effect  = "Allow"
    actions = ["sts:AssumeRoleWithWebIdentity"]

    principals {
      type        = "Federated"
      identifiers = [aws_iam_openid_connect_provider.eks.arn]
    }

    condition {
      test     = "StringEquals"
      variable = "${replace(aws_iam_openid_connect_provider.eks.url, "https://", "")}:sub"
      values   = ["system:serviceaccount:production:s3-reader-sa"]
    }

    condition {
      test     = "StringEquals"
      variable = "${replace(aws_iam_openid_connect_provider.eks.url, "https://", "")}:aud"
      values   = ["sts.amazonaws.com"]
    }
  }
}

resource "aws_iam_role" "s3_reader" {
  name               = "eks-s3-reader-role"
  assume_role_policy = data.aws_iam_policy_document.irsa_trust.json

  tags = {
    Environment = "production"
    ManagedBy   = "terraform"
    Team        = "platform"
  }
}

resource "aws_iam_role_policy_attachment" "s3_reader" {
  role       = aws_iam_role.s3_reader.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess"
}
```

---

## How This Connects to the Rest of Your Learning Path

IAM touches every single topic that comes after this. Here's specifically what you're building toward:

**VPC (Topic 2):** VPC endpoints use resource-based policies to control which IAM identities can use them. Your private S3 access from EKS pods flows through both VPC endpoints and IAM.

**EKS AWS Layer (Topic 4):** IRSA, aws-auth, node instance profiles — all pure IAM. This topic gave you the foundation for all of it.

**ECR (Topic 5):** ECR has resource-based policies controlling which accounts and roles can pull images. Your GitHub Actions pipeline needs an IAM role to push, your EKS nodes need permissions to pull.

**Secrets Manager (Topic 10):** The External Secrets Operator uses IRSA to assume a role that can read secrets. Without this topic, that pattern wouldn't make sense.

**Security (Topic 13):** CloudTrail logs every IAM API call. IAM Access Analyzer identifies overly permissive policies. KMS key policies are resource-based IAM policies.

---

## Interview Cheat Sheet

| Question | Crisp Answer |
|----------|-------------|
| What is the difference between an IAM User and an IAM Role? | A User is a permanent identity with long-lived credentials. A Role is a temporary identity assumed by anyone or anything that the trust policy permits — credentials expire automatically. |
| What is the default permission in AWS when no policy exists? | Implicit deny — everything is denied by default unless explicitly allowed. |
| What always wins — an Allow or a Deny? | An explicit Deny always overrides any Allow, from any policy source. |
| What is IRSA and why does it matter? | IRSA lets Kubernetes pods assume IAM Roles using OIDC token exchange via STS, giving pod-level AWS permissions without node-level credentials or static keys. |
| What are the two policies every IAM Role has? | A Trust Policy (who can assume the role) and a Permission Policy (what the role can do once assumed). |
| What is the difference between identity-based and resource-based policies? | Identity-based is attached to a principal (user/role). Resource-based is attached to a resource (S3/SQS/KMS) and defines who can access that resource. |
| How do you grant cross-account access in AWS? | You need both: an identity-based policy on the assuming role allowing it to call STS, AND a resource-based trust policy on the target role (or resource) trusting the source account. |
| What is an SCP and how does it differ from an IAM policy? | SCPs are AWS Organizations guardrails that set the maximum permissions for an entire account. They don't grant permissions — they only restrict them. Even account root cannot bypass an SCP. |
| How do EKS nodes authenticate to the Kubernetes API server? | Via the `aws-auth` ConfigMap which maps the node group's IAM role to the `system:nodes` RBAC group in Kubernetes. |
| How would you debug an AccessDenied error? | Read the error ARN, use IAM Policy Simulator, check identity-based and resource-based policies, check for explicit denies in SCPs and bucket policies, verify the resource ARN in the policy is correct. |
| What is a Permissions Boundary? | A guardrail IAM policy that sets the maximum permissions a role or user can ever have — even if their attached policies grant more. Used in delegated administration. |
| What is the confused deputy problem? | A third-party service tricks your account into performing actions using your account's role. Mitigated with the `sts:ExternalId` condition in cross-account trust policies. |
| What is the IAM Access Advisor? | A feature in the IAM console showing the last time each service was accessed by a role or user — used to identify and remove unused permissions (least privilege enforcement). |
| How does a Jenkins pipeline authenticate to AWS? | In production, the Jenkins EC2 instance has an IAM Instance Profile attached. The pipeline assumes a specific deployment role from that instance profile using STS. No static credentials. |
