---
name: axel-cmd-todos-create-workflow
description: Create todo document from synthesis data
type: workflow
triggers:
  - todos create
  - create todos
---

# AXEL Workflow: Cmd Todos Create

```xml
<document type="workflow">

  <enforcement>
    <![CDATA[
    PATH RESOLUTION:
    - Read the `src`, `ref`, or `target` attribute from the document XML to locate referenced files
    - ${CLAUDE_PLUGIN_ROOT} resolves to plugin installation directory

    REFERENCE-BASED CREATION:
    - ALWAYS read AXEL-Todo.md for structure, implementation steps, and validation
    - DO NOT duplicate content from reference documents
    - Reference documents are already loaded - use them as source of truth

    SYNTHESIS REQUIRED:
    - This workflow REQUIRES synthesis data from Understanding phase
    - IF synthesis is missing → run Understanding workflow first
    - Synthesis provides: todo_type, complexity, priority, requirements, affected_files

    TEMPLATE SELECTION:
    - MUST follow template chain: AXEL-Todo.md → Specific Template
    - Match synthesis (todo_type + complexity) against template type
    - Template determines todo document structure

    WORKSPACE BOOTSTRAP:
    - Check for ${workspace}-Bootstrap.md in workspace folder
    - IF exists → load and apply workspace-specific rules
    - Bootstrap is OPTIONAL - workflow continues if not found

    FORBIDDEN:
    - Elements not in AXEL-Todo.md structure
    - "Creative" additions not in template
    - Adding CLAUDE.md to todo documents (it's a project config)
    - Adding AXEL-*.md to todo documents (framework resources)
    ]]>
  </enforcement>

  <objective>
    Create AXEL todo documents from synthesis data.
    All specifications, checklists, and patterns are read from AXEL-Todo.md.

    This is the CREATE phase - Understanding phase must complete first.
    Receives: topic, todo_type, complexity, priority, requirements, affected_files
  </objective>

  <documents load="always" mode="context">
    <read src="${AXEL_CORE_PLUGIN_ROOT}/AXEL-Bootstrap.md"/>
    <read src="${AXEL_CORE_PLUGIN_ROOT}/references/AXEL-Checklist.md"/>
    <read src="${CLAUDE_PLUGIN_ROOT}/skills/skill-axel-todos/references/AXEL-Todo.md"/>
    <understanding>
      <![CDATA[
      !! MANDATORY: READ -> UNDERSTAND -> APPLY !!

      Bootstrap: Core AXEL rules and enforcement

      AXEL-Todo.md provides:
      - <frontmatter>: YAML structure with all fields and formats
      - <axel-tag-structure>: Element order and document hierarchy
      - <templates>: Reference to todo templates
      - <decision name="task-type-structure">: Task types
      - <implementation name="creating-todo">: Step-by-step creation process
      - <checklist name="todo-validation">: Complete validation checklist

      AXEL-Checklist.md: Generic document validation checklist

      This workflow creates the document - Understanding provides the data.
      ]]>
    </understanding>
  </documents>

  <variables>
    <var name="topic" from="param.topic"/>
    <var name="todo_type" from="param.todo_type" default="coding"/>
    <var name="complexity" from="param.complexity" default="simple"/>
    <var name="priority" from="param.priority" default="medium"/>
    <var name="requirements" from="param.requirements"/>
    <var name="affected_files" from="param.affected_files"/>
    <var name="split_mode" from="param.split_mode" default="false"/>
    <var name="subtasks" from="param.subtasks" default="[]"/>
  </variables>

  <execution flow="linear">
    <![CDATA[
    LINEAR EXECUTION - Create todo from synthesis:

    Step 0 - Check Split Mode:
    - IF split_mode = true AND subtasks is not empty:
      → GO TO SPLIT FLOW (Step 1S)
    - ELSE:
      → Continue with SINGLE FLOW (Step 1)

    --- SINGLE FLOW (split_mode = false) ---

    Step 1 - Validate Synthesis:
    - IF topic is empty → print error and stop
    - IF todo_type is empty → default to "coding"
    - IF complexity is empty → default to "simple"
    - IF priority is empty → default to "medium"
    - Print: "## Todo Creation"
    - Print: "**Topic:** ${topic}"
    - Print: "**Type:** ${todo_type} | **Complexity:** ${complexity} | **Priority:** ${priority}"

    Step 2 - Select Workspace:
    - Determine project root:
      * Find nearest directory containing .claude/ folder
      * Start from current working directory, search upward
      * Set ${project_root} = found directory
    - List ONLY directories in ${project_root}/.claude/workspaces/
      * Filter to directories only (exclude files like BACKLOGS.md)
      * A valid workspace is a directory containing pending/, in-progress/, completed/ subfolders
    - IF no workspace directories exist:
      * Print: "No workspace found."
      * Run: /axel:workspace init (creates workspace from CLAUDE.md project name)
      * Re-list directories in ${project_root}/.claude/workspaces/
      * IF still no workspace → Print error and stop workflow
    - AUTO-SELECT if single workspace:
      * IF workspace_count = 1 → auto-select, print: "Using workspace: ${workspace}"
      * IF workspace_count > 1 → ask user to select from list
    - Set base_path = ${project_root}/.claude/workspaces/${workspace}
    - Set pending_path = ${base_path}/pending

    Step 2.5 - Load Workspace Bootstrap (if exists):
    - Check if ${base_path}/${workspace}-Bootstrap.md exists
    - IF exists:
      * Read the workspace bootstrap file
      * Apply workspace-specific enforcement rules
      * Note discovered project references for <documents> generation
      * Print: "Loaded workspace bootstrap: ${workspace}-Bootstrap.md"
    - IF not exists:
      * Skip (workspace bootstrap is optional)

    Step 3 - Select Template:
    - Determine execution flow based on complexity:

      * LINEAR (default - use for most todos):
        - Sequential steps without loops or branching
        - No skill/workflow/agent invocation needed
        - Single responsibility, predictable outcome
        - Examples: Bug fix, feature, refactor, analysis, research

      * STAGED (only when truly needed):
        - Skill invocation (<invoke name="Skill">)
        - Workflow execution (<workflow src="...">)
        - Agent delegation (<invoke name="Task"> with subagent)
        - Iterative refinement loops
        - User approval gates
        - Examples: Multi-phase migration, complex orchestration

    - Load selected template:
      * Linear: ${CLAUDE_PLUGIN_ROOT}/skills/skill-axel-todos/templates/todos/AXEL-Todo-Linear-Tpl.md
      * Staged: ${CLAUDE_PLUGIN_ROOT}/skills/skill-axel-todos/templates/todos/AXEL-Todo-Staged-Tpl.md

    Step 4 - Generate Document:
    - Create slug from topic (kebab-case, max 50 chars)
    - Apply AXEL-Todo.md <frontmatter> format:
      * Reference: AXEL-Todo.md <frontmatter> for exact field order
      * Use synthesis data for priority, description
      * Set status: pending, created_at: current date
      * Add workspace field

    - Generate <documents> element:
      * EXCLUDE from suggestions:
        - CLAUDE.md (project config, not task resource)
        - AXEL-*.md files (framework resources, not task-specific)
        - .claude/ folder contents (system files)
      * Use affected_files from synthesis
      * For each related file, determine load type:
        - load="always": Core files needed throughout execution
        - load="on-demand": Reference files needed for specific steps
      * Each <read> must have <understanding> explaining WHY the file is needed

    - Apply selected template structure
    - Map synthesis data to document elements:
      * requirements → <requirements>
      * affected_files → <output>
      * Generate <execution> steps from requirements
      * Generate <todos> from execution steps
      * Generate <verification> from requirements
    - Path: ${pending_path}/${slug}.md

    Step 5 - Generate Verification Items:
    - FOR EACH requirement in requirements:
      * Write a verification item that proves the requirement is done
      * Focus on WHAT to verify, not HOW (agent decides method)

    - Verification principles:
      * Concrete: Specific file, function, behavior - no ambiguity
      * Testable: Can be checked programmatically
      * Assertion: Statement of expected state, not a question

    - FORBIDDEN:
      * Question format ("is it...?", "does it...?")
      * Vague terms ("properly", "correctly", "well")
      * Missing target ("code works" → WHICH code? WHERE?)

    Step 6 - Validate Document:
    - Use AXEL-Todo.md <checklist name="todo-validation">
    - Check: frontmatter, structure, elements
    - Verify element order matches <axel-tag-structure>
    - Validate against AXEL-Checklist.md standards
    - IF validation fails → fix immediately before proceeding

    Step 7 - Save and Confirm:
    - Create pending folder if needed
    - Save todo document to ${pending_path}/${slug}.md
    - Print: "✅ Created: ${pending_path}/${slug}.md"
    - Print: "   Type: ${todo_type} | Complexity: ${complexity} | Priority: ${priority}"
    - END SINGLE FLOW

    --- SPLIT FLOW (split_mode = true) ---

    Step 1S - Validate Split Data:
    - IF subtasks is empty → print error and stop
    - Print: "## Creating ${subtasks.length} Todos"
    - Print: "**Parent Topic:** ${topic}"

    Step 2S - Select Workspace (same as Step 2):
    - Determine project root
    - List workspace directories
    - Auto-select if single workspace
    - Set base_path and pending_path

    Step 3S - Load Workspace Bootstrap (same as Step 2.5):
    - Check if ${base_path}/${workspace}-Bootstrap.md exists
    - IF exists → load and apply

    Step 4S - Create Each Todo:
    - Set created_count = 0
    - Set index = 1
    - FOR EACH subtask in subtasks:

        4S.1 - Extract subtask data:
          * title = subtask.title
          * priority = subtask.priority
          * requirements = subtask.requirements
          * affected_files = subtask.affected_files

        4S.2 - Determine template (same logic as Step 3):
          * Default to LINEAR for most todos
          * Use STAGED only when skill/workflow/agent invocation needed

        4S.3 - Generate document:
          * Create slug from title (kebab-case, max 50 chars)
          * Create index_prefix = zero-padded 3-digit number (001, 002, 003, etc.)
          * Final slug = ${index_prefix}-${slug}
          * Apply AXEL-Todo.md frontmatter format
          * Use subtask data for fields
          * Generate <execution>, <todos>, <verification>
          * Path: ${pending_path}/${index_prefix}-${slug}.md

        4S.4 - Validate document:
          * Use AXEL-Todo.md <checklist name="todo-validation">
          * IF fails → fix before proceeding

        4S.5 - Save:
          * Save to ${pending_path}/${index_prefix}-${slug}.md
          * Increment created_count
          * Increment index
          * Print: "✅ [${created_count}/${subtasks.length}] ${index_prefix}-${slug}.md (${priority})"

    Step 5S - Summary:
    - Print: ""
    - Print: "✅ Created ${created_count} todos in ${workspace}/pending/"
    - FOR EACH created todo:
      * Print: "   - ${index_prefix}-${slug}.md (${priority})"
    ]]>
  </execution>

  <output format="json">
    // Single mode (split_mode = false):
    {
      "split_mode": false,
      "path": "created file path",
      "slug": "todo-slug",
      "todo_type": "coding|analysis|research|migration",
      "complexity": "simple|medium|complex",
      "flow": "linear|staged",
      "workspace": "workspace name"
    }

    // Split mode (split_mode = true):
    {
      "split_mode": true,
      "workspace": "workspace name",
      "created_count": 3,
      "todos": [
        {"path": "...", "slug": "001-todo-first", "priority": "high"},
        {"path": "...", "slug": "002-todo-second", "priority": "medium"},
        {"path": "...", "slug": "003-todo-third", "priority": "low"}
      ]
    }
  </output>

  <understanding/>

</document>
```
