"""List commands."""

from typing import Optional

import typer

from kanbn_cli.api.client import KanbnClient
from kanbn_cli.config import load_config
from kanbn_cli.utils.display import display_lists, print_error, print_success
from kanbn_cli.utils.errors import KanbnError

app = typer.Typer(help="Manage lists")


@app.command("create")
def create_list(
    board_id: str = typer.Argument(..., help="Board ID"),
    name: str = typer.Argument(..., help="List name"),
    position: Optional[int] = typer.Option(None, "--position", "-p", help="Position"),
):
    """Create a new list."""
    try:
        config = load_config()
        client = KanbnClient(config)

        data = {"name": name, "board_id": board_id}
        if position is not None:
            data["position"] = position

        lst = client.post("lists", json=data)
        print_success(f"Created list: {lst.get('name')}")

    except KanbnError as e:
        print_error(str(e))
        raise typer.Exit(1)


@app.command("update")
def update_list(
    list_id: str = typer.Argument(..., help="List ID"),
    name: Optional[str] = typer.Option(None, "--name", "-n", help="New name"),
    position: Optional[int] = typer.Option(None, "--position", "-p", help="New position"),
):
    """Update a list."""
    try:
        config = load_config()
        client = KanbnClient(config)

        data = {}
        if name:
            data["name"] = name
        if position is not None:
            data["position"] = position

        if not data:
            print_error("No update fields provided")
            raise typer.Exit(1)

        lst = client.put(f"lists/{list_id}", json=data)
        print_success("List updated")

    except KanbnError as e:
        print_error(str(e))
        raise typer.Exit(1)


@app.command("delete")
def delete_list(
    list_id: str = typer.Argument(..., help="List ID"),
    confirm: bool = typer.Option(False, "--yes", "-y", help="Skip confirmation"),
):
    """Delete a list."""
    try:
        if not confirm:
            confirm = typer.confirm(f"Are you sure you want to delete list {list_id}?")
            if not confirm:
                raise typer.Abort()

        config = load_config()
        client = KanbnClient(config)

        client.delete(f"lists/{list_id}")
        print_success(f"Deleted list {list_id}")

    except typer.Abort:
        print_error("Cancelled")
        raise typer.Exit(1)
    except KanbnError as e:
        print_error(str(e))
        raise typer.Exit(1)
