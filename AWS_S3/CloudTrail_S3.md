## Track S3 Bucket Access with CloudTrail ##

Let's say you have an **S3 bucket** named `example-bucket-siddy-312`

### Enable AWS CloudTrail for S3 ###
- Go to the **AWS Console → CloudTrail**. Click on **Create Trail**.
- Provide a Trail Name (e.g., `s3-access-log-trail`)
- Enable "Event Type" as Management & Data Events:
    - **Management Events:** Logs administrative actions (e.g., bucket creation, deletion).
    - **Data Events:** Logs actions on objects (e.g., PutObject, GetObject, DeleteObject).
- Create the CloudTrail

![image](https://github.com/user-attachments/assets/1d7078fb-92e7-4f16-9b3b-6f05833e8915)

![image](https://github.com/user-attachments/assets/b34daa5c-5f04-4745-a6cb-0798247d3098)

### View CloudTrail Logs for S3 Events ###

**Management Events**
- Where are they stored?
    - Visible directly in the **CloudTrail Console** (`Event History tab`).
    - `Event history shows you the last 90 days of management events.` -> *Written on AWS Event History Tab*
![image](https://github.com/user-attachments/assets/2cbf58fe-4a05-4cbd-b975-88d14f4acbf8)

**Data Events**
- Where are they stored?
    - Not shown in the CloudTrail console (Event History tab).
    - Stored in S3 under: `s3://<your-cloudtrail-bucket>/AWSLogs/<account-id>/CloudTrail/<region>/YYYY/MM/DD/`
- Examples S3 object-level actions (`PutObject`, `GetObject`, `DeleteObject`)

![image](https://github.com/user-attachments/assets/80bda5ce-962a-4a87-bb1e-08ee67dec1c2)

### Download All JSON Files for a Specific Date from S3 ###

- Download All Log Files for That Date
```bash
aws s3 cp s3://aws-cloudtrail-logs-28022025/AWSLogs/961341511681/CloudTrail/us-east-1/2025/02/28 ./cloudtrail_logs_sid/ --recursive
```

- Extract All `.json.gz` Files
```bash
cd cloudtrail_logs_sid
gunzip *.json.gz
```

- Merge and Analyze Logs
```bash
jq -s '.' cloudtrail_logs_sid/*.json > merged_logs.json
```



