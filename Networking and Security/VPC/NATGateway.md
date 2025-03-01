**AWS NAT Gateway (Network Address Translation Gateway)** is a service in AWS that allows instances in a private subnet within a Virtual Private Cloud (VPC) to access the internet, without directly exposing them to the internet

![image](https://github.com/user-attachments/assets/6f4b16e7-73d7-45eb-87e0-e3c6c75e4e44)

### How it Works: ###
- **Private Subnet Instances:** These instances do not have public IP addresses, so they cannot communicate directly with the internet.
- **NAT Gateway:** The NAT Gateway resides in a public subnet and has a public IP address. It allows outbound internet traffic for instances in private subnets.
- **Routing:** The routing table for the private subnet is configured to route internet-bound traffic to the NAT Gateway, which then forwards this traffic to the internet. The NAT Gateway will return the responses to the originating instance.
