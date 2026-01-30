---
name: axel:backlogs
description: Backlog management - create, list, convert to todos
type: command
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - AskUserQuestion
---

# AXEL Command: /axel:backlogs

```xml
<document type="command" entry="cmd:main">

  <enforcement>
    <![CDATA[
    BACKLOGS FILE: .claude/workspaces/BACKLOGS.md
    FORMAT: Only bullet list inside <description>, NO headers
    ]]>
  </enforcement>

  <objective>
    Backlog management command with embedded workflow execution.
    Routes to appropriate stage based on action.
  </objective>

  <variables>
    <var name="action" from="args.0"/>
    <var name="description" from="args.1+"/>
  </variables>

  <command id="cmd:main">
    <goto when="action = ''" to="stage_list"/>
    <goto when="action = 'list'" to="stage_list"/>
    <goto when="action = 'create'" to="stage_create"/>
    <goto when="action = 'convert'" to="stage_convert"/>
    <goto to="stage_help"/>
  </command>

  <execution flow="staged">

    <!-- STAGE: Help -->
    <stage id="stage_help"><![CDATA[
      Print usage:
      ## /axel:backlogs

      **Usage:**
        /axel:backlogs                 - List backlogs
        /axel:backlogs create {desc}   - Create a new backlog item
        /axel:backlogs convert         - Convert backlog to todo
    ]]></stage>

    <!-- STAGE: List Backlogs -->
    <stage id="stage_list"><![CDATA[
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
    ]]></stage>

    <!-- STAGE: Create Backlog -->
    <stage id="stage_create"><![CDATA[
      Step 1 - Analyze:
      - Input: ${description}
      - Generate title (5-10 words) and expand into bullet points

      Step 2 - Prepare File:
      - Check if .claude/workspaces/BACKLOGS.md exists
      - If NOT exists, create with template:
        ---
        name: product-backlogs
        description: Product backlog items
        type: backlogs
        ---

        # Product Backlogs

        ```xml
        <document type="backlogs">

        </document>
        ```

      Step 3 - Insert Backlog:
      - Insert BEFORE closing </document> tag:
        <backlog>
          <title>{title}</title>
          <description>
        - {requirement 1}
        - {requirement 2}
          </description>
        </backlog>

      Step 4 - Report:
      - Print: "## Backlog Created"
      - Print: "**Title:** {title}"
      - Print: "Use `/axel:backlogs` to view."
    ]]></stage>

    <!-- STAGE: Convert Backlogs to Todos -->
    <stage id="stage_convert"><![CDATA[
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
    ]]></stage>

  </execution>

  <understanding/>

</document>
```
