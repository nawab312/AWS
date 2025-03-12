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


