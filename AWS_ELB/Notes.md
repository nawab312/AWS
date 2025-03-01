AWS Elastic Load Balancer (ELB) is a fully managed service that automatically distributes incoming application traffic across multiple targets—such as EC2 instances, containers, and IP addresses—in one or more Availability Zones.

### ELB Types and Their Use Cases ###
- **Classic Load Balancer (CLB):** The original load balancer, suitable for simple load balancing of traffic across EC2 instances. It supports both HTTP/HTTPS and TCP protocols but lacks many advanced features.
- **Application Load Balancer (ALB):** Designed for modern application architectures, ALB works at the application layer (Layer 7) and supports advanced routing, host/path-based routing, WebSocket, and HTTP/2. It is ideal for microservices and container-based applications.
- **Network Load Balancer (NLB):** Operating at the transport layer (Layer 4), NLB is optimized for high-performance, low-latency, and high-throughput traffic. It is best for applications that require extreme performance and static IP addresses.
- **Gateway Load Balancer (GWLB):** Intended for third-party virtual appliances, such as firewalls, it transparently scales and manages traffic between networks.

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

