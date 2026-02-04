"""Main CLI entry point for Kan.bn CLI."""

import typer

from kanbn_cli import __version__
from kanbn_cli.commands import admin, attachment, auth, board, card, checklist, comment, import_cmd, integration, invite, label, list, user, workspace

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
app.add_typer(checklist.app, name="checklist")
app.add_typer(comment.app, name="comment")
app.add_typer(invite.app, name="invite")
app.add_typer(user.app, name="user")
app.add_typer(import_cmd.app, name="import")
app.add_typer(integration.app, name="integration")
app.add_typer(attachment.app, name="attachment")

# Register admin commands at root level
app.command(name="health")(admin.health_check)
app.command(name="stats")(admin.statistics)


@app.command()
def version():
    """Show version information."""
    typer.echo(f"kanbn-cli version {__version__}")


if __name__ == "__main__":
    app()
