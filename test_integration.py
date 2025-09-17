#!/usr/bin/env python3
"""
Integration test for Congress API MCP Server.

This script tests the complete MCP server with real API calls.
Requires a valid CONGRESSIONAL_API_KEY to be set.
"""

import os
import sys
import json
import configparser
from pathlib import Path
from typing import Optional
from unittest.mock import patch

import pytest

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

from congress_api_mcp import DependencyContainer, CongressApiServer


def _lookup_api_key() -> Optional[str]:
    """Try to locate an API key from the environment or secrets.ini."""

    api_key = os.getenv("CONGRESSIONAL_API_KEY")
    if api_key:
        return api_key

    config = configparser.ConfigParser()
    secrets_path = Path(__file__).parent / "api_client" / "secrets.ini"
    if secrets_path.exists():
        config.read(secrets_path)
        if config.has_section("cdg_api"):
            secret_key = config.get("cdg_api", "api_auth_key", fallback=None)
            if secret_key and secret_key != "PASTE_KEY_HERE":
                return secret_key

    return None


def test_api_key_available():
    """Check if API key is available for testing."""

    api_key = _lookup_api_key()
    if api_key is None:
        pytest.skip("CONGRESSIONAL_API_KEY not configured for live API tests")

    assert api_key


def test_server_initialization():
    """Test that the server can be initialized."""

    container = DependencyContainer()
    server = CongressApiServer(container)

    tools = server.tools
    assert tools, "expected server to expose at least one tool"

    tool_names = {tool.name for tool in tools}
    assert "list_amendments" in tool_names
    assert "list_bill" in tool_names
    assert "list_house_communication" in tool_names


def test_api_connectivity():
    """Exercise a real API request when credentials are available."""

    api_key = _lookup_api_key()
    if api_key is None:
        pytest.skip("CONGRESSIONAL_API_KEY not configured for live API tests")

    container = DependencyContainer()
    service = container.get_amendment_service()

    try:
        response = service.list_amendments(limit=1)
    except Exception as exc:  # pragma: no cover - network/credential guard
        pytest.skip(f"Live API request failed: {exc}")
    assert response.amendments, "expected at least one amendment from live API"
    first_amendment = response.amendments[0]
    assert first_amendment.number is not None

@pytest.fixture
def anyio_backend():
    return "asyncio"


@pytest.mark.anyio("asyncio")
async def test_tool_execution_async():
    """Test tool execution with mock data across endpoints."""

    await _exercise_tool_flow()


def test_tool_execution():
    """Sync wrapper that reuses the async tool execution flow."""
    import asyncio

    asyncio.run(_exercise_tool_flow())


async def _exercise_tool_flow():
    with patch.dict(os.environ, {"CONGRESSIONAL_API_KEY": "test_key"}):
        with patch("http_client.HttpClient.get") as mock_get:
            def _fake_get(endpoint, params=None):
                if endpoint.startswith("amendment"):
                    return {
                        "amendments": [
                            {
                                "number": 1,
                                "congress": 118,
                                "type": "SAMDT",
                                "description": "Test amendment",
                            }
                        ],
                        "pagination": {"count": 1}
                    }
                if endpoint == "bill":
                    return {"bills": [{"congress": 118, "type": "hr", "number": 2670}]}
                if endpoint == "bill/118/hr/2670":
                    return {"bill": {"title": "Test Bill"}}
                if endpoint.startswith("bill/118/hr/2670/text"):
                    return {"textVersions": []}
                if endpoint == "house-requirement":
                    return {"houseRequirements": [{"requirementNumber": 100}]}
                if endpoint == "house-requirement/100":
                    return {"houseRequirement": {"requirementNumber": 100}}
                if endpoint == "house-requirement/100/matching-communications":
                    return {"matchingCommunications": []}
                return {"results": []}

            mock_get.side_effect = _fake_get

            container = DependencyContainer()
            server = CongressApiServer(container)

            result = await server.handle_tool_call("list_amendments", {"limit": 1})
            assert len(result) == 1
            amendment_payload = json.loads(result[0].text)
            assert amendment_payload["amendments"][0]["number"] == 1

            list_bill_result = await server.handle_tool_call("list_bill", {"params": {"limit": 1}})
            bill_payload = json.loads(list_bill_result[0].text)
            assert "bills" in bill_payload

            subresource_result = await server.handle_tool_call(
                "get_bill_subresource",
                {
                    "path_segments": [118, "hr", 2670],
                    "subresource": "text"
                }
            )
            text_payload = json.loads(subresource_result[0].text)
            assert "textVersions" in text_payload

            house_requirement_detail = await server.handle_tool_call(
                "get_house_requirement",
                {"path_segments": [100]}
            )
            requirement_payload = json.loads(house_requirement_detail[0].text)
            assert requirement_payload["houseRequirement"]["requirementNumber"] == 100

            requirement_subresource = await server.handle_tool_call(
                "get_house_requirement_subresource",
                {
                    "path_segments": [100],
                    "subresource": "matching-communications"
                }
            )
            requirement_matches = json.loads(requirement_subresource[0].text)
            assert "matchingCommunications" in requirement_matches


def create_usage_example():
    """Create an example of how to use the MCP server."""
    example = '''
# Example usage of Congress API MCP Server

## Available Tools

1. **list_amendments** - List amendments with optional filtering
   Parameters: congress, amendment_type, limit, offset

2. **get_amendment** - Get detailed information about a specific amendment
   Parameters: congress, amendment_type, amendment_number (required)

3. **get_amendment_actions** - Get all actions taken on an amendment
   Parameters: congress, amendment_type, amendment_number, limit, offset

4. **get_amendment_cosponsors** - Get cosponsors of an amendment
   Parameters: congress, amendment_type, amendment_number, limit, offset

5. **get_amendment_text** - Get text versions of an amendment
   Parameters: congress, amendment_type, amendment_number, limit, offset

6. **get_amendments_to_amendment** - Get amendments that amend another amendment
   Parameters: congress, amendment_type, amendment_number, limit, offset

7. **search_amendments** - Search amendments by text content
   Parameters: query (required), congress, limit

8. **get_amendments_by_sponsor** - Get amendments by a specific sponsor
   Parameters: bioguide_id (required), congress, limit

9. **get_recent_amendments** - Get recently active amendments
   Parameters: congress, days_back, limit

## Example MCP Tool Call

```json
{
  "method": "tools/call",
  "params": {
    "name": "get_amendment",
    "arguments": {
      "congress": 117,
      "amendment_type": "SAMDT",
      "amendment_number": 2137
    }
  }
}
```
'''
    return example


def main():
    """Run integration tests."""
    print("Running Congress API MCP Server integration tests...\n")

    tests_passed = 0
    total_tests = 4

    # Test 1: Server initialization
    if test_server_initialization():
        tests_passed += 1
    print()

    # Test 2: API connectivity
    if test_api_connectivity():
        tests_passed += 1
    print()

    # Test 3: Tool execution
    if test_tool_execution():
        tests_passed += 1
    print()

    # Test 4: Create usage documentation
    print("Creating usage documentation...")
    usage_example = create_usage_example()
    print("✓ Usage documentation created")
    tests_passed += 1
    print()

    # Summary
    print(f"Integration test results: {tests_passed}/{total_tests} tests passed")

    if tests_passed == total_tests:
        print("🎉 All integration tests passed!")
        print("\n" + "="*60)
        print("Congress API MCP Server is ready to use!")
        print("="*60)
        print(usage_example)
    else:
        print("❌ Some integration tests failed")

    return tests_passed == total_tests


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
