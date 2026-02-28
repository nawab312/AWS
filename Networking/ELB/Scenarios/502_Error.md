### 502 from ALB — Step-by-Step Troubleshooting ###

**Step 1 — Check Target Group Health**
- Target Group → Targets → Health status
- If Unhealthy → Check Health Check Path, Port, Response Code.
- If Healthy → Issue is happening during real traffic, not health checks.

**Step 2 — Verify Application Is Running**
- On the instance/container:
  - Is the app process running?
  - Is it listening on the correct port?
  - Is the correct port mapped (for containers)?
```bash
netstat -tulnp | grep 8080
```

**Step 3 — Validate Port & Protocol**
- Check:
  - Target group port matches app port
  - HTTP vs HTTPS configuration
  - If backend expects HTTPS but TG is HTTP → 502
 
**Step 4 — Check Application Logs**

**Step 5 — Check ALB Access Logs**
- Enable ALB logs and verify: `target_status_code` and `error_reason`
- This tells if: Backend closed connection, Timeout, TLS handshake failure
