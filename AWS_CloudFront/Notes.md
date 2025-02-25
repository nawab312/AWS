Amazon CloudFront is a **content delivery network (CDN)** service provided by AWS that securely delivers data, videos, applications, and APIs to users with **low latency** and **high transfer speeds**. It uses a network of globally distributed **edge locations** to cache and serve content closer to end users.
- CloudFront has over **450 Points of Presence (PoPs)** across the globe, ensuring that content is served from a location nearest to the user.
- By caching static and dynamic content at edge locations, CloudFront reduces round-trip times and accelerates content delivery.
- Static Content (Images, Videos, CSS, JavaScript, etc.) is cached at edge locations.
- Dynamic Content (API responses, HTML pages) is delivered with **Lambda@Edge** or **Origin Shield**.
- Default TTL (Time-To-Live) in CloudFront is 24 hours (86,400 seconds).

![CloudFront Distribution](https://github.com/nawab312/AWS/blob/main/AWS_CloudFront/Images/Cloudfront_Distribution.png)

- **Origin** in an AWS CloudFront distribution is the source location from which CloudFront fetches content to serve to users. The origin can be an AWS service (like an S3 bucket or an EC2 instance) or an external web server. Types of Origins
    - Amazon S3 Bucket (for Static Content): Used to serve static assets like images, CSS, JavaScript, or HTML files. Example: `s3://my-bucket.s3.amazonaws.com`
    - Amazon EC2 or Load Balancer (for Dynamic Content): Example: `https://my-load-balancer.amazonaws.com`

- **Origin Path** in CloudFront is an optional configuration that specifies a subdirectory (path) in the origin from which CloudFront should fetch content. When you define an Origin Path, CloudFront automatically appends it to the origin domain name for every request.
  - S3 Bucket as Origin (Serving Content from a Specific Folder): Suppose you have an S3 bucket: `my-static-bucket.s3.amazonaws.com`. Inside the bucket, you have a folder: `/assets`. If you set Origin Path = `/assets`, CloudFront will fetch files from: `https://my-static-bucket.s3.amazonaws.com/assets/`
  - Web Server as Origin (Serving Content from a Specific Subdirectory): Suppose you have a website hosted at: `https://example.com`. Your images are stored in: `https://example.com/media`. If you set Origin Path = `/media`, CloudFront will automatically fetch from: `https://example.com/media/`
 
- **Edge Location** in AWS CloudFront is a geographically **distributed data center** where CloudFront caches copies of content to reduce latency and improve performance for end users. These locations are closer to users than the origin server (such as an S3 bucket, EC2 instance, or an HTTP server), allowing faster content delivery.

