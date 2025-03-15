- **Virtual Private Cloud (VPC)** is a logically isolated virtual network that you define in the AWS Cloud. It enables you to launch AWS resources in a virtual network that you specify, with complete control over the network configuration,
including IP address range, subnets, route tables, and network gateways.

### VPC Components ###
- **VPC CIDR (Classless Inter-Domain Routing)** is a block of IP addresses that defines the address space of your VPC.
![image](https://github.com/user-attachments/assets/733f53a3-0adf-4d04-965e-076e0caa9aaa) ![image](https://github.com/user-attachments/assets/890edc95-76f3-440d-8165-8785e19d1ff1)

- **Subnets** are segments of your VPC's IP address range. You can create multiple subnets in different Availability Zones (AZs) for high availability and fault tolerance
  - Public Subnet: Accessible from the internet (using an Internet Gateway).
  - Private Subnet: Not directly accessible from the internet. Typically used for internal resources (e.g., databases, application servers).

- **Internet Gateway** An Internet Gateway allows communication between instances in your VPC and the internet. It's attached to your VPC and enables instances in public subnets to access the internet (and vice versa). Only one per VPC

- **Route Tables** Controls how traffic is directed within the VPC.
  - https://github.com/nawab312/AWS/blob/main/Networking%20and%20Security/VPC/RouteTable.md
 
- **Security Mechanisms**
  - **Security Groups (SGs)**
    - These are like firewalls at the instance level.
    - They control inbound and outbound traffic to your EC2 instances.
    - You can define rules to allow or deny specific traffic based on source/destination IP addresses, ports, and protocols.
  - **Network ACLs (NACLs)**
    - These are like firewalls at the subnet level.
    - They control traffic entering and leaving a subnet. 
    - They are applied before security groups, providing a more granular level of control.
  
- **NAT Gateway / NAT Instance**
  - NAT Gateway (managed AWS service) and NAT Instance (self-managed EC2 instance) allow outbound internet access from private subnets.
  - NAT Gateway https://github.com/nawab312/AWS/blob/main/Networking%20and%20Security/VPC/NATGateway.md

- **Rule Number * (Wildcard Rule):** In this case, the wildcard * (often interpreted as "any") doesn't directly translate to a specific rule number in AWS NACLs. This could refer to the default rule, which is applied if no other rules match the traffic. The wildcard rule (Deny all traffic) is essentially redundant because Rule #100 already allows all traffic.


**VPC Peering** 
- Direct connection between two VPCs for private communication.
- https://github.com/nawab312/AWS/blob/main/Networking%20and%20Security/VPC/VPCPeering.md

**AWS Transit Gateway** 
- Centralized hub for connecting multiple VPCs and on-premises networks.
- https://github.com/nawab312/AWS/blob/main/Networking%20and%20Security/VPC/TransitGateway.md

**VPN and Direct Connect**
- VPN (Virtual Private Network): Secure connection between on-premises and AWS over the internet. https://github.com/nawab312/AWS/blob/main/Networking%20and%20Security/VPC/AWS_VPN.md
- AWS Direct Connect: Dedicated private network link from on-premises to AWS. https://github.com/nawab312/AWS/blob/main/Networking%20and%20Security/VPC/DirectConnect.md

**Endpoint Services**
- *VPC Gateway Endpoints:* For S3 and DynamoDB access without internet.
- *VPC Interface Endpoints:* For private access to AWS services like SNS, SQS, etc.
- https://github.com/nawab312/AWS/blob/main/Networking%20and%20Security/VPC/VPCEndpoint.md
