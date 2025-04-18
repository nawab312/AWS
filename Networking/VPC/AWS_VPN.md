A **VPN (Virtual Private Network)** is a *secure tunnel* that protects your data when you connect to the internet or a private network. It *encrypts your data* so that no one can *spy on your online activity* or *steal sensitive information*. Example of VPN Usage
- A company with an office in New York and another in London uses a VPN to securely connect both offices over the internet.
- A remote worker uses a *Client VPN* to access company resources securely while working from home.

AWS Virtual Private Network (AWS VPN) enables secure connectivity between on-premises networks, remote users, and AWS cloud resources. It consists of **AWS Site-to-Site VPN** and **AWS Client VPN**, each serving different use cases.

### AWS Site-to-Site VPN ###

AWS Site-to-Site VPN is used to securely connect an on-premises network to AWS over an *IPSec-encrypted tunnel*. It comprises:
- **Virtual Private Gateway (VGW):** This is the AWS side of the VPN connection, acting as a gateway for the VPC. It allows communication between your VPC and your on-premises network over the VPN tunnel.
- **Customer Gateway (CGW):** his is the on-premises device or software appliance, such as a hardware VPN router or a VPN appliance (e.g., Cisco ASA, pfSense, etc.), that initiates and manages the VPN connection from your side.
- **IPSec Tunnel:** The secure tunnel is established between the Customer Gateway and the Virtual Private Gateway over the internet using IPsec (Internet Protocol Security) to encrypt and secure data.
- **BGP Routing (Optional):** BGP can be used for dynamic routing instead of static routes.

![image](https://github.com/user-attachments/assets/19fd92f8-35e1-445f-9a5c-504632029906)

Integrated with AWS Transit Gateway for multi-VPC connectivity.

![image](https://github.com/user-attachments/assets/c801fdeb-a26a-444d-a5b1-050e1910966a)


**Establishing the VPN Connection**
- *Step 1*: In AWS, you create a *Virtual Private Gateway (VGW)* and associate it with your VPC.
- *Step 2:* You configure the *Customer Gateway (CGW)* on your side, which represents your on-premises VPN device. This includes providing details like the public IP address of the CGW and the type of routing (static or dynamic) for your on-premises network.
- *Step 3:* AWS will automatically create the VPN connection, which will use IPsec to secure the communication between the Virtual Private Gateway and the Customer Gateway.
- *Step 4:* Once the VPN connection is created, you configure your Customer Gateway to connect to the Virtual Private Gateway using the provided tunnel information from AWS (such as tunnel IP addresses, encryption methods, and shared keys).

**Routing**

- **Static Routing:** If you use static routing, you manually define the routes for the on-premises network to reach the VPC and vice versa.
- **Dynamic Routing (BGP):** Alternatively, you can use *Border Gateway Protocol (BGP)* to automatically exchange routes between your on-premises network and AWS VPC. This is more scalable and easier to manage, especially for larger or more complex networks.

**What is BGP**
- BGP (Border Gateway Protocol) is the protocol used to exchange routing information between different networks (Autonomous Systems) on the internet or private enterprise networks.
  - It's a path vector protocol, meaning it chooses the best path based on various attributes (e.g., AS-PATH, MED, LOCAL_PREF).
  - It's primarily used for interconnecting different networks—like between your company network and AWS.
- *Think of BGP as a GPS that selects the best road from your home (on-prem network) to AWS, and it's smart enough to change roads if one is blocked.*

**Redundancy and High Availability**
- AWS Site-to-Site VPN provides high availability through the use of *two VPN tunnels*. AWS automatically provisions two VPN tunnels for each VPN connection, ensuring that if one tunnel goes down, the other can continue to carry traffic. You can configure your on-premises VPN device to monitor both tunnels and automatically failover to the backup tunnel if necessary.

EC2 Instance resides in a Private Subnet within a VPC that connects to the On-Premises Network via a Site-to-Site VPN
- Ensure the Route to On-Premises Exists

  ![image](https://github.com/user-attachments/assets/1cbc4b5e-f7f2-4b92-be70-35063567bf7f)
- Network ACL (NACL) Configuration

  ![image](https://github.com/user-attachments/assets/78145cb2-593e-4f15-adbd-3d92556656ee) ![image](https://github.com/user-attachments/assets/9f98352b-1eb4-4755-908c-a019f831fa60)
- Security Group Settings
  - Ensure your EC2 security group allows outbound traffic to the database port (3306 for MySQL).

### AWS Client VPN ###

AWS Client VPN is a fully managed, elastic VPN service that allows users to securely access AWS resources and on-premises networks from any device, regardless of location. It enables secure remote access for individual users (like employees or contractors) to AWS VPCs (Virtual Private Clouds) and on-premises networks, using a secure VPN connection.
- **OpenVPN-based connectivity**.
- **User authentication** via AWS Directory Service, Active Directory, or mutual authentication with certificates.
- **Authorization rules** to control access.
- **Split Tunneling** to decide which traffic goes through VPN and which goes directly to the internet.

**How AWS Client VPN Works:**
- **Create a Client VPN Endpoint:** It is the entry point into your AWS environment. It’s a managed resource in AWS that provides the VPN connection for users.
  - You create a Client VPN Endpoint in the AWS Management Console, which is associated with an AWS VPC and allows remote clients to connect to it.
  - You also define the Authentication Method (either Active Directory, mutual certificate authentication, or another method) and specify the VPC Subnets you want to access.
- **Configure Authorization and Access Control:**
  - After authentication, AWS Client VPN uses *authorization rules* to control who can access which resources within the VPC or on-premises networks.
  - You define access control policies by associating specific *CIDR blocks* (IP ranges) that a user is authorized to access.
- **Client VPN Configuration:**
  - Users must configure their *VPN client software* (such as OpenVPN or AWS VPN Client) to connect to the AWS Client VPN Endpoint.
  - AWS provides configuration files and certificates (if applicable) that the user will load into their VPN client. This file contains all the necessary details to establish the connection (e.g., the endpoint address, authentication method, etc.).
  - The VPN client software establishes a secure *IPsec tunnel* between the remote user and the Client VPN Endpoint in AWS.
 
**Example Use Case:**
- A company has a global workforce, and employees need secure access to AWS resources (like EC2 instances or RDS databases) and on-premises systems. Using AWS Client VPN, each employee can install the VPN client on their device (laptop, phone, etc.) and securely connect to AWS from anywhere in the world, using their company credentials or certificates for authentication.

![image](https://github.com/user-attachments/assets/8c9dba26-4613-4c46-b4c7-a84259cee8fd)

- https://github.com/nawab312/AWS/blob/main/Networking%20and%20Security/VPC/AWS_VPN/Scenario1.md


**Scenario: Hybrid Cloud with AWS VPC & On-Premises Data Center**

Your company has a hybrid cloud setup where an on-premises data center is connected to an AWS VPC via AWS Site-to-Site VPN.

✅ The on-premises data center can access EC2 instances in the private subnet of AWS.

✅ AWS EC2 instances in the private subnet can communicate with on-prem servers.

❌ However, EC2 instances in the public subnet cannot reach on-premises servers, even though you have updated Security Groups and NACLs correctly.


**Solution**

Missing Route in the Public Subnet's Route Table
- Since VPN traffic does not pass through IGW, the public subnet route table must explicitly route traffic to the on-premises CIDR through the VPN connection.
- Solution: Add the following entry in the public subnet route table:
![image](https://github.com/user-attachments/assets/e7a0f909-4595-4965-8a01-13b4700329ed)

---

Your company uses AWS Direct Connect for low-latency private connectivity between its on-premises data center and a VPC. To ensure high availability, you configure a Site-to-Site VPN as a backup connection over the public internet.

How should you configure your routing to ensure failover to VPN only when Direct Connect is down, and avoid asymmetric routing?

**Answer** *Configure BGP on both Direct Connect and VPN, and use AS path prepending on the VPN to make it less preferred.*
- What is AS Path Prepending?
  - In BGP, shorter AS paths are more preferred. Example: If a route goes through 2 autonomous systems vs. 5, the 2-AS path is preferred.
  - AS path prepending is a trick to artificially lengthen the AS path to make it look less attractive.
- Why use AS Path Prepending on VPN?
  - You want Direct Connect to be used as the primary route because it's faster.
  - So you configure BGP to prepend multiple copies of your AS number in the VPN route advertisements. That way, AWS thinks: “Hmm… this VPN route looks long and inefficient. Let me use the Direct Connect route instead.”
