---
name: axel:todos
description: Todo management - create, list, run
type: command
allowed-tools:
  - Skill
  - Task
---

# AXEL Command: /axel:todos

```xml
<document type="command" entry="cmd:main">

  <enforcement>
    <![CDATA[
    ROUTER COMMAND:
    - Parses args to determine trigger
    - Sends explicit trigger and parameters to skill

    TWO-PHASE CREATE:
    - "todos create" or direct topic → triggers understanding phase first
    - Understanding phase produces synthesis
    - Understanding asks user: "Create todo" → triggers create phase with synthesis
    - This prevents long waits by getting early user alignment

    ⛔ NO ASSUMPTIONS - ASSUMPTION = TASK FAILED

    - NEVER assume without investigating the codebase first
    - Making assumptions = INCORRECT WORK
    - If uncertain → SEARCH the codebase, then propose

    ⛔ INVESTIGATION REQUIRED

    - ALWAYS read and understand relevant files before proposing
    - If user references a file/path → MUST open and inspect it first
    - Review style, conventions, and patterns before proposing changes

    ⛔ LIGHTWEIGHT PHASE

    - Understanding phase is FAST - no template loading, no document generation
    - Focus: Understand request → Present synthesis → Get approval
    - Output: Synthesis data for Create phase

    ⛔ OUTPUT FORMAT

    - MUST use exact output format from <output> section
    - Sections: 🎯 Problem, 📋 Tasks, ✅ Verification, 📁 Scope
    ]]>
  </enforcement>

  <objective>
    Router for skill-axel-todos todo operations.
    Determines trigger from args and delegates to skill.

    Create flow:
    1. User: /axel:todos {topic}
    2. Understanding phase: Investigate → Synthesize → Present → Ask
    3. User confirms: "Create todo"
    4. Create phase: Workspace → Template → Generate → Save
  </objective>

  <variables>
    <var name="action" from="args.0"/>
    <var name="rest_args" from="args.1+"/>
    <var name="all_args" from="args.*"/>
  </variables>

  <command id="cmd:main">
    <goto when="action = 'help'" to="todos:help"/>
    <goto when="action = 'list'" to="todos:list"/>
    <goto when="action = 'run'" to="todos:run"/>
    <goto when="action = 'create'" to="todos:understanding"/>
    <goto when="action = ''"  to="todos:understanding"/>
  </command>

  <execution flow="staged">

    <!-- todos:help: Display usage information -->
    <stage id="todos:help">
      <print>
        ## /axel:todos

        **Usage:**
          /axel:todos {topic}         - Create new todo (understanding → create)
          /axel:todos list            - List todos
          /axel:todos run             - Run todos (with workspace selection)
          /axel:todos run {workspace} - Run todos from specific workspace
          /axel:todos run {path}      - Run specific todo file directly
      </print>
      <stop kind="end"/>
    </stage>

    <!-- todos:understanding: Investigate, analyze, synthesize -->
    <stage id="todos:understanding">
      <tasks output="synthesis"><![CDATA[
        Step 1 - Investigate (MANDATORY):
        - Use Glob/Grep to find related files
        - Read files that will be affected
        - Check existing patterns/conventions
        - Determine task scope

        Step 2 - Analyze and Synthesize:
        - Analyze the topic using relevant perspectives based on complexity:

          Simple tasks (bug fix, small feature):
          → Use only DISCOVERY + ELICITATION

          Medium tasks (new feature, refactor):
          → Use DISCOVERY + ELICITATION + DEEP INQUIRY

          Complex tasks (migration, architecture change):
          → Use all four perspectives

          DISCOVERY (What?):
          - What exactly is being asked? What's the core request?
          - What's the scope - what's in and out?

          ELICITATION (How?):
          - How should this be implemented?
          - What are the acceptance criteria?

          DEEP INQUIRY (What if?) - for medium/complex:
          - What could go wrong? What are the risks?
          - What dependencies exist?

          SOCRATIC (Why?) - for complex only:
          - Why this approach? Are there alternatives?
          - What assumptions are being made?

        - Generate synthesis:
          * summary: Brief description of what needs to be done
          * todo_type: coding | analysis | research | migration
          * complexity: simple | medium | complex
          * priority: critical | high | medium | low
          * requirements: List of key requirements
          * constraints: Any limitations or boundaries
          * risks: Identified risks (from Deep Inquiry)
          * assumptions: Key assumptions made (from Socratic)
          * affected_files: Files that will be created/modified

        Step 3 - Display synthesis using <output id="understanding-output"> format:
        - Show: Problem, Tasks, Verification, Scope, Type/Complexity/Priority
      ]]></tasks>
      <goto to="todos:review"/>
    </stage>


    <!-- todos:review: Present synthesis and get user choice -->
    <stage id="todos:review">
      <ask id="user_choice" prompt="What should we do?">
        <choice key="1" value="create-single" label="Create single todo"/>
        <choice key="2" value="create-multiple" label="Create multiple todos"/>
        <choice key="3" value="edit" label="Edit synthesis"/>
        <choice key="4" value="cancel" label="Cancel"/>
      </ask>
      <goto when="${user_choice.value} == 'create-single'" to="todos:create-single"/>
      <goto when="${user_choice.value} == 'create-multiple'" to="todos:split-plan"/>
      <goto when="${user_choice.value} == 'edit'" to="todos:edit"/>
      <goto to="todos:cancel"/>
    </stage>

    <!-- todos:edit: Handle user edits to synthesis -->
    <stage id="todos:edit">
      <ask var="edit_request" prompt="What would you like to change? (tasks, scope, priority, requirements, etc.)"/>
      <tasks output="synthesis"><![CDATA[
        Apply user's requested changes to synthesis:
        - User request: ${edit_request}
        - Update relevant fields in synthesis
        - Re-display updated synthesis using <output id="understanding-output"> format
      ]]></tasks>
      <goto to="todos:review"/>
    </stage>

    <!-- todos:split-plan: Create and review split plan -->
    <stage id="todos:split-plan">
      <tasks output="subtasks"><![CDATA[
        Analyze requirements and group into logical subtasks:
        For each subtask determine:
          * title: Clear, actionable title
          * priority: critical | high | medium | low (based on dependencies)
          * requirements: Subset of original requirements
          * affected_files: Relevant files for this subtask

        Present split plan:
        ### 📦 Todo Split Plan

        | # | Todo | Priority | Files |
        |---|------|----------|-------|
        | 1 | [subtask_1_title] | [priority] | [files] |
        | 2 | [subtask_2_title] | [priority] | [files] |
      ]]></tasks>
      <ask id="split_choice" prompt="Is this plan okay?">
        <choice key="1" value="create-all" label="Yes, create all"/>
        <choice key="2" value="edit-plan" label="Edit plan"/>
        <choice key="3" value="cancel" label="Cancel"/>
      </ask>
      <goto when="${split_choice.value} == 'create-all'" to="todos:create-multiple-prep"/>
      <goto when="${split_choice.value} == 'edit-plan'" to="todos:split-plan"/>
      <goto to="todos:cancel"/>
    </stage>

    <!-- todos:create-single: Prepare for single todo creation -->
    <stage id="todos:create-single">
      <set var="split_mode" value="false"/>
      <goto to="todos:create"/>
    </stage>

    <!-- todos:create-multiple-prep: Prepare for multiple todo creation -->
    <stage id="todos:create-multiple-prep">
      <set var="split_mode" value="true"/>
      <goto to="todos:create"/>
    </stage>

    <!-- todos:create: Invoke skill for todo creation (single or multiple) -->
    <stage id="todos:create">
      <invoke name="Skill">
        <param name="skill" value="axel-todos:skill-axel-todos"/>
        <param name="trigger" value="todos:create"/>
        <param name="split_mode" value="${split_mode}"/>
        <param name="topic" value="${all_args}"/>
        <param name="synthesis" value="${synthesis}"/>
        <param name="subtasks" value="${subtasks}"/>
      </invoke>
      <stop kind="end"/>
    </stage>

    <!-- todos:cancel: User cancelled operation -->
    <stage id="todos:cancel">
      <print>Operation cancelled.</print>
      <stop kind="end"/>
    </stage>

    <!-- todos:list: List all todos -->
    <stage id="todos:list">
      <invoke name="Skill">
        <param name="skill" value="axel-todos:skill-axel-todos"/>
        <param name="trigger" value="todos:list"/>
      </invoke>
      <stop kind="end"/>
    </stage>

    <!-- todos:run: Route to run-direct, run-workspace, or run-select -->
    <stage id="todos:run">
      <goto when="rest_args = ''" to="todos:run-select"/>
      <goto when="rest_args ends_with '.md'" to="todos:run-direct"/>
      <goto when="rest_args contains '/' OR rest_args contains '\\'" to="todos:run-direct"/>
      <goto to="todos:run-workspace"/>
    </stage>

    <!-- todos:run-direct: Run specific todo by path -->
    <stage id="todos:run-direct">
      <invoke name="Task">
        <param name="subagent_type">axel-todos:agent-axel-todo-runner:agent-axel-todo-runner</param>
        <param name="description">Run todo: ${rest_args}</param>
        <param name="prompt"><![CDATA[
          todo_file_path: ${rest_args}
        ]]></param>
      </invoke>
      <stop kind="end"/>
    </stage>

    <!-- todos:run-workspace: Run todos by workspace name -->
    <stage id="todos:run-workspace">
      <invoke name="Skill">
        <param name="skill" value="axel-todos:skill-axel-todos"/>
        <param name="trigger" value="todos:run"/>
        <param name="workspace_name" value="${rest_args}"/>
      </invoke>
      <stop kind="end"/>
    </stage>

    <!-- todos:run-select: Select and run todo via skill -->
    <stage id="todos:run-select">
      <invoke name="Skill">
        <param name="skill" value="axel-todos:skill-axel-todos"/>
        <param name="trigger" value="todos:run"/>
      </invoke>
      <stop kind="end"/>
    </stage>

  </execution>

  <output id="understanding-output" format="markdown">
    ## Here's what I understood:

    ### 🎯 Problem
    [What user wants, why it matters - from synthesis.summary]

    ### 📋 Tasks
    - [ ] [Task 1 from requirements]
    - [ ] [Task 2 from requirements]
    - [ ] [Task 3 from requirements]

    ### ✅ Verification
    - [How to verify task 1 works]
    - [How to verify task 2 works]
    - [How to verify task 3 works]

    ### 📁 Scope
    - [File 1 to create/modify]
    - [File 2 to create/modify]

    ---
    **Type:** [todo_type] | **Complexity:** [complexity] | **Priority:** [priority]
  </output>

  <understanding>
    ⛔ WORKFLOW COMPLIANCE:
    - Step 2 (Investigate) → CANNOT be skipped
    - Step 3 (Analyze) → MUST generate synthesis
    - Step 4 (Present & Interact) → LOOP until user decides
    - Step 5 (Create) → FINAL action, only after user confirms
    - Order CANNOT be changed
    - "Not necessary" or "we can skip" = NOT ACCEPTABLE

    ⛔ STEP 4 LOOP RULES:
    - Present synthesis → Show options → Handle choice
    - "Edit" → Apply changes → Show updated synthesis (loop)
    - "Create" → Exit loop → Go to Step 5
    - "Cancel" → Stop immediately
    - User controls the loop - iterate until satisfied

    ⛔ OUTPUT TO CREATE PHASE:
    - Understanding phase produces synthesis data
    - Create phase receives: topic, todo_type, complexity, priority, requirements, affected_files
    - Create phase handles: workspace, template, document generation, validation

    ⛔ SPLIT DECISION:
    - ALWAYS ask user: single or multiple todos
    - DO NOT decide based on complexity - let user choose
    - IF multiple: group logically, assign priorities based on dependencies
    - IF multiple: present plan before creating, allow user to modify
  </understanding>

</document>
```
