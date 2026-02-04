"""Admin/System commands."""

import typer

from kanbn_cli.api.client import KanbnClient
from kanbn_cli.config import load_config
from kanbn_cli.utils.display import print_error, print_info, print_success
from kanbn_cli.utils.errors import KanbnError, AuthenticationError
from rich.console import Console
from rich.panel import Panel

app = typer.Typer(help="System commands")
console = Console()


@app.command("health")
def health_check():
    """Check API health status."""
    try:
        config = load_config()
        client = KanbnClient(config)

        # Increase timeout for health check as it might take longer
        health = client.get("health", timeout=15.0)
        status = health.get("status", "unknown")
        if status == "ok":
            print_success(f"System Health: {status}")
        else:
            print_error(f"System Health: {status}")
        
        console.print(health)

    except KanbnError as e:
        print_error(str(e))
        raise typer.Exit(1)


@app.command("stats")
def statistics():
    """View system statistics."""
    try:
        config = load_config()
        client = KanbnClient(config)

        stats = client.get("stats")
        console.print(Panel.fit(str(stats), title="System Statistics"))

    except AuthenticationError:
        print_error("Stats endpoint requires admin permissions")
        raise typer.Exit(1)
    except KanbnError as e:
        print_error(str(e))
        raise typer.Exit(1)
