### Blue - Green ###

**Step-by-Step Architecture**
- Create Two Identical Environments
  - Blue → Current Production. Green → New Version
  - Each environment has: EC2 / Auto Scaling Group or ECS service, Same VPC, Subnets, Same Security Groups, Same Database (or compatible version)
- Use an Application Load Balancer
  - Blue → Target Group A, Green → Target Group B
- Deploy New Version to Green
  - Deploy code to Green ASG / ECS service
  - Run health checks. Validate logs & metrics
- Switch Traffic
  - Change listener rule to forward traffic from Blue TG → Green TG OR
  - Change weight from 100/0 → 0/100 (if weighted routing)
 
**Blue-Green and DB Risks**
- Blue-green assumes: “I can switch traffic back anytime.”
- That assumption is false if your database change is not backward compatible.

Breaking Schema Changes (Rollback Becomes Impossible)
- You deploy Green. Green changes the schema (drop column, rename column, add NOT NULL without default, change datatype). Green starts writing data in the new format. You detect a bug. You switch traffic back to Blue.
- Blue now:
  - Can’t read new data
  - Fails on inserts
  - Crashes on queries
- The Correct Solution: Expand → Migrate → Contract
  - Expand (Make the DB More Flexible, Not Different)
    - Introduce new structure without breaking the old app. You are only allowed to: Add nullable columns, Add new tables, Add indexes
    - You are NOT allowed to: Drop columns, Rename columns, Change datatypes, Add NOT NULL constraints
    - Example: Current schema: `users(id, full_name)`, You want: `users(id, first_name, last_name)`
    - Expand step:
      ```sql
      ALTER TABLE users ADD COLUMN first_name TEXT;
      ALTER TABLE users ADD COLUMN last_name TEXT;
      ```
  - Migrate (Move Data Safely)
    - Options: Background job, One-time migration script, Dual-write logic in application
    - Example: Parse `full_name`. Populate `first_name` and `last_name`
    - At this stage: Green reads from new fields. Blue still reads from old field
  - Contract (Remove Old Structure Later)
    - Only after: All traffic is on Green. Migration completed. No rollback risk
    - ```sql
      ALTER TABLE users DROP COLUMN full_name;
      ALTER TABLE users ALTER COLUMN first_name SET NOT NULL;
      ```
    - This is irreversible. So it must happen in a *separate release cycle*. Never in same deploy as Expand.
   
Data Mutation During Green (Irreversible Writes)
- When you deploy Green (new version), it may start writing data in a new format or with new rules. If you later rollback to Blue (old version), Blue may not understand that new data.
- Example:
  - Blue version understands only:
    ```bash
    status = PENDING
    status = APPROVED
    ```
  - Green introduces a new status: `status = EXPIRED`.
  - Green runs for 10 minutes. It writes `EXPIRED` into the database. Now you detect a bug and rollback to Blue. Blue reads EXPIRED and: Crashes, Throws error
  - Schema didn’t change. But data meaning changed.
- How To Prevent This. There are 3 practical strategies:
  - Make Blue Tolerant (Best Approach)
    - Old version must: Ignore unknown enum values, Ignore unknown JSON fields, Handle missing fields safely
    - Never write strict logic like: `if status not in (PENDING, APPROVED) → crash`
    - Instead: `unknown status → treat as PENDING or ignore`
  - Use Feature Flags
    - Instead of immediately writing new data: Deploy Green. Keep new behavior disabled. Gradually enable
  - Accept Some Changes Are One-Way. If data change is irreversible:
    - Admit rollback is not possible
    - Use canary instead of full blue-green
    - Monitor before full rollout
