"""Service layer for Congress Amendment API operations."""

from typing import List, Optional, Dict, Any, Union
from http_client import HttpClient
from models import (
    Amendment, AmendmentsResponse, AmendmentResponse,
    ActionsResponse, CosponsorsResponse, TextVersionsResponse,
    AmendmentsToAmendmentResponse, ApiError
)


class AmendmentService:
    """Service class for Congress Amendment API operations.

    This class follows the Single Responsibility Principle by containing
    all business logic related to amendment operations.
    """

    def __init__(self, http_client: HttpClient):
        """Initialize amendment service.

        Args:
            http_client: HTTP client for API communication.
        """
        self.http_client = http_client

    def list_amendments(
        self,
        congress: Optional[int] = None,
        amendment_type: Optional[str] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None
    ) -> AmendmentsResponse:
        """List amendments with optional filtering.

        Args:
            congress: Congress number to filter by.
            amendment_type: Amendment type (HAMDT, SAMDT, SUAMDT).
            limit: Maximum number of results.
            offset: Number of results to skip.

        Returns:
            AmendmentsResponse containing list of amendments.
        """
        endpoint = "amendment"
        params = {}

        if congress:
            endpoint = f"amendment/{congress}"
            if amendment_type:
                endpoint = f"amendment/{congress}/{amendment_type}"

        if limit:
            params['limit'] = limit
        if offset:
            params['offset'] = offset

        response_data = self.http_client.get(endpoint, params)

        # Parse response into model
        try:
            return AmendmentsResponse(**response_data)
        except (ValueError, TypeError) as e:
            raise ApiError(
                error="ParseError",
                message=f"Failed to parse amendments response: {str(e)}",
                status_code=500
            )

    def get_amendment(
        self,
        congress: int,
        amendment_type: str,
        amendment_number: int
    ) -> AmendmentResponse:
        """Get detailed information about a specific amendment.

        Args:
            congress: Congress number.
            amendment_type: Amendment type (HAMDT, SAMDT, SUAMDT).
            amendment_number: Amendment number.

        Returns:
            AmendmentResponse containing amendment details.
        """
        endpoint = f"amendment/{congress}/{amendment_type}/{amendment_number}"

        response_data = self.http_client.get(endpoint)

        try:
            return AmendmentResponse(**response_data)
        except (ValueError, TypeError) as e:
            raise ApiError(
                error="ParseError",
                message=f"Failed to parse amendment response: {str(e)}",
                status_code=500
            )

    def get_amendment_actions(
        self,
        congress: int,
        amendment_type: str,
        amendment_number: int,
        limit: Optional[int] = None,
        offset: Optional[int] = None
    ) -> ActionsResponse:
        """Get actions taken on a specific amendment.

        Args:
            congress: Congress number.
            amendment_type: Amendment type.
            amendment_number: Amendment number.
            limit: Maximum number of results.
            offset: Number of results to skip.

        Returns:
            ActionsResponse containing amendment actions.
        """
        endpoint = f"amendment/{congress}/{amendment_type}/{amendment_number}/actions"
        params = {}

        if limit:
            params['limit'] = limit
        if offset:
            params['offset'] = offset

        response_data = self.http_client.get(endpoint, params)

        try:
            return ActionsResponse(**response_data)
        except (ValueError, TypeError) as e:
            raise ApiError(
                error="ParseError",
                message=f"Failed to parse actions response: {str(e)}",
                status_code=500
            )

    def get_amendment_cosponsors(
        self,
        congress: int,
        amendment_type: str,
        amendment_number: int,
        limit: Optional[int] = None,
        offset: Optional[int] = None
    ) -> CosponsorsResponse:
        """Get cosponsors of a specific amendment.

        Args:
            congress: Congress number.
            amendment_type: Amendment type.
            amendment_number: Amendment number.
            limit: Maximum number of results.
            offset: Number of results to skip.

        Returns:
            CosponsorsResponse containing amendment cosponsors.
        """
        endpoint = f"amendment/{congress}/{amendment_type}/{amendment_number}/cosponsors"
        params = {}

        if limit:
            params['limit'] = limit
        if offset:
            params['offset'] = offset

        response_data = self.http_client.get(endpoint, params)

        try:
            return CosponsorsResponse(**response_data)
        except (ValueError, TypeError) as e:
            raise ApiError(
                error="ParseError",
                message=f"Failed to parse cosponsors response: {str(e)}",
                status_code=500
            )

    def get_amendment_text(
        self,
        congress: int,
        amendment_type: str,
        amendment_number: int,
        limit: Optional[int] = None,
        offset: Optional[int] = None
    ) -> TextVersionsResponse:
        """Get text versions of a specific amendment.

        Args:
            congress: Congress number.
            amendment_type: Amendment type.
            amendment_number: Amendment number.
            limit: Maximum number of results.
            offset: Number of results to skip.

        Returns:
            TextVersionsResponse containing amendment text versions.
        """
        endpoint = f"amendment/{congress}/{amendment_type}/{amendment_number}/text"
        params = {}

        if limit:
            params['limit'] = limit
        if offset:
            params['offset'] = offset

        response_data = self.http_client.get(endpoint, params)

        try:
            return TextVersionsResponse(**response_data)
        except (ValueError, TypeError) as e:
            raise ApiError(
                error="ParseError",
                message=f"Failed to parse text versions response: {str(e)}",
                status_code=500
            )

    def get_amendments_to_amendment(
        self,
        congress: int,
        amendment_type: str,
        amendment_number: int,
        limit: Optional[int] = None,
        offset: Optional[int] = None
    ) -> AmendmentsToAmendmentResponse:
        """Get amendments to a specific amendment.

        Args:
            congress: Congress number.
            amendment_type: Amendment type.
            amendment_number: Amendment number.
            limit: Maximum number of results.
            offset: Number of results to skip.

        Returns:
            AmendmentsToAmendmentResponse containing amendments to the amendment.
        """
        endpoint = f"amendment/{congress}/{amendment_type}/{amendment_number}/amendments"
        params = {}

        if limit:
            params['limit'] = limit
        if offset:
            params['offset'] = offset

        response_data = self.http_client.get(endpoint, params)

        try:
            return AmendmentsToAmendmentResponse(**response_data)
        except (ValueError, TypeError) as e:
            raise ApiError(
                error="ParseError",
                message=f"Failed to parse amendments to amendment response: {str(e)}",
                status_code=500
            )

    def search_amendments_by_text(
        self,
        query: str,
        congress: Optional[int] = None,
        limit: Optional[int] = None
    ) -> AmendmentsResponse:
        """Search amendments by text content.

        Note: This is a simplified search that filters amendments
        based on description and purpose fields.

        Args:
            query: Search query string.
            congress: Congress number to filter by.
            limit: Maximum number of results.

        Returns:
            AmendmentsResponse containing matching amendments.
        """
        # Get all amendments and filter client-side
        # In a production system, you'd want server-side search
        amendments_response = self.list_amendments(
            congress=congress,
            limit=limit or 250  # Use higher limit for search
        )

        matching_amendments = []
        query_lower = query.lower()

        for amendment in amendments_response.amendments:
            # Search in description and purpose
            if amendment.description and query_lower in amendment.description.lower():
                matching_amendments.append(amendment)
            elif amendment.purpose and query_lower in amendment.purpose.lower():
                matching_amendments.append(amendment)

        # Return filtered results
        return AmendmentsResponse(
            amendments=matching_amendments[:limit] if limit else matching_amendments,
            pagination=amendments_response.pagination,
            request=amendments_response.request
        )

    def get_amendments_by_sponsor(
        self,
        bioguide_id: str,
        congress: Optional[int] = None,
        limit: Optional[int] = None
    ) -> AmendmentsResponse:
        """Get amendments sponsored by a specific member.

        Args:
            bioguide_id: Bioguide ID of the sponsor.
            congress: Congress number to filter by.
            limit: Maximum number of results.

        Returns:
            AmendmentsResponse containing amendments by the sponsor.
        """
        # Get all amendments and filter by sponsor
        amendments_response = self.list_amendments(
            congress=congress,
            limit=limit or 250
        )

        sponsored_amendments = []
        for amendment in amendments_response.amendments:
            if amendment.sponsors:
                for sponsor in amendment.sponsors:
                    if sponsor.bioguideId == bioguide_id:
                        sponsored_amendments.append(amendment)
                        break

        return AmendmentsResponse(
            amendments=sponsored_amendments[:limit] if limit else sponsored_amendments,
            pagination=amendments_response.pagination,
            request=amendments_response.request
        )

    def get_recent_amendments(
        self,
        congress: Optional[int] = None,
        days_back: int = 30,
        limit: Optional[int] = None
    ) -> AmendmentsResponse:
        """Get recently active amendments.

        Args:
            congress: Congress number to filter by.
            days_back: Number of days to look back.
            limit: Maximum number of results.

        Returns:
            AmendmentsResponse containing recent amendments.
        """
        from datetime import datetime, timedelta

        amendments_response = self.list_amendments(
            congress=congress,
            limit=limit or 100
        )

        cutoff_date = datetime.now() - timedelta(days=days_back)
        recent_amendments = []

        for amendment in amendments_response.amendments:
            if amendment.latestAction and amendment.latestAction.actionDate:
                try:
                    action_date = datetime.strptime(
                        amendment.latestAction.actionDate,
                        "%Y-%m-%d"
                    )
                    if action_date >= cutoff_date:
                        recent_amendments.append(amendment)
                except ValueError:
                    # Skip amendments with invalid dates
                    continue

        return AmendmentsResponse(
            amendments=recent_amendments[:limit] if limit else recent_amendments,
            pagination=amendments_response.pagination,
            request=amendments_response.request
        )
