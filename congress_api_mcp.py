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
from mcp_tools import create_amendment_tools, handle_amendment_tool


class DependencyContainer:
    """Dependency injection container following the Dependency Inversion Principle."""

    def __init__(self):
        self._config: Config = None
        self._http_client: HttpClient = None
        self._amendment_service: AmendmentService = None

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


class CongressApiServer:
    """Main MCP server class following Single Responsibility Principle."""

    def __init__(self, container: DependencyContainer):
        """Initialize the MCP server.

        Args:
            container: Dependency injection container.
        """
        self.container = container
        self.server = Server("congress-api-mcp")
        self.tools = self._create_tools()

    def _create_tools(self) -> List[Tool]:
        """Create MCP tools from amendment service operations."""
        service = self.container.get_amendment_service()
        tool_definitions = create_amendment_tools(service)

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
        service = self.container.get_amendment_service()
        result = await handle_amendment_tool(name, arguments, service)

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
