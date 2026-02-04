#!/usr/bin/env python3
"""Demo script to show the beautiful colored output of kanbn-cli."""

import sys
sys.path.insert(0, '/Users/mikkelfreltoftkrogsholm/Projekter/kanbn-cli')

from kanbn_cli.utils.display import (
    print_success,
    print_error,
    print_warning,
    print_info,
    display_workspaces,
    display_boards,
    display_card,
    console
)
from rich.panel import Panel

# Demo success/error/warning/info messages
console.print("\n[bold cyan]═══ Message Types ═══[/bold cyan]\n")
print_success("Successfully created workspace 'My Project'")
print_error("Failed to authenticate - invalid token")
print_warning("This action will delete all data")
print_info("API URL: https://kanban.mikkelkrogsholm.dk/api")

# Demo workspace table
console.print("\n[bold cyan]═══ Workspace List ═══[/bold cyan]\n")
workspaces = [
    {
        "public_id": "ws_abc123",
        "name": "Personal Projects",
        "slug": "personal",
        "description": "My personal task management workspace"
    },
    {
        "public_id": "ws_def456",
        "name": "Work Tasks",
        "slug": "work",
        "description": "Professional projects and deliverables for Q1 2026"
    },
    {
        "public_id": "ws_ghi789",
        "name": "Team Collaboration",
        "slug": "team",
        "description": "Shared workspace for the engineering team"
    }
]
display_workspaces(workspaces)

# Demo board table
console.print("\n[bold cyan]═══ Board List ═══[/bold cyan]\n")
boards = [
    {
        "public_id": "brd_123",
        "name": "Website Redesign",
        "slug": "website",
        "description": "Complete overhaul of company website with modern stack"
    },
    {
        "public_id": "brd_456",
        "name": "Mobile App",
        "slug": "mobile",
        "description": "iOS and Android app development"
    }
]
display_boards(boards)

# Demo card detail view
console.print("\n[bold cyan]═══ Card Details ═══[/bold cyan]\n")
card = {
    "public_id": "card_789",
    "title": "Implement User Authentication",
    "description": "Add OAuth2 login with Google and GitHub providers",
    "labels": [
        {"name": "Feature", "color": "#00FF00"},
        {"name": "Priority: High", "color": "#FF0000"}
    ],
    "due_date": "2026-02-15",
    "checklists": [
        {
            "title": "Implementation Steps",
            "items": [
                {"title": "Set up OAuth providers", "completed": True},
                {"title": "Create login UI", "completed": True},
                {"title": "Add session management", "completed": False},
                {"title": "Write tests", "completed": False}
            ]
        }
    ]
}
display_card(card)

# Show styled panel
console.print("\n[bold cyan]═══ Styled Panels ═══[/bold cyan]\n")
console.print(Panel.fit(
    "[bold green]✓[/bold green] All systems operational\n"
    "[cyan]API Status:[/cyan] Connected\n"
    "[yellow]Rate Limit:[/yellow] 98/100 requests remaining",
    title="[bold]System Status[/bold]",
    border_style="green"
))

console.print("\n[bold magenta]🎨 This is what your CLI will look like! 🎨[/bold magenta]\n")
