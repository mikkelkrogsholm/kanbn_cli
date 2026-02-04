"""Authentication commands."""

import typer
from rich.prompt import Prompt

from kanbn_cli.config import clear_config, load_config, save_config
from kanbn_cli.utils.display import print_error, print_info, print_success

app = typer.Typer(help="Manage authentication")


@app.command("login")
def login(
    api_url: str = typer.Option(
        "https://kanban.mikkelkrogsholm.dk/api",
        "--api-url",
        "-u",
        help="API base URL"
    ),
    token: str = typer.Option(None, "--token", "-t", help="API token"),
):
    """Store API credentials for authentication."""
    try:
        # Prompt for token if not provided
        if not token:
            token = Prompt.ask("Enter your API token", password=True)

        # Load existing config
        config = load_config()
        config.api_url = api_url
        config.api_token = token

        # Save configuration
        save_config(config)
        print_success(f"Authentication configured for {api_url}")

    except Exception as e:
        print_error(f"Failed to save configuration: {str(e)}")
        raise typer.Exit(1)


@app.command("logout")
def logout():
    """Clear stored credentials."""
    try:
        clear_config()
        print_success("Authentication credentials cleared")
    except Exception as e:
        print_error(f"Failed to clear configuration: {str(e)}")
        raise typer.Exit(1)


@app.command("status")
def status():
    """Show current authentication status."""
    try:
        config = load_config()
        
        print_info(f"API URL: {config.api_url}")
        
        if config.api_token:
            # Mask the token
            masked_token = config.api_token[:8] + "..." + config.api_token[-4:]
            print_info(f"API Token: {masked_token}")
            print_success("Authenticated")
        else:
            print_error("Not authenticated. Run 'kanbn auth login' to authenticate.")
            raise typer.Exit(1)

    except Exception as e:
        print_error(f"Failed to check status: {str(e)}")
        raise typer.Exit(1)
