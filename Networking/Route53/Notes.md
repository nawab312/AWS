- **Domain Name System** translates the human friendly hostnames into the machine IP addresses
- DNS Terminologies:
  - Domain Registrar: Amazon Route 53, GoDaddy
  - DNS Resolver: A DNS resolver (typically provided by your ISP, or services like Google DNS or Cloudflare DNS) is responsible for querying DNS records on behalf of a client (like your browser). It resolves domain names to IP addresses by querying the DNS hierarchy (including authoritative DNS servers).
  - DNS Records: A, AAAA, CNAME, NS
  - Zone File: Contains DNS record
  - Name Server: resolves DNS queries (Authoritative or Non-Authoritative)
  - Top Level Domain (TLD): .com, .us, .in, .gov, .org,
  - Second Level Domain (SLD): amazon.com, google.com
- `http://api.www.example.com`
  - `.com` TLD
  - `example.com` SLD
  - `www.example.com` Sub Domain
  - `api.www.example.com` FQDN (Fully Qualified Dcomain Name)
  - `http` Protocol
 
- **Route53** A highly available, scalable, fully managed and Authoritative DNS
  - Authoritative = The Customer (you) can update the DNS records
  - Route 53 is also a Domain Registrar
  - Ability to check the health of your resources
  - The only AWS service which provides 100% availability SLA

![image](https://github.com/user-attachments/assets/ecda88ca-695c-4b6f-ab15-6393aa82ff79)

- **Route 53–Records** Route 53 records are DNS entries used to map domain names to specific IP addresses, services, or resources.
  - Domain/Subdomain Name – e.g., example.com
  - Record Type – e.g., A or AAAA
  - Value – e.g., 12.34.56.78
  - Routing Policy – How Route 53 responds to Queries
  - TTL – DNS caching is the process where DNS resolvers (servers that handle domain name resolution) store the results of DNS lookups for a certain period of time, known as the Time to Live (TTL).
    
![image](https://github.com/user-attachments/assets/0dec6009-08f7-4088-95e3-24bf36d70bb3)

- **Route 53–Hosted Zones** Hosted Zone is a container for DNS records for a specific domain. It is a fundamental concept for managing your domain names and routing traffic in AWS. A hosted zone acts like a directory of DNS records that define how traffic is directed for a domain (e.g.,example.com) or subdomains (e.g., www.example.com).
  - **Public Hosted Zones** These are used for domains that are publicly accessible on the internet (e.g., websites or services exposed to the public). Public hosted zones contain records that allow domain names to resolve to IP addresses over the internet.
  - **Private Hosted Zones** These are used for domains that are only accessible within an Amazon VPC ( Meaning only AWS resources can query it).However, there’s no restriction on what kind of IP addresses you store inside PHZ. Private hosted zones are ideal for managing internal services within AWS, such as private APIs or databases that shouldn’t be publicly accessible.
    - It can store private AWS IPs (`10.0.0.10`)
    - It can store private on-prem IPs (`192.168.1.100`)
    - It can even store public IPs (`8.8.8.8`)
 
*If you override /etc/resolv.conf to use 8.8.8.8 in an AWS EC2 instance, will private Route 53 DNS names still resolve?*
- Route 53 private hosted zone names wont resolve with 8.8.8.8
- Private hosted zones in Route 53 are only accessible from within the VPC via AmazonProvidedDNS, which is at:
```bash
169.254.169.253 (hidden behind VPC base + 2)
```
- If you override /etc/resolv.conf and set it to Google DNS (8.8.8.8):
  - You're bypassing the VPC-resolved DNS
  - 8.8.8.8 has no knowledge of your private zone

![image](https://github.com/user-attachments/assets/9b2aed3c-bc87-466f-83ca-eb6efc3dc98b) ![image](https://github.com/user-attachments/assets/2a57424b-7652-48e8-8c07-dce3eb48188b)

- **Components of a Hosted Zone**
  - *Domain Name:* The primary domain for which the hosted zone is created. For example, example.com would be the domain name for the hosted zone. You can also create subdomains (like api.example.com or www.example.com) within the hosted zone.
  - *Name Servers (NS) Record:* When you create a hosted zone, Route 53 automatically generates a set of name servers (NS records) for the hosted zone. These NS records tell the internet where to find your DNS records. When you register a domain or transfer one to Route 53, you typically update the domain registrar to point to these NS records.
  - SOA (Start of Authority) Record: Every hosted zone automatically includes a Start of Authority (SOA) record. This record specifies the authoritative DNS server for the domain, the email address of the domain administrator, and other settings related to the domain’s DNS configuration (e.g., TTL values).
 
![image](https://github.com/user-attachments/assets/436d1407-3178-40d9-9429-275bf3606ddf)

**You need to create a subdomain (e.g. api.abc.com) that points to a load balancer. How would you set this up in Route 53, and what record type would you use?**
- Go to the AWS Management Console and navigate to Route 53.
- Create or Update Hosted Zone:
  - Ensure that you have a hosted zone for *abc.com*. If you don’t, you can create one
  - If the hosted zone for abc.com already exists, select it.
- Get the Load Balancer DNS Name:`my-load-balancer-1234567890.us-west-2.elb.amazonaws.com`
- Create the Record Set for Subdomain:
  - In your Route 53 hosted zone for abc.com, click on Create record
  - *Record Type:* Choose *CNAME*. This is because you want to map the subdomain (api.abc.com) to the DNS name of your load balancer.
  - Name: Enter `api` (this will create `api.abc.com`).
  - Value: Enter the DNS name of your load balancer (e.g., `my-load-balancer-1234567890.us-west-2.elb.amazonaws.com`).
  - Click Create records

![image](https://github.com/user-attachments/assets/ef4e9c90-f176-48df-b18d-5cc1dd49e55a) ![image](https://github.com/user-attachments/assets/99cb0598-77a7-4994-bc68-3e845eee1839)

**Route 53–Records TTL (Time To Live)**

![image](https://github.com/user-attachments/assets/25176d8c-d4c2-4a2a-9cd5-9562c9e28e52)

**Difference Between CNAME and Alias Record**
- A **CNAME** record maps a subdomain (e.g., api.abc.com) to another domain name (e.g., my-load-balancer-1234567890.us-west-2.elb.amazonaws.com). A CNAME record *can only be used for subdomains, not for root domains (e.g., abc.com)*. If you use a CNAME record, like `www.example.com -> example.com`, the DNS first returns `example.com`, and then a *second lookup* is needed to resolve example.com to an IP address.
- The **ALIAS** record is a special AWS Route 53 feature that allows you to point a *root domain (e.g., abc.com) or subdomain (e.g., api.abc.com)* directly to AWS resources like Elastic Load Balancers (ELBs), CloudFront distributions, or
S3 buckets, *without needing to use the resource’s DNS name*.If you use an ALIAS record for `www.example.com` pointing to an AWS resource (e.g., `example.elasticloadbalancing.com`), the DNS resolver *will directly return the IP address of the AWS resource in one step*, without the need for another query.

**Routing Policies** https://github.com/nawab312/AWS/blob/main/Networking%20and%20Security/Route53/RoutingPolicies.md

---

**Route 53 Health Checks & DNS Failover**

Route 53 health checks are a function that allow you to monitor the health of selected types of AWS resources or any endpoints that can respond to requests. Route 53 health checks can provide notifications of a change in the state of the health check and can help Route 53 to recognize when a record is pointing to an unhealthy resource, allowing Route 53 to failover to an alternate record.

![image](https://github.com/user-attachments/assets/2ce883cf-f41c-4333-b446-122a14e780a3)

Types of Route 53 health checks
- *Endpoint health checks*: You can configure to monitor an endpoint that you specify by IP address or domain name. Within a fixed time interval that you specify. Route 53 submits automated requests over the Internet to your application, server, or other resources to verify that it is accessible, available, and functioning properly
- *Health checks that monitor other health checks*: This type of health check monitors other Route 53 health checks. Basically, a "parent" health check will monitor one or more "child" health checks. If the provided number of child health checks report as healthy, then parent health checks will also be healthy. If the number of healthy "child" checks falls below a set threshold, the "parent" check will be unhealthy.
![image](https://github.com/user-attachments/assets/e779585b-8cde-450c-ad96-e6ed8ad70aa0)
- *Health checks for Amazon CloudWatch Alarms*: You can also perform health checks associated with alarms created in the CloudWatch service. These types of Route 53 health checks monitor CloudWatch data streams sent to previously configured alarms. If the status of the CloudWatch alarm is OK, the health check will report as OK.

Route 53 active-passive vs active-active failover

*Active-active failover*
- Active-active failover is used when you want all of your app nodes in all regions to be available simultaneously. Use this failover configuration when you want all of your resources to be available the majority of the time.
- In this example, both region 1 and region 2 are active all the time. When a resource becomes unavailable, Route 53 can detect that it's unhealthy and stop including it when responding to queries.
- For example, this can be created by using Route 53 weighted, geolocation, geoproximity, latency and multivalue answer routing policy.

![image](https://github.com/user-attachments/assets/c3e3550d-7737-475b-908e-976f2f5bd728)

*Active-passive failover*
- Use an active-passive failover configuration when you want a primary resource or group of resources to be available the majority of the time and you want a secondary resource or group of resources to be on standby in case all the primary resources become unavailable.
- In this example, only region 1 is active all the time and region 2 will be only active when failover starts (after region 1 is unavailable).
- This can be created by using Route 53 failover routing policy.

![image](https://github.com/user-attachments/assets/e7d7d788-c061-493f-b782-e1e56dea0117)









