# AXEL Todos Plugin

```xml
<document type="project">

  <enforcement>
    <![CDATA[
    PATH RESOLUTION:
    - Read the `src`, `ref`, or `target` attribute from the document XML to locate referenced files
    - Plugin internal: ${CLAUDE_PLUGIN_ROOT}/...
    - Core resources: ${AXEL_CORE_PLUGIN_ROOT}/...
    ]]>
  </enforcement>

  <project name="axel-todos" version="1.0.0">
    <description>
      AXEL Todo management plugin. Provides todo creation, listing,
      and execution capabilities with template-based workflow support.
    </description>
    <stack>
      - language: XML, Markdown, Python
      - platform: Claude Code
      - type: AXEL Plugin
    </stack>
  </project>

 <locale default="en">
    - code: en
    - docs: en
    - communication: tr
    - commits: en
    - todos: tr
  </locale>

  <configurations>
    <var name="AXEL_CORE_PLUGIN_ROOT" value="D:\Projects\Axel\axel-plugins\axel-core"/>
    <var name="COMMIT_MESSAGE_FORMAT" value="conventional"/>
  </configurations>

  <understanding/>

</document>
```
