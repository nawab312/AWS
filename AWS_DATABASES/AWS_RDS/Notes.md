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

