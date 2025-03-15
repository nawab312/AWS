**AWS NAT Gateway (Network Address Translation Gateway)** is a service in AWS that allows instances in a private subnet within a Virtual Private Cloud (VPC) to access the internet, without directly exposing them to the internet

![image](https://github.com/user-attachments/assets/6f4b16e7-73d7-45eb-87e0-e3c6c75e4e44)

### How it Works: ###
- **Private Subnet Instances:** These instances do not have public IP addresses, so they cannot communicate directly with the internet.
- **NAT Gateway:** A NAT Gateway is used to allow outbound traffic from instances in a private subnet to the internet but does not allow inbound traffic from the internet to those instances. This means that instances in private subnets can initiate connections to the internet (e.g., for downloading software updates or accessing external APIs), but they cannot accept incoming traffic directly from the internet.
- **Routing:** The routing table for the private subnet is configured to route internet-bound traffic to the NAT Gateway, which then forwards this traffic to the internet. The NAT Gateway will return the responses to the originating instance.
  ![image](https://github.com/user-attachments/assets/19a1f7bd-c2f3-4947-bf96-86ed6fff139d)

