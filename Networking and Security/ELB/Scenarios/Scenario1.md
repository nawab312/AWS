Your company has an application hosted on EC2 instances behind an AWS ALB (Application Load Balancer). 
Users report intermittent 504 Gateway Timeout errors. 
How will you troubleshoot this issue? Explain step by step, covering potential causes at different layers (ALB, EC2, security groups, network, etc.).

### Solution ###

**504 status code** means that the Application Load Balancer (ALB) is acting as a **gateway or proxy** and it didn't receive a timely response from the **backend EC2 instance** it forwarded the request to. 
Essentially, the ALB is waiting for a response from the EC2 instance, but the instance didn't respond in time, so the ALB returns a 504 Gateway Timeout to the client (user).

**Check ALB Logs and Metrics**
- First, I'd start by checking the *ALB access logs* to see if there’s any correlation between the 504 errors and specific backend instances or paths.
- Next, I would review *CloudWatch metrics* for the ALB:
  - `Target Response Time` to see if there’s any latency in response from the EC2 instances.
  - `HTTP 504 count` to check if the 504 errors are spiking at any specific time.
  - `Healthy Hosts` in the target group to ensure all instances are marked healthy.

**Check EC2 Instance Health**
- I’d then investigate the *performance metrics* of the EC2 instances, including CPU, memory, and disk usage, to identify any resource bottlenecks that could be slowing down the application.
- I would also check the *application logs* for any internal errors or processes that could be taking longer than expected, causing delays.

**Review ALB Configuration**
- I’d verify the *ALB’s timeout settings*, ensuring that the idle timeout isn’t set too short (the default is 60 seconds). If the application takes longer to respond, this could lead to a 504 error.

**Check Security Groups and Network ACLs**
- I would ensure the *security groups* for both the ALB and EC2 instances are configured to allow the necessary inbound and outbound traffic on the appropriate ports (e.g., 80/443).

**Network Configuration**
- Finally, I would check the *VPC/subnet configuration* to ensure there are no network misconfigurations or isolation issues preventing proper communication between the ALB and EC2 instanc
