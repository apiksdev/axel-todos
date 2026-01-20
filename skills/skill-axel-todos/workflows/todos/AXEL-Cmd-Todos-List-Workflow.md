---
name: axel-cmd-todos-list-workflow
description: List and improve todos with workspace selection
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
    First select workspace, then list and improve todos.
  </objective>

  <variables>
    <var name="plugin_root" value="${CLAUDE_PLUGIN_ROOT}"/>
    <var name="workspace" value=""/>
    <var name="base_path" value=""/>
    <var name="todos" value="[]"/>
    <var name="todo_file" value=""/>
    <var name="todo_content" value=""/>
    <var name="focus" value=""/>
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
      <print>
        ---
        Enter number to improve, or 'q' to quit:
      </print>
      <ask id="selection" prompt="Select:" type="text"/>
      <goto when="selection = 'q'" to="complete"/>
      <goto when="selection = ''" to="complete"/>
      <tasks output="selected_todo">
        Find todo from todos array where key = ${selection}.
        Return the todo object or null if not found.
      </tasks>
      <print when="selected_todo = null">Invalid selection: ${selection}</print>
      <goto when="selected_todo = null" to="list_todos"/>
      <set var="todo_file" value="${selected_todo.file}"/>
      <goto when="selected_todo != null" to="improve_todo"/>
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

    <!-- improve_todo: Read, ask focus, run brainstorm -->
    <stage id="improve_todo">
      <read src="${todo_file}" output="todo_content" mode="raw"/>
      <print when="todo_content = error">File not found: ${todo_file}</print>
      <stop when="todo_content = error" kind="end"/>
      <print>
        ## Todo: ${todo_file}

        ${todo_content}
      </print>
      <ask var="focus" prompt="What would you like to improve?" type="text"/>
      <goto when="focus = ''" to="complete"/>
      <print>Improving todo with focus: ${focus}</print>
      <workflow src="${AXEL_CORE_PLUGIN_ROOT}/workflows/brainstorm/AXEL-Brainstorm-Bootstrap.md" output="synthesis">
        <param name="topic" value="Improve todo: ${focus}"/>
        <param name="mode" value="improve"/>
        <param name="context" value="${todo_content}"/>
      </workflow>
      <goto when="synthesis.status = 'error'" to="complete"/>
      <tasks>
        Apply synthesis improvements to todo_content.
        Write updated content to ${todo_file}.
      </tasks>
      <print>Todo improved: ${todo_file}</print>
      <goto when="synthesis.status != 'error'" to="ask_continue"/>
    </stage>

    <!-- ask_continue: Ask if user wants to improve another -->
    <stage id="ask_continue">
      <ask id="continue_choice" prompt="Improve another todo?">
        <choice key="1" value="yes" label="Yes"/>
        <choice key="2" value="no" label="No"/>
      </ask>
      <goto when="continue_choice = 'yes'" to="list_todos"/>
      <goto when="continue_choice != 'yes'" to="complete"/>
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
