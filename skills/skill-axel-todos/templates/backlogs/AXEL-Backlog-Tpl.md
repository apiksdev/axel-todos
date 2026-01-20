---
name: product-backlogs
description: Backlog template for storing feature ideas
type: backlogs
---

# AXEL Template: Backlogs

```xml
<document type="backlogs">

  <!--
    BACKLOGS FILE: .claude/workspaces/BACKLOGS.md
    FORMAT: Only bullet list inside <description>, NO headers
  -->

  <backlog>
    <title>Example: User Authentication</title>
    <description>
    - Implement user authentication with JWT tokens
    - User registration with email and password
    - Login endpoint returning JWT token
    - Token refresh mechanism
    - Password reset via email
    - Stack: Node.js, Express, PostgreSQL
    - Depends: Database schema setup
    </description>
  </backlog>

  <backlog>
    <title>Example: API Rate Limiting</title>
    <description>
    - Add rate limiting to prevent API abuse
    - Per-IP limiting for public endpoints (100/min)
    - Per-user limiting for authenticated (1000/min)
    - Return 429 when limit exceeded
    - Use Redis for distributed limiting
    - Depends: Redis server
    </description>
  </backlog>

</document>
```
