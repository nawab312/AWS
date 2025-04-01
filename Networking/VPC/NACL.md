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
