---
name: axel-cmd-workspace-overview-workflow
description: Generate workspace overview with progress metrics and todo statistics
type: workflow
triggers:
  - workspace overview
  - overview workspace
---

# AXEL Workflow: Cmd Workspace Overview

```xml
<document type="workflow">

  <enforcement>
    <![CDATA[
    - Read the `src`, `ref`, or `target` attribute from the document XML to locate referenced files
    - ${CLAUDE_PLUGIN_ROOT} resolves to plugin installation directory

    ARGUMENT PARSING:
    - workspace_name = param.workspace_name (optional, for specific workspace)
    - If empty, scan all workspaces
    ]]>
  </enforcement>

  <objective>
    Generate workspace overview with progress metrics and todo statistics.
    Supports both all-workspace summary and specific workspace detail.
    Output format selected by user (Markdown or XML).
  </objective>

  <templates name="overview" load="on-trigger" mode="template">
    <read src="${CLAUDE_PLUGIN_ROOT}/skills/skill-axel-todos/templates/workspaces/AXEL-Workspace-Overview-Markdown-Tpl.md" trigger="overview-markdown"/>
    <read src="${CLAUDE_PLUGIN_ROOT}/skills/skill-axel-todos/templates/workspaces/AXEL-Workspace-Overview-Tpl.md" trigger="overview-xml"/>
    <understanding>
      !! MANDATORY: READ -> UNDERSTAND -> APPLY !!
      Two template options available:
      - Markdown: Tables with wikilinks
      - XML: Structured XML format with statistics
      User selects preferred format before generation.
    </understanding>
  </templates>

  <variables>
    <var name="workspace_name" from="param.workspace_name"/>
    <var name="template_format" value=""/>
    <var name="output_file" value=""/>
    <var name="workspace_data" value=""/>
    <var name="overview_content" value=""/>
  </variables>

  <execution flow="linear"><![CDATA[
    Step 1 - Header:
    - Print "## Workspace Overview"

    Step 2 - Analyze Workspaces:
    - IF workspace_name is empty:
      - Print "Scanning workspaces..."
      - output_file = ".claude/workspaces/OVERVIEW.md"
      - Scan .claude/workspaces/ directory:
        - List all subdirectories (each is a workspace)
        - For each workspace, count todos in pending/, in-progress/, completed/
        - Parse each todo file: name, priority, description
        - Calculate: total_workspaces, total_todos, completion_rate
    - ELSE:
      - Print "Analyzing workspace: ${workspace_name}..."
      - output_file = ".claude/workspaces/${workspace_name}/OVERVIEW.md"
      - Verify workspace exists
      - Count todos in pending/, in-progress/, completed/
      - Parse each todo file: name, priority, description
      - Calculate workspace statistics

    Step 3 - Ask Format:
    - Ask user: "Which overview format do you prefer?"
      - Markdown: Tables with wikilinks
      - XML: Structured XML format with statistics

    Step 4 - Generate Overview:
    - IF template_format = 'markdown':
      - Load AXEL-Workspace-Overview-Markdown-Tpl.md
      - Create Markdown with YAML frontmatter
      - Add Workspace Summary table (Workspace | Total | Completed | In Progress | Pending | Progress)
      - Add Statistics bullet list
      - Add Workspace Details with anchor headings and todo tables
    - ELSE (xml):
      - Load AXEL-Workspace-Overview-Tpl.md
      - Create XML with YAML frontmatter
      - Add statistics section (total_workspaces, total_todos, completion_rate)
      - Add overview section with workspace summaries
      - Add workspaces section with todo details
    - Write to ${output_file}

    Step 5 - Display Result:
    - Print summary:
      - Format: ${template_format}
      - File: ${output_file}
  ]]></execution>

  <understanding/>

</document>
```
