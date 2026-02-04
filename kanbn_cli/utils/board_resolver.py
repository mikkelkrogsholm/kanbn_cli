"""Board name resolution from boards.md"""
from pathlib import Path
import re
from typing import Optional, Dict

def load_board_mappings(skill_dir: Path) -> Dict[str, str]:
    """Parse boards.md for name -> ID mappings"""
    boards_file = skill_dir / "boards.md"
    if not boards_file.exists():
        # Fallback: check parent directories or default locations if needed
        # For now, just return empty if not found in strict location
        return {}

    content = boards_file.read_text()
    mappings = {}

    # Pattern: ### Board Name\n**ID:** `id`
    # We'll make it a bit robust to handle variations
    pattern = r'###\s+([^\n]+)\n\*\*ID:\*\*\s*`([a-z0-9]+)`'
    for match in re.finditer(pattern, content):
        name = match.group(1).strip()
        board_id = match.group(2)
        mappings[name.lower()] = board_id

    return mappings

def resolve_board_name(name_or_id: str, skill_dir: Path) -> str:
    """Resolve board name to ID, or return as-is if already ID"""
    # If it's approx 12 chars and alphanumeric, assume it's an ID
    # Kanbn IDs are typically 12 chars public IDs (e.g. x248npxfjymc)
    if len(name_or_id) >= 10 and len(name_or_id) <= 14 and name_or_id.isalnum():
        return name_or_id

    # Try to resolve from boards.md
    mappings = load_board_mappings(skill_dir)
    board_id = mappings.get(name_or_id.lower())

    if board_id:
        return board_id

    # Not found, return as-is (let API handle/fail)
    return name_or_id
