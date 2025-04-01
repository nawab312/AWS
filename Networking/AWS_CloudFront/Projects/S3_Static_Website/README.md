## S3 Static Website with CloudFront ##
This project sets up a static website hosted on **Amazon S3** with **AWS CloudFront** as a CDN for improved performance, security, and caching.

![S3 Static Website](https://github.com/nawab312/AWS/blob/main/AWS_CloudFront/Projects/S3_Static_Website/Images/Static_Website_S3.png)

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

#### Access the Website using Cloudfront Distribution domain name ####
`https://d1vupevz38k2p1.cloudfront.net/index.html`

![MyWebsite](https://github.com/nawab312/AWS/blob/main/AWS_CloudFront/Projects/S3_Static_Website/Images/MyWebsite.png)

* Even after Deleting S3 Bucket Policy you will be able to access Cloudfront Domain Because of the Cache Content

* **CloudFront invalidation** is a process used to remove cached content from AWS CloudFront so that it fetches the latest version from the origin (e.g., S3, EC2, or any backend server).

* Create Invalidation from Cloudfront Console
![Invalidation](https://github.com/nawab312/AWS/blob/main/AWS_CloudFront/Projects/S3_Static_Website/Images/Invalidation.png)

* Now if you try to access `https://d1vupevz38k2p1.cloudfront.net/index.html` you will get `Access Invalid`
