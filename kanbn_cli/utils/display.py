"""Display utilities for rich terminal output."""

from typing import Any, Dict, List, Optional

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import print as rprint

console = Console()


def print_success(message: str) -> None:
    """Print a success message."""
    console.print(f"[green]✓[/green] {message}")


def print_error(message: str) -> None:
    """Print an error message."""
    console.print(f"[red]✗[/red] {message}", style="red")


def print_warning(message: str) -> None:
    """Print a warning message."""
    console.print(f"[yellow]⚠[/yellow] {message}", style="yellow")


def print_info(message: str) -> None:
    """Print an info message."""
    console.print(f"[blue]ℹ[/blue] {message}")


def display_workspace(workspace: Dict[str, Any]) -> None:
    """Display workspace details."""
    console.print(Panel.fit(
        f"[bold]{workspace.get('name')}[/bold]\n"
        f"ID: {workspace.get('publicId') or workspace.get('public_id') or workspace.get('id')}\n"
        f"Slug: {workspace.get('slug', 'N/A')}\n"
        f"Description: {workspace.get('description', 'N/A')}",
        title="Workspace",
        border_style="blue"
    ))


def display_workspaces(workspaces: List[Dict[str, Any]]) -> None:
    """Display a table of workspaces."""
    if not workspaces:
        print_info("No workspaces found")
        return

    table = Table(title="Workspaces")
    table.add_column("ID", style="cyan")
    table.add_column("Name", style="green")
    table.add_column("Slug", style="yellow")
    table.add_column("Description")

    for ws in workspaces:
        # Handle API response structure that may wrap workspace in {role, workspace}
        workspace_data = ws.get("workspace", ws)
        table.add_row(
            workspace_data.get("publicId") or workspace_data.get("public_id") or workspace_data.get("id", ""),
            workspace_data.get("name", ""),
            workspace_data.get("slug", ""),
            workspace_data.get("description", "")[:50] if workspace_data.get("description") else ""
        )

    console.print(table)


def display_boards(boards: List[Dict[str, Any]]) -> None:
    """Display a table of boards."""
    if not boards:
        print_info("No boards found")
        return

    table = Table(title="Boards")
    table.add_column("ID", style="cyan")
    table.add_column("Name", style="green")
    table.add_column("Slug", style="yellow")
    table.add_column("Description")

    for board in boards:
        table.add_row(
            board.get("publicId") or board.get("public_id") or board.get("id", ""),
            board.get("name", ""),
            board.get("slug", ""),
            board.get("description", "")[:50] if board.get("description") else ""
        )

    console.print(table)


def display_lists(lists: List[Dict[str, Any]]) -> None:
    """Display a table of lists."""
    if not lists:
        print_info("No lists found")
        return

    table = Table(title="Lists")
    table.add_column("ID", style="cyan")
    table.add_column("Name", style="green")
    table.add_column("Position", style="yellow")

    for lst in lists:
        table.add_row(
            lst.get("publicId") or lst.get("public_id") or lst.get("id", ""),
            lst.get("name", ""),
            str(lst.get("position", ""))
        )

    console.print(table)


def display_cards(cards: List[Dict[str, Any]]) -> None:
    """Display a table of cards."""
    if not cards:
        print_info("No cards found")
        return

    table = Table(title="Cards")
    table.add_column("ID", style="cyan")
    table.add_column("Title", style="green")
    table.add_column("Description")
    table.add_column("Labels", style="yellow")

    for card in cards:
        labels = ", ".join([l.get("name", "") for l in card.get("labels", [])])
        table.add_row(
            card.get("publicId") or card.get("public_id") or card.get("id", ""),
            card.get("title", ""),
            card.get("description", "")[:40] if card.get("description") else "",
            labels
        )

    console.print(table)


def display_card(card: Dict[str, Any]) -> None:
    """Display detailed card information."""
    labels = ", ".join([l.get("name", "") for l in card.get("labels", [])])
    
    content = f"[bold]{card.get('title')}[/bold]\n\n"
    content += f"ID: {card.get('publicId') or card.get('public_id') or card.get('id')}\n"
    content += f"Description: {card.get('description', 'N/A')}\n"
    content += f"Labels: {labels or 'None'}\n"
    content += f"Due Date: {card.get('dueDate') or card.get('due_date', 'N/A')}\n"
    
    # Display checklists
    checklists = card.get("checklists", [])
    if checklists:
        content += "\n[bold]Checklists:[/bold]\n"
        for checklist in checklists:
            name = checklist.get('name') or checklist.get('title') or 'Untitled'
            clid = checklist.get('publicId') or checklist.get('public_id') or checklist.get('id')
            content += f"  • {name} (ID: {clid})\n"
            for item in checklist.get("items", []):
                status = "✓" if item.get("completed") else "○"
                iid = item.get('publicId') or item.get('public_id') or item.get('id')
                content += f"    {status} {item.get('title')} (ID: {iid})\n"
    
    console.print(Panel.fit(content, title="Card Details", border_style="green"))


def display_activities(activities: List[Dict[str, Any]]) -> None:
    """Display card activities."""
    if not activities or not activities.get("activities"):
        print_info("No activities found")
        return

    table = Table(title="Card Activity")
    table.add_column("Date", style="cyan")
    table.add_column("User", style="green")
    table.add_column("Action", style="yellow")
    table.add_column("Details")
    
    for activity in activities.get("activities", []):
        table.add_row(
            activity.get("createdAt", ""),
            activity.get("user", {}).get("name", ""),
            activity.get("action", ""),
            activity.get("details", "") or ""
        )
    console.print(table)


def display_user(user: Dict[str, Any]) -> None:
    """Display user profile."""
    console.print(Panel.fit(
        f"[bold]{user.get('name')}[/bold]\n"
        f"Email: {user.get('email')}\n"
        f"ID: {user.get('publicId')}",
        title="User Profile",
        border_style="blue"
    ))


def display_activities(activities: List[Dict[str, Any]]) -> None:
    """Display card activities."""
    if not activities or not activities.get("activities"):
        print_info("No activities found")
        return

    table = Table(title="Card Activity")
    table.add_column("Date", style="cyan")
    table.add_column("User", style="green")
    table.add_column("Action", style="yellow")
    table.add_column("Details")
    
    for activity in activities.get("activities", []):
        table.add_row(
            activity.get("createdAt", ""),
            activity.get("user", {}).get("name", ""),
            activity.get("action", ""),
            activity.get("details", "") or ""
        )
    console.print(table)


def display_integrations(providers: List[Dict[str, Any]]) -> None:
    """Display integration providers."""
    if not providers:
        print_info("No integrations found")
        return

    table = Table(title="Integrations")
    table.add_column("Provider", style="cyan")
    table.add_column("Connected", style="green")
    
    for provider in providers:
        connected = "✓" if provider.get("connected") else "○"
        table.add_row(
            provider.get("name", ""),
            connected
        )
    console.print(table)


def display_trello_boards(boards: List[Dict[str, Any]]) -> None:
    """Display Trello boards."""
    if not boards:
        print_info("No Trello boards found")
        return

    table = Table(title="Trello Boards")
    table.add_column("ID", style="cyan")
    table.add_column("Name", style="green")
    table.add_column("URL")
    
    for board in boards:
        table.add_row(
            board.get("id", ""),
            board.get("name", ""),
            board.get("url", "")
        )
    console.print(table)
