**ServerLess:** is a cloud computing model that allows developers to build and run applications without having to manage server infrastructure. What Defines Serverless?
- No servers to provision or manage
- Automatically scales with usage
- Never pay for idle

**Lambda’s Key Components**
- *Runtime:* The environment in which your code runs (e.g., Node.js, Python, Java, etc.).
- *Handler:* The entry point to your function; it processes incoming events.
- *Triggers:* Events that invoke your Lambda function (e.g., API Gateway, S3, DynamoDB, EventBridge).
- *Execution Role:* An IAM role that grants permissions for Lambda to access AWS resources.

- **Execution Context** AWS Lambda maintains an execution environment that includes: Code and libraries, Temporarystorage (500 MB in /tmp), Network connections. This context is reused across invocations to optimize performance.

- **Cold Starts**
 - A cold start in AWS Lambda refers to the initial delay experienced when a Lambda function is invoked for the first time or after being idle for a period.
 - During this time, AWS needs to *allocate resources, deploy the function code, and initialize the runtime environment*, leading to increased invocation times. Mitigation:
   - Use *Provisioned Concurrency to reduce cold starts*.

**String Capitalization Function**
```python
#function

def lambda_handler(event, context):
    text = event.get("text", "")
    capital_text = text.upper()
    return {
        'statusCode': 200,
        'body': capital_text
    }
```
- Event Payload
  ```json
  {
      "text": "value"
  }
  ```
 
**When to Use EC2 Over AWS Lambda**
- **Long-Running Workloads**
  - Lambda Limitation: A function can run for a maximum of 15 minutes.
  - EC2 Advantage: No runtime limit—you can run continuous, long-running processes.
  - Example: Running a machine learning model that takes 30 minutes to train.
- **Stateful Applications**
  - Lambda Limitation: AWS Lambda is stateless by design, meaning it does not persist data between executions. Each time a Lambda function is invoked, it runs in a new execution environment, and any in-memory data (session, variables, cache) is lost once the function completes.
  - EC2 instances: Are stateful, meaning they can maintain persistent connections, in-memory storage, and long-lived sessions.
  - Example: A multiplayer online game server that needs to maintain player sessions.
- **Heavy & Frequent Requests**
  - Lambda Limitation: Has a cold start issue (delay when first invoked). Has an invocation limit (concurrent execution limits).
  - EC2 Advantage: No cold starts, and you can handle unlimited concurrent requests.
  - Example: A 24/7 real-time stock market data API that serves thousands of requests per second.
 
- **Start and Stop EC2 instances based on Time** https://github.com/nawab312/AWS/blob/main/Compute/Lambda/Scenarios/Scenario1.md
