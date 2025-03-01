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
