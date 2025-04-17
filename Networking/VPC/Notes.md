- **Virtual Private Cloud (VPC)** is a logically isolated virtual network that you define in the AWS Cloud. It enables you to launch AWS resources in a virtual network that you specify, with complete control over the network configuration,
including IP address range, subnets, route tables, and network gateways.
  - Max VPC per Account Per Region = 5

### VPC Components ###
- **VPC CIDR (Classless Inter-Domain Routing)** is a block of IP addresses that defines the address space of your VPC.
- If you run out of IP Address in a Subnet we can not resize by adjusting *CIDR of Subnet*
![image](https://github.com/user-attachments/assets/733f53a3-0adf-4d04-965e-076e0caa9aaa) ![image](https://github.com/user-attachments/assets/890edc95-76f3-440d-8165-8785e19d1ff1)

- **Subnet Masking**
  - Subnet masking is a method used in networking to divide an IP address into two parts: Network portion AND Host portion
  - Every IP address (like 192.168.1.10) comes with a subnet mask (like 255.255.255.0). The subnet mask tells you which part of the IP address refers to the network and which part refers to the host.
  - Example
```bash
IP Address: 192.168.1.10
Subnet Mask: 255.255.255.0	
Binary IP Address: 11000000.10101000.00000001.00001010
Binary Subnet Mask: 11111111.11111111.11111111.00000000
```
  - The first 24 bits (set to 1 in the subnet mask) are the network portion. The last 8 bits are for the hosts in that network.
  - Network Address = `192.168.1.0` Host Address = anything from `192.168.1.1` to `192.168.1.254`

- Example: IP address `192.168.10.50` with a subnet mask of `255.255.255.192`
  - What is the network address?
  - What is the broadcast address?
  - How many valid hosts can be in this subnet?
- Step 1: Convert Subnet Mask to CIDR
  - `255.255.255.192` = `/26` (because 192 in binary is `11000000`
- Step 2: Calculate Subnet Block Size
  - Since this is a `/26`, that leaves 6 bits for hosts (32 total bits - 26 = 6).
  - 2⁶ = 64 addresses per subnet
- Step 3: Identify Subnets in 192.168.10.0/24
  - The subnet increment is 64 (based on the 4th octet).
  - The subnet ranges would be:
    - `192.168.10.0` to `192.168.10.63`
    - `192.168.10.64` to `192.168.10.127` and so on
  - Since the IP address is `192.168.10.50`, it falls into the first subnet.
- Step 4: Final Answers
  - Network Address: `192.168.10.0`
  - Broadcast Address: `192.168.10.63`
  - Valid Host Range: `192.168.10.1` to `192.168.10.62`
 
![image](https://github.com/user-attachments/assets/16381f6f-1d8a-4023-97af-4fbff7b3997f)
    
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


When you SSH from your local machine to your EC2 instance's public IP, this is what happens under the hood:
- Public IP is just a NAT mapping to the private IP (`10.x.x.x`) of your EC2.
- The Elastic Network Interface (ENI) attached to the EC2 only has:
 - A private IP (always)
 - A public IP (optional, and only for external reachability)
- Once the packet enters the VPC, AWS automatically translates the public IP → private IP (via NAT or routing).
- VPC Flow Logs are collected at the ENI level, and ENIs only see private IP traffic inside the VPC.
