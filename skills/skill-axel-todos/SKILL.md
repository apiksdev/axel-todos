---
name: skill-axel-todos
description: |
  Trigger-based workflow dispatcher for todos and workspaces. Receives explicit trigger from command and dispatches to matching workflow.
type: skill
model: inherit
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Bash
  - AskUserQuestion
---

# AXEL Skill: Todos

```xml
<document type="skill">

  <enforcement>
    <![CDATA[
    PATH RESOLUTION:
    - Read the `src`, `ref`, or `target` attribute from the document XML to locate referenced files
    - ${CLAUDE_PLUGIN_ROOT} resolves to plugin installation directory

    TRIGGER-BASED DISPATCH:
    - Command sends explicit trigger parameter
    - Skill matches trigger against workflows registry
    - Matching workflow is loaded and executed

    DOCUMENT CREATION VALIDATION:
    - Only todos:create requires AXEL-Checklist.md validation

    BASH TAG EXECUTION:
    - MUST use Bash tool for <bash> element in workflows
    - ❌ NEVER interpret <bash> content semantically
    - ❌ NEVER substitute with Glob, Read, Grep tools
    - <bash>python script.py</bash> → Run via Bash tool, not Read files
    ]]>
  </enforcement>

  <objective>
    Trigger-based workflow dispatcher.
    Matches incoming trigger to workflow registry and executes.
  </objective>

  <documents name="bootstrap" load="always" mode="context">
    <read src="${AXEL_CORE_PLUGIN_ROOT}/AXEL-Bootstrap.md"/>
    <understanding>
      !! MANDATORY: READ → UNDERSTAND → APPLY !!
      Bootstrap provides AXEL syntax, enforcement rules, and understanding guidelines.
    </understanding>
  </documents>

  <documents name="references" load="on-demand" mode="context">
    <read src="${CLAUDE_PLUGIN_ROOT}/skills/skill-axel-todos/references/AXEL-Todo.md" ask="todo, task, template, frontmatter, structure, create"/>
    <read src="${CLAUDE_PLUGIN_ROOT}/skills/skill-axel-todos/references/AXEL-Todo-Standards.md" ask="element, standard, xml, tag, format"/>
    <understanding>
      !! LOAD ON-DEMAND: When keywords match !!
      AXEL-Todo.md: Todo document structure, templates, frontmatter format, creation process
      AXEL-Todo-Standards.md: Todo-specific XML elements, tag definitions, format rules
    </understanding>
  </documents>

  <role>
    Workflow dispatcher that routes trigger-based requests
    to appropriate todo or workspace workflows.
  </role>

  <capabilities>
    - Receive trigger parameter from command
    - Match trigger against workflows registry
    - Load and execute matching workflow
    - Pass parameters to workflow
  </capabilities>

  <workflows name="operations" load="on-trigger">
    <read src="${CLAUDE_PLUGIN_ROOT}/skills/skill-axel-todos/workflows/todos/AXEL-Cmd-Todos-Create-Workflow.md" trigger="todos:create"/>
    <read src="${CLAUDE_PLUGIN_ROOT}/skills/skill-axel-todos/workflows/todos/AXEL-Cmd-Todos-List-Workflow.md" trigger="todos:list"/>
    <read src="${CLAUDE_PLUGIN_ROOT}/skills/skill-axel-todos/workflows/todos/AXEL-Cmd-Todos-Run-Workflow.md" trigger="todos:run"/>
    <read src="${CLAUDE_PLUGIN_ROOT}/skills/skill-axel-todos/workflows/workspaces/AXEL-Cmd-Workspace-Overview-Workflow.md" trigger="workspace:overview"/>
    <understanding>
      !! MANDATORY: READ → UNDERSTAND → APPLY !!
      Trigger-based workflow registry. Match resolved trigger to execute workflow.

      TWO-PHASE CREATE:
      - todos:understanding → Handled inline by axel-todos.md command
      - todos:create → Receives synthesis, generates document
    </understanding>
  </workflows>

  <execution flow="linear"><![CDATA[
    WORKFLOW DISPATCH:

    Step 1 - Receive Parameters:
    - trigger: ${param.trigger} (optional)
    - prompt: ${param.prompt} (optional)
    - Additional: topic, workspace_name, description

    Step 2 - Resolve Trigger:
    - IF trigger provided → use directly
    - IF trigger empty → detect from prompt:

      Keyword Priority (first match):
      1. "workspace" → workspace:overview
      2. "list"      → todos:list
      3. "run"       → todos:run
      4. "create"    → todos:create

    Step 3 - Match Workflow:
    - Check if resolved trigger matches workflows:operations registry
    - IF trigger matched → GO TO Step 4 (Execute workflow)
    - IF trigger NOT matched → print error and stop

    NOTE: todos:understanding is handled inline by axel-todos.md command
          It invokes todos:create after user approval

    Step 4 - Execute Workflow:
    - IF trigger = todos:create:
      → Load ${CLAUDE_PLUGIN_ROOT}/skills/skill-axel-todos/references/AXEL-Todo.md
      → Load ${AXEL_CORE_PLUGIN_ROOT}/references/AXEL-Checklist.md
      → Execute create workflow with synthesis parameters
      → Validate created document step-by-step against checklist

    - ELSE (todos:list, todos:run, workspace:overview):
      → Execute matched workflow with parameters
  ]]></execution>

  <understanding/>

</document>
```
