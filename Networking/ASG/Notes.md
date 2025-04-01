AWS Auto Scaling Group (ASG) is a service that automatically adjusts the number of Amazon EC2 instances in a group based on demand. It ensures that your application maintains the desired performance while optimizing cost by adding or removing instances dynamically.

- **Automatic Scaling** – Increases or decreases the number of EC2 instances based on scaling policies.
- **Health Monitoring & Replacement** – Continuously checks the health of instances and replaces unhealthy ones.
- **Load Balancer Integration** – Can be attached to an Application Load Balancer (ALB) or Network Load Balancer (NLB).
- **Multi-AZ Deployment** – Can span multiple Availability Zones (AZs) to increase fault tolerance.
- **Scheduled Scaling** – Can be configured to scale up/down at specific times.
- **Lifecycle Hooks** – Allows executing custom scripts during instance launch or termination.
- **Cooldown Period** – Prevents excessive scaling actions by defining a waiting period between scaling activities.

**How AWS ASG Works?**
- **Define Launch Template or Launch Configuration** Specifies AMI, instance type, security group, IAM role, key pair, and user data script.
- **Create an Auto Scaling Group** Define the minimum, maximum, and desired number of instances. Specify Availability Zones (AZs) for high availability.
- **Attach Load Balancer (Optional)**
- **Set Scaling Policies**
  - **Target Tracking Scaling:** Adjusts capacity based on CloudWatch metrics (e.g., maintaining CPU at 60%).
  - **Step Scaling:** Increases or decreases instances in steps based on metric thresholds.
  - **Scheduled Scaling:** Triggers scaling at specific times.

**Troubleshooting ASG**

![image](https://github.com/user-attachments/assets/05f18b4c-1a5e-4ca9-8217-5b0fab278cdb)

### LifeCycle Hooks ###
Lifecycle Hooks allow you to execute custom actions at specific points during an instance’s lifecycle (before launching or terminating).

**AWS ASG has two key lifecycle hook phases:**
- Instance Launching (`autoscaling:EC2_INSTANCE_LAUNCHING`) – Runs before the instance becomes active.
  - When a new instance is launched, install necessary software, update packages, or configure logging.
  - Automatically register new instances with CloudWatch, Prometheus, or Datadog for monitoring.
  - When launching an instance, mount an AWS Elastic File System (EFS) to ensure shared storage.
- Instance Terminating (`autoscaling:EC2_INSTANCE_TERMINATING`) – Runs before the instance is terminated.
  - Before terminating an instance, ensure it stops serving traffic and cleanly deregisters from the Application Load Balancer (ALB).
  - Before shutting down an instance, take a backup of logs, database dumps, or persistent data.
