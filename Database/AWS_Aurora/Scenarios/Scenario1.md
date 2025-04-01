Amazon Aurora supports **Global Databases**, allowing a single database to span multiple AWS regions. Suppose you have an **Aurora PostgreSQL Global Database** deployed across two regions: **Primary (us-east-1)** and **Secondary (eu-west-1)**.
- If the **Primary Region (us-east-1) fails completely**, how do you **promote the Secondary Region (eu-west-1) to become the new primary?**
- What happens to replication lag during a **region-wide network disruption**, and how does Aurora handle it upon recovery?
- How does **Aurora's storage architecture** enable low-latency replication across regions, and what are the potential trade-offs?

---

**Promoting the Secondary Region (eu-west-1) to Primary**

If the *Primary Region (us-east-1) fails completely*, you need to *failover* to the secondary region manually (Aurora Global Database does not perform automatic failover across regions).
- Stopping Replication from the Primary
- Promote the Secondary Cluster in `eu-west-1` to a *Standalone Primary*.
- Redirect application traffic to the new primary using *Route 53* or *application-level changes*.
Aurora Global Database supports fast region-level failover (typically <1 min) by keeping read replicas in multiple regions. However, the failover is manual and requires DNS updates or application changes.

**Replication Lag During a Network Disruption**
- If the network between *us-east-1 (Primary) and eu-west-1 (Secondary)* is disrupted, the secondary region *cannot receive updates* from the primary.
- Aurora continues to accept *writes* in the primary region, and these transactions *queue up* for replication once connectivity is restored.
- If the *lag grows too large*, queries on the secondary region may return *stale data* until the backlog catches up.
- Aurora provides *lag monitoring metrics* (`aurora_replica_lag` in CloudWatch), which helps detect issues early.

**How Aurora’s Storage Architecture Enables Low-Latency Replication**

Aurora uses a *distributed storage architecture* that separates *compute (DB instances)* from *storage (replicated storage across 6 copies in 3 AZs per region)*.

For cross-region replication:
- Aurora *does not replicate binary logs* like traditional databases (e.g., MySQL). Instead, it replicates *redo logs* asynchronously across regions, which is *faster and more efficient.*
- Each write operation is replicated at the *storage level*, reducing the amount of data transmitted across regions.
- This ensures low-latency replication (often <1 second) and fast recovery in case of a failover.

Trade-offs:
- *Write latency increases slightly* when using a Global Database due to cross-region coordination.
- Network costs are incurred for cross-region replication.
- Failover is not automatic, requiring manual intervention.
