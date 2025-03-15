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

Establishing the VPN Connection
- *Step 1*: In AWS, you create a *Virtual Private Gateway (VGW)* and associate it with your VPC.
- *Step 2:* You configure the *Customer Gateway (CGW)* on your side, which represents your on-premises VPN device. This includes providing details like the public IP address of the CGW and the type of routing (static or dynamic) for your on-premises network.
- *Step 3:* AWS will automatically create the VPN connection, which will use IPsec to secure the communication between the Virtual Private Gateway and the Customer Gateway.
- *Step 4:* Once the VPN connection is created, you configure your Customer Gateway to connect to the Virtual Private Gateway using the provided tunnel information from AWS (such as tunnel IP addresses, encryption methods, and shared keys).

**Routing**

- **Static Routing:** If you use static routing, you manually define the routes for the on-premises network to reach the VPC and vice versa.
- **Dynamic Routing (BGP):** Alternatively, you can use *Border Gateway Protocol (BGP)* to automatically exchange routes between your on-premises network and AWS VPC. This is more scalable and easier to manage, especially for larger or more complex networks.

**Redundancy and High Availability**
- AWS Site-to-Site VPN provides high availability through the use of *two VPN tunnels*. AWS automatically provisions two VPN tunnels for each VPN connection, ensuring that if one tunnel goes down, the other can continue to carry traffic. You can configure your on-premises VPN device to monitor both tunnels and automatically failover to the backup tunnel if necessary.
