If you're not seeing `DeleteObject` events in your CloudTrail logs, it's likely that **Data Events** for Amazon S3 are not enabled in your CloudTrail configuration. By default, CloudTrail logs **only Management Events (like bucket creation, IAM policy changes)** but not `Data Events` (like object-level operations such as `PutObject`, `GetObject`, `DeleteObject`)

**Verify If S3 Data Events Are Enabled**
Run the following AWS CLI command to check if S3 Data Events are enabled in your CloudTrail:

```bash
aws cloudtrail get-event-selectors --trail-name s3-logging-trail
```

```json
#Output

{
    "TrailARN": "arn:aws:cloudtrail:us-east-1:961341511681:trail/s3-logging-trail",
    "AdvancedEventSelectors": [
        {
            "Name": "S3-AllEvents",
            "FieldSelectors": [
                {
                    "Field": "eventCategory",
                    "Equals": [
                        "Data"
                    ]
                },
                {
                    "Field": "resources.type",
                    "Equals": [
                        "AWS::S3::Object"
                    ]
                }
            ]
        },
        {
            "Name": "Management events selector",
            "FieldSelectors": [
                {
                    "Field": "eventCategory",
                    "Equals": [
                        "Management"
                    ]
                }
            ]
        }
    ]
}

```

- If `DataResources` is missing or empty, then S3 Data Events are NOT enabled.
- Our `CloudTrail Advanced Event Selectors` are correctly set up to capture:
    - **S3 Data Events** (object-level operations like `PutObject`, `GetObject`, `DeleteObject`)
    - **Management Events** (bucket-level changes like `CreateBucket`, `DeleteBucket`, `PutBucketPolicy`)
