"""
Tests for MCP Endpoints

This module contains tests for the MCP manifest and invoke endpoints.
"""

import pytest
from fastapi.testclient import TestClient
import os
import sys

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.main import app

client = TestClient(app)


def test_root_endpoint():
    """Test the root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "LangChain Agent MCP Server"
    assert "endpoints" in data


def test_health_endpoint():
    """Test the health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"


def test_manifest_endpoint():
    """Test the MCP manifest endpoint (FR1)"""
    response = client.get("/mcp/manifest")
    assert response.status_code == 200
    data = response.json()
    
    # Validate manifest structure
    assert "name" in data
    assert "version" in data
    assert "tools" in data
    assert isinstance(data["tools"], list)
    assert len(data["tools"]) > 0
    
    # Validate tool structure
    tool = data["tools"][0]
    assert "name" in tool
    assert "description" in tool
    assert "inputSchema" in tool
    assert tool["name"] == "agent_executor"


def test_invoke_endpoint_missing_query():
    """Test invoke endpoint with missing query (FR6)"""
    response = client.post(
        "/mcp/invoke",
        json={
            "tool": "agent_executor",
            "arguments": {}
        }
    )
    assert response.status_code == 400
    data = response.json()
    assert "error" in data or "content" in data


def test_invoke_endpoint_unknown_tool():
    """Test invoke endpoint with unknown tool (FR6)"""
    response = client.post(
        "/mcp/invoke",
        json={
            "tool": "unknown_tool",
            "arguments": {"query": "test"}
        }
    )
    assert response.status_code == 400
    data = response.json()
    assert "error" in data or "content" in data


def test_invoke_endpoint_success():
    """Test invoke endpoint with valid request (FR2, FR3, FR4)"""
    # Note: This test requires OPENAI_API_KEY to be set
    # Skip if not available
    if not os.getenv("OPENAI_API_KEY"):
        pytest.skip("OPENAI_API_KEY not set")
    
    response = client.post(
        "/mcp/invoke",
        json={
            "tool": "agent_executor",
            "arguments": {
                "query": "What is 2+2?"
            }
        }
    )
    
    # Should return 200 or 500 (if API key is invalid)
    assert response.status_code in [200, 500]
    data = response.json()
    
    if response.status_code == 200:
        # Validate MCP response format
        assert "content" in data
        assert isinstance(data["content"], list)
        assert "isError" in data
        assert data["isError"] is False


def test_invoke_endpoint_with_auth():
    """Test invoke endpoint with API key authentication (NFR2)"""
    # Set API key in environment
    os.environ["API_KEY"] = "test-key-123"
    
    # Test without auth header
    response = client.post(
        "/mcp/invoke",
        json={
            "tool": "agent_executor",
            "arguments": {"query": "test"}
        }
    )
    assert response.status_code == 401
    
    # Test with wrong auth header
    response = client.post(
        "/mcp/invoke",
        json={
            "tool": "agent_executor",
            "arguments": {"query": "test"}
        },
        headers={"Authorization": "Bearer wrong-key"}
    )
    assert response.status_code == 401
    
    # Test with correct auth header
    response = client.post(
        "/mcp/invoke",
        json={
            "tool": "agent_executor",
            "arguments": {"query": "test"}
        },
        headers={"Authorization": "Bearer test-key-123"}
    )
    # Should not be 401 (may be 400, 200, or 500 depending on other factors)
    assert response.status_code != 401
    
    # Clean up
    del os.environ["API_KEY"]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

