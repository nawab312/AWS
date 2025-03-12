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
