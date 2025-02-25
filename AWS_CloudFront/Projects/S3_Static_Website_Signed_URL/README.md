## Secure Content Delivery with Signed URLs ##
It is a mechanism in AWS CloudFront that restricts access to content (videos, PDFs, images, etc.) by allowing only authenticated users with a **signed URL** to access private resources. Normally, when you distribute content via CloudFront, anyone with the CloudFront URL can access it. But what if you want to:
- Restrict access to only authenticated users?
- Set an expiration time for URLs?
- Prevent unauthorized downloads and sharing?
This is where **signed URLs** help. Instead of exposing a direct URL, you generate a **temporary, unique URL** with an **expiration time**. Only users with this signed URL can access the content.

### To sign CloudFront URLs, you need a CloudFront Key Pair. This allows your backend (Python/Node.js) to generate signed URLs. ###
- Navigate to IAM → Security Credentials
- Scroll down to **CloudFront Key Pairs**. Click Create Key Pair
- AWS will generate a Key Pair ID `(e.g., APKAXXXXXXXXXXXX)`
- Download the private key file `(pk-APKAXXXXXXXXXXXX.pem)`
- Key Pair ID and Private Key (.pem) will be used to sign URLs.

### Attach the Public Key to CloudFront ###
- Open CloudFront Console. Click Public Keys (Under Key Management)
- Click Create Public Key. Enter a name `(e.g., MyCloudFrontKey)`
- Upload the **public key** extracted from your `.pem` file
- Now in CloudFront Console there will be Key Groups (Under Key Management)
- Enter a name `MyCloudFrontKeyGroup`. Under Public Keys chose `MyCloudFrontKey`

### Refer this Project: https://github.com/nawab312/AWS/tree/main/AWS_CloudFront/Projects/S3_Static_Website ###

### Only when creating CloudFront Distribution under `Restrict viewer access` check `Yes` ###
![Restrict Access]()
