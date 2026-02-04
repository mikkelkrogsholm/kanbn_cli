"""Integration commands."""

import typer

from kanbn_cli.api.client import KanbnClient
from kanbn_cli.config import load_config
from kanbn_cli.utils.display import display_integrations, print_error, print_info, print_success
from kanbn_cli.utils.errors import KanbnError

app = typer.Typer(help="Manage integrations")


@app.command("list")
def list_integrations():
    """List connected integrations."""
    try:
        config = load_config()
        client = KanbnClient(config)

        providers = client.get("integration/providers")
        display_integrations(providers)

    except KanbnError as e:
        print_error(str(e))
        raise typer.Exit(1)


@app.command("connect")
def connect_integration(
    provider: str = typer.Argument(..., help="Provider name (e.g., trello)"),
):
    """Connect an integration."""
    try:
        config = load_config()
        client = KanbnClient(config)

        auth_url = client.get(f"integration/{provider}/auth-url")
        print_success(f"To connect {provider}, visit:")
        print_info(auth_url.get('authUrl'))

    except KanbnError as e:
        print_error(str(e))
        raise typer.Exit(1)


@app.command("disconnect")
def disconnect_integration(
    provider: str = typer.Argument(..., help="Provider name"),
    confirm: bool = typer.Option(False, "--yes", "-y", help="Skip confirmation"),
):
    """Disconnect an integration."""
    try:
        if not confirm:
            confirm = typer.confirm(f"Are you sure you want to disconnect {provider}?")
            if not confirm:
                raise typer.Abort()

        config = load_config()
        client = KanbnClient(config)

        client.delete(f"integration/{provider}")
        print_success(f"Disconnected {provider}")

    except typer.Abort:
        print_error("Cancelled")
        raise typer.Exit(1)
    except KanbnError as e:
        print_error(str(e))
        raise typer.Exit(1)
