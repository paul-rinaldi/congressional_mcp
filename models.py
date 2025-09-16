"""Pydantic models for Congress API data structures."""

from typing import List, Optional, Dict, Any, Union
from datetime import datetime
from pydantic import BaseModel, Field, HttpUrl


class Pagination(BaseModel):
    """Pagination information from API responses."""
    count: int
    next: Optional[HttpUrl] = None
    prev: Optional[HttpUrl] = None


class RequestInfo(BaseModel):
    """Request information from API responses."""
    contentType: str
    format: str


class LatestAction(BaseModel):
    """Latest action taken on an amendment."""
    actionDate: str
    text: str
    actionTime: Optional[str] = None


class Sponsor(BaseModel):
    """Sponsor information for an amendment."""
    bioguideId: str
    fullName: str
    firstName: str
    middleName: Optional[str] = None
    lastName: str
    party: str
    state: str
    district: Optional[str] = None
    url: HttpUrl


class OnBehalfOfSponsor(BaseModel):
    """Person who submitted amendment on behalf of sponsor."""
    bioguideId: str
    fullName: str
    firstName: str
    middleName: Optional[str] = None
    lastName: str
    party: str
    state: str
    type: str
    url: HttpUrl


class Cosponsor(BaseModel):
    """Cosponsor information for an amendment."""
    bioguideId: str
    fullName: str
    firstName: str
    middleName: Optional[str] = None
    lastName: str
    party: str
    state: str
    url: HttpUrl
    sponsorshipDate: str
    isOriginalCosponsor: bool
    sponsorshipWithdrawnDate: Optional[str] = None


class Cosponsors(BaseModel):
    """Container for amendment cosponsors."""
    countIncludingWithdrawnCosponsors: int
    count: int
    url: HttpUrl
    item: Optional[List[Cosponsor]] = None


class AmendedBill(BaseModel):
    """Bill that an amendment amends."""
    congress: int
    type: str
    originChamber: str
    originChamberCode: str
    number: int
    url: HttpUrl
    title: str


class AmendedAmendment(BaseModel):
    """Amendment that another amendment amends."""
    number: int
    description: Optional[str] = None
    purpose: Optional[str] = None
    congress: int
    type: str
    url: HttpUrl


class AmendmentsToAmendment(BaseModel):
    """Container for amendments to an amendment."""
    count: int
    url: HttpUrl


class SourceSystem(BaseModel):
    """Source system information for actions."""
    code: int
    name: str


class RecordedVote(BaseModel):
    """Recorded vote information."""
    rollNumber: int
    url: HttpUrl
    chamber: str
    congress: int
    date: str
    sessionNumber: int


class Committee(BaseModel):
    """Committee associated with an action."""
    url: HttpUrl
    systemCode: str
    name: str


class Action(BaseModel):
    """Action taken on an amendment."""
    actionDate: str
    actionTime: Optional[str] = None
    text: str
    type: str
    actionCode: Optional[str] = None
    sourceSystem: SourceSystem
    committees: Optional[List[Committee]] = None
    recordedVotes: Optional[List[RecordedVote]] = None


class Actions(BaseModel):
    """Container for amendment actions."""
    count: int
    url: HttpUrl
    item: Optional[List[Action]] = None


class Note(BaseModel):
    """Note attached to an amendment."""
    text: str


class Notes(BaseModel):
    """Container for amendment notes."""
    item: List[Note]


class AmendedTreaty(BaseModel):
    """Treaty that an amendment amends."""
    congress: int
    treatyNumber: int
    url: HttpUrl


class TextFormat(BaseModel):
    """Text format information."""
    type: str
    url: HttpUrl


class TextFormats(BaseModel):
    """Container for text formats."""
    item: List[TextFormat]


class TextVersion(BaseModel):
    """Text version of an amendment."""
    type: str
    date: str
    formats: TextFormats


class TextVersions(BaseModel):
    """Container for amendment text versions."""
    item: List[TextVersion]


class Amendment(BaseModel):
    """Complete amendment data structure."""
    number: int
    description: Optional[str] = None
    purpose: Optional[str] = None
    congress: int
    type: str
    chamber: Optional[str] = None
    latestAction: Optional[LatestAction] = None
    sponsors: Optional[List[Sponsor]] = None
    onBehalfOfSponsor: Optional[List[OnBehalfOfSponsor]] = None
    cosponsors: Optional[Cosponsors] = None
    proposedDate: Optional[str] = None
    submittedDate: Optional[str] = None
    amendedBill: Optional[AmendedBill] = None
    amendedAmendment: Optional[AmendedAmendment] = None
    amendmentsToAmendment: Optional[AmendmentsToAmendment] = None
    notes: Optional[Notes] = None
    amendedTreaty: Optional[AmendedTreaty] = None
    actions: Optional[Actions] = None
    textVersions: Optional[TextVersions] = None
    updateDate: Optional[str] = None
    url: Optional[HttpUrl] = None


class AmendmentsResponse(BaseModel):
    """Response containing list of amendments."""
    amendments: List[Amendment]
    pagination: Optional[Pagination] = None
    request: Optional[RequestInfo] = None


class AmendmentResponse(BaseModel):
    """Response containing single amendment details."""
    amendment: Amendment
    request: Optional[RequestInfo] = None


class ActionsResponse(BaseModel):
    """Response containing amendment actions."""
    actions: List[Action]
    pagination: Optional[Pagination] = None
    request: Optional[RequestInfo] = None


class CosponsorsResponse(BaseModel):
    """Response containing amendment cosponsors."""
    cosponsors: List[Cosponsor]
    pagination: Optional[Pagination] = None
    request: Optional[RequestInfo] = None


class TextVersionsResponse(BaseModel):
    """Response containing amendment text versions."""
    textVersions: List[TextVersion]
    pagination: Optional[Pagination] = None
    request: Optional[RequestInfo] = None


class AmendmentsToAmendmentResponse(BaseModel):
    """Response containing amendments to an amendment."""
    amendments: List[Amendment]
    pagination: Optional[Pagination] = None
    request: Optional[RequestInfo] = None


class ApiError(Exception):
    """API error exception."""
    def __init__(self, error: str, message: str, status_code: int):
        super().__init__(message)
        self.error = error
        self.message = message
        self.status_code = status_code


class ApiErrorResponse(BaseModel):
    """API error response structure."""
    error: str
    message: str
    status_code: int


# Union types for flexible response handling
AmendmentApiResponse = Union[
    AmendmentsResponse,
    AmendmentResponse,
    ActionsResponse,
    CosponsorsResponse,
    TextVersionsResponse,
    AmendmentsToAmendmentResponse,
    ApiError
]
