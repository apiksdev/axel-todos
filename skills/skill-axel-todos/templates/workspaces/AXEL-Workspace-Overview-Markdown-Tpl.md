---
name: workspace-overview-markdown
description: Workspace overview with Markdown tables
type: template
---

# AXEL Workspace Overview

> Last Updated: 2026-01-11 14:30

## Workspace Summary

| Workspace | Total | Completed | In Progress | Pending | Progress |
|-----------|-------|-----------|-------------|---------|----------|
| [auth-module](#auth-module) | 6 | 3 | 1 | 2 | 50% |
| [billing-system](#billing-system) | 4 | 1 | 1 | 2 | 25% |
| [api-gateway](#api-gateway) | 2 | 1 | 1 | 0 | 50% |

- **Total Workspaces:** 3
- **Total Todos:** 12
- **Completed:** 5
- **In Progress:** 3
- **Pending:** 4
- **Completion Rate:** 42%

---

## Workspace Details

<a id="auth-module"></a>
### auth-module

> **Path:** `.claude/workspaces/auth-module/`

| Status | Priority | Todo | File |
|--------|----------|------|------|
| in-progress | high | Session Management | [[session-management]] |
| pending | high | JWT Token Revocation | [[jwt-revocation]] |
| pending | medium | OAuth2 Provider Integration | [[oauth2-provider]] |

---

<a id="billing-system"></a>
### billing-system

> **Path:** `.claude/workspaces/billing-system/`

| Status | Priority | Todo | File |
|--------|----------|------|------|
| in-progress | high | Subscription Renewal Logic | [[subscription-renewal]] |
| pending | high | Invoice PDF Generation | [[invoice-pdf]] |
| pending | medium | Payment Gateway Webhook | [[payment-webhook]] |

---

<a id="api-gateway"></a>
### api-gateway

> **Path:** `.claude/workspaces/api-gateway/`

| Status | Priority | Todo | File |
|--------|----------|------|------|
| pending | low | Rate Limiting Implementation | [[rate-limiting]] |
