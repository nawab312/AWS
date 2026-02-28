**Route Table** in a Virtual Private Cloud (VPC) is a set of rules, or routes, used to determine where network traffic is directed within a VPC. Each route table contains a set of destination IP addresses and the target (the next hop) that will handle the traffic destined for those addresses. Route tables are essential in a VPC because they dictate how traffic flows within the VPC and between the VPC and external networks, such as the internet or on-premises networks.
Components of Route Table:
- **Destination:** The destination is a range of IP addresses that the route will apply to. This can be a specific IP address (like `10.0.0.0/16` or `192.168.1.0/24`), or a more general address (like `0.0.0.0/0` for all addresses).
- **Target:** The target is where the traffic is sent when it matches a specific destination. The target can be:
  - Internet Gateway (IGW): Routes traffic to the internet.
  - Virtual Private Gateway (VGW): Routes traffic to a VPN connection.
  - Network Interface (ENI): Routes traffic to an Elastic Network Interface (a specific EC2 instance).
  - VPC Peering Connection: Routes traffic between VPCs.
  - NAT Gateway: Allows instances in a private subnet to access the internet.
  - Local: Indicates the route within the VPC for communication between subnets.
- **Route Propagation:** 
  - Route propagation is when a gateway (like a VPN or Direct Connect) automatically adds routes to your VPC route table. Instead of manually creating routes, AWS updates the route table based on routes learned dynamically.
  - Why is it needed?: It is needed in hybrid setups where on-prem networks can have multiple or changing CIDR blocks. Route propagation keeps the route table updated automatically, reducing manual work and preventing routing mistakes when networks change.
  - Private subnet route table → Enable propagation
    - Private subnets usually need to talk to on-prem networks (databases, legacy systems, internal APIs). So enabling route propagation allows dynamically learned on-prem routes to be added automatically
  - Public subnet route table → Do not enable propagation
    - Public subnets are meant to send internet traffic to an Internet Gateway. If you enable propagation there, a dynamically advertised route (like `0.0.0.0/0`) from on-prem could override the internet route and redirect all traffic to the VPN.

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
