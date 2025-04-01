**Basic VPC Peering Setup**

You have two VPCs, VPC-A and VPC-B, in the same AWS region. You need to enable communication between resources in these two VPCs. How would you set up VPC peering,

![image](https://github.com/user-attachments/assets/5d2bcea6-43b8-4e6e-9904-a75a04594906)

**Create VPC Peering Connection**
- Initiate Peering from VPC-A

![image](https://github.com/user-attachments/assets/b4de1e9f-7531-4929-921e-4cc029e726d9)

- Accept Peering from VPC-B

![image](https://github.com/user-attachments/assets/14b8c263-31eb-4d6c-b3de-e9e776765848)

**Update Route Tables**
- Update Route Table in VPC-A
  - Select the route table associated with `VPC-A`.
  - Click on Edit Routes.
  - Add a new route:
  
  ![image](https://github.com/user-attachments/assets/f01d1f62-4e56-431d-859c-f745e2f207a9)

- Update Route Table in VPC-B

**Update Security Groups and Network ACLs**

You need to ensure that the security groups and network ACLs allow traffic between the two VPCs.
- Update Security Groups in VPC-A
  - Go to Security Groups in the VPC dashboard.
  - Select the *Security Group* associated with your resources in `VPC-A`.
  - Click on *Inbound Rules* and *Edit*. Add a new rule to allow inbound traffic from `VPC-B`:
    - Type: Custom TCP (or ICMP if testing pings).
    - Protocol: TCP (or ICMP).
    - Port Range: Specific ports (e.g., `80` or `22`).
    - Source: `10.1.0.0/16` (CIDR block of `VPC-B`).
- Update Security Groups in VPC-b
