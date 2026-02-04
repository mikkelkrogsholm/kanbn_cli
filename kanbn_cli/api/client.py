"""HTTP client for Kan.bn API."""

from typing import Any, Dict, Optional

import httpx
from kanbn_cli.config import KanbnConfig
from kanbn_cli.utils.errors import APIError, AuthenticationError, NotFoundError


class KanbnClient:
    """HTTP client for Kan.bn API."""

    def __init__(self, config: KanbnConfig):
        """Initialize the client with configuration."""
        self.config = config
        self.base_url = config.api_url.rstrip("/")

    def _handle_response(self, response: httpx.Response) -> Any:
        """Handle API response and errors."""
        if response.status_code == 401:
            raise AuthenticationError("Authentication failed. Please check your API token.")
        elif response.status_code == 404:
            raise NotFoundError("Resource")
        elif response.status_code >= 400:
            try:
                error_data = response.json()
                message = error_data.get("message", response.text)
            except Exception:
                message = response.text or f"HTTP {response.status_code}"
            raise APIError(message, status_code=response.status_code)

        if response.status_code == 204:
            return None

        try:
            return response.json()
        except Exception:
            return response.text

    def _build_headers(self) -> Dict[str, str]:
        """Build request headers with API key."""
        if not self.config.api_token:
            raise AuthenticationError("Not authenticated. Run 'kanbn auth login' first.")
        
        return {
            "x-api-key": self.config.api_token,
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

    def get(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Any:
        """Make a GET request."""
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        with httpx.Client() as client:
            response = client.get(url, headers=self._build_headers(), params=params)
            return self._handle_response(response)

    def post(
        self, endpoint: str, data: Optional[Dict[str, Any]] = None, json: Optional[Dict[str, Any]] = None
    ) -> Any:
        """Make a POST request."""
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        with httpx.Client() as client:
            response = client.post(url, headers=self._build_headers(), data=data, json=json)
            return self._handle_response(response)

    def put(self, endpoint: str, json: Optional[Dict[str, Any]] = None) -> Any:
        """Make a PUT request."""
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        with httpx.Client() as client:
            response = client.put(url, headers=self._build_headers(), json=json)
            return self._handle_response(response)

    def patch(self, endpoint: str, json: Optional[Dict[str, Any]] = None) -> Any:
        """Make a PATCH request."""
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        with httpx.Client() as client:
            response = client.patch(url, headers=self._build_headers(), json=json)
            return self._handle_response(response)

    def delete(self, endpoint: str) -> Any:
        """Make a DELETE request."""
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        with httpx.Client() as client:
            response = client.delete(url, headers=self._build_headers())
            return self._handle_response(response)
