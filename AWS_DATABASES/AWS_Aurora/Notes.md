- **AWS Proprietary Technology:** Aurora is a database engine built by Amazon and is not open-source. This means you can only use it within the AWS ecosystem.
- Compatibility with MySQL and PostgreSQL
- Key Features and Benefits
  - **Performance:** Aurora is advertised as "AWS cloud optimized" and boasts significant performance improvements over standard RDS (Relational Database Service) offerings
    - Up to 5x faster than MySQL on RDS
    - Up to 3x faster than PostgreSQL on RDS.
  - **Scalable Storage:** Aurora's storage automatically scales in 10GB increments as your data grows, up to a massive 128TB. You don't need to manually provision storage
  - **Fast Replication:** Aurora supports up to 15 read replicas, allowing you to distribute your database workload and improve read performance. The replication process is very fast, with a replica lag of less than 10ms.
  - **High Availability and Read Scaling**
 
### Easy Create Aurora MySQL Databases ###
- After Creating the Aurora MySQL DB You Get:

![image](https://github.com/user-attachments/assets/b20e2dec-875f-4d31-97b9-1c7c33faec46)

**Primary Instance (Writer):**
- This is the main database instance that handles both read and write operations. This corresponds to `database-1` (Regional Cluster).

**Replica Instance (Reader):**
- Aurora automatically creates a Read Replica if you selected *"Multiple instances"* during setup or enabled *Aurora Replicas*.
- This instance is used for Read Scaling and High Availability

**Why Two Instances?**
- Aurora MySQL follows a *Cluster-Based Architecture*, where a single cluster can have multiple instances (one writer, multiple readers).


