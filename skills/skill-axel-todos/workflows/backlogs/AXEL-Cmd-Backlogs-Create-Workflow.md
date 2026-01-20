---
name: axel-cmd-backlogs-create-workflow
description: Create new backlog entry
type: workflow
triggers:
  - backlogs create
  - create backlog
---

# AXEL Workflow: Cmd Backlogs Create

```xml
<document type="workflow">

  <enforcement>
    <![CDATA[
    BACKLOGS.md: .claude/workspaces/BACKLOGS.md
    FORMAT: Only bullet list inside <description>, NO headers
    ]]>
  </enforcement>

  <objective>
    Create new backlog entry from user description.
  </objective>

  <execution flow="linear"><![CDATA[
    Step 1 - Analyze:
    - Input: ${param.description}
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
  ]]></execution>

  <understanding/>

</document>
```
