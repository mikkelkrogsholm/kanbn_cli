"""Comment commands."""

import typer

from kanbn_cli.api.client import KanbnClient
from kanbn_cli.config import load_config
from kanbn_cli.utils.display import print_error, print_success
from kanbn_cli.utils.errors import KanbnError

app = typer.Typer(help="Manage comments")


@app.command("update")
def update_comment(
    comment_id: str = typer.Argument(..., help="Comment ID"),
    text: str = typer.Argument(..., help="New comment text"),
):
    """Update a comment."""
    try:
        config = load_config()
        client = KanbnClient(config)

        data = {"comment": text}
        client.put(f"comments/{comment_id}", json=data)
        print_success("Comment updated")

    except KanbnError as e:
        print_error(str(e))
        raise typer.Exit(1)


@app.command("delete")
def delete_comment(
    comment_id: str = typer.Argument(..., help="Comment ID"),
    confirm: bool = typer.Option(False, "--yes", "-y", help="Skip confirmation"),
):
    """Delete a comment."""
    try:
        if not confirm:
            confirm = typer.confirm(f"Are you sure you want to delete comment {comment_id}?")
            if not confirm:
                raise typer.Abort()

        config = load_config()
        client = KanbnClient(config)

        client.delete(f"comments/{comment_id}")
        print_success(f"Deleted comment {comment_id}")

    except typer.Abort:
        print_error("Cancelled")
        raise typer.Exit(1)
    except KanbnError as e:
        print_error(str(e))
        raise typer.Exit(1)
