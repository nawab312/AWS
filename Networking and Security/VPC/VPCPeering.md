AWS VPC Peering is a networking connection between two Virtual Private Clouds (VPCs) that enables them to route traffic between each other using *private IP addresses*. This allows instances in one VPC to communicate with instances in another VPC as if they were within the same network. VPC peering can be set up between VPCs in the same AWS account or across different AWS accounts.
- **Private Communication:** VPC peering allows private IP communication between the peered VPCs without using the public internet.
- **Same or Different Regions:** VPC peering can be established between VPCs in the same region (intra-region) or across different regions (inter-region).
- **Non-Transitive:** VPC peering is non-transitive, meaning that if VPC-A is peered with VPC-B and VPC-B is peered with VPC-C, VPC-A cannot communicate with VPC-C unless there's a direct peering between VPC-A and VPC-C.
- **Traffic Routing:** You need to update the route tables of both VPCs to allow traffic to flow between them. Once set up, instances in both VPCs can communicate as if they were in the same network.
- **Security:** VPC peering *does not automatically change the security settings*. For example, security groups and network ACLs still apply, and you may need to modify them to allow traffic between VPCs.
- *A peering connection cannot be created between 2 VPCs that have overlapping CIDRs.*

![image](https://github.com/user-attachments/assets/ee498cf3-6d59-487f-9c69-af73c5aec650)

**Basic VPC Peering Setup**
- You have two VPCs, VPC-A and VPC-B, in the same AWS region. You need to enable communication between resources in these two VPCs. How would you set up VPC peering?
