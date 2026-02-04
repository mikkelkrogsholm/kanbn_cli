"""Checklist commands."""

from typing import Optional

import typer

from kanbn_cli.api.client import KanbnClient
from kanbn_cli.config import load_config
from kanbn_cli.utils.display import print_error, print_success
from kanbn_cli.utils.errors import KanbnError

app = typer.Typer(help="Manage checklists")


@app.command("create")
def create_checklist(
    card_id: str = typer.Argument(..., help="Card ID"),
    title: str = typer.Argument(..., help="Checklist title"),
):
    """Add a checklist to a card."""
    try:
        config = load_config()
        client = KanbnClient(config)

        data = {"name": title}
        checklist = client.post(f"cards/{card_id}/checklists", json=data)
        print_success(f"Created checklist '{title}'")
        
    except KanbnError as e:
        print_error(str(e))
        raise typer.Exit(1)


@app.command("delete")
def delete_checklist(
    checklist_id: str = typer.Argument(..., help="Checklist ID"),
    confirm: bool = typer.Option(False, "--yes", "-y", help="Skip confirmation"),
):
    """Delete a checklist."""
    try:
        if not confirm:
            confirm = typer.confirm(f"Are you sure you want to delete checklist {checklist_id}?")
            if not confirm:
                raise typer.Abort()

        config = load_config()
        client = KanbnClient(config)

        client.delete(f"checklists/{checklist_id}")
        print_success(f"Deleted checklist {checklist_id}")

    except typer.Abort:
        print_error("Cancelled")
        raise typer.Exit(1)
    except KanbnError as e:
        print_error(str(e))
        raise typer.Exit(1)


@app.command("add-item")
def add_item(
    checklist_id: str = typer.Argument(..., help="Checklist ID"),
    title: str = typer.Argument(..., help="Item title"),
):
    """Add item to checklist."""
    try:
        config = load_config()
        client = KanbnClient(config)

        data = {"title": title}
        client.post(f"checklists/{checklist_id}/items", json=data)
        print_success(f"Added item '{title}' to checklist")

    except KanbnError as e:
        print_error(str(e))
        raise typer.Exit(1)


@app.command("update-item")
def update_item(
    item_id: str = typer.Argument(..., help="Item ID"),
    title: Optional[str] = typer.Option(None, "--title", "-t", help="New title"),
    completed: Optional[bool] = typer.Option(None, "--completed/--not-completed", "-c/-C", help="Mark as completed/not completed"),
):
    """Update checklist item."""
    try:
        config = load_config()
        client = KanbnClient(config)

        data = {}
        if title:
            data["title"] = title
        if completed is not None:
            data["completed"] = completed

        if not data:
            print_error("No update fields provided")
            raise typer.Exit(1)

        client.put(f"checklist-items/{item_id}", json=data)
        print_success("Checklist item updated")

    except KanbnError as e:
        print_error(str(e))
        raise typer.Exit(1)


@app.command("delete-item")
def delete_item(
    item_id: str = typer.Argument(..., help="Item ID"),
    confirm: bool = typer.Option(False, "--yes", "-y", help="Skip confirmation"),
):
    """Delete checklist item."""
    try:
        if not confirm:
            confirm = typer.confirm(f"Are you sure you want to delete item {item_id}?")
            if not confirm:
                raise typer.Abort()

        config = load_config()
        client = KanbnClient(config)

        client.delete(f"checklist-items/{item_id}")
        print_success(f"Deleted checklist item {item_id}")

    except typer.Abort:
        print_error("Cancelled")
        raise typer.Exit(1)
    except KanbnError as e:
        print_error(str(e))
        raise typer.Exit(1)
