- Get the Function ARN:
```python
context.invoked_function_arn
```

### BOTO3 RDS ###
- Create a Manual snapshot of an RDS Database Instance.
```python
rds.create_db_snapshot(
    DBInstanceIdentifier='your-db-instance-id',
    DBSnapshotIdentifier='your-snapshot-id'
)
```

### BOTO3 S3 ###
- Connect to S3
```bash
s3_client = boto3.client("s3")
```

- Listing Buckets
```bash
response = s3_client.list_buckets()
print(response)
```

- What is inside response?
```json
{
  "Buckets": [
    {"Name": "my-bucket-1", "CreationDate": "2024-03-25T12:00:00Z"},
    {"Name": "my-bucket-2", "CreationDate": "2024-03-20T15:30:00Z"}
  ],
  "Owner": {"DisplayName": "my-name", "ID": "abcd1234"}
}
```

- To print only the Bucket names:
```bash
for bucket in response["Buckets"]:
    print(bucket["Name"])
```
