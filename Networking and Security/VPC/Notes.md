- **Virtual Private Cloud (VPC)** is a logically isolated virtual network that you define in the AWS Cloud. It enables you to launch AWS resources in a virtual network that you specify, with complete control over the network configuration, including IP address range, subnets, route tables, and network gateways.
- **Subnets** are segments of your VPC's IP address range. You can create multiple subnets in different Availability Zones (AZs) for high availability and fault tolerance
  - Public Subnet: Accessible from the internet (using an Internet Gateway).
  - Private Subnet: Not directly accessible from the internet. Typically used for internal resources (e.g., databases, application servers).
- **Internet Gateway** An Internet Gateway allows communication between instances in your VPC and the internet. It's attached to your VPC and enables instances in public subnets to access the internet (and vice versa).

### Route Tables ###
Route Table in a Virtual Private Cloud (VPC) is a set of rules, or routes, used to determine where network traffic is directed within a VPC. Each route table contains a set of destination IP addresses and the target (the next hop) that will handle the traffic destined for those addresses. Route tables are essential in a VPC because they dictate how traffic flows within the VPC and between the VPC and external networks, such as the internet or on-premises networks.
Components of Route Table:
- **Destination:** The destination is a range of IP addresses that the route will apply to. This can be a specific IP address (like `10.0.0.0/16` or `192.168.1.0/24`), or a more general address (like `0.0.0.0/0` for all addresses).
- **Target:** The target is where the traffic is sent when it matches a specific destination. The target can be:
  - Internet Gateway (IGW): Routes traffic to the internet.
  - Virtual Private Gateway (VGW): Routes traffic to a VPN connection.
  - Network Interface (ENI): Routes traffic to an Elastic Network Interface (a specific EC2 instance).
  - VPC Peering Connection: Routes traffic between VPCs.
  - NAT Gateway: Allows instances in a private subnet to access the internet.
  - Local: Indicates the route within the VPC for communication between subnets.
- **Route Propagation:** Route tables can also have route propagation enabled for certain VPN and Direct Connect connections. This means the route table can automatically be updated with routes that are learned from other networks.

**Default Route Table**
When you create a new VPC in AWS, a default route table is automatically created. This default route table includes a route that allows instances in the VPC to communicate with each other using their private IP addresses (via `Local route`). Additionally, it may include a route for internet access if an Internet Gateway (IGW) is attached to the VPC.
- Example:
  - VPC CIDR Block: `10.0.0.0/16`
  - Internet Gateway (IGW) is attached to the VPC.
  - Public Subnet (Subnet A): `10.0.1.0/24`
  - Private Subnet (Subnet B):`10.0.2.0/24`
![image](https://github.com/user-attachments/assets/75467013-6476-428d-827b-46edb9de4152)

**Custom Route Tables**
- You can create custom route tables in your VPC
- For instance, a *public subnet* might have a route to an *Internet Gateway*, while a *private subnet* might route traffic to a *NAT Gateway* to allow instances in the *private subnet* to access the internet but prevent direct incoming internet traffic.
- *You can associate multiple subnets with a single route table, but each subnet can only be associated with one route table at a time.*

### Network Access Control Lists (NACLs) ###
Network Access Control List (NACL) is an optional security layer for controlling network traffic to and from subnets within your AWS VPC. It is a stateless firewall that operates at the subnet level, enabling you to control the flow of traffic based on IP addresses, ports, and protocols.
**How NACLs Work**
- *Subnet-level security:* NACLs control traffic for all resources within the subnet to which the NACL is associated.
- **Stateless:** Means that NACLs do not remember any previous traffic or connections. So, every time a new request or connection comes through, the NACL checks it from scratch, without considering any prior interactions.
- Evaluate rules in numerical order: When a packet enters or exits a subnet, the NACL evaluates the rules in numerical order, starting with the lowest rule number (from 1 upwards). If a rule matches, it is applied and the evaluation stops. If no rule matches, the **default rule (deny)** is applied.
- Rules are assigned a number between `1 and 32766`
- When you create a VPC, AWS automatically assigns a default NACL to all subnets. The default NACL allows all inbound and outbound traffic (allow all rule).

![image](https://github.com/user-attachments/assets/c841600b-72a6-460b-a2eb-583b86bf2cde)

![image](https://github.com/user-attachments/assets/6603cb23-d69a-4120-890c-b6c8d3fc7d1e)

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
