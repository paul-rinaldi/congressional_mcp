"""Generic services for additional Congress API endpoints."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Iterable, List, Mapping, Optional

from http_client import HttpClient


@dataclass(frozen=True)
class ResourceDefinition:
    """Metadata describing a Congress API resource."""

    name: str
    path: str
    tool_prefix: str
    description: str
    path_parameter_hint: str
    sample_path: str

    def build_description(self) -> str:
        """Human friendly description used for MCP tool definitions."""

        return (
            f"{self.description} This tool works with the `/v3/{self.path}` "
            f"endpoint. {self.path_parameter_hint}"
        )


class GenericResourceService:
    """Service capable of querying any Congress API resource."""

    def __init__(self, http_client: HttpClient, definition: ResourceDefinition):
        self._http_client = http_client
        self._definition = definition

    @property
    def definition(self) -> ResourceDefinition:
        """Return the resource definition."""

        return self._definition

    def list_resources(self, params: Optional[Mapping[str, Any]] = None) -> Dict[str, Any]:
        """List resources using optional query parameters."""

        query = self._prepare_query(params)
        return self._http_client.get(self._definition.path, query)

    def get_resource(
        self,
        path_segments: Iterable[Any],
        params: Optional[Mapping[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Retrieve a single resource using explicit path segments."""

        endpoint = self._build_endpoint(path_segments)
        return self._http_client.get(endpoint, self._prepare_query(params))

    def get_subresource(
        self,
        path_segments: Iterable[Any],
        subresource: str,
        params: Optional[Mapping[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Retrieve a nested subresource for a resource."""

        if not subresource or not subresource.strip():
            raise ValueError("subresource must be a non-empty string")

        endpoint = self._build_endpoint(path_segments, subresource=subresource)
        return self._http_client.get(endpoint, self._prepare_query(params))

    def _build_endpoint(
        self,
        path_segments: Iterable[Any],
        *,
        subresource: Optional[str] = None,
    ) -> str:
        """Construct an endpoint path from segments and optional subresource."""

        segments = [self._definition.path]

        for segment in path_segments or []:
            if segment is None:
                continue
            value = str(segment).strip("/")
            if value:
                segments.append(value)

        if subresource:
            segments.extend(part for part in subresource.split("/") if part)

        return "/".join(segments)

    @staticmethod
    def _prepare_query(params: Optional[Mapping[str, Any]]) -> Optional[Dict[str, Any]]:
        if not params:
            return None

        query: Dict[str, Any] = {}
        for key, value in params.items():
            if value is not None:
                query[key] = value
        return query or None


RESOURCE_DEFINITIONS: List[ResourceDefinition] = [
    ResourceDefinition(
        name="bill",
        path="bill",
        tool_prefix="bill",
        description="Work with bills and joint resolutions, including metadata and related content.",
        path_parameter_hint="Provide path segments as [congress, bill_type, bill_number], such as [118, 'hr', 2670].",
        sample_path="bill/118/hr/2670",
    ),
    ResourceDefinition(
        name="summaries",
        path="summaries",
        tool_prefix="summaries",
        description="Access CRS-authored bill summaries from the `/v3/summaries` collection.",
        path_parameter_hint="Provide [congress, bill_type, bill_number] to target summaries for a specific bill.",
        sample_path="summaries/118/hr/2670",
    ),
    ResourceDefinition(
        name="congress",
        path="congress",
        tool_prefix="congress",
        description="Retrieve data about individual congresses and related session metadata.",
        path_parameter_hint="Use segments such as [118] to target a single congress or append ['current'] for the latest.",
        sample_path="congress/118",
    ),
    ResourceDefinition(
        name="committee",
        path="committee",
        tool_prefix="committee",
        description="Query congressional committee information including history and membership.",
        path_parameter_hint="Segments often follow [chamber, committee_code] or [congress, chamber, committee_code], e.g., ['house', 'hsap00'].",
        sample_path="committee/house/hsap00",
    ),
    ResourceDefinition(
        name="committee-report",
        path="committee-report",
        tool_prefix="committee_report",
        description="Retrieve committee reports and related metadata or text attachments.",
        path_parameter_hint="Segments typically follow [congress, report_type, report_number], such as [118, 'hrpt', 5].",
        sample_path="committee-report/118/hrpt/5",
    ),
    ResourceDefinition(
        name="committee-print",
        path="committee-print",
        tool_prefix="committee_print",
        description="Access committee prints and supporting documents produced for hearings.",
        path_parameter_hint="Use [congress, chamber, jacket_number], for example [118, 'house', 'CPRT-118HPRT00361'].",
        sample_path="committee-print/118/house/CPRT-118HPRT00361",
    ),
    ResourceDefinition(
        name="committee-meeting",
        path="committee-meeting",
        tool_prefix="committee_meeting",
        description="Access hearings and meetings scheduled by committees.",
        path_parameter_hint="Provide [congress, chamber, event_id] to retrieve a specific meeting when available.",
        sample_path="committee-meeting/118/house/115538",
    ),
    ResourceDefinition(
        name="hearing",
        path="hearing",
        tool_prefix="hearing",
        description="Retrieve committee hearing transcripts, metadata, and witness information.",
        path_parameter_hint="Segments commonly include [congress, chamber, jacket_number].",
        sample_path="hearing/118/house/HHRG-118-II24-20230324-SD001",
    ),
    ResourceDefinition(
        name="member",
        path="member",
        tool_prefix="member",
        description="Access information about members of Congress, including biographical data and sponsored items.",
        path_parameter_hint="Use a bioguide ID such as ['A000360'] or segments like ['congress', 118, 'state', 'CA'] for rosters.",
        sample_path="member/A000360",
    ),
    ResourceDefinition(
        name="nomination",
        path="nomination",
        tool_prefix="nomination",
        description="Query presidential nominations and their status, actions, and hearing history.",
        path_parameter_hint="Segments usually follow [congress, nomination_number], such as [118, 'PN56'].",
        sample_path="nomination/118/PN56",
    ),
    ResourceDefinition(
        name="treaty",
        path="treaty",
        tool_prefix="treaty",
        description="Retrieve treaties submitted to the Senate and related actions or texts.",
        path_parameter_hint="Use [congress, treaty_number] for treaty details, for example [118, 1].",
        sample_path="treaty/118/1",
    ),
    ResourceDefinition(
        name="crsreport",
        path="crsreport",
        tool_prefix="crs_report",
        description="Fetch Congressional Research Service reports and associated metadata.",
        path_parameter_hint="Provide [report_number] such as ['R47355'] to access a specific CRS report.",
        sample_path="crsreport/R47355",
    ),
    ResourceDefinition(
        name="law",
        path="law",
        tool_prefix="law",
        description="Retrieve public and private laws, including text and related actions.",
        path_parameter_hint="Segments typically follow [congress, law_type, law_number], such as [117, 'publaw', 58].",
        sample_path="law/117/publaw/58",
    ),
    ResourceDefinition(
        name="house-communication",
        path="house-communication",
        tool_prefix="house_communication",
        description="Work with executive and agency communications received by the House.",
        path_parameter_hint="Segments commonly include [congress, communication_type, communication_number], e.g., [118, 'EC', 1].",
        sample_path="house-communication/118/EC/1",
    ),
    ResourceDefinition(
        name="senate-communication",
        path="senate-communication",
        tool_prefix="senate_communication",
        description="Access executive and presidential communications received by the Senate.",
        path_parameter_hint="Segments commonly include [congress, communication_type, communication_number], e.g., [118, 'PN', 1].",
        sample_path="senate-communication/118/PN/1",
    ),
    ResourceDefinition(
        name="house-requirement",
        path="house-requirement",
        tool_prefix="house_requirement",
        description="Inspect House communication requirements and their matching submissions.",
        path_parameter_hint="Provide [requirement_number] such as [1201] to review a specific requirement.",
        sample_path="house-requirement/1201",
    ),
    ResourceDefinition(
        name="house-vote",
        path="house-vote",
        tool_prefix="house_vote",
        description="Retrieve roll call votes published as part of the House vote beta endpoint.",
        path_parameter_hint="Segments follow [congress, session, vote_number], for example [118, 1, 5].",
        sample_path="house-vote/118/1/5",
    ),
    ResourceDefinition(
        name="congressional-record",
        path="congressional-record",
        tool_prefix="congressional_record",
        description="Work with the daily Congressional Record collection and its articles.",
        path_parameter_hint="This endpoint relies on query parameters such as fromDateTime and issue identifiers.",
        sample_path="congressional-record",
    ),
    ResourceDefinition(
        name="daily-congressional-record",
        path="daily-congressional-record",
        tool_prefix="daily_congressional_record",
        description="Browse the digitized daily Congressional Record by volume and issue number.",
        path_parameter_hint="Provide [volume_number, issue_number] like [169, '100'] for a particular issue.",
        sample_path="daily-congressional-record/169/100",
    ),
    ResourceDefinition(
        name="bound-congressional-record",
        path="bound-congressional-record",
        tool_prefix="bound_congressional_record",
        description="Access bound Congressional Record volumes organized by year, month, and day.",
        path_parameter_hint="Use [year, month, day] values such as [169, 5, 1] to reach a bound issue.",
        sample_path="bound-congressional-record/169/5/1",
    ),
]


def build_generic_services(http_client: HttpClient) -> Dict[str, GenericResourceService]:
    """Create services for each supported resource definition."""

    services: Dict[str, GenericResourceService] = {}
    for definition in RESOURCE_DEFINITIONS:
        services[definition.name] = GenericResourceService(http_client, definition)
    return services
