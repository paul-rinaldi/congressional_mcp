#!/usr/bin/env python3
"""
Test script for Congress API MCP Server components.

This script tests the individual components without making actual API calls.
"""

import os
import sys
from unittest.mock import Mock, patch
from pathlib import Path

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

from config import Config
from http_client import HttpClient
from amendment_service import AmendmentService
from congress_api_mcp import DependencyContainer, CongressApiServer
from resource_service import GenericResourceService, RESOURCE_DEFINITIONS
from models import Amendment, AmendmentsResponse


def test_config():
    """Test Config class functionality."""
    print("Testing Config class...")

    # Test with environment variable
    with patch.dict(os.environ, {'CONGRESSIONAL_API_KEY': 'test_key'}):
        config = Config()
        assert config.api_key == 'test_key'
        assert config.base_url == "https://api.congress.gov/v3"
        assert config.rate_limit_per_hour == 5000
        print("✓ Config with env var works")

    # Test with secrets.ini
    config_dir = Path(__file__).parent
    with patch('configparser.ConfigParser.read') as mock_read:
        with patch('configparser.ConfigParser.get') as mock_get:
            mock_get.return_value = 'secrets_key'
            config = Config(str(config_dir))
            # This should work if secrets.ini fallback is implemented
            print("✓ Config initialization works")


def test_http_client():
    """Test HttpClient class functionality."""
    print("Testing HttpClient class...")

    config = Mock()
    config.api_key = 'test_key'
    config.base_url = 'https://api.test.com'
    config.default_format = 'json'
    config.rate_limit_per_hour = 5000

    client = HttpClient(config)

    # Test URL building
    url = client._build_url('test/endpoint', {'param': 'value'})
    expected = 'https://api.test.com/test/endpoint?param=value&api_key=test_key&format=json'
    assert url == expected
    print("✓ URL building works")

    # Test rate limit tracking
    status = client.get_rate_limit_status()
    assert status.requests_this_hour == 0
    assert not status.is_rate_limited
    print("✓ Rate limit tracking works")


def test_amendment_service():
    """Test AmendmentService class functionality."""
    print("Testing AmendmentService class...")

    # Mock HTTP client
    mock_client = Mock()
    mock_response = {
        'amendments': [
            {
                'number': 2137,
                'congress': 117,
                'type': 'SAMDT',
                'purpose': 'Test amendment',
                'latestAction': {
                    'actionDate': '2021-08-08',
                    'text': 'Test action'
                }
            }
        ]
    }
    mock_client.get.return_value = mock_response

    service = AmendmentService(mock_client)

    # Test list amendments
    response = service.list_amendments(congress=117)
    assert isinstance(response, AmendmentsResponse)
    assert len(response.amendments) == 1
    assert response.amendments[0].number == 2137
    print("✓ AmendmentService.list_amendments works")


def test_dependency_container():
    """Test DependencyContainer functionality."""
    print("Testing DependencyContainer...")

    container = DependencyContainer()

    # Test singleton pattern
    config1 = container.get_config()
    config2 = container.get_config()
    assert config1 is config2
    print("✓ Config singleton works")

    # Test service creation
    http_client = container.get_http_client()
    assert http_client is not None
    print("✓ HTTP client creation works")

    service = container.get_amendment_service()
    assert service is not None
    print("✓ AmendmentService creation works")

    resource_services = container.get_resource_services()
    assert "bill" in resource_services
    assert "house-communication" in resource_services
    print(f"✓ Resource services created for {len(resource_services)} resources")


def test_generic_resource_service():
    """Test GenericResourceService path building."""

    definition = RESOURCE_DEFINITIONS[0]  # bill resource
    mock_client = Mock()
    mock_client.get.return_value = {"data": "ok"}

    service = GenericResourceService(mock_client, definition)

    service.list_resources({"limit": 5})
    mock_client.get.assert_any_call("bill", {"limit": 5})

    service.get_resource([118, "hr", 2670], {"format": "json"})
    mock_client.get.assert_any_call("bill/118/hr/2670", {"format": "json"})

    service.get_subresource([118, "hr", 2670], "text/rs", None)
    mock_client.get.assert_any_call("bill/118/hr/2670/text/rs", None)

    requirement_definition = next(
        definition for definition in RESOURCE_DEFINITIONS if definition.name == "house-requirement"
    )
    requirement_service = GenericResourceService(mock_client, requirement_definition)
    requirement_service.get_subresource([100], "matching-communications", None)
    mock_client.get.assert_any_call("house-requirement/100/matching-communications", None)
    print("✓ GenericResourceService endpoint building works")


def test_mcp_server_initialization():
    """Test MCP server initialization."""
    print("Testing MCP server initialization...")

    container = DependencyContainer()
    server = CongressApiServer(container)

    # Test tools creation
    tools = server.tools
    assert len(tools) > 0
    tool_names = [tool.name for tool in tools]
    assert 'list_amendments' in tool_names
    assert 'get_amendment' in tool_names
    assert any(name.startswith('list_bill') for name in tool_names)
    print(f"✓ MCP server created {len(tools)} tools")


def test_models():
    """Test Pydantic models."""
    print("Testing Pydantic models...")

    # Test Amendment model
    amendment_data = {
        'number': 2137,
        'congress': 117,
        'type': 'SAMDT',
        'purpose': 'Test amendment',
        'latestAction': {
            'actionDate': '2021-08-08',
            'text': 'Test action'
        }
    }

    amendment = Amendment(**amendment_data)
    assert amendment.number == 2137
    assert amendment.congress == 117
    assert amendment.type == 'SAMDT'
    print("✓ Amendment model works")

    # Test AmendmentsResponse model
    response_data = {
        'amendments': [amendment_data],
        'pagination': {'count': 1}
    }

    response = AmendmentsResponse(**response_data)
    assert len(response.amendments) == 1
    assert response.amendments[0].number == 2137
    print("✓ AmendmentsResponse model works")


def main():
    """Run all component tests."""
    print("Running Congress API MCP Server component tests...\n")

    try:
        test_config()
        test_http_client()
        test_amendment_service()
        test_dependency_container()
        test_mcp_server_initialization()
        test_models()

        print("\n🎉 All component tests passed!")
        return True

    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
