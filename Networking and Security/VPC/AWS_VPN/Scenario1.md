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
