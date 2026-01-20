---
name: todo-migration
description: Migration task todo template - upgrades, conversions, data transfers
type: template
---

# AXEL Template: Todo Migration

```xml
<document type="todo">

  <enforcement>
    - MUST document current state accurately before planning migration
    - MUST define rollback procedure for every migration step
    - NEVER proceed without user confirmation on breaking changes
    - MUST verify compatibility requirements with stakeholders
  </enforcement>

  <objective>
    Migrate authentication system from session-based to JWT-based.
    Zero downtime required, backward compatibility for 2 weeks.
  </objective>

  <!-- Documents element: Load references and affected files -->
  <documents load="always" mode="context">
    <read src="references/api/Authentication-Standards.md" ask="[auth, jwt, token]"/>
    <read src="src/Services/AuthService.cs"/>
    <read src="src/Middleware/SessionMiddleware.cs"/>
    <read src="docs/API-Documentation.md"/>
    <understanding>
      - READ all affected files to understand current state
      - IDENTIFY dependencies and integration points
      - MAP all components that will be impacted
    </understanding>
  </documents>

  <current_state>
    - Session-based authentication using ASP.NET Core Session
    - Session stored in Redis (distributed)
    - 15-minute sliding expiration
    - Cookie-based session ID transport
    - 50+ API endpoints depend on session
  </current_state>

  <target_state>
    - JWT-based stateless authentication
    - Access token (15 min) + Refresh token (7 days)
    - Bearer token transport
    - Token validation middleware
    - Same 50+ endpoints using new auth
  </target_state>

  <migration_steps>
    Phase 1 - Preparation:
    1. Add JWT infrastructure alongside session
    2. Create token generation service
    3. Add JWT validation middleware (inactive)

    Phase 2 - Dual Support:
    4. Enable both auth methods simultaneously
    5. Update login endpoint to return JWT + session
    6. Monitor metrics for both auth types

    Phase 3 - Migration:
    7. Notify API consumers of deprecation
    8. Migrate internal services to JWT
    9. Add deprecation headers to session auth

    Phase 4 - Cleanup:
    10. Remove session auth after grace period
    11. Clean up Redis session store
    12. Update documentation
  </migration_steps>

  <rollback_plan>
    Trigger: JWT auth failure rate > 5% or critical bug

    Steps:
    1. Disable JWT middleware (feature flag)
    2. Re-enable session-only authentication
    3. Communicate rollback to API consumers
    4. Investigate and fix JWT issues

    Data Recovery:
    - Sessions remain in Redis during migration
    - No data migration needed for rollback
  </rollback_plan>

  <compatibility>
    Breaking Changes:
    - Authorization header required (was optional with cookies)
    - Token refresh flow required for long sessions

    Non-Breaking:
    - Same endpoint URLs
    - Same request/response formats
    - Same permission model

    Deprecation Timeline:
    - Week 1-2: Dual support, deprecation warnings
    - Week 3-4: Session auth disabled
  </compatibility>

  <output format="markdown">
    ## Migration Summary
    - Migration type: [type]
    - Total phases: [count]
    - Estimated duration: [timeline]

    ## Completed Steps
    - [Step description with status]

    ## Rollback Status
    - Rollback tested: [yes/no]
    - Rollback procedure documented: [yes/no]
  </output>

  <!-- Todos: Derived from execution steps -->
  <todos>
    <![CDATA[
    - [ ] Step 1: Preparation complete
    - [ ] Step 2: Planning complete
    - [ ] Step 3: Validation passed
    - [ ] Step 4: Migration executed
    - [ ] Step 5: Completion verified
    ]]>
  </todos>

  <!-- Execution: References other sections for what to do -->
  <execution flow="linear">
    <![CDATA[
    Step 1 - Prepare:
    - Read <documents> for context
    - Verify <current_state> documented
    - Confirm <target_state> defined

    Step 2 - Plan:
    - Review <migration_steps>
    - Prepare <rollback_plan>
    - Check <compatibility>

    Step 3 - Validate:
    - Test <rollback_plan> procedure
    - Review with stakeholders

    Step 4 - Execute:
    - Execute phases in <migration_steps>
    - Monitor for issues

    Step 5 - Complete:
    - Run <verification> checks
    - Answer <checklist> questions
    ]]>
  </execution>

  <verification>
    - Test JWT auth on all 50+ endpoints
    - Verify session auth still works during dual period
    - Confirm rollback procedure works
    - Validate token refresh flow
    - Check no data loss during migration
  </verification>

  <checklist>
    - Is current state accurately documented?
    - Is target state clearly defined?
    - Are migration steps ordered and atomic?
    - Is rollback plan tested and ready?
    - Are breaking changes communicated?
    - Is deprecation timeline realistic?
    - Are all affected endpoints identified?
  </checklist>

  <understanding/>

</document>
```
