AWS Elastic Load Balancer (ELB) is a fully managed service that automatically distributes incoming application traffic across multiple targets—such as EC2 instances, containers, and IP addresses—in one or more Availability Zones. 

*Minimum Number of Availability Zones (AZs) Required For An AWS Application Load Balancer (ALB) is 2*

### ELB Types and Their Use Cases ###
- **Classic Load Balancer (CLB):** The original load balancer, suitable for simple load balancing of traffic across EC2 instances. It supports both HTTP/HTTPS and TCP protocols but lacks many advanced features.
- **Application Load Balancer (ALB):** Designed for modern application architectures, ALB works at the application layer (Layer 7) and supports advanced routing, host/path-based routing, WebSocket, and HTTP/2. It is ideal for microservices and container-based applications.
- **Network Load Balancer (NLB):** Operating at the transport layer (Layer 4), NLB is optimized for high-performance, low-latency, and high-throughput traffic. It is best for applications that require extreme performance and static IP addresses.
- **Gateway Load Balancer (GWLB):** Intended for third-party virtual appliances, such as firewalls, it transparently scales and manages traffic 
between networks.

---

You have an application deployed across three Availability Zones (AZs) behind an Application Load Balancer (ALB). You observe that even though all AZs have healthy targets, one AZ is receiving significantly more traffic than others. Why?
- When **Cross-Zone Load Balancing** is disabled, the ALB only routes traffic to targets within the same Availability Zone as the client request.
- Cross-Zone LB is always enabled for ALB 

---

**Target Types**

![image](https://github.com/user-attachments/assets/a63bd173-8283-40ba-88fb-b11866fa4784)


### Key Concepts and Features ###
- **Health Checks:** ELB continuously monitors the health of its targets. Unhealthy targets are automatically removed from the pool, ensuring that only healthy instances serve traffic.
- **Listeners and Rules:** A listener is a process that checks for connection requests. For ALB, you can define routing rules based on host headers, path patterns, or query strings.
- **Sticky Sessions (Session Affinity):** This feature allows ELB to bind a user’s session to a specific target, ensuring consistent experience during multi-step transactions.
- **SSL Termination:** ELB can offload the SSL/TLS decryption from your instances, simplifying certificate management and reducing processing load on your back-end servers.
- **Integration with Auto Scaling:** ELB works seamlessly with Auto Scaling, automatically adding or removing targets as your application scales.
- **Load Balancing Algorithms**
  - *Round Robin:* Distributes requests evenly across all available targets.
  - *Least Outstanding Requests:* (For ALB) Directs traffic to the target with the fewest outstanding requests.
  - *Flow Hash:* (For NLB) Uses network flow information to ensure the same client is consistently routed to the same target.

### Headers in AWS ALB ###
Headers in ALB (Application Load Balancer) are **extra pieces of information** that **travel with HTTP requests and responses**. These headers help ALB make decisions about **where to send traffic, how to secure requests, and how to balance the load** among servers.

**How Headers Work in ALB?***
When a client (like a browser or mobile app) sends a request to a website, it includes **headers**. The ALB reads these headers and decides how to handle the request. For example:
- A user visits `www.example.com`.
- Their browser sends an HTTP request with headers (e.g., `User-Agent: Chrome`, `X-Forwarded-For: <IP address>`).
- The ALB checks these headers to:
  - Route the request to the correct server.
  - Apply security rules.
  - Ensure proper load balancing.

**Types of Headers in ALB**
- **Request Headers** These are headers sent by the client (browser, API, or service) to ALB. ALB can use these headers for routing and security rules.  How ALB Uses Request Headers:
  - Host-Based Routing → Routes based on `Host` header.
  - User-Agent-Based Routing → Routes traffic to a mobile backend if the `User-Agent` contains "Mobile".
  - Security Checks → Uses `Authorization` and `Cookie` headers for authentication

![image](https://github.com/user-attachments/assets/339a1f21-b2a1-4e0e-8bcc-4fcbff0cf377)

- **Response Headers** These are headers that ALB sends back to the client after processing the request. How ALB Uses Response Headers:
  - **Redirects & Security** → Uses `Location` and `Strict-Transport-Security`.
  - **CORS Handling** → Uses `Access-Control-Allow-Origin` for cross-origin requests.
  - **Debugging** → `X-Amzn-Trace-Id` helps track requests in AWS logs.

![image](https://github.com/user-attachments/assets/6a0e1785-6c54-467a-831e-6a0ace792369)
 
### Listener & Listener Rules ###
A **listener** in AWS Application Load Balancer (ALB) is a process that listens for incoming client requests on a **specified port and protocol** and forwards them to the target groups based on rules.
-  A listener must be configured with a port (e.g., 80, 443) and protocol (HTTP, HTTPS).
-  **Rules-Based Routing:** Determines how traffic is distributed to different targets using listener rules.
-  For HTTPS listeners, SSL certificates are required for secure communication.
-  ALB can have multiple listeners (e.g., one for HTTP on port 80 and another for HTTPS on port 443).

**Listener rules** define how the ALB processes incoming requests and which target groups they should be forwarded to based on conditions. Key Components of Listener Rules
  - **Priority** Rules are evaluated in order, starting from the lowest number (1 is the highest priority).
  - **Conditions** Defines how to match requests (Host-header, Path, Headers, Query parameters, etc.).
  - **Actions** Specifies what to do when the condition matches (Forward, Redirect, Fixed response).

**Types of Conditions in Listener Rules**

- **Host-based Routing (Host Header Condition)** 
  - Routes traffic based on the *domain name* in the request.
  - `Rule: If Host = "bank.example.com" → Forward to Banking Service Target Group`
  - Useful for multi-domain applications running behind the same ALB. Example: `app.example.com`, `api.example.com`, `admin.example.com`.
- **Path-based Routing (Path Condition)**
  - Routes traffic based on the *URL path*.
  - `Rule: If Path = "/api/*" → Forward to API Target Group`
  - Splitting traffic based on application components like: `/app/*` → Frontend UI, `/api/*` → Backend API, `/admin/*` → Admin Dashboard
- **Header-based Routing**
  - Routes traffic based on specific **HTTP headers**.
  - `Rule: If Header "User-Agent" contains "Mobile" → Forward to Mobile Service Target Group`
  - Use Case: Direct mobile users to a mobile-optimized backend.
- **Query Parameter-based Routing**
  - Routes traffic based on *query parameters* in the URL.
  - `Rule: If Query parameter "version=v2" → Forward to Beta API Target Group`
  - Use Case: A/B testing, version-based routing.
 
**Types of Actions in Listener Rules**
- **Forward Action (Default Behavior)**
  - Sends traffic to a specific *Target Group*.
  - `Rule: If Path = "/api/*" → Forward to API Target Group`
  - Use Case: Forward requests to a set of EC2 instances, Lambda functions, or containers.
- **Redirect Action**
  - Redirects traffic to a different URL (internal or external).
  - `Rule: If HTTP request → Redirect to HTTPS (301 Permanent Redirect)`
  - Use Case: Enforce HTTPS (`http://example.com` → `https://example.com`).
- **Fixed Response Action**
  - ALB sends a custom response instead of forwarding requests.
  - `Rule: If Path = "/maintenance" → Return 503 with "Service Unavailable"`
  - Use Case: Show a maintenance page without hitting the backend.

![image](https://github.com/user-attachments/assets/93723889-a2c3-444e-9a50-108d70a04167)

The request is coming to api.example.com/admin/1. Let's analyze the ALB routing rules based on priority:
- Priority 1:
  - Condition: `Host = api.example.com`
  - This condition matches because the request is for `api.example.com`
  - However, we need to check if a more specific rule applies before routing.
- Priority 2:
  - Condition: `Path = /admin/*`
  - The request path is `/admin/1`, which matches this condition.
  - Since rule Priority 2 matches, the request will be forwarded to the Admin Target Group.
 
### ALB Monitoring ###
- Critical ALB Metrics to Monitor:
  - **RequestCount:** The number of requests processed by the ALB.
  - **ActiveConnectionCount:** The number of active connections to the load balancer.
  - **HealthyHostCount:** The number of healthy targets in the target group.
  - **UnHealthyHostCount:** The number of unhealthy targets in the target group.
  - **TargetResponseTime:** The response time of the targets (back-end servers).
  - **HTTPCode_ELB_5XX:** The number of 5xx errors from the load balancer.
  - **HTTPCode_Target_5XX:** The number of 5xx errors from the targets (back-end instances).
  - **RequestProcessingTime:** The time it takes the ALB to process a request.
  - **TargetProcessingTime:** The time it takes for the target to process the request.
  - **ResponseProcessingTime:** The time it takes the ALB to send the response back to the client.
 
---

Question:

Your company has deployed an Application Load Balancer (ALB) in AWS to handle incoming traffic for a web application. The ALB routes requests to a group of EC2 instances based on URL path-based routing. Recently, users started reporting intermittent HTTP 503 errors when accessing certain application endpoints.

What is the MOST LIKELY cause of these intermittent 503 Service Unavailable errors?

- The ALB security group is blocking inbound traffic from users.
- The ALB target group has unhealthy instances due to failed health checks.
- The EC2 instances are blocking ALB requests in their security groups.
- The ALB has reached its maximum request limit and is throttling connections.

Correct Answer: ALB returns HTTP 503 errors when all targets in the target group are unhealthy
- HTTP 503 - "Service Unavailable" means that the ALB cannot forward requests because it has no healthy targets
- ALB routes requests to registered targets (EC2, ECS, Lambda, etc.)
- If all targets in the target group are unhealthy, ALB has no backend to forward the request to → returns HTTP 503

![image](https://github.com/user-attachments/assets/00237dea-5f2e-4927-8fe4-f0a28b1e05f1)

---

Question:

Your company is using an AWS Application Load Balancer (ALB) to route traffic to an auto-scaled group of EC2 instances. You recently added a new target group and registered instances, but the ALB is still not routing traffic to them. The application is running on port 8080 on the instances.

What is the MOST LIKELY reason for this issue?

- The ALB security group does not allow inbound traffic on port 8080.
- The target group is using HTTP (port 80), but the application runs on port 8080.
- The ALB listener is not configured to forward requests to the new target group.
- The EC2 instances are missing IAM permissions to accept ALB traffic.

Correct Answer:
- The target group is using HTTP (port 80), but the application runs on port 8080.
  - ALB forwards requests to the target group’s defined port.
  - If your target group expects traffic on port 80, but your app listens on 8080, health checks will fail → ALB won't route traffic.
- The ALB listener is not configured to forward requests to the new target group.
  - ALB needs a listener rule to forward traffic to the correct target group.
  - If the listener isn’t updated, it won’t send traffic to the new group.
 
Why Not the Other Options?

![image](https://github.com/user-attachments/assets/bca0d252-cc6e-4ae6-95e5-d4fd1a440aae)

---

![image](https://github.com/user-attachments/assets/67e93498-c2ca-48d4-b4dd-3c18fb6689bd)


**Troubleshoot Intermittent 504 Gateway Timeout Errors for an Application behind an AWS ALB** https://github.com/nawab312/AWS/blob/main/Networking%20and%20Security/ELB/Scenarios/Scenario1.md

**Apache Webserver on 2 EC2 with LB** https://github.com/nawab312/AWS/blob/main/AWS_ELB/Projects/Apache2_WebServer_on_EC2_with_LB.md



