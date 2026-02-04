"""Invite commands."""

import typer

from kanbn_cli.api.client import KanbnClient
from kanbn_cli.config import load_config
from kanbn_cli.utils.display import print_error, print_success, print_info
from kanbn_cli.utils.errors import KanbnError
from rich.panel import Panel
from kanbn_cli.utils.display import console

app = typer.Typer(help="Manage invites")


@app.command("create")
def create_invite(
    workspace_id: str = typer.Argument(..., help="Workspace ID"),
):
    """Generate workspace invite link."""
    try:
        config = load_config()
        client = KanbnClient(config)

        invite = client.post(f"workspaces/{workspace_id}/invites")
        print_success(f"Invite link created: {invite.get('inviteUrl')}")

    except KanbnError as e:
        print_error(str(e))
        raise typer.Exit(1)


@app.command("get")
def get_invite(
    workspace_id: str = typer.Argument(..., help="Workspace ID"),
):
    """Get active invite link."""
    try:
        config = load_config()
        client = KanbnClient(config)

        invite = client.get(f"workspaces/{workspace_id}/invites/active")
        if invite:
            print_success(f"Active invite link: {invite.get('inviteUrl')}")
            print_info(f"Expires at: {invite.get('expiresAt')}")
        else:
            print_info("No active invite link found")

    except KanbnError as e:
        print_error(str(e))
        raise typer.Exit(1)


@app.command("revoke")
def revoke_invite(
    workspace_id: str = typer.Argument(..., help="Workspace ID"),
    confirm: bool = typer.Option(False, "--yes", "-y", help="Skip confirmation"),
):
    """Revoke active invite link."""
    try:
        if not confirm:
            confirm = typer.confirm(f"Are you sure you want to revoke invite for workspace {workspace_id}?")
            if not confirm:
                raise typer.Abort()

        config = load_config()
        client = KanbnClient(config)

        client.delete(f"workspaces/{workspace_id}/invites")
        print_success("Invite link revoked")

    except typer.Abort:
        print_error("Cancelled")
        raise typer.Exit(1)
    except KanbnError as e:
        print_error(str(e))
        raise typer.Exit(1)


@app.command("accept")
def accept_invite(
    code: str = typer.Argument(..., help="Invite code"),
):
    """Accept invitation."""
    try:
        config = load_config()
        client = KanbnClient(config)

        client.post(f"invites/{code}/accept")
        print_success("Invitation accepted!")

    except KanbnError as e:
        print_error(str(e))
        raise typer.Exit(1)


@app.command("info")
def get_invite_info(
    code: str = typer.Argument(..., help="Invite code"),
):
    """Get invite information."""
    try:
        config = load_config()
        client = KanbnClient(config)

        invite = client.get(f"invites/{code}")
        
        console.print(Panel.fit(
            f"Workspace: {invite.get('workspace', {}).get('name')}\n"
            f"Inviter: {invite.get('inviter', {}).get('name')}\n"
            f"Expires: {invite.get('expiresAt')}",
            title="Invite Information",
            border_style="blue"
        ))

    except KanbnError as e:
        print_error(str(e))
        raise typer.Exit(1)
