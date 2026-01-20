---
name: todo-analysis
description: Analysis task todo template - code review, performance analysis, security audit
type: template
---

# AXEL Template: Todo Analysis

```xml
<document type="todo">

  <enforcement>
    - MUST analyze all files listed in documents
    - MUST categorize findings by severity (Critical/Major/Minor)
    - NEVER skip verification steps
  </enforcement>

  <objective>
    Analyze UserService for performance bottlenecks and security vulnerabilities.
    Focus on database query optimization and authentication flow.
  </objective>

  <!-- Documents element: Load references and target files for analysis -->
  <documents load="always" mode="context">
    <read src="references/quality/Security-Standards.md" ask="[security, vulnerability]"/>
    <read src="references/quality/Performance-Guidelines.md" ask="[performance, optimization]"/>
    <read src="src/Services/UserService.cs"/>
    <read src="src/Repositories/UserRepository.cs"/>
    <read src="src/Controllers/UserController.cs"/>
    <understanding>
      - READ all target files completely before analysis
      - COMPARE against standards documents
      - IDENTIFY patterns that violate guidelines
    </understanding>
  </documents>

  <requirements>
    - Identify N+1 query problems
    - Check for SQL injection vulnerabilities
    - Review authentication token handling
    - Measure response time for critical endpoints
    - Check error handling and logging
  </requirements>

  <output format="markdown">
    ## Summary
    - Overall health score (1-10)
    - Critical issues count
    - Recommendations count

    ## Findings
    ### Critical
    - [Issue description, file:line, fix suggestion]

    ### Major
    - [Issue description, file:line, fix suggestion]

    ### Minor
    - [Issue description, file:line, fix suggestion]

    ## Recommendations
    - [Prioritized list of improvements]
  </output>

  <!-- Todos: Derived from execution steps -->
  <todos>
    <![CDATA[
    - [ ] Step 1: Setup complete
    - [ ] Step 2: Analysis complete
    - [ ] Step 3: Report generated
    ]]>
  </todos>

  <!-- Execution: References other sections for what to do -->
  <execution flow="linear">
    <![CDATA[
    Step 1 - Setup:
    - Read files in <documents>
    - Review <requirements> criteria

    Step 2 - Analyze:
    - Examine each file systematically
    - Document findings with file:line references

    Step 3 - Report:
    - Generate <output> in specified format
    - Run <verification> checks
    - Answer <checklist> questions
    ]]>
  </execution>

  <verification>
    - Analyze all files listed in documents
    - Categorize findings by severity
    - Include fix suggestion for each finding
    - Provide actionable recommendations
  </verification>

  <checklist>
    - Have all target files been analyzed?
    - Are findings categorized by severity?
    - Does each finding include a fix suggestion?
    - Are recommendations actionable?
  </checklist>

  <understanding/>

</document>
```
