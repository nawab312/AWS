RDS is a managed DB service for DB use SQL as a query language. It allows you to create databases in the cloud that are managed by AWS.
Postgres, MySQL, MariaDB, Oracle, Microsoft SQL Server, IBM DB2, Aurora (AWS Proprietary database)

- **Default RDS Ports By Data Engines**
  - MySQL / MariaDB: 3306
  - PostgreSQL: 5432
  - Oracle: 1521
  - SQL Server: 1433
  - Amazon Aurora (MySQL-compatible): 3306
  - Amazon Aurora (PostgreSQL-compatible): 5432

- **RDS – Storage Auto Scaling** Helps you increase storage on your RDS DB instance dynamically. When RDS detects you are running out of free database storage, it scales automatically. Avoid manually scaling your database storage

- **RDS Read Replicas for read scalability**
  - Up to 15 Read Replicas Within AZ, Cross AZ or Cross Region.
  - Replication is ASYNC(Method of Copying Data from One System to Another, but with a Slight Delay), so reads are eventually consistent. 
  - Replicas can be promoted to their own DB.
  - Applications must update the Connection String to leverage Read Replicas
  - Example: RDS Read Replicas – Use Case
    - You have a production database that is taking on normal load. You want to run a reporting application to run some analytics. You create a Read Replica to run the new workload there. The production application is unaffected. Read replicas are used for SELECT (=read) only kind of statements (not INSERT, UPDATE, DELETE)
  - **RDS Read Replicas – Network Cost**
    - In AWS there’s a network cost when data goes from one AZ to another. *For RDS Read Replicas within the same region, you don’t pay that fee*
    - Diagaram:  ![image](https://github.com/user-attachments/assets/2dc36c4b-c1f2-4d9b-ba05-3aa1d592a396)

- **RDS Multi-AZ**
  - Amazon RDS Multi-AZ is a high-availability feature that provides *automatic failover* to a standby instance in a different *Availability Zone (AZ)* in case of a primary database failure. It ensures *data durability and minimal downtime* for critical applications.
  - How Does Multi-AZ Work?
    - When you enable Multi-AZ, Amazon RDS automatically creates a *standby replica* of your database in a different Availability Zone.
    - The primary and standby instances use *synchronous replication* to ensure *real-time data consistency*.
    - If the primary instance fails (e.g., hardware failure, AZ outage, or maintenance), AWS automatically switches to the standby instance with minimal disruption
    - The *endpoint remains the same*, so no application changes are required during failover.
  - Application Experience Downtime Even with Multi-AZ because:
    - DNS Propagation Delay: AWS RDS updates the DNS to point to the new primary instance, but applications using cached DNS records may take longer to reconnect.
    - Uncommitted Transactions: Any in-flight transactions on the failed primary instance are rolled back, requiring applications to handle retries.
    - Connection Pool Issues: If the application does not properly handle database connection failures, it might not immediately reconnect to the new primary instance.
    - Failover Time: AWS RDS typically takes 30-60 seconds to complete failover, during which new connections might fail.
  - Steps to Minimize Downtime in Multi-AZ Failovers
    - Application-Level Optimizations:
      - Use Retry Logic: Implement exponential backoff in database connection logic to automatically retry failed queries.
      - Reduce DNS Cache TTL: Set a lower TTL (e.g., 30 seconds) for database hostname resolution to ensure faster reconnection.
      - Use Connection Poolers: Utilize tools like HikariCP (for Java applications) to detect failures and re-establish connections quickly.
    - RDS & AWS Configurations:
      - Enable RDS Proxy: AWS RDS Proxy maintains persistent connections and automatically reroutes them to the new primary instance.

- **Connection pooling** is a technique where a set of database connections is maintained and reused, reducing the overhead of repeatedly opening and closing connections for each database request.

- **RDS Security** https://github.com/nawab312/AWS/blob/main/AWS_DATABASES/AWS_RDS/RDS_SECURITY.md

- **Amazon RDS Proxy**
  - Amazon RDS Proxy is a service provided by AWS that acts as a middle layer between your application and the Amazon RDS (Relational Database Service). In simple terms, it helps manage the connection between your app and the database more efficiently.
  - **Improved Connection Management:** When your application needs to talk to a database, it opens a connection. Normally, each request to the database needs a new connection, which can quickly become slow and difficult to manage if there are many requests. RDS Proxy helps by pooling and reusing database connections, so your app doesn't need to constantly create new ones. This speeds up performance.
  - **Scalability:** When your app gets more traffic, RDS Proxy can handle a larger number of connections to the database without putting too much strain on the database itself. This helps your app scale more easily as it grows.
  ![image](https://github.com/user-attachments/assets/a175a223-2b9d-41db-85a7-7325ccdd3052)

---

**RDS Monitoring**

Key RDS Monitoring Tools

*Amazon CloudWatch Metrics*
- CPUUtilization → High values indicate heavy query load.
- FreeableMemory → It is the amount of unused memory (RAM) available in your RDS instance. Low values indicate possible memory bottlenecks.
- ReadIOPS / WriteIOPS → High values indicate heavy disk usage.
- DatabaseConnections → Tracks active connections.
- ReplicaLag → Measures the delay between the primary database (master) and its read replicas in RDS.
- SwapUsage → It refers to the amount of disk space being used as a temporary substitute for RAM when your system runs out of memory (RAM). If SwapUsage is HIGH, it means:
  - The database is running out of memory (RAM) and is relying on the disk to store data temporarily.
  - Disk is much slower than RAM, so using swap space leads to performance degradation (slow queries, lag, etc.).

Use CloudWatch Alarms to notify when thresholds are exceeded

*RDS Performance Insights*

Amazon RDS Performance Insights is a powerful tool that helps you monitor and analyze the performance of your RDS database. It provides deep insights into query execution times, wait events, and overall database load. This helps you identify performance bottlenecks, optimize queries, and troubleshoot issues more effectively. Key Features of RDS Performance Insights:
- Top SQL Queries
  - Shows which queries are consuming the most resources.
  - Helps identify slow-running queries that could be optimized.
  - Great for query tuning and figuring out which queries need indexing or rewriting.
- Wait Events
  - Wait events show what the database is waiting on (e.g., CPU, I/O, locking).
  - Common wait events include:
    - CPU wait: Indicates high CPU usage.
    - I/O wait: Indicates slow disk or database access.
    - Lock wait: Indicates blocking issues where one query is waiting for another to finish.
- Load Graphs
  - Provides a visual representation of your database's load over time.
  - Helps you spot spikes in load, trends, and patterns related to high traffic or query issues.
- Top Waits and Host Metrics
  - You can also see the system-level metrics, like CPU usage and disk I/O, alongside database-specific information.
  - Helps identify if the issue is at the database or system level.
 
*Enhanced Monitoring*
Enhanced Monitoring provides detailed operating system (OS) level metrics for your RDS instances, allowing you to gain deeper visibility into the performance of your database. This goes beyond the basic CloudWatch metrics and gives you real-time, granular data about CPU usage, memory usage, disk I/O, and more, at a 1-second granularity. Key Features of Enhanced Monitoring:
- Real-Time OS Metrics. Enhanced Monitoring gives you real-time statistics for the operating system that your RDS instance is running on. These include:
  - CPU Utilization per core
  - Memory Usage (Free, Used, Swap)
  - Disk I/O (Reads/Writes and Latency)
  - Network Traffic (Incoming/Outgoing)
  - Processes (Which processes are consuming the most resources)
- Granular Data
  - Unlike CloudWatch metrics (which provide data at 1-minute intervals), Enhanced Monitoring gives you data at 1-second intervals, providing more accurate and detailed insights into the system's behavior.
- Process-Level Metrics
  - You can also see which processes are consuming the most resources on the instance. This is helpful for identifying runaway processes or queries that are hogging CPU or memory.
 
*RDS Logs (CloudWatch Logs & Console Logs)*

AWS RDS Logs are important tools for troubleshooting and monitoring your RDS databases. Logs provide detailed information about the database's activities, including errors, slow queries, and general operations. By using CloudWatch Logs and Console Logs, you can easily access and analyze this data to identify and resolve issues. Types of RDS Logs:
- Error Logs
  - What it shows: Logs any critical errors or issues within the database, such as crashes, startup failures, or connection issues.
  - Why it’s important: Helps you identify problems like database corruption, crash recovery, or failed start-ups.
  - Example of use: If your database instance is failing to restart, the error log can tell you why.
- Slow Query Logs
  - What it shows: Logs queries that take longer than a specified threshold to execute.
  - Why it’s important: Helps you identify inefficient or long-running queries, which can cause performance bottlenecks.
  - Example of use: You notice your app is slow. Checking the slow query log reveals a query taking several seconds, which you can then optimize.
- General Logs
  - What it shows: Records every query executed on the database, regardless of whether it’s slow or not.
  - Why it’s important: Helps with debugging issues in the database by giving a full list of activities, including the queries that are being executed.
  - Example of use: If you suspect there’s a security issue (e.g., unauthorized access), the general log can provide a complete list of all executed commands.
- Audit Logs (for compliance)
  - What it shows: Records who did what on the database—such as user logins, changes to database objects, or grants/revokes of privileges.
  - Why it’s important: Ensures that all changes are tracked for security audits and compliance purposes.
  - Example of use: If you need to track which users have modified sensitive data, the audit logs can help you trace those changes.
 
How to Access RDS Logs:
- Viewing Logs in CloudWatch
- Viewing Logs in the AWS Console under RDS
- Using AWS CLI to Retrieve Logs:
  ```bash
  aws rds describe-db-log-files --db-instance-identifier mydb-instance
  ```
  - This will give you a list of available logs. You can download any log using:
  ```bash
  aws rds download-db-log-file-portion --db-instance-identifier mydb-instance --log-file-name error/mysql-error-running.log --starting-token 0 --output text
  ```

*Amazon RDS Proxy Monitoring*

Key Metrics for Monitoring RDS Proxy:
- Active Connections
  - What it shows: The number of active connections that RDS Proxy is maintaining to the database.
  - Why it's important: Helps you monitor how many connections are in use. If you see unusually high numbers, it could indicate connection bottlenecks, which might need to be optimized (e.g., increasing the proxy's connection pool size or adjusting connection management).
- Database Connections
  - What it shows: The number of connections RDS Proxy is making to the database.
  - Why it's important: If the number of database connections grows too high, it can cause database performance issues (e.g., throttling, slow queries). Monitoring this helps ensure that the proxy is managing database connections efficiently.
- Idle Connections
  - What it shows: The number of idle connections maintained by RDS Proxy.
  - Why it's important: If too many idle connections are open, it can waste database resources. Ideally, RDS Proxy should only maintain the number of connections that are actively being used by your application.
- Connection Pooling Statistics
  - What it shows: Information about how effectively RDS Proxy is pooling database connections. This includes how many connections are available versus in use.
  - Why it's important: Helps you understand whether RDS Proxy is optimally reusing connections or if there’s too much overhead in creating new ones, which can lead to delays in requests.
- Query Execution Time
  - What it shows: The amount of time queries take to execute through RDS Proxy.
  - Why it's important: Long query times may indicate issues with your application or database performance, and monitoring query execution time can help you identify slow-performing queries that may need optimization.
- Failed Connection Attempts
  - What it shows: The number of failed connection attempts made through RDS Proxy to the database.
  - Why it's important: A high number of failed connection attempts could indicate misconfigurations, or issues with network connectivity, or database resource limitations that are preventing connections from being established.
- Proxy Failures
  - What it shows: The number of failures on the proxy level, such as proxy outages or failures to forward requests to the database.
  - Why it's important: This can highlight problems with the RDS Proxy service itself. Monitoring proxy failures helps identify and respond to issues before they impact application performance.

---



 
