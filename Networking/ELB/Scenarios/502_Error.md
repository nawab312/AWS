### 502 from ALB — Step-by-Step Troubleshooting ###

**Step 1 — Check ALB Access Logs**
- Enable ALB access logs
- Look at fields: `elb_status_code`, `target_status_code`, `error_reason`
- Case A:
  - ```bash
    elb_status_code = 502
    target_status_code = -
    ```
  - ALB could not establish proper connection to target. Likely connection reset / port issue / app not listening.
- Case B:
  - ```bash
    elb_status_code = 502
    target_status_code = 502
    ```
  - Backend itself returned 502. Issue is in your application or reverse proxy (like Nginx).
 
**Step 2 — Verify Target Group Health**
- If all targets unhealthy: You’ll usually see 503, not 502.
- If targets healthy: Problem happens during actual request handling.

**Step 3 — Test Backend Directly (Bypass ALB)**
- From inside VPC:
  ```bash
  curl http://<private-ip>:<app-port>
  ```
- If:
  - Connection Refused → App not listening
  - Hangs → App stuck
  - Works → Issue may be Protocol Mismatch
 
**Step 4 — Check Port & Protocol Mismatch**
- Target group: Protocol: HTTP, Port: 80
- App actually running: HTTPS on 443
- ALB sends plain HTTP. Backend expects TLS. Handshake fails -> 502

**Step 5 — Check If App Is Crashing During Request**
- Check: Application logs, OOMKilled events (if container), CPU/memory Spikes
- If app accepts connection but crashes before sending full HTTP response: ALB returns 502.

**Dont need to Check Security Groups**
- If inbound from ALB SG not allowed:
  - TCP won’t establish
  - Target unhealthy
  - Usually 503, not 502
