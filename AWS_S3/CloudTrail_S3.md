If you're not seeing `DeleteObject` events in your CloudTrail logs, it's likely that **Data Events** for Amazon S3 are not enabled in your CloudTrail configuration. By default, CloudTrail logs **only Management Events (like bucket creation, IAM policy changes)** but not `Data Events` (like object-level operations such as `PutObject`, `GetObject`, `DeleteObject`)

**Verify If S3 Data Events Are Enabled**
Run the following AWS CLI command to check if S3 Data Events are enabled in your CloudTrail:

```bash
aws cloudtrail get-event-selectors --trail-name s3-logging-trail
```

```json
#Output

{
    "TrailARN": "arn:aws:cloudtrail:us-east-1:123456789012:trail/MyTrail",
    "EventSelectors": [
        {
            "ReadWriteType": "All",
            "IncludeManagementEvents": true,
            "DataResources": [
                {
                    "Type": "AWS::S3::Object",
                    "Values": ["arn:aws:s3:::your-bucket-name/"]
                }
            ]
        }
    ]
}
```
