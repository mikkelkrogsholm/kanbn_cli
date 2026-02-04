"""Board commands."""

from typing import Optional

import typer

from kanbn_cli.api.client import KanbnClient
from kanbn_cli.config import load_config
from kanbn_cli.utils.display import display_boards, print_error, print_success
from kanbn_cli.utils.errors import KanbnError

app = typer.Typer(help="Manage boards")


@app.command("list")
def list_boards(
    workspace_id: str = typer.Argument(..., help="Workspace ID"),
):
    """List all boards in a workspace."""
    try:
        config = load_config()
        client = KanbnClient(config)

        boards = client.get(f"workspaces/{workspace_id}/boards")
        display_boards(boards)

    except KanbnError as e:
        print_error(str(e))
        raise typer.Exit(1)


@app.command("create")
def create_board(
    workspace_id: str = typer.Argument(..., help="Workspace ID"),
    name: str = typer.Argument(..., help="Board name"),
    slug: Optional[str] = typer.Option(None, "--slug", "-s", help="Board slug"),
    description: Optional[str] = typer.Option(None, "--description", "-d", help="Description"),
):
    """Create a new board."""
    try:
        config = load_config()
        client = KanbnClient(config)

        data = {"name": name, "workspace_id": workspace_id}
        if slug:
            data["slug"] = slug
        if description:
            data["description"] = description

        board = client.post("boards", json=data)
        print_success(f"Created board: {board.get('name')}")

    except KanbnError as e:
        print_error(str(e))
        raise typer.Exit(1)


@app.command("get")
def get_board(
    identifier: str = typer.Argument(..., help="Board ID or slug"),
    workspace_id: Optional[str] = typer.Option(None, "--workspace", "-w", help="Workspace ID (required if using slug)"),
    by_slug: bool = typer.Option(False, "--slug", "-s", help="Use slug instead of ID"),
):
    """Get board details."""
    try:
        config = load_config()
        client = KanbnClient(config)

        if by_slug:
            if not workspace_id:
                print_error("Workspace ID is required when using slug")
                raise typer.Exit(1)
            board = client.get(f"workspaces/{workspace_id}/boards/slug/{identifier}")
        else:
            board = client.get(f"boards/{identifier}")

        from kanbn_cli.utils.display import console
        console.print(board)

    except KanbnError as e:
        print_error(str(e))
        raise typer.Exit(1)


@app.command("update")
def update_board(
    board_id: str = typer.Argument(..., help="Board ID"),
    name: Optional[str] = typer.Option(None, "--name", "-n", help="New name"),
    slug: Optional[str] = typer.Option(None, "--slug", "-s", help="New slug"),
    description: Optional[str] = typer.Option(None, "--description", "-d", help="New description"),
):
    """Update a board."""
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

        board = client.put(f"boards/{board_id}", json=data)
        print_success("Board updated")

    except KanbnError as e:
        print_error(str(e))
        raise typer.Exit(1)


@app.command("delete")
def delete_board(
    board_id: str = typer.Argument(..., help="Board ID"),
    confirm: bool = typer.Option(False, "--yes", "-y", help="Skip confirmation"),
):
    """Delete a board."""
    try:
        if not confirm:
            confirm = typer.confirm(f"Are you sure you want to delete board {board_id}?")
            if not confirm:
                raise typer.Abort()

        config = load_config()
        client = KanbnClient(config)

        client.delete(f"boards/{board_id}")
        print_success(f"Deleted board {board_id}")

    except typer.Abort:
        print_error("Cancelled")
        raise typer.Exit(1)
    except KanbnError as e:
        print_error(str(e))
        raise typer.Exit(1)
