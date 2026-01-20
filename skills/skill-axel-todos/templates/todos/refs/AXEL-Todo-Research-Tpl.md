---
name: todo-research
description: Research task todo template - investigation, exploration, information gathering
type: template
---

# AXEL Template: Todo Research

```xml
<document type="todo">

  <enforcement>
    - MUST evaluate all options within defined scope
    - MUST cite sources for claims and benchmarks
    - NEVER skip verification steps
  </enforcement>

  <objective>
    Investigate caching strategies for high-traffic API endpoints.
    Compare Redis, Memcached, and in-memory caching options.
    Determine best fit for current .NET 9 architecture.
  </objective>

  <!-- Documents element: Load relevant references for research context -->
  <!-- Populated dynamically based on brainstorm suggested_documents -->
  <documents load="always" mode="context">
    <read src="references/architecture/Caching-Patterns.md" ask="[cache, caching]"/>
    <read src="docs/Architecture-Overview.md"/>
    <understanding>
      - READ existing architecture before researching alternatives
      - UNDERSTAND current constraints and requirements
      - EVALUATE options against project context
    </understanding>
  </documents>

  <scope>
    Include:
    - Performance benchmarks for each option
    - .NET 9 integration complexity
    - Hosting and operational costs
    - Scalability considerations

    Exclude:
    - CDN caching (out of scope)
    - Database-level caching (separate initiative)
  </scope>

  <deliverables>
    - Comparison table with key metrics
    - Pros/cons analysis for each option
    - Implementation effort estimate
    - Recommended approach with justification
    - Sample configuration code
  </deliverables>

  <output format="markdown">
    ## Research Summary
    - Topic: [research topic]
    - Options evaluated: [count]
    - Recommendation: [brief recommendation]

    ## Comparison Table
    | Option | Performance | Cost | Complexity | Score |
    |--------|-------------|------|------------|-------|
    | Option1 | ... | ... | ... | ... |

    ## Recommendation
    - Recommended option: [option]
    - Justification: [brief justification]
    - Next steps: [action items]
  </output>

  <!-- Todos: Derived from execution steps -->
  <todos>
    <![CDATA[
    - [ ] Step 1: Setup complete
    - [ ] Step 2: Research complete
    - [ ] Step 3: Deliverables ready
    ]]>
  </todos>

  <!-- Execution: References other sections for what to do -->
  <execution flow="linear">
    <![CDATA[
    Step 1 - Setup:
    - Read <documents> for context
    - Review <scope> boundaries

    Step 2 - Research:
    - Investigate options within <scope>
    - Gather information from reliable sources

    Step 3 - Deliver:
    - Prepare items in <deliverables>
    - Generate <output> report
    - Run <verification> checks
    - Answer <checklist> questions
    ]]>
  </execution>

  <verification>
    - Evaluate all options listed in scope
    - Cite sources for all claims
    - Provide actionable recommendation
    - Define clear next steps
  </verification>

  <checklist>
    - Have all options been evaluated?
    - Is information from reliable sources?
    - Are benchmarks recent and relevant?
    - Is the recommendation justified?
    - Are trade-offs clearly explained?
    - Are next steps clear?
  </checklist>

  <understanding/>

</document>
```
