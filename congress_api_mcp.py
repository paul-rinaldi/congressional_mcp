#!/usr/bin/env python3
"""
Congress API MCP Server - SOLID Design Implementation

This MCP server provides access to the Congress.gov API with a focus on amendments.
It follows SOLID principles with proper separation of concerns and dependency injection.
"""

import asyncio
import json
from typing import Any, Dict, List
from mcp import Tool, types
from mcp.server import Server
from mcp.types import TextContent

from config import Config
from http_client import HttpClient
from amendment_service import AmendmentService
from resource_service import build_generic_services
from mcp_tools import (
    create_amendment_tools,
    create_generic_resource_tools,
    handle_amendment_tool,
    handle_generic_resource_tool,
)


class DependencyContainer:
    """Dependency injection container following the Dependency Inversion Principle."""

    def __init__(self):
        self._config: Config = None
        self._http_client: HttpClient = None
        self._amendment_service: AmendmentService = None
        self._resource_services = None

    def get_config(self) -> Config:
        """Get or create Config instance."""
        if self._config is None:
            self._config = Config()
        return self._config

    def get_http_client(self) -> HttpClient:
        """Get or create HttpClient instance."""
        if self._http_client is None:
            self._http_client = HttpClient(self.get_config())
        return self._http_client

    def get_amendment_service(self) -> AmendmentService:
        """Get or create AmendmentService instance."""
        if self._amendment_service is None:
            self._amendment_service = AmendmentService(self.get_http_client())
        return self._amendment_service

    def get_resource_services(self):
        """Get services for non-amendment Congress API resources."""
        if self._resource_services is None:
            self._resource_services = build_generic_services(self.get_http_client())
        return self._resource_services


class CongressApiServer:
    """Main MCP server class following Single Responsibility Principle."""

    def __init__(self, container: DependencyContainer):
        """Initialize the MCP server.

        Args:
            container: Dependency injection container.
        """
        self.container = container
        self.server = Server("congress-api-mcp")
        self.generic_tool_registry = {}
        self.amendment_tool_names = set()
        self.tools = self._create_tools()

    def _create_tools(self) -> List[Tool]:
        """Create MCP tools from amendment service operations."""
        service = self.container.get_amendment_service()
        tool_definitions = create_amendment_tools(service)
        self.amendment_tool_names = {tool["name"] for tool in tool_definitions}

        resource_services = self.container.get_resource_services()
        generic_definitions, registry = create_generic_resource_tools(resource_services)
        self.generic_tool_registry = registry

        tool_definitions.extend(generic_definitions)

        tools = []
        for tool_def in tool_definitions:
            tools.append(Tool(
                name=tool_def["name"],
                description=tool_def["description"],
                inputSchema=tool_def["inputSchema"]
            ))

        return tools

    async def handle_tool_call(
        self,
        name: str,
        arguments: Dict[str, Any]
    ) -> List[types.TextContent]:
        """Handle MCP tool calls.

        Args:
            name: Tool name.
            arguments: Tool arguments.

        Returns:
            List of text content responses.
        """
        if name in self.amendment_tool_names:
            service = self.container.get_amendment_service()
            result = await handle_amendment_tool(name, arguments, service)
        elif name in self.generic_tool_registry:
            resource_services = self.container.get_resource_services()
            result = handle_generic_resource_tool(
                name,
                arguments,
                resource_services,
                self.generic_tool_registry,
            )
        else:
            raise ValueError(f"Unknown tool: {name}")

        return [TextContent(
            type="text",
            text=result
        )]

    async def run(self):
        """Run the MCP server."""
        @self.server.list_tools()
        async def list_tools() -> List[Tool]:
            return self.tools

        @self.server.call_tool()
        async def call_tool(
            name: str,
            arguments: Dict[str, Any]
        ) -> List[types.TextContent]:
            return await self.handle_tool_call(name, arguments)

        # Run the server
        from mcp.server.stdio import stdio_server

        async with stdio_server() as (read_stream, write_stream):
            await self.server.run(
                read_stream,
                write_stream,
                self.server.create_initialization_options()
            )


def main():
    """Main entry point for the MCP server."""
    try:
        # Initialize dependency container
        container = DependencyContainer()

        # Create and run server
        server = CongressApiServer(container)

        # Run the server
        asyncio.run(server.run())

    except KeyboardInterrupt:
        print("\nServer shutdown requested by user")
    except (ValueError, TypeError, RuntimeError) as e:
        print(f"Server error: {e}")
        raise


if __name__ == "__main__":
    main()
