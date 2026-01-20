---
name: workspace-overview
description: Workspace overview - statistics and pending todos across workspaces
type: template
---

# AXEL Template: AXEL Workspace Overview

```xml
<document type="reference">

  <objective>
    Central view of workspace statistics and pending todos across all workspaces.
  </objective>

  <statistics updated="2025-01-10 14:30">
    <metric name="total_workspaces" value="3"/>
    <metric name="total_todos" value="12"/>
    <metric name="completion_rate" value="41%"/>
  </statistics>

  <overview>
    <workspace name="auth-module" pending="2" in_progress="1" completed="3"/>
    <workspace name="billing-system" pending="2" in_progress="1" completed="1"/>
    <workspace name="api-gateway" pending="1" in_progress="0" completed="1"/>
  </overview>

  <workspaces>

    <workspace name="auth-module">
      <todo status="pending" priority="high" file="jwt-revocation.md">
        JWT Token Revocation
      </todo>
      <todo status="pending" priority="medium" file="oauth2-provider.md">
        OAuth2 Provider Integration
      </todo>
      <todo status="in_progress" priority="high" file="session-management.md">
        Session Management
      </todo>
    </workspace>

    <workspace name="billing-system">
      <todo status="pending" priority="high" file="invoice-pdf.md">
        Invoice PDF Generation
      </todo>
      <todo status="pending" priority="medium" file="payment-webhook.md">
        Payment Gateway Webhook
      </todo>
      <todo status="in_progress" priority="high" file="subscription-renewal.md">
        Subscription Renewal Logic
      </todo>
    </workspace>

    <workspace name="api-gateway">
      <todo status="pending" priority="low" file="rate-limiting.md">
        Rate Limiting Implementation
      </todo>
    </workspace>

  </workspaces>

  <understanding/>

</document>
```
