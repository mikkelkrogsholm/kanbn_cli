"""Card commands."""

from typing import Optional

import typer

from kanbn_cli.api.client import KanbnClient
from kanbn_cli.config import load_config
from kanbn_cli.utils.display import display_card, display_cards, print_error, print_success
from kanbn_cli.utils.errors import KanbnError

app = typer.Typer(help="Manage cards")


@app.command("create")
def create_card(
    list_id: str = typer.Argument(..., help="List ID"),
    title: str = typer.Argument(..., help="Card title"),
    description: Optional[str] = typer.Option(None, "--description", "-d", help="Description"),
    position: Optional[int] = typer.Option(None, "--position", "-p", help="Position in the list"),
):
    """Create a new card."""
    try:
        config = load_config()
        client = KanbnClient(config)

        data = {
            "title": title,
            "description": description or "",
            "listPublicId": list_id,
            "position": position or "end",
            "labelPublicIds": [],
            "memberPublicIds": [],
        }

        card = client.post("cards", json=data)
        print_success(f"Created card: {card.get('title')}")

    except KanbnError as e:
        print_error(str(e))
        raise typer.Exit(1)


@app.command("get")
def get_card(
    card_id: str = typer.Argument(..., help="Card ID"),
):
    """Get card details."""
    try:
        config = load_config()
        client = KanbnClient(config)

        card = client.get(f"cards/{card_id}")
        display_card(card)

    except KanbnError as e:
        print_error(str(e))
        raise typer.Exit(1)


@app.command("update")
def update_card(
    card_id: str = typer.Argument(..., help="Card ID"),
    title: Optional[str] = typer.Option(None, "--title", "-t", help="New title"),
    description: Optional[str] = typer.Option(None, "--description", "-d", help="New description"),
    list_id: Optional[str] = typer.Option(None, "--list", "-l", help="Move to list"),
):
    """Update a card."""
    try:
        config = load_config()
        client = KanbnClient(config)

        data = {}
        if title:
            data["title"] = title
        if description:
            data["description"] = description
        if list_id:
            data["listPublicId"] = list_id # Changed to listPublicId

        if not data:
            print_error("No update fields provided")
            raise typer.Exit(1)

        card = client.put(f"cards/{card_id}", json=data)
        print_success("Card updated")

    except KanbnError as e:
        print_error(str(e))
        raise typer.Exit(1)


@app.command("delete")
def delete_card(
    card_id: str = typer.Argument(..., help="Card ID"),
    confirm: bool = typer.Option(False, "--yes", "-y", help="Skip confirmation"),
):
    """Delete a card."""
    try:
        if not confirm:
            confirm = typer.confirm(f"Are you sure you want to delete card {card_id}?")
            if not confirm:
                raise typer.Abort()

        config = load_config()
        client = KanbnClient(config)

        client.delete(f"cards/{card_id}")
        print_success(f"Deleted card {card_id}")

    except typer.Abort:
        print_error("Cancelled")
        raise typer.Exit(1)
    except KanbnError as e:
        print_error(str(e))
        raise typer.Exit(1)


@app.command("comment")
def add_comment(
    card_id: str = typer.Argument(..., help="Card ID"),
    text: str = typer.Argument(..., help="Comment text"),
):
    """Add a comment to a card."""
    try:
        config = load_config()
        client = KanbnClient(config)

        data = {"comment": text}
        comment = client.post(f"cards/{card_id}/comments", json=data)
        print_success("Comment added")

    except KanbnError as e:
        print_error(str(e))
        raise typer.Exit(1)


@app.command("label")
def manage_label(
    card_id: str = typer.Argument(..., help="Card ID"),
    label_id: str = typer.Argument(..., help="Label ID"),
    remove: bool = typer.Option(False, "--remove", "-r", help="Remove label instead of adding"),
):
    """Add or remove a label from a card."""
    try:
        config = load_config()
        client = KanbnClient(config)

        action = "remove" if remove else "add"
        client.post(f"cards/{card_id}/labels", json={"label_id": label_id, "action": action})
        
        if remove:
            print_success("Label removed from card")
        else:
            print_success("Label added to card")

    except KanbnError as e:
        print_error(str(e))
        raise typer.Exit(1)
