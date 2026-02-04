"""Workspace commands."""

from typing import Optional

import typer

from kanbn_cli.api.client import KanbnClient
from kanbn_cli.config import load_config
from kanbn_cli.utils.display import (
    display_workspace,
    display_workspaces,
    print_error,
    print_success,
)
from kanbn_cli.utils.errors import KanbnError

app = typer.Typer(help="Manage workspaces")


@app.command("list")
def list_workspaces():
    """List all workspaces."""
    try:
        config = load_config()
        client = KanbnClient(config)
        
        workspaces = client.get("workspaces")
        display_workspaces(workspaces)

    except KanbnError as e:
        print_error(str(e))
        raise typer.Exit(1)


@app.command("create")
def create_workspace(
    name: str = typer.Argument(..., help="Workspace name"),
    slug: Optional[str] = typer.Option(None, "--slug", "-s", help="Workspace slug"),
    description: Optional[str] = typer.Option(None, "--description", "-d", help="Description"),
):
    """Create a new workspace."""
    try:
        config = load_config()
        client = KanbnClient(config)

        data = {"name": name}
        if slug:
            data["slug"] = slug
        if description:
            data["description"] = description

        workspace = client.post("workspaces", json=data)
        print_success(f"Created workspace: {workspace.get('name')}")
        display_workspace(workspace)

    except KanbnError as e:
        print_error(str(e))
        raise typer.Exit(1)


@app.command("get")
def get_workspace(
    identifier: str = typer.Argument(..., help="Workspace ID or slug"),
    by_slug: bool = typer.Option(False, "--slug", "-s", help="Use slug instead of ID"),
):
    """Get workspace details."""
    try:
        config = load_config()
        client = KanbnClient(config)

        if by_slug:
            workspace = client.get(f"workspaces/slug/{identifier}")
        else:
            workspace = client.get(f"workspaces/{identifier}")

        display_workspace(workspace)

    except KanbnError as e:
        print_error(str(e))
        raise typer.Exit(1)


@app.command("update")
def update_workspace(
    workspace_id: str = typer.Argument(..., help="Workspace ID"),
    name: Optional[str] = typer.Option(None, "--name", "-n", help="New name"),
    slug: Optional[str] = typer.Option(None, "--slug", "-s", help="New slug"),
    description: Optional[str] = typer.Option(None, "--description", "-d", help="New description"),
):
    """Update a workspace."""
    try:
        config = load_config()
        client = KanbnClient(config)

        data = {}
        if name:
            data["name"] = name
        if slug:
            data["slug"] = slug
        if description:
            data["description"] = description

        if not data:
            print_error("No update fields provided")
            raise typer.Exit(1)

        workspace = client.put(f"workspaces/{workspace_id}", json=data)
        print_success("Workspace updated")
        display_workspace(workspace)

    except KanbnError as e:
        print_error(str(e))
        raise typer.Exit(1)


@app.command("delete")
def delete_workspace(
    workspace_id: str = typer.Argument(..., help="Workspace ID"),
    confirm: bool = typer.Option(False, "--yes", "-y", help="Skip confirmation"),
):
    """Delete a workspace."""
    try:
        if not confirm:
            confirm = typer.confirm(f"Are you sure you want to delete workspace {workspace_id}?")
            if not confirm:
                raise typer.Abort()

        config = load_config()
        client = KanbnClient(config)

        client.delete(f"workspaces/{workspace_id}")
        print_success(f"Deleted workspace {workspace_id}")

    except typer.Abort:
        print_error("Cancelled")
        raise typer.Exit(1)
    except KanbnError as e:
        print_error(str(e))
        raise typer.Exit(1)


@app.command("search")
def search_workspace(
    workspace_id: str = typer.Argument(..., help="Workspace ID"),
    query: str = typer.Argument(..., help="Search query"),
):
    """Search boards and cards in a workspace."""
    try:
        config = load_config()
        client = KanbnClient(config)

        results = client.get(f"workspaces/{workspace_id}/search", params={"query": query})
        
        if isinstance(results, list):
            if not results:
                from kanbn_cli.utils.display import print_info
                print_info(f"No results found for '{query}'")
                return
            # If it returns a list of mixed items, we might need a different display logic
            # For now, let's dump it or try to categorize if possible
            # But the error showed specifically empty list []
            console.print(results)
            return

        if results.get("boards"):
            from kanbn_cli.utils.display import display_boards
            display_boards(results["boards"])
        
        if results.get("cards"):
            from kanbn_cli.utils.display import display_cards
            display_cards(results["cards"])

    except KanbnError as e:
        print_error(str(e))
        raise typer.Exit(1)


@app.command("invite")
def invite_member(
    workspace_id: str = typer.Argument(..., help="Workspace ID"),
    email: str = typer.Argument(..., help="User email"),
):
    """Invite member by email."""
    try:
        config = load_config()
        client = KanbnClient(config)

        data = {"email": email}
        client.post(f"workspaces/{workspace_id}/members", json=data)
        print_success(f"Invited {email} to workspace")

    except KanbnError as e:
        print_error(str(e))
        raise typer.Exit(1)


@app.command("remove-member")
def remove_member(
    workspace_id: str = typer.Argument(..., help="Workspace ID"),
    user_id: str = typer.Argument(..., help="User ID"),
    confirm: bool = typer.Option(False, "--yes", "-y", help="Skip confirmation"),
):
    """Remove member from workspace."""
    try:
        if not confirm:
            confirm = typer.confirm(f"Are you sure you want to remove user {user_id}?")
            if not confirm:
                raise typer.Abort()

        config = load_config()
        client = KanbnClient(config)

        client.delete(f"workspaces/{workspace_id}/members/{user_id}")
        print_success(f"Removed user {user_id} from workspace")

    except typer.Abort:
        print_error("Cancelled")
        raise typer.Exit(1)
    except KanbnError as e:
        print_error(str(e))
        raise typer.Exit(1)
