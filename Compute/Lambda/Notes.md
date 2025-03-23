### Introduction to AWS Lambda ###
- Is a Serverless Compute Service that allows you to run code in response to events without provisioning or managing servers.
- It automatically scales by running code in response to incoming traffic or events, charging only for the time your code runs.

### Lambda Key Components ###
- *Runtime:* The environment in which your code runs (e.g., Node.js, Python, Java, etc.).
- *Handler:* The entry point to your function; it processes incoming events.
- *Triggers:* Events that invoke your Lambda function (e.g., API Gateway, S3, DynamoDB, EventBridge).
- *Execution Role:* An IAM role that grants permissions for Lambda to access AWS resources.

### Lambda Execution Model ###
**Stateless Nature of Lambda**
- AWS Lambda functions are stateless by default. This means that every time a function is triggered, it starts from scratch, without any memory of previous executions unless external state management (like DynamoDB or S3) is used.

**Concurrency in Lambda**
- Concurrency refers to how many instances of a Lambda function can run simultaneously. Lambda can handle multiple invocations at once. You can specify concurrency limits for a function (e.g., reserve concurrency).
  - What are the concurrency limits for AWS Lambda functions?
    - Default Account-Level Limit: 1,000 concurrent executions across all functions in a specific AWS Region.
    - Function-Level Limit: You can set a specific concurrency limit for individual functions to reserve capacity.
    - Increasing the Limit: You can request a quota increase for your account or specific functions through the AWS Service Quotas console.
  -  How can you increase the concurrency limit for a specific function
    - To increase the concurrency limit for a specific function, you can use *Provisioned Concurrency*. This allows you to reserve a specific number of concurrent executions for your function, ensuring it can handle higher traffic loads without being throttled
 
### Types of Lambda Invocation ###
**Synchronous Invocation**
- In a synchronous invocation, the caller waits for the Lambda function to finish executing and returns the result of the execution. The caller is blocked until the Lambda function finishes processing.
- The Lambda function returns a response directly to the caller after execution completes. The response includes the result of the execution, and the caller can process it accordingly.
  - Example: API Gateway invokes a Lambda function synchronously and waits for the result to send the response back to the client.
- *Error Handling* If the Lambda function fails (throws an error), the caller receives the error message directly in the response.

**Asynchronous Invocation**
- In an asynchronous invocation, the caller does not wait for the Lambda function to finish. The function is triggered, and the caller is immediately returned a success message, while the function continues executing in the background.
- The function does not return any result to the caller. Instead, the invocation is considered successful once the event is passed to Lambda, and the actual processing happens independently. If the function fails, AWS retries the execution (with a backoff strategy).
  - Example: S3 events trigger Lambda functions asynchronously, and S3 doesn’t wait for the result.
- *Error Handling* If the function fails, AWS Lambda will retry the execution of the function twice (by default), and if it continues to fail, the event is sent to a dead letter queue (DLQ) or logged in CloudWatch for troubleshooting.

### Lambda Function Configuration ###
- **Memory:** You can configure the memory allocated to your Lambda function, which also affects CPU power. Memory ranges from 128 MB to 10 GB
- **Timeout:** Lambda functions have a max timeout of 15 minutes (900 seconds).
- **Environment Variables:** Lambda functions can be configured with environment variables to store sensitive data or configurations that the function needs.

### Execution Context & Optimization ###
AWS Lambda maintains an execution environment that includes: Code and libraries, Temporarystorage (500 MB in /tmp), Network connections. This context is reused across invocations to optimize performance.

### Cold Starts in Lambda ###
- A cold start in AWS Lambda refers to the initial delay experienced when a Lambda function is invoked for the first time or after being idle for a period.
- During this time, AWS needs to *allocate resources, deploy the function code, and initialize the runtime environment*, leading to increased invocation times. Mitigation:
  - Use *Provisioned Concurrency to reduce cold starts*.

### Example Lambda Function ###
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
 
### When to Use EC2 Over AWS Lambda ###
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

### AWS Lambda Real-World Scenarios ###
 
- **Scenario 1: Start and Stop EC2 Instances Based on Time**
  - https://github.com/nawab312/AWS/blob/main/Compute/Lambda/Scenarios/Scenario1.md

- **Scenario 2: Logging Metadata of S3 Uploaded Files to CloudWatch**
  - https://github.com/nawab312/AWS/blob/main/Compute/Lambda/Scenarios/Scenario3.md
