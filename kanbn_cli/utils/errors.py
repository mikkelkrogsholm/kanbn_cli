"""Custom errors for Kan.bn CLI."""

from typing import Optional


class KanbnError(Exception):
    """Base exception for Kan.bn CLI errors."""

    pass


class AuthenticationError(KanbnError):
    """Raised when authentication fails."""

    pass


class APIError(KanbnError):
    """Raised when an API request fails."""

    def __init__(self, message: str, status_code: Optional[int] = None):
        super().__init__(message)
        self.status_code = status_code


class NotFoundError(APIError):
    """Raised when a resource is not found."""

    def __init__(self, resource: str):
        super().__init__(f"{resource} not found", status_code=404)


class ValidationError(KanbnError):
    """Raised when input validation fails."""

    pass


class ConfigurationError(KanbnError):
    """Raised when configuration is invalid or missing."""

    pass
