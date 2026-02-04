"""Main CLI entry point for Kan.bn CLI."""

import typer

from kanbn_cli import __version__
from kanbn_cli.commands import auth, board, card, label, list, workspace

app = typer.Typer(
    name="kanbn",
    help="Kan.bn CLI - Manage your Kanban boards from the command line",
    add_completion=False,
)

# Add command groups
app.add_typer(auth.app, name="auth")
app.add_typer(workspace.app, name="workspace")
app.add_typer(board.app, name="board")
app.add_typer(list.app, name="list")
app.add_typer(card.app, name="card")
app.add_typer(label.app, name="label")


@app.command()
def version():
    """Show version information."""
    typer.echo(f"kanbn-cli version {__version__}")


if __name__ == "__main__":
    app()
