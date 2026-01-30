#!/usr/bin/env python3
"""
AXEL Workspace Create Script - Fast workspace structure initialization.
Creates workspace folders under .claude/workspaces/{workspace}/.
"""

import argparse
import json
import re
import sys
from pathlib import Path


# Reserved workspace names that cannot be created
RESERVED_WORKSPACES = ["default"]


def validate_kebab_case(name: str) -> bool:
    """Validate workspace name is in kebab-case format."""
    return bool(re.match(r'^[a-z][a-z0-9]*(-[a-z0-9]+)*$', name))


def create_workspace(base_path: Path, workspace: str, overwrite: bool = False) -> dict:
    """Create workspace with given name."""
    result = {
        "success": True,
        "action": "create",
        "workspace": workspace,
        "folders_created": [],
        "errors": []
    }

    # Check reserved names
    if workspace in RESERVED_WORKSPACES:
        result["success"] = False
        result["errors"].append(f"'{workspace}' is a reserved workspace name and cannot be created.")
        return result

    # Validate workspace name
    if not validate_kebab_case(workspace):
        result["success"] = False
        result["errors"].append(f"Workspace name must be in kebab-case format: {workspace}")
        return result

    # Check if workspace exists
    workspace_path = base_path / ".claude" / "workspaces" / workspace
    if workspace_path.exists() and not overwrite:
        result["success"] = False
        result["errors"].append(f"Workspace already exists: {workspace}. Use --overwrite to replace.")
        return result

    try:
        # Create folders
        folders = [
            f".claude/workspaces/{workspace}",
            f".claude/workspaces/{workspace}/pending",
            f".claude/workspaces/{workspace}/in-progress",
            f".claude/workspaces/{workspace}/completed",
        ]

        for folder in folders:
            folder_path = base_path / folder
            if not folder_path.exists():
                folder_path.mkdir(parents=True, exist_ok=True)
                result["folders_created"].append(folder)

        # Verify creation
        all_folders_exist = all((base_path / f).exists() for f in folders)

        if not all_folders_exist:
            result["success"] = False
            result["errors"].append("Some folders could not be created")

    except Exception as e:
        result["success"] = False
        result["errors"].append(str(e))

    return result


def main():
    parser = argparse.ArgumentParser(description="AXEL Workspace Create Script")
    parser.add_argument("--workspace", required=True, help="Workspace name (kebab-case)")
    parser.add_argument("--overwrite", action="store_true", help="Overwrite existing workspace")
    parser.add_argument("--cwd", default=".", help="Working directory")

    args = parser.parse_args()

    base_path = Path(args.cwd).resolve()
    result = create_workspace(base_path, args.workspace, args.overwrite)

    # Output JSON result
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0 if result["success"] else 1


if __name__ == "__main__":
    sys.exit(main())
