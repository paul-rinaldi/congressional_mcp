"""HTTP client for Congress API with rate limiting and error handling."""

import time
import requests
from typing import Dict, Any, Optional
from dataclasses import dataclass
from config import Config


@dataclass
class RateLimitInfo:
    """Information about current rate limiting status."""
    requests_this_hour: int
    hour_start_time: float
    is_rate_limited: bool


class HttpClient:
    """HTTP client with rate limiting for Congress API.

    This class follows the Single Responsibility Principle by handling
    all HTTP communication and rate limiting logic.
    """

    def __init__(self, config: Config):
        """Initialize HTTP client.

        Args:
            config: Configuration instance with API settings.
        """
        self.config = config
        self.session = requests.Session()
        self.rate_limit_info = RateLimitInfo(
            requests_this_hour=0,
            hour_start_time=time.time(),
            is_rate_limited=False
        )

    def _check_rate_limit(self) -> None:
        """Check and enforce rate limiting.

        Raises:
            Exception: If rate limit is exceeded.
        """
        current_time = time.time()

        # Reset counter if hour has passed
        if current_time - self.rate_limit_info.hour_start_time >= 3600:  # 1 hour
            self.rate_limit_info.requests_this_hour = 0
            self.rate_limit_info.hour_start_time = current_time
            self.rate_limit_info.is_rate_limited = False

        # Check if we're approaching the limit
        if self.rate_limit_info.requests_this_hour >= self.config.rate_limit_per_hour:
            self.rate_limit_info.is_rate_limited = True
            raise Exception(
                f"Rate limit exceeded: {self.rate_limit_info.requests_this_hour} "
                f"requests in the last hour. Limit is {self.config.rate_limit_per_hour}"
            )

    def _build_url(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> str:
        """Build complete URL with base URL and endpoint.

        Args:
            endpoint: API endpoint path (without leading slash).
            params: Query parameters.

        Returns:
            Complete URL string.
        """
        url = f"{self.config.base_url}/{endpoint}"

        if params is None:
            params = {}

        # Always include API key and format
        params['api_key'] = self.config.api_key
        params['format'] = self.config.default_format

        # Build query string
        if params:
            query_parts = []
            for key, value in params.items():
                if value is not None:
                    query_parts.append(f"{key}={value}")
            if query_parts:
                url += "?" + "&".join(query_parts)

        return url

    def get(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Make a GET request to the Congress API.

        Args:
            endpoint: API endpoint path (without leading slash).
            params: Additional query parameters.

        Returns:
            JSON response as dictionary.

        Raises:
            Exception: If rate limit is exceeded or API request fails.
        """
        self._check_rate_limit()

        url = self._build_url(endpoint, params)

        try:
            response = self.session.get(url, timeout=30)
            self.rate_limit_info.requests_this_hour += 1

            response.raise_for_status()

            # Check for API error responses
            if response.status_code == 429:
                self.rate_limit_info.is_rate_limited = True
                raise Exception("API rate limit exceeded")

            return response.json()

        except requests.exceptions.RequestException as e:
            raise Exception(f"API request failed: {str(e)}")

    def get_paginated(
        self,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        max_pages: int = 10
    ) -> Dict[str, Any]:
        """Make a paginated GET request to retrieve all results.

        Args:
            endpoint: API endpoint path (without leading slash).
            params: Additional query parameters.
            max_pages: Maximum number of pages to retrieve.

        Returns:
            Combined results from all pages.
        """
        if params is None:
            params = {}

        all_results = []
        offset = 0
        limit = params.get('limit', self.config.default_limit)

        while True:
            current_params = params.copy()
            current_params['offset'] = offset
            current_params['limit'] = limit

            response = self.get(endpoint, current_params)

            # Extract the main data array (different endpoints have different keys)
            data_key = self._get_data_key(endpoint)
            if data_key in response:
                page_results = response[data_key]
                all_results.extend(page_results)

                # Check if we have more pages
                if 'pagination' in response:
                    pagination = response['pagination']
                    if offset + limit >= pagination.get('count', 0):
                        break

                    # Check max pages limit
                    if len(all_results) // limit >= max_pages:
                        break
                else:
                    break
            else:
                # Single item response
                return response

            offset += limit

        # Return combined results
        result_key = self._get_result_key(endpoint)
        return {result_key: all_results}

    def _get_data_key(self, endpoint: str) -> str:
        """Get the data key for a given endpoint.

        Args:
            endpoint: API endpoint path.

        Returns:
            The key containing the data array.
        """
        if 'amendment' in endpoint:
            return 'amendments'
        elif 'bill' in endpoint:
            return 'bills'
        elif 'member' in endpoint:
            return 'members'
        else:
            return 'results'  # fallback

    def _get_result_key(self, endpoint: str) -> str:
        """Get the result key for combined paginated results.

        Args:
            endpoint: API endpoint path.

        Returns:
            The key for the combined results.
        """
        if 'amendment' in endpoint:
            return 'amendments'
        elif 'bill' in endpoint:
            return 'bills'
        elif 'member' in endpoint:
            return 'members'
        else:
            return 'results'  # fallback

    def get_rate_limit_status(self) -> RateLimitInfo:
        """Get current rate limit status.

        Returns:
            RateLimitInfo object with current status.
        """
        return self.rate_limit_info

    def reset_rate_limit(self) -> None:
        """Reset rate limiting counters.

        Useful for testing or manual reset.
        """
        self.rate_limit_info.requests_this_hour = 0
        self.rate_limit_info.hour_start_time = time.time()
        self.rate_limit_info.is_rate_limited = False
