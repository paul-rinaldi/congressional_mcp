"""MCP tools for Congress Amendment API operations."""

import json
from typing import Any, Dict, List, Optional, Tuple

from amendment_service import AmendmentService
from models import ApiError, ApiErrorResponse
from resource_service import GenericResourceService


def create_amendment_tools(service: AmendmentService) -> List[Dict[str, Any]]:
    """Create MCP tools for amendment operations.

    Args:
        service: AmendmentService instance.

    Returns:
        List of MCP tool definitions.
    """
    return [
        {
            "name": "list_amendments",
            "description": "List amendments with optional filtering by congress and type",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "congress": {
                        "type": "integer",
                        "description": "Congress number (e.g., 117)"
                    },
                    "amendment_type": {
                        "type": "string",
                        "enum": ["HAMDT", "SAMDT", "SUAMDT"],
                        "description": "Amendment type: HAMDT (House), SAMDT (Senate), SUAMDT (Senate - old)"
                    },
                    "limit": {
                        "type": "integer",
                        "minimum": 1,
                        "maximum": 250,
                        "default": 20,
                        "description": "Maximum number of results (1-250)"
                    },
                    "offset": {
                        "type": "integer",
                        "minimum": 0,
                        "default": 0,
                        "description": "Number of results to skip"
                    }
                },
                "required": []
            }
        },
        {
            "name": "get_amendment",
            "description": "Get detailed information about a specific amendment",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "congress": {
                        "type": "integer",
                        "description": "Congress number (e.g., 117)"
                    },
                    "amendment_type": {
                        "type": "string",
                        "enum": ["HAMDT", "SAMDT", "SUAMDT"],
                        "description": "Amendment type: HAMDT (House), SAMDT (Senate), SUAMDT (Senate - old)"
                    },
                    "amendment_number": {
                        "type": "integer",
                        "description": "Amendment number (e.g., 2137)"
                    }
                },
                "required": ["congress", "amendment_type", "amendment_number"]
            }
        },
        {
            "name": "get_amendment_actions",
            "description": "Get all actions taken on a specific amendment",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "congress": {
                        "type": "integer",
                        "description": "Congress number (e.g., 117)"
                    },
                    "amendment_type": {
                        "type": "string",
                        "enum": ["HAMDT", "SAMDT", "SUAMDT"],
                        "description": "Amendment type"
                    },
                    "amendment_number": {
                        "type": "integer",
                        "description": "Amendment number"
                    },
                    "limit": {
                        "type": "integer",
                        "minimum": 1,
                        "maximum": 250,
                        "default": 20,
                        "description": "Maximum number of results"
                    },
                    "offset": {
                        "type": "integer",
                        "minimum": 0,
                        "default": 0,
                        "description": "Number of results to skip"
                    }
                },
                "required": ["congress", "amendment_type", "amendment_number"]
            }
        },
        {
            "name": "get_amendment_cosponsors",
            "description": "Get cosponsors of a specific amendment",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "congress": {
                        "type": "integer",
                        "description": "Congress number"
                    },
                    "amendment_type": {
                        "type": "string",
                        "enum": ["HAMDT", "SAMDT", "SUAMDT"],
                        "description": "Amendment type"
                    },
                    "amendment_number": {
                        "type": "integer",
                        "description": "Amendment number"
                    },
                    "limit": {
                        "type": "integer",
                        "minimum": 1,
                        "maximum": 250,
                        "default": 20,
                        "description": "Maximum number of results"
                    },
                    "offset": {
                        "type": "integer",
                        "minimum": 0,
                        "default": 0,
                        "description": "Number of results to skip"
                    }
                },
                "required": ["congress", "amendment_type", "amendment_number"]
            }
        },
        {
            "name": "get_amendment_text",
            "description": "Get text versions of a specific amendment",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "congress": {
                        "type": "integer",
                        "description": "Congress number"
                    },
                    "amendment_type": {
                        "type": "string",
                        "enum": ["HAMDT", "SAMDT", "SUAMDT"],
                        "description": "Amendment type"
                    },
                    "amendment_number": {
                        "type": "integer",
                        "description": "Amendment number"
                    },
                    "limit": {
                        "type": "integer",
                        "minimum": 1,
                        "maximum": 250,
                        "default": 20,
                        "description": "Maximum number of results"
                    },
                    "offset": {
                        "type": "integer",
                        "minimum": 0,
                        "default": 0,
                        "description": "Number of results to skip"
                    }
                },
                "required": ["congress", "amendment_type", "amendment_number"]
            }
        },
        {
            "name": "get_amendments_to_amendment",
            "description": "Get amendments that amend a specific amendment",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "congress": {
                        "type": "integer",
                        "description": "Congress number"
                    },
                    "amendment_type": {
                        "type": "string",
                        "enum": ["HAMDT", "SAMDT", "SUAMDT"],
                        "description": "Amendment type"
                    },
                    "amendment_number": {
                        "type": "integer",
                        "description": "Amendment number"
                    },
                    "limit": {
                        "type": "integer",
                        "minimum": 1,
                        "maximum": 250,
                        "default": 20,
                        "description": "Maximum number of results"
                    },
                    "offset": {
                        "type": "integer",
                        "minimum": 0,
                        "default": 0,
                        "description": "Number of results to skip"
                    }
                },
                "required": ["congress", "amendment_type", "amendment_number"]
            }
        },
        {
            "name": "search_amendments",
            "description": "Search amendments by text content in description or purpose",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Search query string"
                    },
                    "congress": {
                        "type": "integer",
                        "description": "Congress number to filter by"
                    },
                    "limit": {
                        "type": "integer",
                        "minimum": 1,
                        "maximum": 250,
                        "default": 20,
                        "description": "Maximum number of results"
                    }
                },
                "required": ["query"]
            }
        },
        {
            "name": "get_amendments_by_sponsor",
            "description": "Get amendments sponsored by a specific member",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "bioguide_id": {
                        "type": "string",
                        "description": "Bioguide ID of the sponsor (e.g., S001191)"
                    },
                    "congress": {
                        "type": "integer",
                        "description": "Congress number to filter by"
                    },
                    "limit": {
                        "type": "integer",
                        "minimum": 1,
                        "maximum": 250,
                        "default": 20,
                        "description": "Maximum number of results"
                    }
                },
                "required": ["bioguide_id"]
            }
        },
        {
            "name": "get_recent_amendments",
            "description": "Get recently active amendments",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "congress": {
                        "type": "integer",
                        "description": "Congress number to filter by"
                    },
                    "days_back": {
                        "type": "integer",
                        "minimum": 1,
                        "maximum": 365,
                        "default": 30,
                        "description": "Number of days to look back"
                    },
                    "limit": {
                        "type": "integer",
                        "minimum": 1,
                        "maximum": 250,
                        "default": 20,
                        "description": "Maximum number of results"
                    }
                },
                "required": []
            }
        }
    ]


async def handle_amendment_tool(
    tool_name: str,
    arguments: Dict[str, Any],
    service: AmendmentService
) -> str:
    """Handle MCP tool calls for amendment operations.

    Args:
        tool_name: Name of the tool being called.
        arguments: Tool arguments.
        service: AmendmentService instance.

    Returns:
        JSON string response.
    """
    try:
        if tool_name == "list_amendments":
            response = service.list_amendments(
                congress=arguments.get("congress"),
                amendment_type=arguments.get("amendment_type"),
                limit=arguments.get("limit"),
                offset=arguments.get("offset")
            )
            return json.dumps(response.model_dump(), indent=2, default=str)

        elif tool_name == "get_amendment":
            response = service.get_amendment(
                congress=arguments["congress"],
                amendment_type=arguments["amendment_type"],
                amendment_number=arguments["amendment_number"]
            )
            return json.dumps(response.model_dump(), indent=2, default=str)

        elif tool_name == "get_amendment_actions":
            response = service.get_amendment_actions(
                congress=arguments["congress"],
                amendment_type=arguments["amendment_type"],
                amendment_number=arguments["amendment_number"],
                limit=arguments.get("limit"),
                offset=arguments.get("offset")
            )
            return json.dumps(response.model_dump(), indent=2, default=str)

        elif tool_name == "get_amendment_cosponsors":
            response = service.get_amendment_cosponsors(
                congress=arguments["congress"],
                amendment_type=arguments["amendment_type"],
                amendment_number=arguments["amendment_number"],
                limit=arguments.get("limit"),
                offset=arguments.get("offset")
            )
            return json.dumps(response.model_dump(), indent=2, default=str)

        elif tool_name == "get_amendment_text":
            response = service.get_amendment_text(
                congress=arguments["congress"],
                amendment_type=arguments["amendment_type"],
                amendment_number=arguments["amendment_number"],
                limit=arguments.get("limit"),
                offset=arguments.get("offset")
            )
            return json.dumps(response.model_dump(), indent=2, default=str)

        elif tool_name == "get_amendments_to_amendment":
            response = service.get_amendments_to_amendment(
                congress=arguments["congress"],
                amendment_type=arguments["amendment_type"],
                amendment_number=arguments["amendment_number"],
                limit=arguments.get("limit"),
                offset=arguments.get("offset")
            )
            return json.dumps(response.model_dump(), indent=2, default=str)

        elif tool_name == "search_amendments":
            response = service.search_amendments_by_text(
                query=arguments["query"],
                congress=arguments.get("congress"),
                limit=arguments.get("limit")
            )
            return json.dumps(response.model_dump(), indent=2, default=str)

        elif tool_name == "get_amendments_by_sponsor":
            response = service.get_amendments_by_sponsor(
                bioguide_id=arguments["bioguide_id"],
                congress=arguments.get("congress"),
                limit=arguments.get("limit")
            )
            return json.dumps(response.model_dump(), indent=2, default=str)

        elif tool_name == "get_recent_amendments":
            response = service.get_recent_amendments(
                congress=arguments.get("congress"),
                days_back=arguments.get("days_back", 30),
                limit=arguments.get("limit")
            )
            return json.dumps(response.model_dump(), indent=2, default=str)

        else:
            raise ValueError(f"Unknown tool: {tool_name}")

    except ApiError as e:
        error_response = ApiErrorResponse(
            error=e.error,
            message=e.message,
            status_code=e.status_code
        )
        return json.dumps(error_response.model_dump(), indent=2)
    except (ValueError, TypeError, KeyError) as e:
        error_response = ApiErrorResponse(
            error="ValidationError",
            message=f"Invalid input or response format: {str(e)}",
            status_code=400
        )
        return json.dumps(error_response.model_dump(), indent=2)
    except Exception as e:
        error_response = ApiErrorResponse(
            error="InternalError",
            message=f"An unexpected error occurred: {str(e)}",
            status_code=500
        )
        return json.dumps(error_response.model_dump(), indent=2)


def create_generic_resource_tools(
    resource_services: Dict[str, GenericResourceService]
) -> Tuple[List[Dict[str, Any]], Dict[str, Dict[str, str]]]:
    """Create tools for additional Congress API resources."""

    tools: List[Dict[str, Any]] = []
    registry: Dict[str, Dict[str, str]] = {}

    for resource_name, service in resource_services.items():
        definition = service.definition
        prefix = definition.tool_prefix
        sample_segments = _extract_sample_segments(definition.sample_path)
        segments_hint = (
            f"Example path segments: {sample_segments} derived from `{definition.sample_path}`."
            if sample_segments
            else ""
        )

        list_tool_name = f"list_{prefix}"
        tools.append({
            "name": list_tool_name,
            "description": definition.build_description(),
            "inputSchema": {
                "type": "object",
                "properties": {
                    "params": _params_schema(
                        "Optional query parameters to include in the request."
                    )
                },
                "required": []
            }
        })
        registry[list_tool_name] = {"resource": resource_name, "action": "list"}

        detail_tool_name = f"get_{prefix}"
        tools.append({
            "name": detail_tool_name,
            "description": (
                f"Retrieve a specific record from the `/v3/{definition.path}` endpoint. "
                f"{definition.path_parameter_hint} {segments_hint}"
            ).strip(),
            "inputSchema": {
                "type": "object",
                "properties": {
                    "path_segments": _path_segments_schema(
                        "Ordered path segments identifying the record.",
                        minimum=1,
                        example=sample_segments
                    ),
                    "params": _params_schema(
                        "Optional query parameters such as `format` overrides or pagination."
                    )
                },
                "required": ["path_segments"]
            }
        })
        registry[detail_tool_name] = {"resource": resource_name, "action": "detail"}

        sub_tool_name = f"get_{prefix}_subresource"
        tools.append({
            "name": sub_tool_name,
            "description": (
                "Access a nested path beneath a resource, such as actions, text versions, or related data. "
                f"Start with the same path segments used by `{detail_tool_name}` and provide a `subresource` path."
            ),
            "inputSchema": {
                "type": "object",
                "properties": {
                    "path_segments": _path_segments_schema(
                        "Ordered path segments to the parent resource.",
                        minimum=0,
                        example=sample_segments
                    ),
                    "subresource": {
                        "type": "string",
                        "description": "Additional path component(s) appended after the parent resource, e.g., 'text', 'actions', or 'summaries/latest'."
                    },
                    "params": _params_schema(
                        "Optional query parameters to include in the request."
                    )
                },
                "required": ["subresource"]
            }
        })
        registry[sub_tool_name] = {"resource": resource_name, "action": "subresource"}

    return tools, registry


def handle_generic_resource_tool(
    tool_name: str,
    arguments: Dict[str, Any],
    resource_services: Dict[str, GenericResourceService],
    registry: Dict[str, Dict[str, str]]
) -> str:
    """Handle dynamic tool calls for non-amendment resources."""

    if tool_name not in registry:
        raise ValueError(f"Unknown tool: {tool_name}")

    registration = registry[tool_name]
    service = resource_services[registration["resource"]]
    action = registration["action"]

    try:
        params = _validate_params(arguments.get("params"))

        if action == "list":
            response = service.list_resources(params)
        elif action == "detail":
            segments = _normalize_segments(arguments.get("path_segments"))
            if not segments:
                raise ValueError("path_segments must contain at least one value")
            response = service.get_resource(segments, params)
        elif action == "subresource":
            segments = _normalize_segments(arguments.get("path_segments", []))
            subresource = arguments.get("subresource")
            if not isinstance(subresource, str) or not subresource.strip():
                raise ValueError("subresource must be a non-empty string")
            response = service.get_subresource(segments, subresource, params)
        else:
            raise ValueError(f"Unsupported action: {action}")

        return json.dumps(response, indent=2, default=str)

    except (ValueError, TypeError, KeyError) as exc:
        error_response = ApiErrorResponse(
            error="ValidationError",
            message=f"Invalid input: {exc}",
            status_code=400
        )
        return json.dumps(error_response.model_dump(), indent=2)
    except Exception as exc:  # pragma: no cover - defensive catch
        error_response = ApiErrorResponse(
            error="InternalError",
            message=f"An unexpected error occurred: {exc}",
            status_code=500
        )
        return json.dumps(error_response.model_dump(), indent=2)


def _path_segments_schema(description: str, *, minimum: int, example: Optional[List[str]] = None) -> Dict[str, Any]:
    schema: Dict[str, Any] = {
        "type": "array",
        "description": description,
        "items": {
            "oneOf": [
                {"type": "string"},
                {"type": "integer"},
                {"type": "number"}
            ]
        },
        "minItems": minimum,
    }
    if example:
        schema["examples"] = [example]
    return schema


def _params_schema(description: str) -> Dict[str, Any]:
    return {
        "type": "object",
        "description": description,
        "additionalProperties": {
            "oneOf": [
                {"type": "string"},
                {"type": "number"},
                {"type": "boolean"}
            ]
        }
    }


def _extract_sample_segments(sample_path: str) -> List[str]:
    if not sample_path:
        return []
    parts = [segment for segment in sample_path.split("/") if segment]
    return parts[1:] if len(parts) > 1 else []


def _normalize_segments(value: Optional[Any]) -> List[str]:
    if value is None:
        return []
    if not isinstance(value, list):
        raise TypeError("path_segments must be provided as a list")
    normalized: List[str] = []
    for segment in value:
        if segment is None:
            continue
        normalized.append(str(segment))
    return normalized


def _validate_params(value: Optional[Any]) -> Optional[Dict[str, Any]]:
    if value is None:
        return None
    if not isinstance(value, dict):
        raise TypeError("params must be an object/dictionary")
    return value
