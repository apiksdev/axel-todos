---
name: axel-cmd-backlogs-list-workflow
description: List backlogs and view details
type: workflow
triggers:
  - backlogs list
  - list backlogs
---

# AXEL Workflow: Cmd Backlogs List

```xml
<document type="workflow">

  <enforcement>
    <![CDATA[
    BACKLOGS FILE: .claude/workspaces/BACKLOGS.md
    LIST ONLY: Show backlogs, view details
    For conversion use /axel:backlogs convert
    ]]>
  </enforcement>

  <objective>
    List backlogs and view their details.
  </objective>

  <execution flow="linear"><![CDATA[
    Step 1 - Check File:
    - Check if .claude/workspaces/BACKLOGS.md exists
    - IF not exists:
      → Print "No backlogs found. Use /axel:backlogs create {desc} to create one."
      → STOP

    Step 2 - Parse:
    - Read BACKLOGS.md
    - Extract all <backlog> entries (index, title, description)
    - IF count = 0:
      → Print "No backlog entries found."
      → STOP

    Step 3 - Display:
    - Print "## Available Backlogs ({count})"
    - For each backlog: print "{index}. {title}"
    - Print "Tip: Use /axel:backlogs convert to convert backlogs to todos."

    Step 4 - Action Loop:
    - Ask: "View Details" or "Done"
    - IF Done → STOP
    - IF View Details:
      → Ask for backlog number
      → Show title and full description
      → Ask: "Back to list" or "Done"
      → IF Back → GO TO Step 3
      → IF Done → STOP
  ]]></execution>

  <understanding/>

</document>
```
