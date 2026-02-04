"""User commands."""

from typing import Optional

import typer

from kanbn_cli.api.client import KanbnClient
from kanbn_cli.config import load_config
from kanbn_cli.utils.display import display_user, print_error, print_success
from kanbn_cli.utils.errors import KanbnError

app = typer.Typer(help="Manage user profile")


@app.command("get")
def get_user():
    """Get current user profile."""
    try:
        config = load_config()
        client = KanbnClient(config)

        user = client.get("users/me")
        display_user(user)

    except KanbnError as e:
        print_error(str(e))
        raise typer.Exit(1)


@app.command("update")
def update_user(
    name: Optional[str] = typer.Option(None, "--name", "-n", help="New name"),
    email: Optional[str] = typer.Option(None, "--email", "-e", help="New email"),
):
    """Update user profile."""
    try:
        config = load_config()
        client = KanbnClient(config)

        data = {}
        if name:
            data["name"] = name
        if email:
            data["email"] = email

        if not data:
            print_error("No update fields provided")
            raise typer.Exit(1)

        user = client.put("users/me", json=data)
        print_success("Profile updated")
        display_user(user)

    except KanbnError as e:
        print_error(str(e))
        raise typer.Exit(1)
