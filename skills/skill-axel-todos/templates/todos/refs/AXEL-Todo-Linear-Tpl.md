---
name: todo-linear
description: Template for executable todos with linear flow - sequential steps, no branching
type: template
---

# AXEL Template: Todo - Linear

```xml
<document type="todo">

  <enforcement>
    - MUST verify all requirements before execution
    - MUST follow existing code patterns and conventions
    - NEVER skip verification steps
    - Todos are static - written at todo creation time
  </enforcement>

  <objective>
    Executable todo with linear flow.
    Sequential execution without branching or parallel patterns.
    Suitable for straightforward implementation tasks.
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

  <!-- Todos: Derived from execution steps -->
  <todos>
    <![CDATA[
    - [ ] Step 1: Setup complete
    - [ ] Step 2: Database applied
    - [ ] Step 3: Backend implemented
    - [ ] Step 4: Frontend implemented
    - [ ] Step 5: Verification passed
    ]]>
  </todos>

  <!-- Execution: References other sections for what to do -->
  <execution flow="linear">
    <![CDATA[
    Step 1 - Setup:
    - Read <documents> for context
    - Review <requirements>

    Step 2 - Database:
    - Apply <database> schema if defined

    Step 3 - Backend:
    - Execute items in <backend>
    - Create <endpoints> if defined

    Step 4 - Frontend:
    - Execute items in <frontend>

    Step 5 - Verify:
    - Check <output> files created
    - Run <verification> checks
    - Answer <checklist> questions
    ]]>
  </execution>

  <verification>
    - Does implementation meet requirements?
    - Are all items addressed?
    - Do tests pass?
    - Is code following conventions?
  </verification>

  <checklist>
    - Is objective achieved?
    - Are all requirements implemented?
    - Is error handling in place?
    - Is output in correct format?
  </checklist>

  <understanding/>

</document>
```
