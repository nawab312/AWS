A VPC Endpoint is a feature in AWS that allows you to privately connect your Amazon VPC (Virtual Private Cloud) to supported AWS services without requiring an Internet Gateway, NAT Gateway, or VPN connection. Types of VPC Endpoints:

### Interface Endpoint (Powered by AWS PrivateLink) ###
- Uses an *Elastic Network Interface (ENI)* with a *private IP* in your VPC.
- Supports services like Amazon S3, DynamoDB, Lambda, SNS, SQS, and more.

**How Does It Work?**
- AWS creates a virtual network cable (ENI - Elastic Network Interface) in your VPC.
- This ENI gets a private IP address inside your VPC.
- Your EC2, Lambda, or any private server can now talk to AWS services through this private IP.

### Gateway Endpoint ###
- Uses a route table entry to route traffic directly to AWS services
- Only supports Amazon S3 and DynamoDB.

**How Does It Work?**
- You create a Gateway Endpoint for S3 or DynamoDB.
- AWS adds an entry to your VPC's route table, pointing to the AWS service.
- When your EC2/Lambda wants to access S3 or DynamoDB, it follows this private route instead of using the internet.

![image](https://github.com/user-attachments/assets/92443a88-e801-4d5a-87af-ab00c1601f73)
