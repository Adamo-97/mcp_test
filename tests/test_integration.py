"""
Integration Tests for MCP Multi-Server System

This module contains integration tests that verify the complete flow of:
1. Server startup and MCP handshake
2. Tool discovery from multiple servers
3. Tool execution and result validation
4. Graceful disconnection

These tests spawn actual server processes and communicate via stdio transport,
providing true end-to-end validation of the MCP implementation.
"""

import pytest
import pytest_asyncio
import sys
from contextlib import AsyncExitStack
from pathlib import Path

from src.orchestrator.main import (
    Orchestrator,
    ServerConfig,
    get_default_server_configs,
)


# ============================================================================
# Fixtures
# ============================================================================


@pytest_asyncio.fixture
async def orchestrator():
    """
    Fixture that provides a connected orchestrator instance.

    This fixture:
    1. Creates an Orchestrator as async context manager
    2. Configures it with both MCP servers
    3. Connects to all servers
    4. Yields the orchestrator for testing
    5. Cleans up automatically when exiting context
    """
    async with Orchestrator() as orch:
        for config in get_default_server_configs():
            orch.add_server(config)

        await orch.connect_all()
        yield orch


@pytest_asyncio.fixture
async def math_server_only():
    """
    Fixture that provides an orchestrator connected only to the math server.
    """
    async with Orchestrator() as orch:
        python_cmd = sys.executable
        orch.add_server(
            ServerConfig(
                name="math-server",
                command=python_cmd,
                args=["-m", "src.server_a.server"],
            )
        )

        await orch.connect_all()
        yield orch


@pytest_asyncio.fixture
async def string_server_only():
    """
    Fixture that provides an orchestrator connected only to the string server.
    """
    async with Orchestrator() as orch:
        python_cmd = sys.executable
        orch.add_server(
            ServerConfig(
                name="string-server",
                command=python_cmd,
                args=["-m", "src.server_b.server"],
            )
        )

        await orch.connect_all()
        yield orch


# ============================================================================
# Connection Tests
# ============================================================================


class TestServerConnection:
    """Tests for server connection and initialization."""

    @pytest.mark.asyncio
    async def test_connect_to_math_server(self, math_server_only: Orchestrator):
        """Verify that we can connect to Server A (Math)."""
        assert "math-server" in math_server_only.connections
        connection = math_server_only.connections["math-server"]
        assert connection.session is not None
        assert len(connection.tools) > 0

    @pytest.mark.asyncio
    async def test_connect_to_string_server(self, string_server_only: Orchestrator):
        """Verify that we can connect to Server B (String)."""
        assert "string-server" in string_server_only.connections
        connection = string_server_only.connections["string-server"]
        assert connection.session is not None
        assert len(connection.tools) > 0

    @pytest.mark.asyncio
    async def test_connect_to_both_servers(self, orchestrator: Orchestrator):
        """Verify that we can connect to both servers simultaneously."""
        assert len(orchestrator.connections) == 2
        assert "math-server" in orchestrator.connections
        assert "string-server" in orchestrator.connections


# ============================================================================
# Tool Discovery Tests
# ============================================================================


class TestToolDiscovery:
    """Tests for tool discovery functionality."""

    @pytest.mark.asyncio
    async def test_discover_math_tools(self, math_server_only: Orchestrator):
        """Verify that math tools are discovered correctly."""
        tools = math_server_only.list_all_tools()
        tool_names = [t.name for t in tools]

        assert "add" in tool_names
        assert "multiply" in tool_names

    @pytest.mark.asyncio
    async def test_discover_string_tools(self, string_server_only: Orchestrator):
        """Verify that string tools are discovered correctly."""
        tools = string_server_only.list_all_tools()
        tool_names = [t.name for t in tools]

        assert "uppercase" in tool_names
        assert "concat" in tool_names

    @pytest.mark.asyncio
    async def test_discover_all_tools(self, orchestrator: Orchestrator):
        """Verify that all tools from both servers are discovered."""
        tools = orchestrator.list_all_tools()
        tool_names = [t.name for t in tools]

        # Math tools
        assert "add" in tool_names
        assert "multiply" in tool_names

        # String tools
        assert "uppercase" in tool_names
        assert "concat" in tool_names

        # Total count
        assert len(tools) == 4

    @pytest.mark.asyncio
    async def test_tool_registry_populated(self, orchestrator: Orchestrator):
        """Verify that the tool registry correctly maps tools to servers."""
        assert orchestrator.tool_registry["add"] == "math-server"
        assert orchestrator.tool_registry["multiply"] == "math-server"
        assert orchestrator.tool_registry["uppercase"] == "string-server"
        assert orchestrator.tool_registry["concat"] == "string-server"


# ============================================================================
# Math Tool Execution Tests
# ============================================================================


class TestMathTools:
    """Tests for math tool execution."""

    @pytest.mark.asyncio
    async def test_add_positive_numbers(self, orchestrator: Orchestrator):
        """Test addition of positive integers."""
        result = await orchestrator.call_tool("add", {"a": 5, "b": 3})
        assert result == "8"

    @pytest.mark.asyncio
    async def test_add_negative_numbers(self, orchestrator: Orchestrator):
        """Test addition with negative integers."""
        result = await orchestrator.call_tool("add", {"a": -10, "b": 5})
        assert result == "-5"

    @pytest.mark.asyncio
    async def test_add_zero(self, orchestrator: Orchestrator):
        """Test addition with zero."""
        result = await orchestrator.call_tool("add", {"a": 42, "b": 0})
        assert result == "42"

    @pytest.mark.asyncio
    async def test_multiply_positive_numbers(self, orchestrator: Orchestrator):
        """Test multiplication of positive integers."""
        result = await orchestrator.call_tool("multiply", {"a": 7, "b": 6})
        assert result == "42"

    @pytest.mark.asyncio
    async def test_multiply_by_zero(self, orchestrator: Orchestrator):
        """Test multiplication by zero."""
        result = await orchestrator.call_tool("multiply", {"a": 100, "b": 0})
        assert result == "0"

    @pytest.mark.asyncio
    async def test_multiply_negative_numbers(self, orchestrator: Orchestrator):
        """Test multiplication with negative integers."""
        result = await orchestrator.call_tool("multiply", {"a": -3, "b": 4})
        assert result == "-12"


# ============================================================================
# String Tool Execution Tests
# ============================================================================


class TestStringTools:
    """Tests for string tool execution."""

    @pytest.mark.asyncio
    async def test_uppercase_simple(self, orchestrator: Orchestrator):
        """Test simple uppercase conversion."""
        result = await orchestrator.call_tool("uppercase", {"text": "hello"})
        assert result == "HELLO"

    @pytest.mark.asyncio
    async def test_uppercase_mixed_case(self, orchestrator: Orchestrator):
        """Test uppercase with mixed case input."""
        result = await orchestrator.call_tool("uppercase", {"text": "HeLLo WoRLd"})
        assert result == "HELLO WORLD"

    @pytest.mark.asyncio
    async def test_uppercase_empty_string(self, orchestrator: Orchestrator):
        """Test uppercase with empty string."""
        result = await orchestrator.call_tool("uppercase", {"text": ""})
        assert result == ""

    @pytest.mark.asyncio
    async def test_uppercase_with_numbers(self, orchestrator: Orchestrator):
        """Test uppercase with numbers (should pass through)."""
        result = await orchestrator.call_tool("uppercase", {"text": "test123"})
        assert result == "TEST123"

    @pytest.mark.asyncio
    async def test_concat_with_space(self, orchestrator: Orchestrator):
        """Test concatenation with space separator."""
        result = await orchestrator.call_tool(
            "concat", {"a": "Hello", "b": "World", "separator": " "}
        )
        assert result == "Hello World"

    @pytest.mark.asyncio
    async def test_concat_with_comma(self, orchestrator: Orchestrator):
        """Test concatenation with comma separator."""
        result = await orchestrator.call_tool(
            "concat", {"a": "First", "b": "Second", "separator": ", "}
        )
        assert result == "First, Second"

    @pytest.mark.asyncio
    async def test_concat_with_empty_separator(self, orchestrator: Orchestrator):
        """Test concatenation with empty separator."""
        result = await orchestrator.call_tool(
            "concat", {"a": "Hello", "b": "World", "separator": ""}
        )
        assert result == "HelloWorld"

    @pytest.mark.asyncio
    async def test_concat_empty_strings(self, orchestrator: Orchestrator):
        """Test concatenation of empty strings."""
        result = await orchestrator.call_tool(
            "concat", {"a": "", "b": "", "separator": "-"}
        )
        assert result == "-"


# ============================================================================
# Error Handling Tests
# ============================================================================


class TestErrorHandling:
    """Tests for error handling scenarios."""

    @pytest.mark.asyncio
    async def test_call_unknown_tool(self, orchestrator: Orchestrator):
        """Verify that calling an unknown tool raises ValueError."""
        with pytest.raises(ValueError, match="Tool 'unknown_tool' not found"):
            await orchestrator.call_tool("unknown_tool", {})

    @pytest.mark.asyncio
    async def test_add_server_duplicate_name(self):
        """Test behavior when adding servers with duplicate names."""
        orch = Orchestrator()
        config1 = ServerConfig(name="test", command="echo", args=["1"])
        config2 = ServerConfig(name="test", command="echo", args=["2"])

        orch.add_server(config1)
        orch.add_server(config2)  # Should overwrite

        # The second config should have replaced the first
        assert orch.connections["test"].config.args == ["2"]


# ============================================================================
# Integration Workflow Tests
# ============================================================================


class TestIntegrationWorkflow:
    """Tests for complete integration workflows."""

    @pytest.mark.asyncio
    async def test_full_workflow(self, orchestrator: Orchestrator):
        """
        Test a complete workflow using tools from both servers.

        Workflow:
        1. Add two numbers
        2. Multiply the result
        3. Convert the result to uppercase as a string
        4. Concatenate with a message
        """
        # Step 1: Add 10 + 5 = 15
        add_result = await orchestrator.call_tool("add", {"a": 10, "b": 5})
        assert add_result == "15"

        # Step 2: Multiply 15 * 2 = 30
        multiply_result = await orchestrator.call_tool(
            "multiply", {"a": int(add_result), "b": 2}
        )
        assert multiply_result == "30"

        # Step 3: Create a message with the result
        message = f"result: {multiply_result}"
        upper_result = await orchestrator.call_tool("uppercase", {"text": message})
        assert upper_result == "RESULT: 30"

        # Step 4: Concatenate for final output
        final_result = await orchestrator.call_tool(
            "concat", {"a": "The answer is", "b": multiply_result, "separator": " "}
        )
        assert final_result == "The answer is 30"

    @pytest.mark.asyncio
    async def test_rapid_sequential_calls(self, orchestrator: Orchestrator):
        """Test multiple rapid sequential calls to ensure stability."""
        results = []
        for i in range(10):
            result = await orchestrator.call_tool("add", {"a": i, "b": i})
            results.append(int(result))

        expected = [i * 2 for i in range(10)]
        assert results == expected

    @pytest.mark.asyncio
    async def test_alternating_server_calls(self, orchestrator: Orchestrator):
        """Test alternating calls between different servers."""
        # Math
        r1 = await orchestrator.call_tool("add", {"a": 1, "b": 2})
        assert r1 == "3"

        # String
        r2 = await orchestrator.call_tool("uppercase", {"text": "a"})
        assert r2 == "A"

        # Math
        r3 = await orchestrator.call_tool("multiply", {"a": 3, "b": 4})
        assert r3 == "12"

        # String
        r4 = await orchestrator.call_tool(
            "concat", {"a": "x", "b": "y", "separator": "-"}
        )
        assert r4 == "x-y"
