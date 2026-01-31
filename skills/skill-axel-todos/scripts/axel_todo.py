#!/usr/bin/env python3
"""
AXEL Todo Script - Folder-based todo management with frontmatter parsing.
Reads todo files from status folders and extracts frontmatter metadata.
"""

import argparse
import json
import re
import shutil
import sys
from datetime import date
from pathlib import Path
from typing import Optional


def parse_frontmatter(file_path: Path) -> Optional[dict]:
    """Parse YAML frontmatter from a markdown file."""
    try:
        content = file_path.read_text(encoding="utf-8")
    except Exception:
        return None

    # Match frontmatter between --- markers
    match = re.match(r'^---\s*\n(.*?)\n---', content, re.DOTALL)
    if not match:
        return None

    frontmatter = {}
    yaml_content = match.group(1)

    # Simple YAML parsing for flat key-value pairs and lists
    current_key = None
    for line in yaml_content.split('\n'):
        line = line.rstrip()
        if not line or line.startswith('#'):
            continue

        # Check for list item
        if line.startswith('  - '):
            if current_key and current_key in frontmatter:
                if not isinstance(frontmatter[current_key], list):
                    frontmatter[current_key] = []
                frontmatter[current_key].append(line[4:].split('#')[0].strip())
            continue

        # Key-value pair
        if ':' in line:
            key, _, value = line.partition(':')
            key = key.strip()
            value = value.split('#')[0].strip()  # Remove inline comments
            current_key = key

            if value:
                frontmatter[key] = value
            else:
                # Could be a list or empty value
                frontmatter[key] = []

    return frontmatter


def list_todos(base_path: Path, status_filter: str = "", workspace_filter: str = "", check_deps: bool = False) -> dict:
    """List todos from status folders, sorted by priority.

    If check_deps=True, each todo includes 'ready' and 'blocked_by' fields.
    """
    result = {"success": True, "todos": [], "errors": []}

    if not base_path.exists():
        result["success"] = False
        result["errors"].append(f"Base path not found: {base_path}")
        return result

    # Priority order: critical > high > medium > low
    priority_order = {"critical": 0, "high": 1, "medium": 2, "low": 3}
    # Status folders to scan
    status_folders = ["pending", "in-progress", "completed"]

    if status_filter:
        status_folders = [status_filter]

    todos = []
    for status in status_folders:
        status_path = base_path / status
        if not status_path.exists():
            continue

        for file_path in status_path.glob("*.md"):
            frontmatter = parse_frontmatter(file_path)
            if not frontmatter:
                continue

            # Apply workspace filter if provided
            if workspace_filter and frontmatter.get("workspace") != workspace_filter:
                continue

            # Get depends_on as list
            depends_on = frontmatter.get("depends_on", [])
            if isinstance(depends_on, str):
                depends_on = [depends_on] if depends_on else []

            todo_item = {
                "name": frontmatter.get("name", file_path.stem),
                "description": frontmatter.get("description", ""),
                "status": frontmatter.get("status", status),
                "priority": frontmatter.get("priority", "medium"),
                "workspace": frontmatter.get("workspace", ""),
                "depends_on": depends_on,
                "created_at": frontmatter.get("created_at", ""),
                "completed_at": frontmatter.get("completed_at", ""),
                "file": str(file_path),
                "value": str(file_path),
                "_priority_order": priority_order.get(frontmatter.get("priority", "medium"), 99)
            }

            # Check dependencies if requested
            if check_deps:
                dep_result = check_dependencies(file_path, base_path)
                todo_item["ready"] = dep_result["can_run"]
                todo_item["blocked_by"] = [d["file"] for d in dep_result["pending_deps"]]
                # Update label to show status
                base_label = frontmatter.get("description", frontmatter.get("name", file_path.stem))
                if dep_result["can_run"]:
                    todo_item["label"] = base_label
                else:
                    blocked_names = ", ".join(todo_item["blocked_by"])
                    todo_item["label"] = f"[BLOCKED] {base_label} (by: {blocked_names})"
            else:
                todo_item["label"] = frontmatter.get("description", frontmatter.get("name", file_path.stem))

            todos.append(todo_item)

    # Sort by priority (and if check_deps, ready ones first)
    if check_deps:
        todos.sort(key=lambda t: (0 if t.get("ready", True) else 1, t["_priority_order"]))
    else:
        todos.sort(key=lambda t: t["_priority_order"])

    # Assign keys - put full display text in key for <ask options> compatibility
    for i, todo in enumerate(todos, 1):
        todo["key"] = f"{i}. {todo['label']}"  # Full display text
        todo["label"] = ""  # Empty - key is shown as main text
        todo["number"] = str(i)  # Keep for selection matching
        del todo["_priority_order"]

    result["todos"] = todos
    return result


def move_todo(file_path: Path, new_status: str, base_path: Path, check_deps: bool = True) -> dict:
    """Move todo file to new status folder and update frontmatter."""
    result = {"success": True, "new_path": "", "blocked": False, "pending_deps": [], "errors": []}

    valid_statuses = ["pending", "in-progress", "completed"]
    if new_status not in valid_statuses:
        result["success"] = False
        result["errors"].append(f"Invalid status: {new_status}. Must be one of: {valid_statuses}")
        return result

    if not file_path.exists():
        result["success"] = False
        result["errors"].append(f"File not found: {file_path}")
        return result

    # Check dependencies before moving to in-progress
    if check_deps and new_status == "in-progress":
        dep_result = check_dependencies(file_path, base_path)
        if not dep_result["can_run"]:
            result["success"] = False
            result["blocked"] = True
            result["pending_deps"] = dep_result["pending_deps"]
            result["errors"].append("Dependencies not completed")
            return result

    # Read current content
    try:
        content = file_path.read_text(encoding="utf-8")
    except Exception as e:
        result["success"] = False
        result["errors"].append(f"Read error: {e}")
        return result

    # Update status in frontmatter
    content = re.sub(
        r'^(status:\s*)(\S+)',
        f'\\g<1>{new_status}',
        content,
        flags=re.MULTILINE
    )

    # Update completed_at if status is completed
    if new_status == "completed":
        today = date.today().isoformat()
        if re.search(r'^completed_at:', content, re.MULTILINE):
            content = re.sub(
                r'^(completed_at:\s*).*$',
                f'\\g<1>{today}',
                content,
                flags=re.MULTILINE
            )
        else:
            # Add completed_at after status line
            content = re.sub(
                r'^(status:\s*.*)$',
                f'\\1\ncompleted_at: {today}',
                content,
                flags=re.MULTILINE
            )

    # Create target folder if needed (completed uses date subfolder)
    if new_status == "completed":
        today = date.today().isoformat()  # YYYY-MM-DD
        target_folder = base_path / new_status / today
    else:
        target_folder = base_path / new_status
    target_folder.mkdir(parents=True, exist_ok=True)

    # Move file
    new_path = target_folder / file_path.name
    try:
        # Write updated content to new location
        new_path.write_text(content, encoding="utf-8")
        # Remove old file if different location
        if file_path != new_path:
            file_path.unlink()
    except Exception as e:
        result["success"] = False
        result["errors"].append(f"Move error: {e}")
        return result

    result["new_path"] = str(new_path)
    return result


def list_workspaces(todos_path: Path) -> dict:
    """List all workspaces from .claude/workspaces/ directory."""
    result = {"success": True, "workspaces": [], "count": 0, "errors": []}

    if not todos_path.exists():
        result["success"] = False
        result["errors"].append(f"Todos path not found: {todos_path}")
        return result

    workspaces = []
    for item in sorted(todos_path.iterdir()):
        if item.is_dir() and not item.name.startswith('.'):
            # Check if it has status folders (valid workspace structure)
            has_pending = (item / "pending").exists()
            idx = len(workspaces) + 1
            workspace_item = {
                "key": f"{idx}. {item.name}",  # Full display text
                "value": item.name,
                "label": "",  # Empty - key is shown as main text
                "name": item.name,
                "number": str(idx),  # Keep for reference
                "has_pending": has_pending,
                "path": str(item)
            }
            workspaces.append(workspace_item)

    result["workspaces"] = workspaces
    result["count"] = len(workspaces)
    return result


def check_workspace(todos_path: Path, workspace_name: str) -> dict:
    """Check if workspace exists and list all workspaces."""
    result = list_workspaces(todos_path)
    result["exists"] = (todos_path / workspace_name).is_dir()
    result["requested"] = workspace_name
    return result


def check_dependencies(file_path: Path, base_path: Path) -> dict:
    """Check if all dependencies are completed."""
    result = {"success": True, "can_run": True, "pending_deps": [], "errors": []}

    frontmatter = parse_frontmatter(file_path)
    if not frontmatter:
        result["success"] = False
        result["errors"].append(f"Cannot parse frontmatter: {file_path}")
        return result

    depends_on = frontmatter.get("depends_on", [])
    if isinstance(depends_on, str):
        depends_on = [depends_on] if depends_on else []

    if not depends_on:
        return result

    # Check each dependency
    for dep_file in depends_on:
        dep_found = False
        dep_completed = False

        # Search in all status folders
        for status in ["pending", "in-progress", "completed"]:
            dep_path = base_path / status / dep_file
            if dep_path.exists():
                dep_found = True
                dep_fm = parse_frontmatter(dep_path)
                if dep_fm and dep_fm.get("status") == "completed":
                    dep_completed = True
                break

        if not dep_found:
            result["pending_deps"].append({"file": dep_file, "reason": "not found"})
            result["can_run"] = False
        elif not dep_completed:
            result["pending_deps"].append({"file": dep_file, "reason": "not completed"})
            result["can_run"] = False

    return result


def get_next_number(base_path: Path) -> dict:
    """Get next available number by scanning all status folders including completed/{date}/."""
    result = {"success": True, "next_number": 1, "max_found": 0, "scanned_folders": []}

    if not base_path.exists():
        result["success"] = False
        result["errors"] = [f"Base path not found: {base_path}"]
        return result

    max_num = 0

    # Scan pending and in-progress folders
    for status in ["pending", "in-progress"]:
        status_path = base_path / status
        if status_path.exists():
            result["scanned_folders"].append(str(status_path))
            for f in status_path.glob("*.md"):
                match = re.match(r'^(\d{3})-', f.name)
                if match:
                    max_num = max(max_num, int(match.group(1)))

    # Scan completed/{date}/ subfolders
    completed_path = base_path / "completed"
    if completed_path.exists():
        for date_folder in completed_path.iterdir():
            if date_folder.is_dir():
                result["scanned_folders"].append(str(date_folder))
                for f in date_folder.glob("*.md"):
                    match = re.match(r'^(\d{3})-', f.name)
                    if match:
                        max_num = max(max_num, int(match.group(1)))

    result["max_found"] = max_num
    result["next_number"] = max_num + 1
    result["next_prefix"] = f"{max_num + 1:03d}"
    return result


def main():
    parser = argparse.ArgumentParser(description="AXEL Todo Script")
    parser.add_argument("--action", required=True,
                        choices=["list", "move", "check-deps", "list-workspaces", "check-workspace", "next-number"],
                        help="Action to perform")
    parser.add_argument("--base-path", default="",
                        help="Base path for todos (e.g., .claude/workspaces/{workspace})")
    parser.add_argument("--status", default="",
                        help="Filter by status (pending, in-progress, completed)")
    parser.add_argument("--workspace", default="",
                        help="Filter by workspace name")
    parser.add_argument("--file", default="",
                        help="File path for move/check-deps actions")
    parser.add_argument("--new-status", default="",
                        help="New status for move action")
    parser.add_argument("--skip-deps", action="store_true",
                        help="Skip dependency check for move action")
    parser.add_argument("--check-deps", action="store_true",
                        help="Include dependency status in list output")
    parser.add_argument("--todos-path", default=".claude/workspaces",
                        help="Path to workspaces directory (for list-workspaces action)")
    parser.add_argument("--workspace-name", default="",
                        help="Workspace name to check (for check-workspace action)")

    args = parser.parse_args()
    base_path = Path(args.base_path) if args.base_path else None

    if args.action == "list-workspaces":
        result = list_workspaces(Path(args.todos_path))
    elif args.action == "check-workspace":
        result = check_workspace(Path(args.todos_path), args.workspace_name)
    elif args.action == "list":
        result = list_todos(base_path, args.status, args.workspace, args.check_deps)
    elif args.action == "move":
        if not args.file or not args.new_status:
            result = {"success": False, "errors": ["--file and --new-status required for move"]}
        else:
            result = move_todo(Path(args.file), args.new_status, base_path, check_deps=not args.skip_deps)
    elif args.action == "check-deps":
        if not args.file:
            result = {"success": False, "errors": ["--file required for check-deps"]}
        else:
            result = check_dependencies(Path(args.file), base_path)
    elif args.action == "next-number":
        if not base_path:
            result = {"success": False, "errors": ["--base-path required for next-number"]}
        else:
            result = get_next_number(base_path)
    else:
        result = {"success": False, "errors": [f"Unknown action: {args.action}"]}

    print(json.dumps(result, indent=2, ensure_ascii=True))
    return 0 if result["success"] else 1


if __name__ == "__main__":
    sys.exit(main())
