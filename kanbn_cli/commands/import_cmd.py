"""Import commands."""

import typer

from kanbn_cli.api.client import KanbnClient
from kanbn_cli.config import load_config
from kanbn_cli.utils.display import display_trello_boards, print_error, print_success
from kanbn_cli.utils.errors import KanbnError

app = typer.Typer(help="Import data from other services")


@app.command("trello-list")
def list_trello_boards():
    """List available Trello boards."""
    try:
        config = load_config()
        client = KanbnClient(config)

        boards = client.get("integration/trello/boards")
        display_trello_boards(boards)

    except KanbnError as e:
        print_error(str(e))
        raise typer.Exit(1)


@app.command("trello")
def import_trello(
    board_id: str = typer.Argument(..., help="Trello Board ID"),
    workspace_id: str = typer.Option(..., "--workspace", "-w", help="Target Workspace ID"),
):
    """Import Trello board."""
    try:
        config = load_config()
        client = KanbnClient(config)

        data = {
            "boardId": board_id,
            "workspacePublicId": workspace_id
        }
        result = client.post("imports/trello", json=data)
        print_success(f"Import started: {result.get('status', 'Started')}")

    except KanbnError as e:
        print_error(str(e))
        raise typer.Exit(1)
