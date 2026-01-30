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
    <var name="workspace_name" description="Resolved workspace name for create/init"/>
  </variables>

  <command id="cmd:main">
    <goto when="action = ''" to="stage_help"/>
    <goto when="action = 'overview'" to="stage_overview"/>
    <goto when="action = 'init'" to="stage_init"/>
    <goto when="action = 'bootstrap'" to="stage_bootstrap"/>
    <goto to="stage_create"/>
  </command>

  <execution flow="staged">

    <!-- stage_help: Help -->
    <stage id="stage_help"><![CDATA[
      Print usage:
      ## /axel:workspace

      **Usage:**
        /axel:workspace {name}             - Create new workspace
        /axel:workspace create {name}      - Create new workspace
        /axel:workspace init               - Initialize workspace from CLAUDE.md project name
        /axel:workspace overview           - Overview of all workspaces
        /axel:workspace overview {name}    - Overview of specific workspace
        /axel:workspace bootstrap {name}   - Create bootstrap for existing workspace
    ]]></stage>

    <!-- stage_create: Create workspace -->
    <stage id="stage_create"><![CDATA[
      Step 1 - Resolve workspace name:
      - IF ${action} = "create" → workspace_name = ${param1}
      - ELSE → workspace_name = ${action}

      Step 2 - Validate:
      - IF workspace_name is empty:
        → Print "Error: Workspace name is required."
        → STOP

      Step 3 - Create:
      - Run: PYTHONIOENCODING=utf-8 python "${CLAUDE_PLUGIN_ROOT}/skills/skill-axel-todos/scripts/axel_workspace.py" --workspace "${workspace_name}" --cwd "."

      Step 4 - Report:
      - IF success:
        ## Workspace Created: ${workspace_name}
        Path: .claude/workspaces/${workspace_name}/
      - ELSE → error message from result → STOP

      Step 5 - Ask Bootstrap:
      - AskUserQuestion:
          header: "Bootstrap"
          question: "Create bootstrap for this workspace?"
          multiSelect: false
          options:
            - label: "Yes", description: "Create bootstrap file"
            - label: "No", description: "Skip for now"
      - IF "Yes" → set param1 = workspace_name → goto stage_bootstrap
      - IF "No" → STOP
    ]]></stage>

    <!-- stage_init: Init from CLAUDE.md -->
    <stage id="stage_init"><![CDATA[
      Step 1 - Find and Read CLAUDE.md:
      - Search for CLAUDE.md in current directory or parent directories
      - IF not found → Print "Error: CLAUDE.md not found." → STOP

      Step 2 - Extract Project Name:
      - Find <project name="..."> tag in CLAUDE.md
      - IF not found → Print "Error: No <project name> tag in CLAUDE.md" → STOP

      Step 3 - Convert to kebab-case:
      - workspace_name = project_name converted to kebab-case
        (lowercase, spaces/underscores → hyphens, remove special chars)

      Step 4 - Create Workspace:
      - Run: PYTHONIOENCODING=utf-8 python "${CLAUDE_PLUGIN_ROOT}/skills/skill-axel-todos/scripts/axel_workspace.py" --workspace "${workspace_name}" --cwd "."
      - Parse JSON result

      Step 5 - Report:
      - IF success:
        ## Workspace Initialized: ${workspace_name}
        Path: .claude/workspaces/${workspace_name}/
      - ELSE → error message from result.errors → STOP

      Step 6 - Ask Bootstrap:
      - AskUserQuestion:
          header: "Bootstrap"
          question: "Create bootstrap for this workspace?"
          multiSelect: false
          options:
            - label: "Yes", description: "Create bootstrap file"
            - label: "No", description: "Skip for now"
      - IF "Yes" → set param1 = workspace_name → goto stage_bootstrap
      - IF "No" → STOP
    ]]></stage>

    <!-- stage_bootstrap: Validate and prepare bootstrap creation -->
    <stage id="stage_bootstrap"><![CDATA[
      Step 1 - Resolve workspace name:
      - IF ${param1} is not empty → ws_name = ${param1}
      - ELSE IF ${workspace_name} is not empty → ws_name = ${workspace_name}
      - ELSE → Print "Error: Workspace name is required." → STOP

      Step 2 - Check workspace exists:
      - Check if .claude/workspaces/${ws_name}/ directory exists
      - IF not exists:
        → Print "Error: Workspace '${ws_name}' not found."
        → STOP

      Step 3 - Prepare parameters:
      - Set bootstrap_topic = "Workspace bootstrap for ${ws_name}. Scan path: .claude/ Output path: .claude/workspaces/${ws_name}/${ws_name}-Bootstrap.md"
      - goto stage_bootstrap_invoke
    ]]></stage>

    <!-- stage_bootstrap_invoke: Call bootstrap creator skill -->
    <stage id="stage_bootstrap_invoke">
      <invoke name="Skill">
        <param name="skill" value="axel-core:skill-axel-core"/>
        <param name="trigger" value="create:bootstrap"/>
        <param name="topic" value="${bootstrap_topic}"/>
      </invoke>
      <stop kind="end"/>
    </stage>

    <!-- stage_overview: Delegate to skill -->
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
