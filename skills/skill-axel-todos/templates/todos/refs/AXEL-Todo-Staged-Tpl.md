---
name: todo-staged
description: Template for executable todos with staged flow - supports branching, parallel, loops, delegation
type: template
---

# AXEL Template: Todo - Staged

```xml
<document type="todo">

  <enforcement>
    - MUST verify all requirements before execution
    - MUST follow existing code patterns and conventions
    - NEVER skip verification steps
    - Todos are static - written at todo creation time
    - Every execution path must terminate with <stop/>
  </enforcement>

  <objective>
    Executable todo with staged flow.
    Supports branching, parallel execution, loops, and agent delegation.
    Suitable for complex implementation tasks with multiple paths.
  </objective>

  <!-- Documents element: Load references and target files as context -->
  <documents load="always" mode="context">
    <read src="references/standards.md" ask="[standard, pattern, convention]"/>
    <read src="src/target-file.ts"/>
    <understanding>
      !! MANDATORY: READ → UNDERSTAND → APPLY !!
      - READ referenced files before execution
      - FOLLOW patterns from existing code
      - MATCH conventions from standards documents
    </understanding>
  </documents>

  <context>
    - Project: [Project type and tech stack]
    - Existing: [Available resources and dependencies]
    - Target: [Files to create or modify]
  </context>

  <requirements>
    - [Requirement 1]
    - [Requirement 2]
    - [Requirement 3]
  </requirements>

  <implementation>
    - [Implementation detail 1]
    - [Implementation detail 2]
    - [Implementation detail 3]
  </implementation>

  <!-- Optional: Database schema changes -->
  <database>
    Tables:
    - table_name (create)
      - id: uuid, primary key
      - field_name: type, constraints
    - existing_table (alter)
      - new_field: type (add)

    Indexes:
    - idx_table_field on table_name(field_name)
  </database>

  <!-- Optional: API endpoints -->
  <endpoints base="/api/v1/resource">
    - POST /create → { id, data }
    - GET /:id → { resource }
    - PUT /:id → { updated }
    - DELETE /:id → 204 No Content
  </endpoints>

  <!-- Optional: Frontend pages -->
  <frontend lang="typescript" path="src/pages/">
    - PageName (create): component description
    - ExistingPage (alter): modification description
  </frontend>

  <!-- Optional: Backend services -->
  <backend lang="csharp" path="src/Services/">
    ServiceName (create):
    - inject: IDependency1, IDependency2
    - methods: Method1, Method2, Method3
    - sub:
      - SubService (create):
        - inject: IDependency
        - methods: SubMethod1, SubMethod2

    ExistingService (alter):
    - inject: INewDependency
    - methods: NewMethod
  </backend>

  <output>
    Backend:
    - Create ./src/Services/ServiceName.cs
    - Alter ./src/Services/ExistingService.cs
    - Create ./src/Controllers/ResourceController.cs

    Frontend:
    - Create ./src/pages/PageName.tsx
    - Alter ./src/pages/ExistingPage.tsx
  </output>

  <!-- Todos: Derived from execution stages -->
  <todos>
    <![CDATA[
    - [ ] Stage: init - Setup complete
    - [ ] Stage: understand - Analysis complete
    - [ ] Stage: execute - Implementation complete
    - [ ] Stage: parallel-checks - Quality checks passed
    - [ ] Stage: complete - Todo finished
    ]]>
  </todos>

  <!-- Staged execution: XML-based with full pattern support -->
  <execution flow="staged">

    <!-- INIT: Parse parameters and setup -->
    <stage id="init">
      <tasks output="params">
        Step 1 - Parse Input:
        - Extract execution mode from context
        - Identify target files
        - Load project configuration
      </tasks>
      <set var="mode" from="params.mode"/>
      <set var="target" from="params.target"/>
      <goto to="understand"/>
    </stage>

    <!-- UNDERSTAND: Analyze requirements -->
    <stage id="understand">
      <print>Analyzing requirements...</print>
      <tasks output="analysis">
        Step 1 - Read Context:
        - Load referenced documents
        - Analyze existing patterns

        Step 2 - Assess Complexity:
        - Determine task complexity (simple|complex)
        - Identify dependencies
      </tasks>
      <set var="complexity" from="analysis.complexity"/>
      <goto when="${complexity} = 'simple'" to="execute-simple"/>
      <goto to="execute-complex"/>
    </stage>

    <!-- BRANCHING: Simple vs Complex execution paths -->
    <stage id="execute-simple">
      <print>Executing simple path...</print>
      <tasks output="simple_result">
        Step 1 - Quick Implementation:
        - Apply straightforward changes
        - Minimal modifications
      </tasks>
      <set var="result" from="simple_result"/>
      <goto to="verify"/>
    </stage>

    <stage id="execute-complex">
      <print>Executing complex path...</print>
      <tasks output="complex_result">
        Step 1 - Detailed Analysis:
        - Break down into sub-tasks
        - Identify critical paths

        Step 2 - Core Implementation:
        - Implement main functionality
        - Handle edge cases

        Step 3 - Integration:
        - Connect components
        - Verify interactions
      </tasks>
      <set var="result" from="complex_result"/>
      <goto to="parallel-checks"/>
    </stage>

    <!-- PARALLEL: Concurrent quality checks -->
    <parallel id="parallel-checks">
      <stage id="check-lint">
        <tasks output="lint_result">
          Step 1 - Lint Check:
          - Verify code style
          - Check formatting
        </tasks>
        <set var="lint_ok" from="lint_result.passed"/>
      </stage>
      <stage id="check-tests">
        <tasks output="test_result">
          Step 1 - Test Check:
          - Run unit tests
          - Verify coverage
        </tasks>
        <set var="tests_ok" from="test_result.passed"/>
      </stage>
    </parallel>

    <!-- LOOP: Retry pattern with validation -->
    <stage id="verify">
      <set var="retry_count" value="${retry_count} + 1"/>
      <goto when="${lint_ok} = false AND ${retry_count} < 3" to="fix-lint"/>
      <goto when="${tests_ok} = false AND ${retry_count} < 3" to="fix-tests"/>
      <goto when="${retry_count} >= 3" to="fail"/>
      <goto to="confirm"/>
    </stage>

    <stage id="fix-lint">
      <print>Fixing lint issues...</print>
      <tasks>
        Step 1 - Apply Fixes:
        - Correct style violations
        - Reformat code
      </tasks>
      <goto to="verify"/>
    </stage>

    <stage id="fix-tests">
      <print>Fixing test failures...</print>
      <tasks>
        Step 1 - Debug:
        - Identify failing tests
        - Fix implementation issues
      </tasks>
      <goto to="verify"/>
    </stage>

    <!-- CONFIRM: User confirmation checkpoint -->
    <confirm id="confirm">
      <print>
        ## Execution Summary
        **Mode:** ${mode}
        **Target:** ${target}
        **Complexity:** ${complexity}
        **Lint:** ${lint_ok}
        **Tests:** ${tests_ok}

        Proceed with completion?
      </print>
      <ask var="proceed" prompt="Continue? (y/n):" default="y">
        <goto when="${proceed} = 'n'" to="cancelled"/>
        <goto when="${proceed} = 'y'" to="complete"/>
      </ask>
    </confirm>

    <!-- INVOKE: Agent delegation example -->
    <stage id="delegate">
      <invoke name="Task" output="delegate_result">
        <param name="subagent_type">validation-agent</param>
        <param name="prompt"><![CDATA[
          - mode: validate
          - target: ${target}
          - context: ${result}
        ]]></param>
      </invoke>
      <set var="validation" from="delegate_result.status"/>
      <goto when="${validation} = 'failed'" to="fail"/>
      <goto to="complete"/>
    </stage>

    <!-- WORKFLOW: External workflow invocation -->
    <stage id="run-workflow">
      <workflow src=".claude/workflows/quality-check.md" output="workflow_result">
        <param name="target" value="${target}"/>
        <param name="mode" value="strict"/>
      </workflow>
      <set var="workflow_status" from="workflow_result.status"/>
      <goto when="${workflow_status} = 'failed'" to="fail"/>
      <goto to="complete"/>
    </stage>

    <!-- COMPLETION STAGES -->
    <stage id="complete">
      <print>
        ## Todo Executed Successfully
        - Target: ${target}
        - Mode: ${mode}
        - All checks passed
      </print>
      <stop kind="end"/>
    </stage>

    <stage id="cancelled">
      <print>Execution cancelled by user.</print>
      <stop kind="end"/>
    </stage>

    <stage id="fail">
      <print>
        ## Execution Failed
        - Retry count: ${retry_count}
        - Lint: ${lint_ok}
        - Tests: ${tests_ok}
      </print>
      <stop kind="error"/>
    </stage>

  </execution>

  <verification>
    - Does implementation meet requirements?
    - Are all items addressed?
    - Do all quality checks pass?
    - Is code following conventions?
  </verification>

  <checklist>
    - Is objective achieved?
    - Are all requirements implemented?
    - Did parallel checks complete successfully?
    - Is output in correct format?
  </checklist>

  <understanding/>

</document>
```
