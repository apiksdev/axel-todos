---
name: workspace-bootstrap-template
description: Template for workspace-specific bootstrap files
type: template
---

# AXEL Template: Workspace Bootstrap

```xml
<document type="reference">

  <enforcement>
    <![CDATA[
    PATH RESOLUTION:
    - Read the `src`, `ref`, or `target` attribute from the document XML to locate referenced files
    - ${AXEL_CORE_PLUGIN_ROOT} resolves to AXEL core plugin directory (defined in CLAUDE.md)
    - ${WORKSPACE_ROOT} resolves to .claude/workspaces/{{workspace_name}}/
    - ${PROJECT_ROOT} resolves to project root directory
    - All paths are resolved relative to appropriate root directories

    MANDATORY LOADING:
    - This bootstrap is loaded automatically by todos in this workspace
    - All enforcement rules are cumulative and must be applied
    - Core AXEL-Bootstrap.md loaded on-demand for DSL work

    COMPLIANCE:
    - Every rule MUST be applied
    - Skipping a rule = TASK FAILURE
    - If uncertain → ASK the user

    WORKSPACE-SPECIFIC RULES:
    - Add workspace-specific enforcement rules below
    - These rules apply to all todos in this workspace
    - Keep rules focused and actionable
    ]]>
  </enforcement>

  <objective>
    Workspace Bootstrap for {{display_name}}. Contains workspace-specific references
    and enforcement rules. Loaded automatically by todos in this workspace.
  </objective>

  <documents name="workspace-always" load="always" mode="context">
{{refs_always}}
    <understanding>
      !! MANDATORY: READ -> UNDERSTAND -> APPLY !!
      Always-loaded workspace references. Core files needed throughout execution.
    </understanding>
  </documents>

  <documents name="core-bootstrap" load="on-demand" mode="context">
    <read src="${AXEL_CORE_PLUGIN_ROOT}/AXEL-Bootstrap.md" ask="axel, bootstrap, core"/>
    <understanding>
      !! MANDATORY: READ -> UNDERSTAND -> APPLY !!
      Core AXEL DSL rules and enforcement. Load when working with AXEL components.
    </understanding>
  </documents>

  <documents name="workspace-on-demand" load="on-demand" mode="context">
{{refs_on_demand}}
    <understanding>
      !! MANDATORY: READ -> UNDERSTAND -> APPLY !!
      On-demand workspace references. Loaded when specific topics arise.
    </understanding>
  </documents>

  <documents name="workspace-on-trigger" load="on-trigger" mode="context">
{{refs_on_trigger}}
    <understanding>
      !! MANDATORY: READ -> UNDERSTAND -> APPLY !!
      Trigger-based workspace references. Loaded on specific events or commands.
    </understanding>
  </documents>

  <understanding/>

</document>
```
