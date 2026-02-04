"""Label commands."""

from typing import Optional

import typer

from kanbn_cli.api.client import KanbnClient
from kanbn_cli.config import load_config
from kanbn_cli.utils.display import print_error, print_success
from kanbn_cli.utils.errors import KanbnError

app = typer.Typer(help="Manage labels")


@app.command("create")
def create_label(
    board_id: str = typer.Argument(..., help="Board ID"),
    name: str = typer.Argument(..., help="Label name"),
    color: str = typer.Argument(..., help="Label color (hex code)"),
):
    """Create a new label."""
    try:
        config = load_config()
        client = KanbnClient(config)

        data = {"name": name, "color": color, "board_id": board_id}
        label = client.post("labels", json=data)
        print_success(f"Created label: {label.get('name')}")

    except KanbnError as e:
        print_error(str(e))
        raise typer.Exit(1)


@app.command("get")
def get_label(
    label_id: str = typer.Argument(..., help="Label ID"),
):
    """Get label details."""
    try:
        config = load_config()
        client = KanbnClient(config)

        label = client.get(f"labels/{label_id}")
        from kanbn_cli.utils.display import console
        console.print(label)

    except KanbnError as e:
        print_error(str(e))
        raise typer.Exit(1)


@app.command("update")
def update_label(
    label_id: str = typer.Argument(..., help="Label ID"),
    name: Optional[str] = typer.Option(None, "--name", "-n", help="New name"),
    color: Optional[str] = typer.Option(None, "--color", "-c", help="New color"),
):
    """Update a label."""
    try:
        config = load_config()
        client = KanbnClient(config)

        data = {}
        if name:
            data["name"] = name
        if color:
            data["color"] = color

        if not data:
            print_error("No update fields provided")
            raise typer.Exit(1)

        label = client.put(f"labels/{label_id}", json=data)
        print_success("Label updated")

    except KanbnError as e:
        print_error(str(e))
        raise typer.Exit(1)


@app.command("delete")
def delete_label(
    label_id: str = typer.Argument(..., help="Label ID"),
    confirm: bool = typer.Option(False, "--yes", "-y", help="Skip confirmation"),
):
    """Delete a label."""
    try:
        if not confirm:
            confirm = typer.confirm(f"Are you sure you want to delete label {label_id}?")
            if not confirm:
                raise typer.Abort()

        config = load_config()
        client = KanbnClient(config)

        client.delete(f"labels/{label_id}")
        print_success(f"Deleted label {label_id}")

    except typer.Abort:
        print_error("Cancelled")
        raise typer.Exit(1)
    except KanbnError as e:
        print_error(str(e))
        raise typer.Exit(1)
