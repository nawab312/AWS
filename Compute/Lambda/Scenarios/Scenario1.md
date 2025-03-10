### Situation ###

Your company has a fleet of EC2 instances running a web application. To optimize costs, you want to automatically start and stop non-essential EC2 instances based on usage patterns. For example:
- Start EC2 instances at 8 AM when business hours begin.
- Stop EC2 instances at 8 PM when business hours end.
- Ensure that only specific instances (tagged as Environment: Dev) are affected.

**Question**
- How would you design a serverless solution using AWS Lambda to automate this process?
- Which AWS service(s) will you use to trigger the Lambda function at specific times?
- How will you ensure that only EC2 instances with the Dev environment tag are started/stopped?
- How can you make this solution fault-tolerant, ensuring that instances start/stop even if a Lambda execution fails?


### Solution ###

- **Designing a Serverless Solution with AWS Lambda**
  - Use AWS Lambda to execute start/stop commands on specific EC2 instances.
  - Use Amazon EventBridge (CloudWatch Events) to trigger the Lambda function at specific times (8 AM for start, 8 PM for stop).
  - Use EC2 Tags (e.g., Environment: Dev) to filter and affect only the relevant instances.
- **Triggering the Lambda Function**
  - I would create two EventBridge rules:
    - Rule 1: Triggers Lambda at 8 AM to start instances.
    - Rule 2: Triggers Lambda at 8 PM to stop instances.
  - The EventBridge rule would invoke the Lambda function using a cron expression, e.g.:
    - `cron(0 8 * * ? *)`  → Runs at 8 AM UTC.
    - `cron(0 20 * * ? *)`  → Runs at 8 PM UTC.

```python
import boto3

def lambda_handler(event, context):
    ec2 = boto3.client('ec2', region_name='us-east-1')  # Change region as needed
    
    action = event.get('action')  # "start" or "stop"
    if action not in ["start", "stop"]:
        return {"status": "Invalid action"}
    
    # Filter EC2 instances with the "Environment: Dev" tag
    instances = ec2.describe_instances(
        Filters=[{"Name": "tag:Environment", "Values": ["Dev"]}]
    )

    instance_ids = [
        i["InstanceId"] 
        for r in instances["Reservations"] 
        for i in r["Instances"]
    ]

    if not instance_ids:
        return {"status": f"No instances found to {action}"}

    # Start or stop the instances
    if action == "start":
        ec2.start_instances(InstanceIds=instance_ids)
    else:
        ec2.stop_instances(InstanceIds=instance_ids)
    
    return {"status": f"Instances {action}ed", "InstanceIDs": instance_ids}
```

**Making the Solution Fault-Tolerant**
- Retries: Configure EventBridge rules to retry execution if Lambda fails.
- IAM Permissions: Ensure the Lambda function has `ec2:DescribeInstances`, `ec2:StartInstances`, and `ec2:StopInstances` permissions.

### Follow-Up: What if the Number of Instances Increases? ###
If the number of instances grows significantly, we might reconsider AWS Lambda due to its **concurrent execution limits (1000 per region by default)**. Alternatives:
- **AWS Systems Manager (SSM) Automation** – Can run bulk EC2 start/stop actions.
