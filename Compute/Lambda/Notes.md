**ServerLess:** is a cloud computing model that allows developers to build and run applications without having to manage server infrastructure. What Defines Serverless?
- No servers to provision or manage
- Automatically scales with usage
- Never pay for idle
 
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
