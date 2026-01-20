---
name: todo-template
description: Routing template for AXEL executable todos
type: template
---

# AXEL Template: Todo

```xml
<document type="todo">

  <enforcement>
    <![CDATA[
    - Read `src` attribute from <read/> elements to locate sub-templates
    - ${CLAUDE_PLUGIN_ROOT} resolves to plugin installation directory
    - load="always" means templates section loads with document
    - ask="[keywords]" triggers template load when user request matches
    - Select appropriate template based on execution complexity
    ]]>
  </enforcement>

  <objective>
    Routing template for executable todo selection.
    Routes to Linear or Staged templates based on complexity needs.
  </objective>

  <templates load="always">
    <!-- Execution Flow Templates -->
    <read src="${CLAUDE_PLUGIN_ROOT}/skills/skill-axel-todos/templates/todos/refs/AXEL-Todo-Linear-Tpl.md"
          ask="[linear, simple, sequential, basic, straightforward, coding, implement, create, build, develop, fix, feature]"/>
    <read src="${CLAUDE_PLUGIN_ROOT}/skills/skill-axel-todos/templates/todos/refs/AXEL-Todo-Staged-Tpl.md"
          ask="[staged, complex, branching, parallel, orchestrate, delegate, workflow, agent, multi-step]"/>
    <!-- Task Type Templates -->
    <read src="${CLAUDE_PLUGIN_ROOT}/skills/skill-axel-todos/templates/todos/refs/AXEL-Todo-Analysis-Tpl.md"
          ask="[analyze, review, inspect, examine, evaluate, audit, check, performance]"/>
    <read src="${CLAUDE_PLUGIN_ROOT}/skills/skill-axel-todos/templates/todos/refs/AXEL-Todo-Research-Tpl.md"
          ask="[research, investigate, explore, find, search, compare, discover]"/>
    <read src="${CLAUDE_PLUGIN_ROOT}/skills/skill-axel-todos/templates/todos/refs/AXEL-Todo-Migration-Tpl.md"
          ask="[migrate, migration, upgrade, convert, port, transition, move, transfer]"/>
    <understanding>
      !! MANDATORY: READ → UNDERSTAND → APPLY !!
      Execution Flow:
      - Linear: Simple sequential steps, no branching (default)
      - Staged: Complex with branching, parallel, loops, delegation
      Task Type:
      - Coding: Implementation, feature development, bug fixes
        → Linear: Simple features, single-file changes, straightforward fixes
        → Staged: Complex features, multi-file orchestration, conditional flows
      - Analysis: Code review, performance, security analysis
      - Research: Investigation, exploration, comparison
      - Migration: Upgrade, conversion, transition
    </understanding>
  </templates>

  <understanding/>

</document>
```
