---
name: axel-cmd-todos-run-workflow
description: Run todos with workspace selection
type: workflow
triggers:
  - todos run
  - run todos
---

# AXEL Workflow: Cmd Todos Run

```xml
<document type="workflow">

  <enforcement>
    <![CDATA[
    - Read the `src`, `ref`, or `target` attribute from the document XML to locate referenced files
    - ${CLAUDE_PLUGIN_ROOT} resolves to plugin installation directory

    TODO LIFECYCLE:
    - Agent handles full lifecycle: pending → in-progress → completed
    - Workflow only orchestrates selection and invocation
    - Agent moves files and updates frontmatter

    WORKSPACE SELECTION:
    - List workspaces from .claude/workspaces/
    - User selects workspace, then list and run todos
    ]]>
  </enforcement>

  <objective>
    Run todos with workspace selection.
    Agent handles lifecycle: pending → in-progress → completed.
  </objective>

  <variables>
    <var name="plugin_root" value="${CLAUDE_PLUGIN_ROOT}"/>
    <var name="workspace_name" from="param.workspace_name"/>
    <var name="workspace" value=""/>
    <var name="base_path" value=""/>
    <var name="files" value="[]"/>
    <var name="results" value="[]"/>
    <var name="exec_mode" value="sequential"/>
    <var name="force_mode" value="false"/>
  </variables>

  <execution flow="staged">

    <!-- select_workspace: Use param or list workspaces for user selection -->
    <stage id="select_workspace" entry="true">
      <!-- If workspace_name provided via param, use it directly -->
      <goto when="workspace_name != ''" to="use_param_workspace"/>
      <!-- Otherwise, list and let user select -->
      <bash output="ws_list">ls -1 .claude/workspaces 2>/dev/null</bash>
      <goto when="ws_list = ''" to="no_workspace"/>
      <print>## Select Workspace</print>
      <ask id="workspace_choice" prompt="Select workspace:" options="${ws_list}"/>
      <set var="workspace" value="${workspace_choice}"/>
      <goto to="list_todos"/>
    </stage>

    <!-- use_param_workspace: Set workspace from param and continue -->
    <stage id="use_param_workspace">
      <set var="workspace" value="${workspace_name}"/>
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

    <!-- list_todos: Show todos with dependency status -->
    <stage id="list_todos">
      <set var="base_path" value=".claude/workspaces/${workspace}"/>
      <print>## ${workspace} Todos</print>
      <bash output="todos_result">
        PYTHONIOENCODING=utf-8 python ${CLAUDE_PLUGIN_ROOT}/skills/skill-axel-todos/scripts/axel_todo.py --action list --base-path "${base_path}" --status pending --check-deps
      </bash>
      <goto when="todos_result.success = false" to="no_todos"/>
      <set var="todos" from="todos_result.todos"/>
      <goto when="todos.length = 0" to="no_todos"/>
      <ask id="selected_todos" prompt="Select todos to run:" multi="true">
        ${todos}
      </ask>
      <goto when="selected_todos.length = 0" to="complete"/>
      <goto when="selected_todos.length > 0" to="check_selection"/>
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

    <!-- check_selection: Separate ready and blocked -->
    <stage id="check_selection">
      <set var="ready_files" value="[]"/>
      <set var="blocked_files" value="[]"/>
      <foreach var="todo" in="${selected_todos}" mode="sequential">
        <append var="ready_files" value="${todo.value}" when="todo.ready = true"/>
        <append var="blocked_files" value="${todo}" when="todo.ready = false"/>
      </foreach>
      <goto when="blocked_files.length > 0" to="ask_blocked"/>
      <set var="files" value="${ready_files}"/>
      <goto when="blocked_files.length = 0" to="select_exec_mode"/>
    </stage>

    <!-- ask_blocked: Handle blocked todos -->
    <stage id="ask_blocked">
      <print>## Some selected todos have unmet dependencies:</print>
      <foreach var="b" in="${blocked_files}" mode="sequential">
        <print>- ${b.name}: blocked by ${b.blocked_by}</print>
      </foreach>
      <ask id="block_action" prompt="What to do?">
        <choice key="1" value="ready_only" label="Run only ready todos (${ready_files.length})" when="ready_files.length > 0"/>
        <choice key="2" value="force_all" label="Force run all (ignore dependencies)"/>
        <choice key="3" value="cancel" label="Cancel"/>
      </ask>
      <goto when="block_action = 'cancel'" to="complete"/>
      <set var="files" value="${ready_files}" when="block_action = 'ready_only'"/>
      <set var="force_mode" value="true" when="block_action = 'force_all'"/>
      <tasks output="files" when="force_mode = 'true'">
        Extract all file paths from selected_todos array into files array.
      </tasks>
      <goto when="block_action != 'cancel'" to="select_exec_mode"/>
    </stage>

    <!-- select_exec_mode: Choose sequential or parallel -->
    <stage id="select_exec_mode">
      <goto when="files.length = 0" to="complete"/>
      <goto when="files.length = 1" to="execute_files"/>
      <print><![CDATA[## Selected Files (${files.length})]]></print>
      <foreach var="f" in="${files}" mode="sequential">
        <print>- ${f}</print>
      </foreach>
      <print>
        **Note:** Parallel execution runs agents in background.
        Requires permission bypass to be enabled.
      </print>
      <ask id="exec_mode" prompt="Execution mode:">
        <choice key="1" value="sequential" label="Sequential (one by one)"/>
        <choice key="2" value="parallel" label="Parallel (all at once)"/>
        <choice key="3" value="cancel" label="Cancel"/>
      </ask>
      <goto when="exec_mode = 'cancel'" to="complete"/>
      <goto when="exec_mode != 'cancel'" to="execute_files"/>
    </stage>

    <!-- execute_files: Run files with agent (agent handles lifecycle) -->
    <stage id="execute_files">
      <set var="exec_mode" value="${exec_mode | default: 'sequential'}"/>
      <print>Executing ${files.length} file(s) in ${exec_mode} mode...</print>
      <foreach var="file_path" in="${files}" mode="${exec_mode}">
        <print>Running: ${file_path}</print>
        <invoke name="Task" output="result">
          <param name="subagent_type">axel-todos:agent-axel-todo-runner:agent-axel-todo-runner</param>
          <param name="description">Run todo: ${file_path}</param>
          <param name="prompt"><![CDATA[
            PLUGIN_ROOT: ${plugin_root}
            todo_file_path: ${file_path}
            base_path: ${base_path}
          ]]></param>
        </invoke>
        <append var="results" value="${result}"/>
      </foreach>
      <goto when="results.length >= 0" to="show_results"/>
    </stage>

    <!-- show_results: Show summary -->
    <stage id="show_results">
      <print>
        ## Execution Complete

        **Workspace:** ${workspace}
        **Files:** ${files.length}
      </print>
      <foreach var="r" in="${results}" mode="sequential">
        <print>- ${r.todo_name}: ${r.status} (${r.final_status})</print>
      </foreach>
      <goto to="complete"/>
    </stage>

    <!-- complete: End workflow -->
    <stage id="complete">
      <print>Todos run workflow completed.</print>
      <stop kind="end"/>
    </stage>

  </execution>

  <understanding/>

</document>
```
