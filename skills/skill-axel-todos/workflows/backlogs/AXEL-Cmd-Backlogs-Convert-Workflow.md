---
name: axel-cmd-backlogs-convert-workflow
description: Convert backlogs to todos
type: workflow
triggers:
  - backlogs convert
  - convert backlogs
---

# AXEL Workflow: Cmd Backlogs Convert

```xml
<document type="workflow">

  <enforcement>
    <![CDATA[
    BACKLOGS FILE: .claude/workspaces/BACKLOGS.md
    CONVERSION: Backlogs → Todos (sequential)
    CLEANUP: Converted backlogs are REMOVED from file
    ]]>
  </enforcement>

  <objective>
    Convert selected backlogs to executable todos.
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

    Step 3 - Select:
    - Print "## Select Backlogs to Convert"
    - For each backlog: print "{index}. {title}"
    - Ask for number(s) to convert (comma-separated), or 'q' to quit
    - IF 'q' or empty → STOP
    - IF invalid selection → show error, GO TO Step 3

    Step 4 - Confirm:
    - Print "## Ready to Convert"
    - List selected backlogs
    - Warn: "Converted backlogs will be REMOVED from BACKLOGS.md"
    - Ask: "Yes, convert" or "Cancel"
    - IF Cancel → STOP

    Step 5 - Convert (Sequential):
    - For each selected backlog:
      → Print "Converting: {title}"
      → Call /axel:todos create {description}
      → Track converted backlog

    Step 6 - Cleanup:
    - Read BACKLOGS.md
    - Remove converted <backlog> entries (match by title)
    - Write updated file

    Step 7 - Summary:
    - Print "## Conversion Complete"
    - List created todos
    - Print "Use /axel:todos list to view and run the created todos."
  ]]></execution>

  <understanding/>

</document>
```
