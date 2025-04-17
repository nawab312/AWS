VPC Flow Logs is a feature in Amazon VPC (Virtual Private Cloud) that allows you to capture information about the IP traffic going to and from network interfaces in your VPC. It records metadata about traffic (not the actual packet data), such as:
- Source and destination IP addresses
- Source and destination ports
- Protocol
- Traffic acceptance (accepted/rejected)
- Packet and byte counts
- Timestamps

Flow Logs can be sent to 
- Amazon CloudWatch Logs – for real-time monitoring and analytics.
- Amazon S3 – for long-term storage, auditing, and analysis with tools like Athena.

Example

```bash
2025-04-17T12:44:15.000+05:30
	
2 961341511681 eni-028738ce9da85b244 10.0.1.15 3.94.91.31 44818 123 17 1 76 1744874055 1744874084 ACCEPT OK
	
2025-04-17T12:44:15.000+05:30
	
2 961341511681 eni-028738ce9da85b244 10.0.1.15 3.86.4.106 46560 123 17 1 76 1744874055 1744874084 ACCEPT OK
	
2025-04-17T12:44:15.000+05:30
	
2 961341511681 eni-028738ce9da85b244 35.203.210.251 10.0.1.15 54345 450 6 1 44 1744874055 1744874084 REJECT OK
	
2025-04-17T12:44:15.000+05:30
	
2 961341511681 eni-028738ce9da85b244 3.86.4.106 10.0.1.15 123 46560 17 1 76 1744874055 1744874084 ACCEPT OK
```

- `version` Flow log version (here, 2)
- `account-id` Your AWS account ID
- `interface-id` Elastic Network Interface (ENI) ID
- `srcaddr` Source IP address
- `dstaddr` Destination IP address
- `srcport` Source port
- `dstport` Destination port
- `protocol` Protocol number: 6 = TCP, 17 = UDP
- `packets` Number of packets transferred
- `bytes` Number of bytes transferred
- `start`Unix timestamp for start of flow
- `end` Unix timestamp for end of flow
- `action` ACCEPT or REJECT
- `log-status` OK, NODATA, or SKIPDATA