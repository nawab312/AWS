RDS is a managed DB service for DB use SQL as a query language. It allows you to create databases in the cloud that are managed by AWS.
Postgres, MySQL, MariaDB, Oracle, Microsoft SQL Server, IBM DB2, Aurora (AWS Proprietary database)

- **RDS – Storage Auto Scaling** Helps you increase storage on your RDS DB instance dynamically. When RDS detects you are running out of free database storage, it scales automatically. Avoid manually scaling your database storage

- **RDS Read Replicas for read scalability**
  - Up to 15 Read Replicas Within AZ, Cross AZ or Cross Region.
  - Replication is ASYNC(method of copying data from one system to another, but with a slight delay), so reads are eventually consistent. 
  - Replicas can be promoted to their own DB.
  - Applications must update the connection string to leverage read replicas
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

