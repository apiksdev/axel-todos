---
name: axel-cmd-todos-create-workflow
description: Create new todo with inline brainstorm and workspace selection
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

    BRAINSTORM GATE (MANDATORY):
    - Todo creation REQUIRES successful brainstorm synthesis
    - IF synthesis incomplete → ask clarification, do NOT proceed
    - User MUST confirm synthesis before todo generation
    - NEVER skip brainstorm - it's the foundation of todo quality

    TEMPLATE SELECTION (MANDATORY - after brainstorm confirmation):
    - MUST follow template chain: AXEL-Todo.md → Template Bootstrap → Specific Template
    - Read AXEL-Todo.md <templates> section first
    - Load AXEL-Todo-Template-Bootstrap.md from referenced path
    - Match synthesis (todo_type + complexity) against template "ask" keywords
    - Select MOST appropriate template - never guess or skip
    - Template determines todo document structure

    FORBIDDEN:
    - Elements not in AXEL-Todo.md structure
    - "Creative" additions not in template
    - Claiming compliance without verification
    - Adding CLAUDE.md to todo documents (it's a project config, not a todo resource)
    - Adding AXEL-Bootstrap.md, AXEL-Checklist.md to todo documents (workflow provides these)

    ARGUMENT PARSING:
    - topic = param.topic (passed from router command)
    - Workspace is selected via folder listing
    ]]>
  </enforcement>

  <objective>
    Create AXEL todo documents through inline brainstorming using reference-based approach.
    All specifications, checklists, and patterns are read from AXEL-Todo.md.
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
      - <templates>: Reference to todo templates (AXEL-Todo-Template-Bootstrap.md)
      - <decision name="task-type-structure">: Task types (coding, analysis, research, migration)
      - <decision name="intake-process">: Pre-generation requirements
      - <implementation name="creating-todo">: Step-by-step creation process (Step 1-10)
      - <checklist name="todo-validation">: Complete validation checklist

      AXEL-Checklist.md: Generic document validation checklist

      This workflow orchestrates the process - all content comes from references.
      ]]>
    </understanding>
  </documents>

  <variables>
    <var name="topic" from="param.topic"/>
  </variables>

  <execution flow="linear">
    <![CDATA[
    LINEAR EXECUTION - Reference-based todo creation with inline brainstorm:

    Step 1 - Validate Input:
    - IF topic is empty → print error and stop
    - Print: "## Todo Creation"
    - Print: "**Topic:** ${topic}"

    Step 2 - Discovery (Understand Topic):
    - Analyze the topic using four perspectives
    - Present findings as bullet lists

      DISCOVERY (What?):
      - What exactly is being asked? What's the core request?
      - What's the big picture? How does this fit into the larger system?
      - Who will use this? Who are the stakeholders?
      - Who is affected by this change? Direct and indirect impact?
      - What's the scope - what's explicitly in?
      - What's explicitly out of scope? What should we NOT do?

      ELICITATION (How?):
      - How should this be implemented? What's the approach?
      - What are the technical details and specifications?
      - What constraints exist? (technical, time, budget, resources)
      - What's the priority? Must-have vs nice-to-have?
      - What are the acceptance criteria? How do we know it's done?

      DEEP INQUIRY (What if?):
      - What could go wrong? What are the risks?
      - What dependencies exist? Are there failure points?
      - What if requirements change mid-way?

      SOCRATIC (Why?):
      - Why this approach? Are there alternatives?
      - What assumptions are being made? Are they valid?
      - What would a critic say about this?

    - Determine task characteristics:
      * Task type: Coding / Analysis / Research / Migration
        → Reference: AXEL-Todo.md <decision name="task-type-structure">
      * Complexity: Simple / Medium / Complex
      * Priority: critical / high / medium / low

    - Generate synthesis:
      * summary: Brief description of what needs to be done
      * todo_type: coding | analysis | research | migration
      * complexity: simple | medium | complex
      * priority: critical | high | medium | low
      * requirements: List of key requirements
      * constraints: Any limitations or boundaries
      * risks: Identified risks (from Deep Inquiry)
      * assumptions: Key assumptions made (from Socratic)

    - GATE CHECK (synthesis completeness):
      * IF any field is empty or unclear → ask clarification questions
      * Use relevant perspective questions (Discovery/Elicitation/Deep/Socratic)
      * Re-analyze with new information
      * Repeat until synthesis is complete
      * NEVER proceed without: summary, todo_type, complexity, requirements

    Step 3 - Confirm Synthesis (GATE):
    - Display synthesis summary:
      * Topic, Type, Complexity, Priority
      * Summary, Requirements, Constraints
      * Risks, Assumptions
    - Ask user: "Is this synthesis correct?"
      * Option 1: "Yes, proceed" → continue to Step 4
      * Option 2: "Needs clarification" → return to Step 2 with feedback
      * Option 3: "Cancel" → stop workflow
    - IF "Needs clarification":
      * Ask: "What needs to be clarified?"
      * Return to Step 2 with user feedback
      * Re-run brainstorm with additional context
    - GATE: ONLY proceed to Step 4 after explicit user confirmation

    Step 4 - Select Workspace:
    - Determine project root:
      * Find nearest directory containing .claude/ folder
      * Start from current working directory, search upward
      * Set ${project_root} = found directory
    - List folders in ${project_root}/.claude/workspaces/
    - IF no workspaces exist:
      * Print: "No workspace found. Run /axel:workspace {name} first."
      * Print: "Searched in: ${project_root}/.claude/workspaces/"
      * Stop workflow
    - Ask user to select workspace from list
    - Set base_path = ${project_root}/.claude/workspaces/${workspace}
    - Set pending_path = ${base_path}/pending

    Step 5 - Understand Document Structure:
    - Read AXEL-Todo.md <axel-tag-structure>
    - Understand element order based on task type
    - Identify required vs optional elements
    - Know where each piece of information belongs in final structure

    Step 6 - Select Template (MANDATORY - follow chain):

    6.1 - Read AXEL-Todo.md <templates> section:
    - Find: <read src="...AXEL-Todo-Template-Bootstrap.md"/>
    - This is the routing template

    6.2 - Load Template Bootstrap:
    - Path: ${CLAUDE_PLUGIN_ROOT}/skills/skill-axel-todos/templates/todos/AXEL-Todo-Template-Bootstrap.md
    - Contains all available templates with "ask" keywords

    6.3 - Match synthesis against template keywords:
    - Linear: [linear, simple, sequential, basic, straightforward, coding, implement, create, build, develop, fix, feature]
    - Staged: [staged, complex, branching, parallel, orchestrate, delegate, workflow, agent, multi-step]
    - Analysis: [analyze, review, inspect, examine, evaluate, audit, check, performance]
    - Research: [research, investigate, explore, find, search, compare, discover]
    - Migration: [migrate, migration, upgrade, convert, port, transition, move, transfer]

    6.4 - Selection logic:

    - Determine execution flow: linear | staged
      * linear: Text-based instructions (RECOMMENDED for most todos)
        - Sequential steps without loops or branching
        - No skill/workflow/agent invocation needed
        - Simple coding, analysis, generation tasks
        - Single responsibility, predictable outcome
        - Examples: Bug fix, single file change, documentation update, code review
      * staged: ONLY for complex scenarios requiring:
        - Skill invocation (<invoke name="Skill">)
        - Workflow execution (<workflow src="...">)
        - Agent delegation (<invoke name="Task"> with subagent)
        - Iterative refinement loops (repeat until quality threshold)
        - User approval gates (generate → review → revise → approve)
        - Dynamic branching based on intermediate results
        - Parallel execution of independent tasks
        - Examples: Multi-file refactoring, feature with dependencies, migration with rollback

    - Apply selection:
      * IF todo_type = "coding":
        → complexity = simple → AXEL-Todo-Linear-Tpl.md (linear flow)
        → complexity = medium/complex → AXEL-Todo-Staged-Tpl.md (staged flow)
      * IF todo_type = "analysis" → AXEL-Todo-Analysis-Tpl.md (linear flow)
      * IF todo_type = "research" → AXEL-Todo-Research-Tpl.md (linear flow)
      * IF todo_type = "migration" → AXEL-Todo-Migration-Tpl.md (staged flow)

    6.5 - Load selected template:
    - Path: ${CLAUDE_PLUGIN_ROOT}/skills/skill-axel-todos/templates/todos/refs/{selected-template}
    - Read template's axel-tag-structure
    - This structure defines the todo document format

    Step 7 - Follow Implementation Guide:
    - Read AXEL-Todo.md <implementation name="creating-todo">
    - This defines Step 1-10 creation process
    - Apply each step using synthesis data from Step 2

    Step 8 - Generate Document:
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
      * Identify related files from synthesis (requirements, context, constraints)
      * Ask user: "Which files are related to this todo?"
        - Show suggested files based on topic analysis
        - Allow user to add/remove files
      * For each related file, determine load type:
        - load="always": Core files needed throughout execution
        - load="on-demand": Reference files needed for specific steps
      * Each <read> must have <understanding> explaining WHY the file is needed
      * Reference: AXEL-Todo.md <axel-tag-structure> for documents format

    - Apply selected template structure from Step 6
    - Map synthesis data to document elements
    - Path: ${pending_path}/${slug}.md

    Step 9 - Validate Document:
    - Use AXEL-Todo.md <checklist name="todo-validation">
    - Check: frontmatter, structure, elements
    - Verify element order matches <axel-tag-structure>
    - Validate against AXEL-Checklist.md standards
    - IF validation fails → fix immediately before proceeding

    Step 10 - Save and Confirm:
    - Create pending folder if needed
    - Save todo document to ${pending_path}/${slug}.md
    - Print: "Created: ${pending_path}/${slug}.md (${todo_type}, ${complexity})"
    - Print: "Todos create workflow completed."
    ]]>
  </execution>

  <output format="json">
    {
      "path": "created file path",
      "slug": "todo-slug",
      "todo_type": "coding|analysis|research|migration",
      "complexity": "simple|medium|complex",
      "flow": "linear|staged",
      "workspace": "workspace name"
    }
  </output>

  <understanding/>

</document>
```
