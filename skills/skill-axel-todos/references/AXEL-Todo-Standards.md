---
name: axel-todos-standards
description: AXEL Todo element reference - structured documentation for todo-specific XML elements
type: reference
---

# AXEL Todos Standards

```xml
<document type="reference">

  <enforcement>
    - Read `src`, `ref`, or `target` attributes from document references to locate files
    - ${CLAUDE_PLUGIN_ROOT} resolves to plugin installation directory
    - Elements listed in document structure order (axel-tag-structure)
  </enforcement>

  <objective>
    AXEL Todo-specific element reference.
    Structured documentation for XML elements used in todo documents.
  </objective>

  <elements>

    <element name="output" depth="1" document_types="agent,todo" parent="document">
    <![CDATA[
    Purpose: Expected output format definition

    Example:
    <output format="markdown|json|yaml|text|xml" target="{optional-filename}">
      ## Review Summary
      - Total Issues: {count}
      - Critical: {critical_count}

      ## Findings
      {findings_list}
    </output>
    ]]>
    </element>

    <element name="objective" depth="1" document_types="skill,agent,workflow,command,todo,brainstorm,reference" parent="document">
    <![CDATA[
    Purpose: Describe what the document does (1-3 sentences)
    Format: Short description text

    Example:
    <objective>
      Manage project brainstorm documents.
      Lists, creates, and edits brainstorm files.
    </objective>
    ]]>
    </element>

    <element name="execution" depth="1" document_types="command,agent,workflow,skill,todo" parent="document">
    <![CDATA[
    Purpose: Container for execution flow

    Example:
    <execution flow="linear|staged">
      <stage id="init">...</stage>
      <stage id="process">...</stage>
    </execution>

    Notes:
    - linear: No stages, text-based instructions in CDATA
    - staged: Stage blocks with sequential/branching/loop patterns

    Children (staged only): stage, parallel, confirm
    ]]>
    </element>

    <element name="context" depth="1" document_types="reference,todo" parent="document">
    <![CDATA[
    Purpose: Usage context and background information
    Format: Bullet list

    Example:
    <context>
      - Used for defining multi-step processes
      - Stage-based flow with implicit sequential execution
    </context>
    ]]>
    </element>

    <element name="requirements" depth="1" document_types="reference,todo" parent="document">
    <![CDATA[
    Purpose: Document requirements specification
    Format: Bullet list

    Example:
    <requirements>
      - Frontmatter must have name, description, type
      - Document root must have type attribute
      - Every stage must end with stop or goto
    </requirements>
    ]]>
    </element>

    <element name="implementation" depth="1" document_types="reference,todo" parent="document">
    <![CDATA[
    Purpose: Implementation steps or file locations

    Example:
    <implementation name="{optional-identifier}">
      .claude/agents/agent-{name}/
      - AGENT.md - Main agent file
    </implementation>
    ]]>
    </element>

    <element name="verification" depth="1" document_types="reference,todo" parent="document">
    <![CDATA[
    Purpose: Verification rules and checks
    Format: Question list or bullet points

    Example:
    <verification>
      - Is document type valid?
      - Does objective explain the purpose?
      - Is understanding at document end?
    </verification>
    ]]>
    </element>

    <element name="checklist" depth="1" document_types="skill,reference,workflow,agent,todo" parent="document">
    <![CDATA[
    Purpose: Validation checklist

    Example:
    <checklist name="{identifier}" src="{optional-external-file}">
      Frontmatter:
      - [ ] name format correct?
      - [ ] type set to "command"?

      Structure:
      - [ ] document type="command"?
      - [ ] single cmd:main block?
    </checklist>
    ]]>
    </element>

    <element name="scope" depth="1" document_types="todo,brainstorm" parent="document">
    <![CDATA[
    Purpose: Define boundaries of work

    Example:
    <scope>
      Include:
      - User authentication module
      Exclude:
      - OAuth integration (phase 2)
      Boundaries:
      - Backend only
    </scope>
    ]]>
    </element>

    <element name="current_state" depth="1" document_types="todo,brainstorm" parent="document" todo_type="migration">
    <![CDATA[
    Purpose: Document current system state (migration todos)
    Format: Bullet list describing current state

    Example:
    <current_state>
      - Database: MySQL 5.7
      - Auth: Cookie-based sessions
    </current_state>
    ]]>
    </element>

    <element name="target_state" depth="1" document_types="todo,brainstorm" parent="document" todo_type="migration">
    <![CDATA[
    Purpose: Define desired end state (migration todos)
    Format: Bullet list describing target state

    Example:
    <target_state>
      - Database: PostgreSQL 15
      - Auth: JWT with refresh tokens
    </target_state>
    ]]>
    </element>

    <element name="database" depth="1" document_types="todo" parent="document" todo_type="coding">
    <![CDATA[
    Purpose: Database schema changes (coding todos, optional)
    Format: Entity/table definitions with fields

    Example:
    <database>
      User (alter):
      - add: RefreshToken string, TokenExpiry datetime
      - index: RefreshToken (unique)
    </database>
    ]]>
    </element>

    <element name="endpoints" depth="1" document_types="todo" parent="document" todo_type="coding">
    <![CDATA[
    Purpose: API endpoint definitions (coding todos, optional)
    Format: HTTP method, path, description

    Example:
    <endpoints>
      POST /api/auth/login - User login, returns JWT
      POST /api/auth/refresh - Refresh access token
    </endpoints>
    ]]>
    </element>

    <element name="frontend" depth="1" document_types="todo" parent="document" todo_type="coding">
    <![CDATA[
    Purpose: Frontend page/component definitions (coding todos, optional)
    Format: Container with lang and path attributes

    Attributes:
    - lang: Programming language (typescript, javascript, etc.)
    - path: Base path for files

    Example:
    <frontend lang="typescript" path="src/pages/">
      - LoginPage (create): email, password inputs
      - DashboardPage (create): user info, navigation
      - ProfilePage (alter): add logout button
    </frontend>
    ]]>
    </element>

    <element name="backend" depth="1" document_types="todo" parent="document" todo_type="coding">
    <![CDATA[
    Purpose: Backend service definitions (coding todos, optional)
    Format: Container with lang and path attributes

    Attributes:
    - lang: Programming language (csharp, typescript, etc.)
    - path: Base path for files

    Structure:
    - ServiceName (action):
      - inject: Constructor dependencies
      - methods: Public method names
      - sub: Nested services (optional)

    Actions: (create), (alter), (delete)

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
    ]]>
    </element>

    <element name="migration_steps" depth="1" document_types="todo" parent="document" todo_type="migration">
    <![CDATA[
    Purpose: Ordered migration steps
    Format: Numbered list with atomic steps

    Example:
    <migration_steps>
      1. Backup existing database
      2. Run schema migration scripts
      3. Update connection strings
      4. Verify data integrity
    </migration_steps>
    ]]>
    </element>

    <element name="rollback_plan" depth="1" document_types="todo" parent="document" todo_type="migration">
    <![CDATA[
    Purpose: Steps to revert if migration fails
    Format: Numbered list with rollback steps

    Example:
    <rollback_plan>
      1. Restore database from backup
      2. Revert connection strings
      3. Verify system functionality
    </rollback_plan>
    ]]>
    </element>

    <element name="compatibility" depth="1" document_types="todo" parent="document" todo_type="migration">
    <![CDATA[
    Purpose: Breaking changes and compatibility notes
    Format: Categorized list

    Example:
    <compatibility>
      Breaking Changes:
      - API response format changed (v1 → v2)

      Backwards Compatible:
      - Old JWT tokens remain valid for 30 days
    </compatibility>
    ]]>
    </element>

    <element name="deliverables" depth="1" document_types="todo" parent="document" todo_type="research">
    <![CDATA[
    Purpose: Expected research outputs
    Format: Bullet list of deliverables

    Example:
    <deliverables>
      - Comparison matrix of auth libraries
      - Recommendation document with pros/cons
    </deliverables>
    ]]>
    </element>

    <element name="todos" depth="1" document_types="todo" parent="document">
    <![CDATA[
    Purpose: Static task list for tracking progress (optional)
    Format: Markdown checkbox syntax

    Example:
    <todos>
      - [ ] Understand requirements and context
      - [ ] Read existing code and patterns
      - [ ] Implement core functionality
      - [ ] Add error handling
      - [ ] Write tests
      - [x] Completed task
    </todos>

    Notes:
    - Static: Written at todo creation time, not modified during execution
    - Format: - [ ] pending, - [x] completed
    - Purpose: Track progress, resume from failure point
    - Placement: After output, before execution
    ]]>
    </element>

  </elements>

  <understanding/>

</document>
```
