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
    ]]>
  </enforcement>

  <objective>
    Router for skill-axel-todos todo operations.
    Determines trigger from args and delegates to skill.
  </objective>

  <variables>
    <var name="action" from="args.0"/>
    <var name="rest_args" from="args.1+"/>
    <var name="all_args" from="args.*"/>
  </variables>

  <command id="cmd:main">
    <goto when="action = ''" to="todos:help"/>
    <goto when="action = 'list'" to="todos:list"/>
    <goto when="action = 'run'" to="todos:run"/>
    <goto when="action = 'create'" to="todos:create"/>
    <goto to="todos:create"/>
  </command>

  <execution flow="staged">

    <stage id="todos:help">
      <print>
        ## /axel:todos

        **Usage:**
          /axel:todos {topic}    - Create new todo
          /axel:todos list       - List todos
          /axel:todos run        - Run todos (with workspace selection)
          /axel:todos run {path} - Run specific todo directly
      </print>
      <stop kind="end"/>
    </stage>

    <stage id="todos:create">
      <invoke name="Skill">
        <param name="skill" value="axel-todos:skill-axel-todos"/>
        <param name="trigger" value="todos:create"/>
        <param name="topic" value="${all_args}"/>
      </invoke>
      <stop kind="end"/>
    </stage>

    <stage id="todos:list">
      <invoke name="Skill">
        <param name="skill" value="axel-todos:skill-axel-todos"/>
        <param name="trigger" value="todos:list"/>
      </invoke>
      <stop kind="end"/>
    </stage>

    <stage id="todos:run">
      <goto when="rest_args != ''" to="todos:run-direct"/>
      <goto when="rest_args = ''" to="todos:run-select"/>
    </stage>

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

    <stage id="todos:run-select">
      <invoke name="Skill">
        <param name="skill" value="axel-todos:skill-axel-todos"/>
        <param name="trigger" value="todos:run"/>
      </invoke>
      <stop kind="end"/>
    </stage>

  </execution>

  <understanding/>

</document>
```
