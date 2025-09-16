"""Configuration management for Congress API MCP Server."""

import os
import configparser
from typing import Optional
from pathlib import Path


class Config:
    """Configuration manager for Congress API integration.

    This class follows the Single Responsibility Principle by handling
    all configuration-related operations.
    """

    def __init__(self, config_dir: Optional[str] = None):
        """Initialize configuration manager.

        Args:
            config_dir: Directory containing configuration files.
                       Defaults to the directory containing this module.
        """
        if config_dir is None:
            config_dir = Path(__file__).parent

        self.config_dir = Path(config_dir)
        self._api_key: Optional[str] = None
        self._secrets_config: Optional[configparser.ConfigParser] = None

    @property
    def api_key(self) -> str:
        """Get the Congress API key.

        First checks environment variable CONGRESSIONAL_API_KEY,
        then falls back to secrets.ini file.

        Returns:
            The API key as a string.

        Raises:
            ValueError: If no API key is found in any configuration source.
        """
        if self._api_key is None:
            # Try environment variable first
            self._api_key = os.getenv('CONGRESSIONAL_API_KEY')

            # Fall back to secrets.ini
            if self._api_key is None:
                secrets_path = self.config_dir / 'api_client' / 'secrets.ini'
                if secrets_path.exists():
                    if self._secrets_config is None:
                        self._secrets_config = configparser.ConfigParser()
                        self._secrets_config.read(secrets_path)

                    if self._secrets_config.has_section('cdg_api'):
                        self._api_key = self._secrets_config.get('cdg_api', 'api_auth_key', fallback=None)

            if self._api_key is None or self._api_key == 'PASTE_KEY_HERE':
                raise ValueError(
                    "Congress API key not found. Please set CONGRESSIONAL_API_KEY environment variable "
                    "or configure api_auth_key in api_client/secrets.ini"
                )

        return self._api_key

    @property
    def base_url(self) -> str:
        """Get the base URL for the Congress API.

        Returns:
            The base URL as a string.
        """
        return "https://api.congress.gov/v3"

    @property
    def rate_limit_per_hour(self) -> int:
        """Get the rate limit for API requests per hour.

        Returns:
            The rate limit as an integer.
        """
        return 5000  # Congress API allows 5,000 requests per hour

    @property
    def default_format(self) -> str:
        """Get the default response format.

        Returns:
            The default format ('json').
        """
        return "json"

    @property
    def default_limit(self) -> int:
        """Get the default pagination limit.

        Returns:
            The default limit for API responses.
        """
        return 20

    def clear_cache(self) -> None:
        """Clear cached configuration values.

        Useful for testing or when configuration changes.
        """
        self._api_key = None
        self._secrets_config = None
