RDS is a managed DB service for DB use SQL as a query language. It allows you to create databases in the cloud that are managed by AWS.
Postgres, MySQL, MariaDB, Oracle, Microsoft SQL Server, IBM DB2, Aurora (AWS Proprietary database)

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

- **Connection pooling** is a technique where a set of database connections is maintained and reused, reducing the overhead of repeatedly opening and closing connections for each database request.

- **Amazon RDS Proxy**
  - Amazon RDS Proxy is a service provided by AWS that acts as a middle layer between your application and the Amazon RDS (Relational Database Service). In simple terms, it helps manage the connection between your app and the database more efficiently.
  - **Improved Connection Management:** When your application needs to talk to a database, it opens a connection. Normally, each request to the database needs a new connection, which can quickly become slow and difficult to manage if there are many requests. RDS Proxy helps by pooling and reusing database connections, so your app doesn't need to constantly create new ones. This speeds up performance.
  - **Scalability:** When your app gets more traffic, RDS Proxy can handle a larger number of connections to the database without putting too much strain on the database itself. This helps your app scale more easily as it grows.
  ![image](https://github.com/user-attachments/assets/a175a223-2b9d-41db-85a7-7325ccdd3052)


### Scenario 1 ###
Your company is running a production PostgreSQL database on AWS RDS. Suddenly, the application team reports increased query latency, and some transactions are failing.
- **Question**  How would you diagnose and resolve performance issues in AWS RDS, ensuring minimal downtime?
- **Follow-ups:**
  - What AWS RDS monitoring tools would you use to identify the root cause?
  - How would you scale RDS to handle increased traffic?

**Diagnosing and Resolving Performance Issues in AWS RDS (PostgreSQL)**
- **Identifying the Root Cause** Leverage the following AWS RDS monitoring tools:
  - **Amazon CloudWatch Metrics:** Check `CPUUtilization`, `ReadIOPS`, `WriteIOPS`, and `DBConnections` to identify resource bottlenecks. Monitor *FreeableMemory* and *SwapUsage* to detect memory pressure.
  - **Performance Insights:** Identify slow queries and high wait times. Analyze database load by top SQL statements, users, and hosts.
- **Resolving Performance Issues** Once I identify the issue, I would take the following actions based on the root cause:
  - **High CPU Usage**
    - Scale up the instance to a larger *instance type (vertical scaling)* if CPU is consistently high.
    - Optimize slow queries by adding indexes or rewriting queries.
    - Enable *connection pooling* to manage database connections efficiently.
  - **High Disk I/O**
    - If disk usage is high, consider upgrading *storage type (e.g., from GP2 to GP3 or provisioned IOPS)*.
  - **High Memory Usage**
    - Increase instance class if memory pressure is observed.
    - Tune PostgreSQL parameters like `work_mem`, `shared_buffers`, and `effective_cache_size` to optimize memory allocation.
  - **Too Many Connections Leading to Failures**
    - Check and adjust *max_connections* in PostgreSQL parameters.
    - Implement *read replicas* to distribute read queries.
  - **Network Latency Issues**
    - Check VPC, subnet, and security group configurations to ensure proper connectivity.
    - Enable *Amazon RDS Proxy* to improve database connection handling.
- **Scaling the RDS Instance to Handle Increased Traffic**
  - Vertical Scaling (Instance Upgrade): Move to a higher instance class (e.g., from `db.m5.large` to `db.m5.xlarge`).
  - Horizontal Scaling (Read Replicas):
    - Create *RDS Read Replicas* and modify the application to route read queries to replicas.
    - Enable *Aurora Auto Scaling* if using Amazon Aurora.
  - Implement Database Caching:
    - Use *Amazon ElastiCache (Redis/Memcached)* to reduce direct database queries.

### Scenario 2 ###
Your company runs a MySQL RDS instance in a Multi-AZ deployment. Suddenly, the primary database instance crashes, but the application experiences a downtime of several seconds before it reconnects.
- **Questions**
  - How does AWS RDS Multi-AZ work in a failover scenario?
  - Why might the application experience downtime even with Multi-AZ enabled?
  - What steps would you take to minimize downtime in such cases?
 
**How Does AWS RDS Multi-AZ Work in a Failover Scenario?**

AWS RDS Multi-AZ provides *high availability and automatic failover* by maintaining a *synchronous standby replica* in a different Availability Zone (AZ). Here's how it works during a failover:
- When the primary RDS instance fails (due to hardware failure, OS crash, or AZ outage), AWS automatically promotes the standby instance to primary.
- The RDS endpoint remains the same, so applications do not need to change the connection string.
- The failover process usually takes *30-60 seconds* (sometimes longer) depending on database activity and uncommitted transactions.

**Why Might the Application Experience Downtime Even with Multi-AZ?**
- **DNS Propagation Delay:** AWS RDS updates the DNS to point to the new primary instance, but applications using cached DNS records may take longer to reconnect.
- **Uncommitted Transactions:** Any in-flight transactions on the failed primary instance are rolled back, requiring applications to handle retries.
- **Connection Pool Issues:** If the application does not properly handle database connection failures, it might not immediately reconnect to the new primary instance.
- **Failover Time:** AWS RDS typically takes 30-60 seconds to complete failover, during which new connections might fail.

**Steps to Minimize Downtime in Multi-AZ Failovers**
- **Application-Level Optimizations:**
  - Use Retry Logic: Implement *exponential backoff* in database connection logic to automatically retry failed queries.
  - Reduce DNS Cache TTL: Set a *lower TTL (e.g., 30 seconds)* for database hostname resolution to ensure faster reconnection.
  - Use Connection Poolers: Utilize tools like HikariCP (for Java applications) to detect failures and re-establish connections quickly.
- **RDS & AWS Configurations:**
  - Enable RDS Proxy: AWS RDS Proxy maintains persistent connections and automatically reroutes them to the new primary instance.

