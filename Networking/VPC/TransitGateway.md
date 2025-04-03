AWS Transit Gateway (TGW) is a highly scalable and flexible service that acts as a hub to connect multiple Virtual Private Clouds (VPCs), on-premises networks, and even other AWS services in a centralized manner.

**Centralized Connectivity:**
- Instead of setting up individual peering connections between VPCs, you can use a **single Transit Gateway** to connect multiple VPCs and on-premises networks. This reduces the complexity of managing a mesh network of VPC peers
- Transit Gateway acts as a router and manages the routing of traffic between VPCs, on-premises networks, and other services. You can easily control the flow of traffic with routing tables for each connection, rather than managing routes on a per-VPC basis. It supports **route propagation** (automatic updates to routing tables)
- It supports a wide range of **attachments**, such as:
  - VPC attachments
  - VPN connections (to connect your on-premises network to AWS)
  - AWS Direct Connect (for high-performance, low-latency connections to your on-premises network)

 ### How AWS Transit Gateway Works: ###
- **Attachments:** You create a Transit Gateway and attach VPCs, VPNs, or Direct Connect connections to it. This acts as a "hub" where all the traffic flows.
- **Routing:** Each attachment has its own routing table. You can configure the routing tables to define how traffic flows between the connected networks. For example, you can define that VPC-A can communicate with VPC-B but not with VPC-C.
- **Use Cases**:
  - **Multi-VPC Architectures:** Connecting multiple VPCs across different regions or accounts in a large organization.
  - **Hybrid Cloud Architectures:** Connecting on-premises networks to multiple VPCs using VPN or Direct Connect.

**How Do VPCs Across Regions Connect Using AWS Transit Gateway?**

AWS Transit Gateway (TGW) is regionally scoped, meaning that by default, it only allows communication between VPCs within the same AWS region. However, AWS provides a feature called Transit Gateway Peering, which allows Transit Gateways in different regions to connect and enable cross-region VPC communication.

*Transit Gateway Peering Connection*

To connect VPCs across regions, you must establish a peering connection between Transit Gateways in different regions. This allows traffic to route between VPCs that are associated with these Transit Gateways. How it Works (Step-by-Step)
- Create Transit Gateways in Each Region
  - `TGW-1` in `us-east-1`
  - `TGW-2` in `eu-west-1`
- Establish a Peering Connection Between TGWs
  - A peering request is sent from `TGW-1` to `TGW-2`
  - The request must be accepted manually in `TGW-2` (unless auto-acceptance is enabled). Once accepted, a peering link is established.
- Update Route Tables in Both Transit Gateways
  - In `TGW-1`, add a route to `TGW-2` for the remote region’s CIDR block.
  - In `TGW-2`, add a route to `TGW-1` for the local region’s CIDR block.
 
*AWS Global Backbone for Peering Traffic*
- AWS does not use the public internet for Transit Gateway Peering.
- Instead, AWS routes the traffic through its private global network, providing:
  - Lower latency compared to VPN-based solutions.
  - Higher security by avoiding exposure to the public internet.

*Considerations & Limitations*
- Peering is Non-Transitive: A VPC connected to TGW-1 cannot automatically communicate with a VPC connected to TGW-2 unless explicitly routed
- Latency: Since traffic flows via AWS’s global backbone, it is lower than internet-based VPNs but still depends on AWS region distances.
- Route Limits: Route Limits	Each Transit Gateway supports a limited number of routes (5,000 by default). Careful planning is needed for large-scale deployments.
- Data Transfer Costs: Cross-region data transfer through Transit Gateway incurs AWS inter-region data transfer charges.


