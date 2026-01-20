---
name: axel:workspace
description: Create new AXEL workspace or generate workspace overview
type: command
allowed-tools:
  - Bash
  - Skill
---

# AXEL Command: /axel:workspace

```xml
<document type="command" entry="cmd:main">

  <enforcement>
    <![CDATA[
    WORKSPACE PATH: .claude/workspaces/{workspace}/

    OUTPUT RULES:
    - Print ONLY the specified message, nothing more
    - NO tips, suggestions, or next steps
    - NO mentioning other commands
    ]]>
  </enforcement>

  <objective>
    Workspace management command with embedded create logic.
    Overview delegated to skill.
  </objective>

  <variables>
    <var name="action" from="args.0"/>
    <var name="param1" from="args.1"/>
  </variables>

  <command id="cmd:main">
    <goto when="action = ''" to="stage_help"/>
    <goto when="action = 'overview'" to="stage_overview"/>
    <goto when="action = 'create'" to="stage_create_from_arg"/>
    <goto to="stage_create"/>
  </command>

  <execution flow="staged">

    <!-- STAGE: Help -->
    <stage id="stage_help"><![CDATA[
      Print usage:
      ## /axel:workspace

      **Usage:**
        /axel:workspace {name}             - Create new workspace
        /axel:workspace create {name}      - Create new workspace
        /axel:workspace overview           - Overview of all workspaces
        /axel:workspace overview {name}    - Overview of specific workspace
    ]]></stage>

    <!-- STAGE: Create (action is workspace name) -->
    <stage id="stage_create"><![CDATA[
      workspace_name = ${action}

      Step 1 - Validate:
      - IF workspace_name is empty:
        → Print "Error: Workspace name is required."
        → STOP

      Step 2 - Create:
      - Run: PYTHONIOENCODING=utf-8 python "${CLAUDE_PLUGIN_ROOT}/skills/skill-axel-todos/scripts/axel_workspace.py" --workspace "${workspace_name}" --cwd "."

      Step 3 - Report (ONLY this, nothing else):
      - IF success → "## Workspace Created: ${workspace_name}"
      - ELSE → error message from result
    ]]></stage>

    <!-- STAGE: Create (explicit create action) -->
    <stage id="stage_create_from_arg"><![CDATA[
      workspace_name = ${param1}

      Step 1 - Validate:
      - IF workspace_name is empty:
        → Print "Error: Workspace name is required."
        → STOP

      Step 2 - Create:
      - Run: PYTHONIOENCODING=utf-8 python "${CLAUDE_PLUGIN_ROOT}/skills/skill-axel-todos/scripts/axel_workspace.py" --workspace "${workspace_name}" --cwd "."

      Step 3 - Report (ONLY this, nothing else):
      - IF success → "## Workspace Created: ${workspace_name}"
      - ELSE → error message from result
    ]]></stage>

    <!-- STAGE: Overview (delegate to skill) -->
    <stage id="stage_overview">
      <invoke name="Skill">
        <param name="skill" value="axel-todos:skill-axel-todos"/>
        <param name="trigger" value="workspace:overview"/>
        <param name="workspace_name" value="${param1}"/>
      </invoke>
      <stop kind="end"/>
    </stage>

  </execution>

  <understanding/>

</document>
```
