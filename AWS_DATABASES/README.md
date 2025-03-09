## Types of Databases in AWS ##

### Relational Databases (SQL-based) ###
Used when data requires structured storage with ACID (Atomicity, Consistency, Isolation, Durability) compliance.
- **Amazon RDS (Relational Database Service)**
  - Fully managed SQL database service.
  - Supports multiple database engines:
    - Amazon Aurora (MySQL & PostgreSQL compatible, AWS’s high-performance database)
    - MySQL, PostgreSQL, MariaDB, Oracle, Microsoft SQL Server
  - Automated backups, patching, and scaling.
- **Amazon Aurora**
  - AWS's proprietary database, compatible with MySQL & PostgreSQL.
  - Offers better performance than standard MySQL/PostgreSQL.
  - Replication across multiple availability zones (AZs) for high availability.
  - Serverless option available for automatic scaling.

### NoSQL Databases (Non-Relational, Schema-less) ###
Used when handling large volumes of unstructured, semi-structured, or schema-flexible data.
- **Amazon DynamoDB**
  - Fully managed key-value and document database.
  - Serverless, automatically scales up/down.
  - Multi-region replication and in-memory caching (DAX).
- **Amazon ElastiCache**
  - Managed caching service to speed up application performance.
  - Supports:
    - **Redis** (In-memory data store)
    - **Memcached** (Simple, high-performance caching system)

### Amazon Redshift ###
Used for business intelligence and big data analytics.
- **Amazon Redshift**
  - Fully managed data warehouse.
  - Uses columnar storage for high-performance analytics.
  - Integrates with BI tools like AWS QuickSight, Tableau, and Power BI.
