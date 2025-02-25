## S3 Static Website with CloudFront ##
This project sets up a static website hosted on **Amazon S3** with **AWS CloudFront** as a CDN for improved performance, security, and caching.

### Architecture ###
- Upload HTML File to S3 Bucket
- Configure S3 Static Website Hosting
- Set up CloudFront distribution with S3 as the origin
- Configure OAC (Origin Access Control) to secure S3

### Deployment Steps ###

#### Create an S3 Bucket for Static Website ####
- Go to AWS S3 Console → Create a bucket `my-website-bucket-sid-312`
- Enable "Block all public access"
- Upload your static website file (index.html)
- Keep Rest as Default

#### Secure S3 with Origin Access Control (OAC) ####
- Go to AWS CloudFront Console → Security → Origin Access
- Click on Create Control Setting
- Give Name `my-website-bucket-sid-312.s3.us-east-1.amazonaws.com` and Origin Type `S3`
- Keep Rest as Default

#### Create a CloudFront Distribution ####
- Go to CloudFront Console → Click Create Distribution
- Origin Domain Name → Select your S3 bucket `my-website-bucket-sid-312.s3.us-east-1.amazonaws.com`
- Origin Access → Origin access control settings → Choose your created OAC
- Set Viewer Protocol Policy: `Redirect HTTP to HTTPS`
- Click Create Distribution
- Web Application Firewall (WAF): `Do not enable security protections`

#### Update S3 Bucket Policy ####
```json
{
	"Version": "2012-10-17",
	"Statement": [
		{
			"Sid": "PublicReadGetObject",
			"Effect": "Allow",
			"Principal": {
				"Service": "cloudfront.amazonaws.com"
			},
			"Action": "s3:GetObject",
			"Resource": "arn:aws:s3:::my-website-bucket-sid-312/*",
			"Condition": {
				"StringEquals": {
					"AWS:SourceARN": "arn:aws:cloudfront::961341511681:distribution/E1CVL7UCR4ON28"
				}
			}
		}
	]
}
```
