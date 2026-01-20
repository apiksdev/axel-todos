# Contributing to AXEL Todos Plugin

Thank you for your interest in contributing to AXEL Todos Plugin! This document provides guidelines and instructions for contributing.

## Table of Contents

- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Project Structure](#project-structure)
- [Contribution Guidelines](#contribution-guidelines)
- [Commit Messages](#commit-messages)
- [Pull Request Process](#pull-request-process)
- [Code Style](#code-style)
- [Reporting Issues](#reporting-issues)

## Getting Started

1. Fork the repository
2. Clone your fork locally
3. Create a new branch for your feature or fix
4. Make your changes
5. Submit a pull request

## Development Setup

AXEL Todos is an XML-based DSL plugin for Claude Code that provides AI-executable task management. To set up your development environment:

1. Ensure you have Claude Code installed
2. Clone the repository:
   ```bash
   git clone https://github.com/apiksdev/axel-todos.git
   cd axel-todos
   ```
3. Review the project structure for existing documents

## Project Structure

```
axel-todos/
├── CLAUDE.md                 # Project instructions
├── README.md                 # Project documentation
├── CODE_OF_CONDUCT.md        # Community guidelines
├── CONTRIBUTING.md           # This file
├── agents/
│   └── agent-axel-todo-runner/
│       └── AGENT.md          # Todo execution agent
├── commands/
│   ├── axel-todos.md         # Todo management command
│   ├── axel-workspace.md     # Workspace management command
│   └── axel-backlogs.md      # Backlog management command
└── skills/
    └── skill-axel-todos/
        ├── SKILL.md          # Skill definition
        ├── scripts/          # Python helper scripts
        ├── references/       # Todo format references
        ├── templates/        # Todo/workspace templates
        └── workflows/        # Todo lifecycle workflows
```

## Contribution Guidelines

### AXEL Documents

When creating or modifying AXEL documents, follow these rules:

1. **Document Format**: AXEL documents use Markdown files with embedded XML:
   ````markdown
   ---
   name: document-name
   description: Brief description of the document
   type: workflow|skill|agent|command|config
   ---

   # Document Title

   ```xml
   <document type="...">
     <!-- XML content here -->
   </document>
   ```
   ````

2. **No Content Duplication**: Never copy content from referenced documents into new documents. Use `<read src=".."/>` references instead.

3. **XML Comment Format**:
   - Use single-line format: `<!-- stage_id: Description -->`
   - Never use multi-line decorative comments or box-style separators

4. **Document Types**: Follow the appropriate schema for each type:
   - Skills: Specialized AI expertise definitions
   - Agents: Autonomous task executor configurations
   - Workflows: Multi-step process definitions
   - Commands: Slash command definitions

### Todo-Specific Guidelines

- **Todo Templates**: When adding new todo templates, place them in `skills/skill-axel-todos/templates/todos/refs/`
- **Workflows**: Todo-related workflows go in `skills/skill-axel-todos/workflows/todos/`
- **Backlog Workflows**: Backlog-related workflows go in `skills/skill-axel-todos/workflows/backlogs/`
- **Workspace Workflows**: Workspace-related workflows go in `skills/skill-axel-todos/workflows/workspaces/`

### Code Quality

- Ensure XML is well-formed and valid
- Follow existing naming conventions
- Keep components focused and single-purpose
- Document complex logic with appropriate comments

## Commit Messages

We follow conventional commit format:

```
type(scope): description

[optional body]

[optional footer]
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Formatting changes
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

**Scopes for this plugin:**
- `todos`: Todo management features
- `workspace`: Workspace features
- `backlogs`: Backlog features
- `agent`: Todo runner agent
- `skill`: Skill definition changes
- `workflow`: Workflow changes
- `template`: Template changes

**Examples:**
```
feat(todos): add priority filtering to list command
fix(agent): resolve parallel execution timeout issue
docs(readme): update usage examples
feat(workspace): add overview statistics
```

## Pull Request Process

1. **Create a descriptive PR title** following commit message conventions
2. **Fill out the PR template** with:
   - Description of changes
   - Related issue numbers
   - Testing performed
3. **Ensure all checks pass**
4. **Request review** from maintainers
5. **Address feedback** promptly
6. **Squash commits** if requested before merge

### PR Checklist

- [ ] Code follows project style guidelines
- [ ] XML documents are well-formed
- [ ] No duplicate content (use references)
- [ ] Comments follow single-line format
- [ ] Documentation updated if needed
- [ ] Commit messages follow conventions
- [ ] Tested with actual todo creation/execution

## Code Style

### XML Guidelines

```xml
<!-- Good: Single-line comment -->
<stage id="todos:create">
  <!-- todos:create: Create a new todo -->
  <invoke name="Skill">
    <param name="skill" value="axel-todos:skill-axel-todos"/>
    <param name="trigger" value="todos:create"/>
  </invoke>
</stage>

<!-- Bad: Decorative multi-line comments -->
<!-- ========================================
     DO NOT USE THIS STYLE
     ======================================== -->
```

### Naming Conventions

**Commands:**
- Directory: `commands/`
- Command files: `axel-{name}.md` (e.g., `axel-todos.md`, `axel-workspace.md`)

**Agents:**
- Directory: `agents/agent-axel-{name}/` (e.g., `agent-axel-todo-runner/`)
- Definition file: `AGENT.md`

**Skills:**
- Directory: `skills/skill-axel-{name}/` (e.g., `skill-axel-todos/`)
- Definition file: `SKILL.md`
- References: `references/AXEL-{Name}.md`

**Templates:**
- Directory: `templates/{category}/` (e.g., `templates/todos/`, `templates/workspaces/`)
- Bootstrap file: `AXEL-{Name}-Template-Bootstrap.md`
- Template files: `refs/AXEL-{Name}-Tpl.md`

**Workflows:**
- Directory: `workflows/{category}/` (e.g., `workflows/todos/`, `workflows/backlogs/`)
- Workflow files: `AXEL-Cmd-{Category}-{Action}-Workflow.md`

**Stage IDs:**
- Use namespace format: `{domain}:{action}` (e.g., `todos:create`, `todos:run-direct`)

## Reporting Issues

When reporting issues, please include:

1. **Clear title** describing the problem
2. **Environment details** (Claude Code version, OS)
3. **Steps to reproduce**
4. **Expected behavior**
5. **Actual behavior**
6. **Relevant logs or error messages**

Use the issue templates when available.

## Questions?

If you have questions about contributing:

- Check existing issues and discussions
- Review the documentation in `CLAUDE.md`
- Contact the team at support@apiks.com.tr

Thank you for contributing to AXEL Todos Plugin!
