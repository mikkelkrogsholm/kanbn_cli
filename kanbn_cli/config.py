"""Configuration management for Kan.bn CLI."""

import json
import os
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv
from pydantic import BaseModel, Field

# Load .env file if it exists
load_dotenv()


class KanbnConfig(BaseModel):
    """Configuration for Kan.bn CLI."""

    api_url: str = Field(
        default="https://kanban.mikkelkrogsholm.dk/api",
        description="Base URL for the Kan.bn API",
    )
    api_token: Optional[str] = Field(default=None, description="API authentication token")
    default_workspace: Optional[str] = Field(
        default=None, description="Default workspace ID or slug"
    )


def get_config_path() -> Path:
    """Get the path to the config file."""
    home = Path.home()
    return home / ".kanbnrc"


def load_config() -> KanbnConfig:
    """Load configuration from environment and config file."""
    # Start with defaults
    api_url = os.getenv("KANBN_API_URL", "https://kanban.mikkelkrogsholm.dk/api")
    api_token = os.getenv("KANBN_API_TOKEN")
    default_workspace = os.getenv("KANBN_DEFAULT_WORKSPACE")

    # Try to load from config file if it exists
    config_path = get_config_path()
    if config_path.exists():
        try:
            with open(config_path) as f:
                data = json.load(f)
                api_url = data.get("api_url", api_url)
                api_token = data.get("api_token", api_token)
                default_workspace = data.get("default_workspace", default_workspace)
        except Exception:
            pass

    return KanbnConfig(
        api_url=api_url,
        api_token=api_token,
        default_workspace=default_workspace
    )


def save_config(config: KanbnConfig) -> None:
    """Save configuration to config file."""
    config_path = get_config_path()
    with open(config_path, "w") as f:
        json.dump(
            {
                "api_url": config.api_url,
                "api_token": config.api_token,
                "default_workspace": config.default_workspace,
            },
            f,
            indent=2,
        )


def clear_config() -> None:
    """Clear the configuration file."""
    config_path = get_config_path()
    if config_path.exists():
        config_path.unlink()
