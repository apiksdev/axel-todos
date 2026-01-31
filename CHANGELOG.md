# Changelog

All notable changes to AXEL Todos plugin will be documented in this file.

## [1.0.2] - 2026-01-31

- Added `axel:todos run {workspace}` command to run todos directly by workspace name
- Added global todo numbering system (scans pending, in-progress, completed/{date}/ folders)
- Added `get_next_number()` function to axel_todo.py for sequential numbering
- Added date-based subfolder for completed todos (completed/{YYYY-MM-DD}/)
- Added bash tag execution enforcement to SKILL.md
- Updated AXEL-Cmd-Todos-Run-Workflow.md with workspace_name parameter support
- Updated AXEL-Cmd-Todos-Create-Workflow.md with automatic numbering prefix

## [1.0.1] - 2026-01-30

- Refactored todo templates: consolidated into Linear (sequential) and Staged (branching/parallel) patterns
- Added workspace bootstrap template for workspace-specific enforcement rules
- Simplified backlogs command to inline execution (removed external workflows)
- Added /axel:workspace init command to create workspace from CLAUDE.md project name
- Added /axel:workspace bootstrap command to generate workspace bootstrap files
- Enhanced agent-axel-todo-runner with verification auto-fix loop (max 10 retries per item)
- Updated README file structure documentation
- Removed legacy template files (refs/ folder consolidated)

## [1.0.0] - 2026-01-19

- Initial release
