- **Domain Name System** translates the human friendly hostnames into the machine IP addresses
- DNS Terminologies:
  - Domain Registrar: Amazon Route 53, GoDaddy
  - DNS Records: A, AAAA, CNAME, NS
  - Zone File: Contains DNS record
  - Name Server: resolves DNS queries (Authoritative or Non-Authoritative)
  - Top Level Domain (TLD): .com, .us, .in, .gov, .org,
  - Second Level Domain (SLD): amazon.com, google.com
- `http://api.example.com`
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
  - TTL – Amount of time the record cached at DNS Resolvers

![image](https://github.com/user-attachments/assets/0dec6009-08f7-4088-95e3-24bf36d70bb3)

- **Route 53–Hosted Zones** Hosted Zone is a container for DNS records for a specific domain. It is a fundamental concept for managing your domain names and routing traffic in AWS. A hosted zone acts like a directory of DNS records that define how traffic is directed for a domain (e.g.,example.com) or subdomains (e.g., www.example.com).
  - **Public Hosted Zones** These are used for domains that are publicly accessible on the internet (e.g., websites or services exposed to the public). Public hosted zones contain records that allow domain names to resolve to IP addresses over the internet.
  - **Private Hosted Zones** These are used for domains that are only accessible within an Amazon VPC. Private hosted zones are ideal for managing internal services within AWS, such as private APIs or databases that shouldn’t be publicly accessible.
 
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





