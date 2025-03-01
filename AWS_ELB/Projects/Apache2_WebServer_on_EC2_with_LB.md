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
