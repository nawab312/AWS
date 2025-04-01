### Key Features of AWS WAF ###
- **Traffic Filtering and Protection:**
  - **Web Application Protection:** AWS WAF protects your applications from common attack vectors such as *SQL injection*, *cross-site scripting (XSS)*, and other *HTTP-based threats*.
  - **Customizable Rules:** You can define custom rules that specify which web traffic should be allowed or blocked based on certain conditions.

- **Integrated with AWS Services:**
  - AWS WAF can be integrated with Amazon CloudFront, Application Load Balancer (ALB), API Gateway, and AWS App Runner.  
  - It works as a part of your application infrastructure and is deployed at the edge of the AWS network to filter traffic before it reaches your applications.

- **Rule Groups and Managed Rules:**
  - **Managed Rule Groups:** AWS provides pre-configured rule groups to protect against common threats, including those from the OWASP Top 10 (e.g., SQL injection, XSS). You can use these managed rule groups instead of creating custom rules from scratch
  - **Custom Rule Groups:** You can create your own set of rules based on specific needs, such as blocking traffic from certain IP ranges, restricting access based on geographic location, or filtering malicious query strings.

- **Rate-Based Rules:**
  - Rate-based rules help prevent DDoS (Distributed Denial of Service) attacks by limiting the number of requests from a specific IP address over a set time period.

- **IP Set:**
  - AWS WAF allows you to define IP Sets that specify a list of IP addresses you want to block or allow. You can also use **Geo Match** conditions to block or allow traffic from certain countries or regions.
 
- **Bot Control:**
  - AWS WAF offers Bot Control to detect and mitigate bot traffic, preventing malicious bots from accessing your web applications and APIs.
 
### Components of AWS WAF ###
**Web ACL (Access Control List):**
- A Web ACL is a set of rules that AWS WAF uses to evaluate web requests. It is the primary container for your rules and rule groups.
- The Web ACL is associated with one or more AWS resources like CloudFront distributions, ALBs, or API Gateway stages.
- You can specify whether you want to allow or block requests or count requests for each rule.

**Rules:**
- **Regular Rules:** These are rules based on conditions you define, such as matching specific IP addresses, query parameters, user-agents, geographic location, and more.
- **Rate-based Rules:** Used to track and limit requests coming from an IP address to mitigate DDoS attacks or brute-force login attempts.

**Conditions:** AWS WAF uses different conditions to determine whether a request matches a rule. These include:
- IP Addresses: Allows you to filter based on specific IP addresses.
- URI Path: Can be used to match the URI in the request.
- Query String: Matches against query parameters in the URL.
- HTTP Headers: Allows matching specific HTTP headers, such as the `User-Agent` or `X-Forwarded-For`.
- Body: This can match text patterns in the body of a POST request.


**Action:** When a rule matches a request, AWS WAF can take different actions:
- *Allow:* The request is allowed to proceed to the backend.
- *Block:* The request is blocked and never reaches the web application
- *Count:* The request is counted, but not blocked or allowed, which is useful for monitoring traffic before making decisions on blocking or allowing.

- **ALB Integration with AWS WAF** https://github.com/nawab312/AWS/blob/main/Security/AWS_WAF/Project1.md
