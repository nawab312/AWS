- **Virtual Private Cloud (VPC)** is a logically isolated virtual network that you define in the AWS Cloud. It enables you to launch AWS resources in a virtual network that you specify, with complete control over the network configuration,
including IP address range, subnets, route tables, and network gateways.
  - Max VPC per Account Per Region = 5

### VPC Components ###
- **VPC CIDR (Classless Inter-Domain Routing)** is a block of IP addresses that defines the address space of your VPC.
- If you run out of IP Address in a Subnet we can not resize by adjusting *CIDR of Subnet*
![image](https://github.com/user-attachments/assets/733f53a3-0adf-4d04-965e-076e0caa9aaa) ![image](https://github.com/user-attachments/assets/890edc95-76f3-440d-8165-8785e19d1ff1)

- **Subnets** are segments of your VPC's IP address range. You can create multiple subnets in different Availability Zones (AZs) for high availability and fault tolerance
  - Public Subnet: Accessible from the internet (using an Internet Gateway).
  - Private Subnet: Not directly accessible from the internet. Typically used for internal resources (e.g., databases, application servers). Often uses a NAT gateway to enable
internet access for instances.

  ![image](https://github.com/user-attachments/assets/8af79818-2828-4380-a1d6-9a945da91939)


- **Internet Gateway** An Internet Gateway allows communication between instances in your VPC and the internet. It's attached to your VPC and enables instances in public subnets to access the internet (and vice versa). Only one per VPC
  - You need to configure the route tables to enable internet traffic. For example, the route table of the subnet must contain a route to the Internet Gateway *(0.0.0.0/0 to the Internet Gateway)*.
    ![image](https://github.com/user-attachments/assets/5d67a2d9-e286-469e-86ce-fa0841b5734d)

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
    - https://github.com/nawab312/AWS/blob/main/Networking%20and%20Security/VPC/NACL.md
  
- **NAT Gateway / NAT Instance**
  - NAT Gateway (managed AWS service) and NAT Instance (self-managed EC2 instance) allow outbound internet access from private subnets.
  - NAT Gateway https://github.com/nawab312/AWS/blob/main/Networking%20and%20Security/VPC/NATGateway.md

- **VPC Peering** 
  - Direct connection between two VPCs for private communication.
  - https://github.com/nawab312/AWS/blob/main/Networking%20and%20Security/VPC/VPCPeering.md

- **AWS Transit Gateway** 
  - Centralized hub for connecting multiple VPCs and on-premises networks.
  - https://github.com/nawab312/AWS/blob/main/Networking%20and%20Security/VPC/TransitGateway.md

- **VPN and Direct Connect**
  - VPN (Virtual Private Network): Secure connection between on-premises and AWS over the internet. https://github.com/nawab312/AWS/blob/main/Networking%20and%20Security/VPC/AWS_VPN.md
  - AWS Direct Connect: Dedicated private network link from on-premises to AWS. https://github.com/nawab312/AWS/blob/main/Networking%20and%20Security/VPC/DirectConnect.md

- **Endpoint Services**
  - *VPC Gateway Endpoints:* For S3 and DynamoDB access without internet.
  - *VPC Interface Endpoints:* For private access to AWS services like SNS, SQS, etc.
  - https://github.com/nawab312/AWS/blob/main/Networking%20and%20Security/VPC/VPCEndpoint.md
 
- **DNS Settings**
 - *Enable DNS Resolution*
   - This setting is enabled, meaning EC2 instances inside this VPC can use AWS's internal DNS resolver (`169.254.169.253`).
   - With this option enabled, instances in private and public subnets can resolve domain names like:
     - AWS internal resources: `ip-10-0-0-12.ec2.internal`
     - Public domains: `google.com`, `s3.amazonaws.com` (if a NAT gateway or internet access is configured).
 - *Enable DNS Hostnames*
   - Since this is disabled, EC2 instances launched in this VPC won’t get a public DNS name, even if they have a public IP.
   - This means:
     - Private instances will not have a hostname like `ip-10-0-0-12.ec2.internal`.
     - Public instances will not get an AWS public DNS like `ec2-52-14-22-11.compute-1.amazonaws.com`.

