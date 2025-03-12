AWS Route 53 provides several routing policies that allow you to manage how DNS queries are directed to your resources. These routing policies help in load balancing,failover, geographic targeting, and more. Here's an overview of the different Route 53 Polcieis

**Simple Routing Policy**
- Description: The simplest routing policy where Route 53 returns a single value (IP address) for a DNS query
- Use Case: This is the default routing policy when you create a DNS record. It is appropriate when you have a single resource, such as one web server or one load balancer, for a domain or subdomain.
- Example: You would use this for pointing www.abc.com to a single IP address or load balancer
- How it works: When a DNS query is made, Route 53 responds with the IP address for the corresponding record

![image](https://github.com/user-attachments/assets/3f64ceba-bbab-450c-8595-c8b9826f0b68)

**Weighted Routing Policy**
- Description: Allows you to distribute traffic across multiple resources (e.g., EC2 instances, load balancers) based on specified weights. Each resource has a weight, and Route 53 will route traffic according to the relative weight assigned.
- Use Case: This is useful when you want to split traffic between different servers, versions of an application, or AWS regions
- Example: You can assign a weight of 70 to one EC2 instance and 30 to another, thereby directing 70% of traffic to the first instance and 30% to the second.

