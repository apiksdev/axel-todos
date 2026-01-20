---
name: axel-todo
description: Todo engineering - creating todos aligned with user expectations
type: reference
---

```xml
<document type="reference">

  <enforcement>
    - MUST identify missing information before creating todo
    - MUST ask clarification questions for ambiguous requirements
    - NEVER assume technical choices without user confirmation
    - Read `src` attribute from template references to locate todo template files
    - ${CLAUDE_PLUGIN_ROOT} resolves to plugin installation directory
  </enforcement>

  <objective>
    Structure of todo definition files. AXEL Todo is an XML-based configuration format for creating effective todos by correctly understanding user expectations. It applies AXEL Methodology principles (question-driven understanding, no assumptions) to todo engineering.
  </objective>

  <frontmatter>
    <![CDATA[
---
name: todo-coding               # Todo name (kebab-case)
description: Coding todo        # Short description, max 200 characters
type: todo                      # Always "todo"
status: pending                 # pending | in-progress | completed
priority: medium                # critical | high | medium | low
workspace: my-workspace         # Workspace name this todo belongs to (optional for default)
depends_on:                     # List of prerequisite todos (with .md extension)
  - setup-database.md           # Must be completed before this todo starts
  - create-models.md
created_at: 2025-01-05          # ISO date (YYYY-MM-DD)
completed_at:                   # ISO date, set when status becomes completed
---
    ]]>
  </frontmatter>

  <templates load="always" mode="context">
    <read src="${CLAUDE_PLUGIN_ROOT}/skills/skill-axel-todos/templates/todos/AXEL-Todo-Template-Bootstrap.md"/>
    <axel-tag-structure>
      <![CDATA[
      Todo Document Structure (Unified)
      +-- Frontmatter (name, description, type, status, priority, workspace, created_at, completed_at, depends_on)
      +-- # Todo Title
      +-- ```xml
      +-- <document type="todo">
      |   +-- <enforcement> [all]
      |   +-- <objective> [all]
      |   +-- <documents name=".." load="always" mode="context">
      |   |   +-- <read src="..."/>
      |   |   +-- <understanding>...</understanding> (required)
      |   +-- <documents name=".." load="on-trigger" mode="context">
      |   |   +-- <read src="..." trigger="..."/>
      |   |   +-- <understanding>...</understanding> (required)
      |   +-- <documents name=".." load="on-demand" mode="context">
      |   |   +-- <read src="..." ask="..."/>
      |   |   +-- <understanding>...</understanding> (required)
      |   +-- <context> [coding]
      |   +-- <scope> [research]
      |   +-- <current_state> [migration]
      |   +-- <target_state> [migration]
      |   +-- <requirements> [coding, analysis]
      |   +-- <implementation> [coding]
      |   +-- <database> [coding, optional]
      |   +-- <endpoints> [coding, optional]
      |   +-- <frontend lang="..."> [coding, optional]
      |   +-- <backend lang="..."> [coding, optional]
      |   +-- <migration_steps> [migration]
      |   +-- <rollback_plan> [migration]
      |   +-- <compatibility> [migration]
      |   +-- <deliverables> [research]
      |   +-- <output format="..."> [coding, analysis]
      |   +-- <todos> [all, required] - Static task tracking
      |   +-- <execution flow="linear|staged"> [Stage Container]
      |   |   +-- (linear) text-based step instructions
      |   |   +-- (staged) <stage id="...">
      |   |       +-- <print>...</print>
      |   |       +-- <tasks output="...">...</tasks>
      |   |       +-- <bash run="..."/>
      |   |       +-- <workflow src="..." output="...">
      |   |       |   +-- <param name="..." value="..."/>
      |   |       +-- <call command="/..."/>
      |   |       +-- <ask var="..." prompt="...">
      |   |       |   +-- <goto when="..." to="stage-id"/>
      |   |       +-- <invoke name="Task|Skill" output="..." resumable="true|false">
      |   |       |   +-- <param name="..." value="..."/>
      |   |       +-- <set var="..." from="..."/>
      |   |       +-- <goto when="..." to="stage-id"/>
      |   |       +-- <stop kind="end|error"/>
      |   +-- <verification> [all]
      |   +-- <checklist> [all]
      |   +-- <understanding/> [all]
      +-- </document>
      +-- ```
      ]]>
    </axel-tag-structure>
    <understanding>
      !! MANDATORY: READ -> UNDERSTAND -> APPLY !!
      - READ the template file first
      - UNDERSTAND the structure and patterns
      - APPLY the template structure EXACTLY
      Reference = HOW to think | Template = HOW to write
    </understanding>
  </templates>

  <context>
    - Used for creating effective AI todos
    - Applies AXEL Methodology to todo engineering
    - Supports multiple task types: Coding, Analysis, Research
    - Ensures todos have clear objectives and verification criteria
    - Prevents unclear requests from producing faulty results
  </context>

  <principle name="core-principles">
    - Clarity First: Unclear request = unclear todo = faulty result
    - Ask Questions: Don't guess missing information, ask the user
    - Provide Context: Specify why the task is being done, who it's for
    - Be Specific: Write concrete, measurable steps instead of general instructions
    - Verify: Add success criteria and verification steps to every todo
  </principle>

  <decision name="task-type-structure" date="2024-12">
    When: Creating todos for different task types
    Action: Use task-specific structure (unified elements)
    - Coding: objective, documents, context, requirements, implementation, [database], [endpoints], [frontend], [backend], output, verification, checklist
    - Analysis: objective, documents, requirements, output, verification, checklist
    - Research: objective, documents, scope, deliverables, verification, checklist
    - Migration: objective, documents, current_state, target_state, migration_steps, rollback_plan, compatibility, verification, checklist
    Note: Elements in [brackets] are optional
    Reason: Each task type has different information requirements but shares common elements
  </decision>

  <decision name="intake-process" date="2024-12">
    <![CDATA[
    When: Before creating any todo
    Action: Assess task characteristics and determine todo structure

    Task Assessment:
    - Task type: Coding / Analysis / Research / Migration
    - Complexity: Simple (single file) / Medium / Complex (multiple files)
    - Todo count: Single / Multiple (are there independent sub-tasks?)
    - Execution strategy: Parallel / Sequential (are there dependencies?)

    Pre-Generation Requirements (MUST determine before writing todo):
    1. First: Define EXECUTION flow
       - Select flow type: linear (simple) or staged (complex)
       - Define all steps/stages with clear actions
       - This is the PRIMARY source of task structure

    2. Then: Generate TODOS from execution
       - Each todo maps to an execution step/stage
       - Todos = progress checkpoints for execution
       - Can add custom todos as needed

    Generation Order:
    - <execution> = PRIMARY (defines what happens)
    - <todos> = DERIVED (tracks execution progress)

    Example:
      <todos>
        - [ ] Step 1: Setup complete
        - [ ] Step 2: Database applied
        - [ ] Step 3: Backend implemented
        - [ ] Step 4: Frontend implemented
        - [ ] Step 5: Verification passed
      </todos>

      <execution flow="linear">
        Step 1 - Setup:
        - Read <documents> for context
        - Review <requirements>

        Step 2 - Database:
        - Apply <database> schema

        Step 3 - Backend:
        - Execute items in <backend>

        Step 4 - Frontend:
        - Execute items in <frontend>

        Step 5 - Verify:
        - Run <verification> checks
        - Answer <checklist> questions
      </execution>

    Execution References Other Sections:
    - "Read <documents>" -> loads document section content
    - "Execute <backend>" -> performs backend section items
    - "Run <verification>" -> applies verification criteria
    - Section references eliminate duplication

    Reason: Execution defines the work; todos track its completion
    ]]>
  </decision>

  <decision name="backend-frontend-format" date="2024-12">
    <![CDATA[
    When: Defining backend services or frontend pages in coding todos
    Action: Use structured bullet list format with lang attribute

    Backend Format:
      <backend lang="csharp" path="src/Services/">
        ServiceName (action):
        - inject: Dependency1, Dependency2
        - methods: Method1, Method2, Method3
        - sub:
          - SubService1 (action):
            - inject: Dependency1
            - methods: Method1, Method2
      </backend>

    Frontend Format:
      <frontend lang="typescript" path="src/pages/">
        - PageName (action): description
      </frontend>

    Actions:
      - (create): New item to be created
      - (alter): Existing item to be modified
      - (delete): Item to be removed

    Backend Properties:
      - inject: Constructor dependencies (DI) - optional
      - methods: Public methods (PascalCase)
      - sub: Nested/child services (optional, can have own inject)

    Example:
      <backend lang="csharp" path="src/Services/">
        AuthService (create):
        - inject: IEmailService, ILogger
        - methods: Login, Logout, Refresh, ValidateToken
        - sub:
          - TokenService (create):
            - inject: IConfiguration
            - methods: Generate, Verify, Decode
      </backend>

      <frontend lang="typescript" path="src/pages/">
        - LoginPage (create): email, password inputs
        - DashboardPage (create): user info, navigation
      </frontend>

    Reason: Clear, editable bullet list format with language info in element
    ]]>
  </decision>

  <decision name="todos-section" date="2024-12">
    <![CDATA[
    When: Tracking progress within a todo
    Action: Use <todos> section with markdown checkbox format

    Format:
      <todos>
        - [ ] Pending task description
        - [ ] Another pending task
        - [x] Completed task
      </todos>

    Characteristics:
      - Static: Written at todo creation time, not modified during execution
      - Purpose: Track progress, resume from failure point
      - Format: Markdown checkbox syntax (- [ ] / - [x])
      - Placement: After implementation, before execution

    Reason: Simple, readable format for task tracking that integrates with todo structure
    ]]>
  </decision>

  <decision name="execution-flow" date="2024-12">
    <![CDATA[
    When: Todo needs to be executable (not just declarative)
    Action: Add <execution> section with flow attribute

    Flow Types:
      - Linear (flow="linear"): Text-based sequential steps in CDATA
      - Staged (flow="staged"): XML-based stages with full pattern support

    Linear Execution:
      <execution flow="linear">
        <![CDATA[
        Step 1 - Understand:
        - Read requirements
        Step 2 - Execute:
        - Implement changes
        ] ]>
      </execution>

    Staged Execution Elements:
      - <stage id="..."> - Named execution stage
      - <parallel id="..."> - Concurrent stage execution
      - <goto when="..." to="..."> - Conditional branching
      - <invoke> - Delegate to agent
      - <workflow> - Call external workflow
      - <ask>, <confirm> - User interaction
      - <tasks> - Task operations
      - <set var="..." from="..."> - Variable assignment
      - <print> - Display message
      - <stop kind="end|error"> - Terminate execution

    Staged Execution Example:
      <execution flow="staged">
        <stage id="init">
          <tasks>Parse input parameters</tasks>
          <goto to="execute"/>
        </stage>
        <stage id="execute">
          <invoke name="Task" output="result">
            <param name="subagent_type">coding-agent</param>
          </invoke>
          <goto to="verify"/>
        </stage>
        <parallel id="checks">
          <stage id="lint">...</stage>
          <stage id="test">...</stage>
        </parallel>
        <stage id="complete">
          <stop kind="end"/>
        </stage>
      </execution>

    Selection Guide:
      - Linear: Simple sequential tasks, no branching needed
      - Staged: Complex tasks with branching, parallel, loops, delegation

    Reason: Enables executable todos that can run autonomously or delegate to agents
    ]]>
  </decision>

  <requirements>
    - Frontmatter must include: name, description, type, status, priority, created_at
    - Optional frontmatter: workspace, depends_on (list), completed_at
    - Status must be one of: pending | in-progress | completed
    - Priority must be one of: critical | high | medium | low
    - Workspace must be a valid workspace name (if specified)
    - Dates must be ISO format (YYYY-MM-DD)
    - depends_on entries must have .md extension and exist in .claude/workspaces/
    - completed_at must be set when status changes to completed
    - Document must have type="todo" root element
    - Use correct template for task type (Coding/Analysis/Research/Migration)
    - Objective must be clear and specific (use <objective> for all types)
    - Verification must exist (all types)
    - Checklist must exist (all types) - question format
    - No vague language allowed
    - File output paths must be relative (./path/to/file.ext) [coding, analysis]
    - Rollback todo must exist [migration]
    - Todos format: markdown checkbox (- [ ] / - [x]) [optional]
    - Execution flow attribute required if execution exists (linear/staged)
    - Staged execution: all stages must end with <stop/> or <goto/>
    - Staged execution: all goto targets must exist as stage ids
  </requirements>

  <implementation name="file-locations">
    Default Workspace:
    .claude/workspaces/default/
    - pending/                   # New todos, not yet started
      - {todo-name}.md
    - in-progress/               # Todos currently being worked on
      - {todo-name}.md
    - completed/                 # Finished todos
      - {todo-name}.md

    Named Workspaces:
    .claude/workspaces/{workspace}/
    - pending/
    - in-progress/
    - completed/

    Folder Structure Rules:
    - New todos are created in pending/ folder
    - When status changes, file moves to corresponding folder
    - Frontmatter status field must match folder location
    - Script handles move + frontmatter update atomically
    - "default" is reserved workspace name (created by /axel:install)
  </implementation>

  <implementation name="creating-todo">
    Step 1 - Determine Task Type:
    - Coding: Implementation tasks
    - Analysis: Review/audit tasks
    - Research: Investigation tasks
    - Migration: System change tasks

    Step 2 - Set Metadata:
    - Workspace: Assign to relevant workspace (optional, defaults to default)
    - Created_at: Set to current date (YYYY-MM-DD)
    - Status: pending (default) | in-progress | completed
      - pending: Not started yet
      - in-progress: Currently being worked on
      - completed: Task finished successfully
    - Priority: medium (default) | critical | high | low
      - critical: Must be done immediately, blocks other work
      - high: Important, should be done soon
      - medium: Normal priority
      - low: Can be deferred

    Step 3 - Define Dependencies:
    - Identify prerequisite todos that must complete first
    - List in depends_on with .md extension (e.g., setup-database.md)
    - If no dependencies, leave depends_on empty or omit
    - Dependencies create implicit blocking relationship

    Step 4 - Assess Complexity:
    - Simple: Single file
    - Medium: Multiple related files
    - Complex: Multiple independent files

    Step 5 - Gather Requirements:
    - Ask clarification questions for missing info
    - Get user confirmation on technical choices

    Step 6 - Define Structure:
    - Objective: Clear and specific goal
    - Requirements: Measurable criteria
    - Implementation: Specific approach

    Step 7 - Add Type-Specific Elements:
    - Coding: context, database, endpoints, frontend, backend
    - Analysis: requirements, output
    - Research: scope, deliverables
    - Migration: current_state, target_state, migration_steps, rollback_plan

    Step 8 - Define Execution:
    - Flow: linear | staged
    - Steps/Stages with clear actions
    - Todos derived from execution steps

    Step 9 - Add Validation:
    - Verification criteria
    - Checklist questions

    Step 10 - AXEL Checklist:
    - MUST validate against AXEL-Checklist.md standards
    - Verify todo-validation checklist
  </implementation>

  <implementation name="dependency-check">
    Before Execution - Check Dependencies (Runtime):
    1. Read depends_on list from frontmatter
    2. For each dependency todo file:
       - Search in all status folders: pending/, in-progress/, completed/
       - Check if file exists in completed/ folder
       - If not in completed/ → BLOCK execution (do not change status)
    3. If all dependencies in completed/ → ALLOW execution
    4. If execution blocked:
       - Report which dependencies are not completed
       - List pending dependency todos for user
       - Suggest running pending dependencies first

    Dependency Resolution:
    - Show dependency chain if nested dependencies exist
    - Re-check dependencies when user requests execution again
  </implementation>

  <output format="markdown">
    File: {todo-name}.md
    Path: .claude/workspaces/{workspace}/pending/{todo-name}.md (new todos start in pending/)
    Structure:
    - YAML frontmatter (---)
    - Markdown title (# Todo Name)
    - AXEL XML in code fence (```xml ... ```)
    - Document type="todo" with objective, requirements, execution
  </output>

  <verification>
    - Is frontmatter complete? (name, description, type, status, priority, created_at)
    - Is status valid? (pending | in-progress | completed)
    - Is priority valid? (critical | high | medium | low)
    - Is workspace valid? (if specified)
    - Is created_at in ISO format? (YYYY-MM-DD)
    - Are depends_on entries valid? (.md extension, existing files)
    - Is completed_at set when status is completed?
    - Is correct template used for task type?
    - Is objective clear and specific?
    - Does verification element exist?
    - Does checklist element exist? (question format)
    - Is vague language avoided?
    - Are file paths relative? [coding, analysis]
    - Is todos format correct? (- [ ] / - [x]) [if todos exists]
    - Does execution have flow attribute? [if execution exists]
    - Do all stages terminate properly? [if staged execution]
    - Do all goto targets exist? [if staged execution]
  </verification>

  <checklist name="todo-validation">
    Pre-generation:
    - Has task type been determined? (Coding/Analysis/Research/Migration)
    - Has workspace been determined? (optional, defaults to default)
    - Has status been set? (pending | in-progress | completed)
    - Has priority been set? (critical | high | medium | low)
    - Have dependencies been identified? (depends_on)
    - Has complexity been assessed?
    - Have questions been asked for missing information?
    - Has user approval been obtained?
    - Is execution needed? (Linear/Staged)

    Post-generation (All Types):
    - Is frontmatter complete? (name, description, type, status, priority, created_at)
    - Is status valid? (pending | in-progress | completed)
    - Is priority valid? (critical | high | medium | low)
    - Is workspace valid? (if specified)
    - Are depends_on entries valid? (.md extension)
    - Is created_at in ISO format?
    - Is objective clear and specific?
    - Does verification exist?
    - Does checklist exist? (question format)

    Pre-execution (Runtime):
    - Are all depends_on todos completed?
    - If not completed → block execution, report pending dependencies
    - Suggest running pending dependencies first

    Post-generation (Coding):
    - Is context sufficient? (project, tech stack)
    - Are requirements measurable?
    - Is implementation approach specified?
    - Are output file paths relative? (./path/to/file.ext)

    Post-generation (Analysis):
    - Are target files listed in documents?
    - Are requirements specified?
    - Is output format defined?

    Post-generation (Research):
    - Is scope defined? (include/exclude boundaries)
    - Are deliverables specified?

    Post-generation (Migration):
    - Is current state documented?
    - Is target state clearly defined?
    - Are migration steps ordered and atomic?
    - Does rollback todo exist?
    - Are breaking changes listed in compatibility?

    Post-generation (Todos):
    - Are todos in checkbox format? (- [ ] / - [x])
    - Are todos actionable and specific?
    - Do todos cover all implementation steps?

    Post-generation (Execution):
    - Does execution have flow attribute? (linear/staged)
    - Is correct flow type selected for complexity?
    - Linear: Are steps sequential and clear?
    - Staged: Do all stages have unique ids?
    - Staged: Do all stages end with stop or goto?
    - Staged: Are all goto targets valid stage ids?
    - Staged: Is there at least one stop element?
  </checklist>

  <understanding/>

</document>
```
