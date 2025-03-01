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

**Resource Map Tab**
![image](https://github.com/user-attachments/assets/f5b1cc28-9ad7-4865-9c80-8129bf687e0a)

### Enable Access Log ###
- In ALB go to the **Attributes** section and click on the Edit button.
- **Enable access logging**: Set it to Enabled.
- **S3 Bucket:** Choose an existing S3 bucket where the logs will be stored, or create a new S3 bucket if necessary. The ALB will write the access logs to this bucket.
  - The S3 bucket must be in the same AWS region as the ALB.
  - Ensure the S3 bucket has proper permissions for the ALB to write logs. Typically, you will create an **S3 bucket policy** to allow access logging.
  - elb-account-id for US East (N. Virginia) – `127311923021`
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "AWS": "arn:aws:iam::elb-account-id:root"
      },
      "Action": "s3:PutObject",
      "Resource": "s3-bucket-arn/*"
    }
  ]
}
```
- To Access Logs
``bash
aws s3 cp s3://example-bucket-siddy-312/AWSLogs/961341511681/elasticloadbalancing/us-east-1/2025/03/01 ./access_logs/ --recursive
```
```bash
cd access_logs/
gunzip *
```
```bash
cat 961341511681_elasticloadbalancing_us-east-1_app.MyALB1.240dbdc5244653c9_20250301T1005Z_44.218.101.212_16w3taku.log
http 2025-03-01T10:03:17.218099Z app/MyALB1/240dbdc5244653c9 205.210.31.158:61084 - -1 -1 -1 400 - 0 272 "- http://myalb1-878688131.us-east-1.elb.amazonaws.com:80- -" "-" - - - "-" "-" "-" - 2025-03-01T10:03:16.682000Z "-" "-" "-" "-" "-" "-" "-" TID_6cfb27fd2ef25c42932bd6e0ff56d631
http 2025-03-01T10:03:17.228026Z app/MyALB1/240dbdc5244653c9 205.210.31.158:61090 - -1 -1 -1 400 - 0 272 "- http://myalb1-878688131.us-east-1.elb.amazonaws.com:80- -" "-" - - - "-" "-" "-" - 2025-03-01T10:03:16.931000Z "-" "-" "-" "-" "-" "-" "-" TID_a063715249462c46b184cd84944a3271
http 2025-03-01T10:03:48.928268Z app/MyALB1/240dbdc5244653c9 103.211.55.184:33674 172.31.27.170:80 0.000 0.001 0.000 304 304 457 216 "GET http://myalb1-878688131.us-east-1.elb.amazonaws.com:80/ HTTP/1.1" "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:135.0) Gecko/20100101 Firefox/135.0" - - arn:aws:elasticloadbalancing:us-east-1:961341511681:targetgroup/MyTargetGroup/98a5d72211ca033a "Root=1-67c2db84-1d00721018e57bc73ebdfb2a" "-" "-" 0 2025-03-01T10:03:48.926000Z "forward" "-" "-" "172.31.27.170:80" "304" "-" "-" TID_5b824cc752b55e45b6a213aa8f44cc8a
```

