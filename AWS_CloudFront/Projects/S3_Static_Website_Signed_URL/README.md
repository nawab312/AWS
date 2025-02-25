## Secure Content Delivery with Signed URLs ##
It is a mechanism in AWS CloudFront that restricts access to content (videos, PDFs, images, etc.) by allowing only authenticated users with a **signed URL** to access private resources. Normally, when you distribute content via CloudFront, anyone with the CloudFront URL can access it. But what if you want to:
- Restrict access to only authenticated users?
- Set an expiration time for URLs?
- Prevent unauthorized downloads and sharing?
This is where **signed URLs** help. Instead of exposing a direct URL, you generate a **temporary, unique URL** with an **expiration time**. Only users with this signed URL can access the content. 
