"""MCP tools for Congress Amendment API operations."""

import json
from typing import Any, Dict, List, Optional
from amendment_service import AmendmentService
from models import ApiError, ApiErrorResponse


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
