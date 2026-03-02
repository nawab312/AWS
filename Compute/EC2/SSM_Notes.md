Amazon SSM (AWS Systems Manager) is a service that lets you manage, automate, and securely access your EC2 and on-premises servers without needing SSH or bastion hosts. It provides features like remote command execution, patching, configuration management, and secure session access using IAM controls.

**How It Works**

*SSM Agent (On the Instance)*
- A lightweight agent installed on the instance.
- Communicates outbound over HTTPS (port 443). It makes an outbound connection to AWS. That’s why you don’t need inbound ports.

**IAM Role**
- The EC2 instance must have an IAM role attached with: `AmazonSSMManagedInstanceCore` Policy

**SSM Service Endpoint**
- When the SSM agent starts on an EC2 instance, it must:
  - Register the instance with AWS Systems Manager
  - Maintain a secure control channel
  - Poll or receive commands
  - Send back command output
- To do that, it connects over HTTPS (port 443) to these AWS endpoints:
  - `ssm.<region>.amazonaws.com`, `ec2messages.<region>.amazonaws.com`, `ssmmessages.<region>.amazonaws.com`
  - These are public AWS service endpoints unless you override them with VPC endpoints.
- Now Think in Networking Terms. Your instance is in a private subnet. Private subnet means: No direct route to Internet Gateway, No public IP. So how does it reach those endpoints?
  - OPTION 1: NAT Gateway
  - OPTION 2: VPC Interface Endpoints (PrivateLink). You create Interface Endpoints for `com.amazonaws.region.ssm`, `com.amazonaws.region.ec2messages`, `com.amazonaws.region.ssmmessages`

**Why This Is Secure & Useful**
- No Inbound Rules Needed
  - Since the SSM Agent initiates communication, your instances don’t need:
    - Public IP addresses
    - Open SSH ports (port 22)
    - Bastion hosts
- Can Work in Private Subnets
  - Even if your EC2 instance is in a private subnet with no internet access, SSM still works if:
    - You have a NAT Gateway or
    - You use VPC Endpoints for SSM
