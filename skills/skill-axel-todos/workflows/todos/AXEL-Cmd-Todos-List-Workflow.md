---
name: axel-cmd-todos-list-workflow
description: List todos with workspace selection
type: workflow
triggers:
  - todos list
  - list todos
---

# AXEL Workflow: Cmd Todos List

```xml
<document type="workflow">

  <enforcement>
    <![CDATA[
    - Read the `src`, `ref`, or `target` attribute from the document XML to locate referenced files
    - ${CLAUDE_PLUGIN_ROOT} resolves to plugin installation directory

    WORKSPACE SELECTION:
    - First, list workspaces from .claude/workspaces/
    - User selects workspace
    - Then list todos from selected workspace

    BASH EXECUTION MANDATORY:
    - All <bash> elements MUST be executed via Bash tool
    - DO NOT skip, summarize, or simulate bash commands
    ]]>
  </enforcement>

  <objective>
    List pending todos with workspace selection at the start.
  </objective>

  <variables>
    <var name="plugin_root" value="${CLAUDE_PLUGIN_ROOT}"/>
    <var name="workspace" value=""/>
    <var name="base_path" value=""/>
    <var name="todos" value="[]"/>
  </variables>

  <execution flow="staged">

    <!-- select_workspace: List workspaces and let user select -->
    <stage id="select_workspace">
      <bash output="ws_list">ls -1 .claude/workspaces 2>/dev/null</bash>
      <goto when="ws_list = ''" to="no_workspace"/>
      <print>## Select Workspace</print>
      <ask id="workspace_choice" prompt="Select workspace:" options="${ws_list}"/>
      <set var="workspace" value="${workspace_choice}"/>
      <goto to="list_todos"/>
    </stage>

    <!-- no_workspace: No workspace found -->
    <stage id="no_workspace">
      <print>
        No workspace found in .claude/workspaces/
        Run `/axel:workspace {name}` first to create a workspace.
      </print>
      <stop kind="end"/>
    </stage>

    <!-- list_todos: Show pending todos -->
    <stage id="list_todos">
      <set var="base_path" value=".claude/workspaces/${workspace}"/>
      <print>## ${workspace} - Pending Todos</print>
      <bash output="todos_result">
        PYTHONIOENCODING=utf-8 python ${CLAUDE_PLUGIN_ROOT}/skills/skill-axel-todos/scripts/axel_todo.py --action list --base-path "${base_path}" --status pending
      </bash>
      <goto when="todos_result.success = false" to="no_todos"/>
      <set var="todos" from="todos_result.todos"/>
      <goto when="todos.length = 0" to="no_todos"/>
      <foreach var="t" in="${todos}" mode="sequential">
        <print>${t.key}</print>
      </foreach>
      <goto to="complete"/>
    </stage>

    <!-- no_todos: No todos in workspace -->
    <stage id="no_todos">
      <print>
        No pending todos found in ${workspace}.
      </print>
      <ask id="retry_choice" prompt="Select another workspace?">
        <choice key="1" value="yes" label="Yes"/>
        <choice key="2" value="no" label="No"/>
      </ask>
      <goto when="retry_choice = 'yes'" to="select_workspace"/>
      <stop kind="end"/>
    </stage>

    <!-- complete: End workflow -->
    <stage id="complete">
      <print>Todos list workflow completed.</print>
      <stop kind="end"/>
    </stage>

  </execution>

  <understanding/>

</document>
```
