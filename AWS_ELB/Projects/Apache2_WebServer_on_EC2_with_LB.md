This project demonstrates the automated deployment of an Apache2 web server on an EC2 instance using a userdata script. The setup also integrates an Application Load Balancer (ALB) to distribute incoming traffic across multiple EC2 instances, ensuring high availability and scalability. The project leverages AWS best practices for security and network configuration, providing a robust solution for hosting web applications in the cloud.

### Create 2 EC2 Instances with UserData File in Different AZs ###
- Create EC2 Instance in **us-east-1a** and **us-east-1b**
- Allow Inbound Traffic of Type **HTTP**
- User Data File
```bash
#!/bin/bash
sudo apt update -y
sudo apt install apache2 -y
sudo systemctl start apache2
sudo systemctl enable apache2
hostname=$(hostname)
echo "Hello from $hostname" | sudo tee /var/www/html/index.html > /dev/null
```
![image](https://github.com/user-attachments/assets/ebe5e9cd-de5d-4875-b9bf-6fa6590d2f06)

- Access the Public IPv4 of Each Instance

![image](https://github.com/user-attachments/assets/47bcfd19-0abf-47ea-9bde-92dee45c9efc)
![image](https://github.com/user-attachments/assets/41a518be-33e5-4811-a0bd-d68d39bece66)

### Create Target Group ###
- Target Type: **Instances**
- Set the protocol to **HTTP** and port to **80**.
- Select **Health check path** as `/` (root path) to verify if Apache is serving content correctly.
- Click on **Targets** and then **Register Targets**
![image](https://github.com/user-attachments/assets/eddd72a6-cd5a-4d24-b772-d1ce591639bc)

### Create ALB ###
- Give Load Balancer a Name
- Select **Scheme**(Scheme refers to whether the load balancer is internal or internet-facing)
  - **Internet-facing:** The load balancer is accessible from the internet. This means it has a publicly resolvable DNS name and can handle requests from external clients (e.g., users accessing your web application through a browser).
  - **Internal:** The load balancer is only accessible within the private network (VPC) and is not exposed to the internet.
- In **Security Group** Allow inbound traffic on **HTTP (Port 80)** from `0.0.0.0/0`.
- Configure **Listeners and Routing**
![image](https://github.com/user-attachments/assets/2c3f261a-0747-4607-afb0-130eae5ebc96)

- Access ALB using its DNS Name

![image](https://github.com/user-attachments/assets/30b3c8c9-5145-449f-99f9-1ae91839c27a)


