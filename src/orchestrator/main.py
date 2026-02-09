#!/usr/bin/env python3
"""
Orchestrator - MCP Multi-Server Client

This module implements an MCP client that connects to multiple servers,
discovers their tools, and executes them in a coordinated workflow.

Key concepts demonstrated:
1. Spawning MCP server processes
2. Establishing MCP client sessions
3. Tool discovery across multiple servers
4. Tool execution and result aggregation
5. Clean async/await patterns with proper resource management
"""

import asyncio
import sys
from contextlib import AsyncExitStack
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from mcp.types import Tool


@dataclass
class ServerConfig:
    """
    Configuration for an MCP server connection.

    Attributes:
        name: Human-readable identifier for this server
        command: The command to execute (e.g., "python")
        args: Command line arguments (e.g., ["-m", "src.server_a.server"])
        env: Optional environment variables
    """

    name: str
    command: str
    args: list[str]
    env: dict[str, str] | None = None


@dataclass
class ToolInfo:
    """
    Information about a discovered tool.

    Attributes:
        name: Tool identifier
        description: Human-readable description
        server_name: Name of the server that provides this tool
        input_schema: JSON Schema for the tool's parameters
    """

    name: str
    description: str
    server_name: str
    input_schema: dict[str, Any]


@dataclass
class MCPConnection:
    """
    Represents an active connection to an MCP server.

    This class manages the lifecycle of a server connection,
    including the subprocess and MCP session.

    Attributes:
        config: Server configuration
        session: Active MCP client session (set after connect)
        tools: List of tools discovered from this server
    """

    config: ServerConfig
    session: ClientSession | None = None
    tools: list[Tool] = field(default_factory=list)

    async def connect(self) -> None:
        """
        Establish connection to the MCP server.

        This spawns the server process and performs the MCP handshake.
        After this method completes, the session is ready for tool calls.
        """
        # Note: In a real implementation, we'd store the context managers
        # For this demo, we use a simpler pattern with the orchestrator
        pass

    async def disconnect(self) -> None:
        """
        Close the connection to the MCP server.

        This gracefully shuts down the session and terminates the subprocess.
        """
        self.session = None
        self.tools = []


class Orchestrator:
    """
    Central coordinator for multi-server MCP operations.

    The Orchestrator manages connections to multiple MCP servers,
    provides unified tool discovery, and routes tool calls to
    the appropriate server.

    Example usage:
        async with Orchestrator() as orchestrator:
            orchestrator.add_server(ServerConfig(...))
            await orchestrator.connect_all()
            result = await orchestrator.call_tool("add", {"a": 5, "b": 3})

    Attributes:
        connections: Dictionary mapping server names to their connections
        tool_registry: Dictionary mapping tool names to their source server
    """

    def __init__(self) -> None:
        """Initialize the Orchestrator with empty connection registry."""
        self.connections: dict[str, MCPConnection] = {}
        self.tool_registry: dict[str, str] = {}  # tool_name -> server_name
        self._exit_stack: AsyncExitStack | None = None

    async def __aenter__(self) -> "Orchestrator":
        """Enter async context - initialize the exit stack."""
        self._exit_stack = AsyncExitStack()
        await self._exit_stack.__aenter__()
        return self

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        """Exit async context - cleanup all connections."""
        if self._exit_stack:
            try:
                await self._exit_stack.__aexit__(exc_type, exc_val, exc_tb)
            except RuntimeError as e:
                # anyio cancel scope errors happen when exiting in a different
                # task context (common in pytest-asyncio). The connections are
                # still properly terminated when the subprocess pipes close.
                if "cancel scope" not in str(e).lower():
                    raise
        self.tool_registry.clear()
        for connection in self.connections.values():
            connection.session = None
            connection.tools = []

    def add_server(self, config: ServerConfig) -> None:
        """
        Register a server configuration for later connection.

        Args:
            config: Server configuration including command and arguments
        """
        self.connections[config.name] = MCPConnection(config=config)

    async def connect_to_server(self, server_name: str) -> None:
        """
        Connect to a specific server and discover its tools.

        Args:
            server_name: Name of the server to connect to

        Raises:
            KeyError: If the server name is not registered
        """
        if not self._exit_stack:
            raise RuntimeError("Orchestrator must be used as async context manager")

        connection = self.connections[server_name]
        config = connection.config

        # Create server parameters for stdio transport
        server_params = StdioServerParameters(
            command=config.command, args=config.args, env=config.env
        )

        # Establish the connection using stdio transport with exit stack
        stdio_transport = stdio_client(server_params)
        read, write = await self._exit_stack.enter_async_context(stdio_transport)

        session = ClientSession(read, write)
        await self._exit_stack.enter_async_context(session)

        # Perform the MCP initialization handshake
        await session.initialize()

        # Store the session
        connection.session = session

        # Discover available tools
        tools_response = await session.list_tools()
        connection.tools = tools_response.tools

        # Register tools in our registry
        for tool in connection.tools:
            self.tool_registry[tool.name] = server_name

    async def connect_all(self) -> None:
        """
        Connect to all registered servers.

        This method connects to each server sequentially and discovers
        their tools. After completion, all tools are available for execution.
        """
        for server_name in self.connections:
            await self.connect_to_server(server_name)

    async def disconnect_all(self) -> None:
        """
        Disconnect from all servers gracefully.

        Note: When using Orchestrator as async context manager (recommended),
        cleanup is automatic. This method is provided for manual cleanup
        in non-context-manager usage patterns.
        """
        # Clear registries
        self.tool_registry.clear()

        # Clear connection sessions
        for connection in self.connections.values():
            connection.session = None
            connection.tools = []

    def list_all_tools(self) -> list[ToolInfo]:
        """
        Get a list of all available tools from all connected servers.

        Returns:
            List of ToolInfo objects with tool metadata
        """
        tools: list[ToolInfo] = []
        for connection in self.connections.values():
            for tool in connection.tools:
                tools.append(
                    ToolInfo(
                        name=tool.name,
                        description=tool.description or "",
                        server_name=connection.config.name,
                        input_schema=tool.inputSchema,
                    )
                )
        return tools

    async def call_tool(self, tool_name: str, arguments: dict[str, Any]) -> str:
        """
        Execute a tool by name on the appropriate server.

        This method routes the tool call to the server that provides it.

        Args:
            tool_name: Name of the tool to execute
            arguments: Dictionary of arguments to pass to the tool

        Returns:
            The tool's result as a string

        Raises:
            ValueError: If the tool is not found in any server
        """
        if tool_name not in self.tool_registry:
            raise ValueError(f"Tool '{tool_name}' not found in any server")

        server_name = self.tool_registry[tool_name]
        connection = self.connections[server_name]

        if connection.session is None:
            raise RuntimeError(f"Not connected to server '{server_name}'")

        # Execute the tool call
        result = await connection.session.call_tool(tool_name, arguments)

        # Extract text content from the result
        if result.content:
            return result.content[0].text
        return ""


def get_default_server_configs() -> list[ServerConfig]:
    """
    Get the default server configurations for this project.

    Returns:
        List of ServerConfig for Server A and Server B
    """
    # Determine the Python executable path
    python_cmd = sys.executable

    return [
        ServerConfig(
            name="math-server", command=python_cmd, args=["-m", "src.server_a.server"]
        ),
        ServerConfig(
            name="string-server", command=python_cmd, args=["-m", "src.server_b.server"]
        ),
    ]


async def run_demo() -> None:
    """
    Run a demonstration of the multi-server orchestration.

    This function:
    1. Creates an orchestrator
    2. Connects to both MCP servers
    3. Lists all available tools
    4. Executes a sample workflow
    5. Displays the results
    """
    print("=" * 60)
    print("MCP Multi-Server Orchestration Demo")
    print("=" * 60)

    # Create and configure the orchestrator using async context manager
    async with Orchestrator() as orchestrator:
        for config in get_default_server_configs():
            orchestrator.add_server(config)

        # Connect to all servers
        print("\n[1] Connecting to MCP servers...")
        await orchestrator.connect_all()
        print("    Connected to all servers")

        # List available tools
        print("\n[2] Discovering available tools...")
        tools = orchestrator.list_all_tools()
        for tool in tools:
            print(f"    - {tool.name} (from {tool.server_name})")
            print(f"      {tool.description}")

        # Execute demo workflow
        print("\n[3] Executing demo workflow...")

        # Math operations
        result_add = await orchestrator.call_tool("add", {"a": 5, "b": 3})
        print(f"    add(5, 3) = {result_add}")

        result_multiply = await orchestrator.call_tool("multiply", {"a": 7, "b": 6})
        print(f"    multiply(7, 6) = {result_multiply}")

        # String operations
        result_upper = await orchestrator.call_tool(
            "uppercase", {"text": "hello world"}
        )
        print(f"    uppercase('hello world') = {result_upper}")

        result_concat = await orchestrator.call_tool(
            "concat", {"a": "Hello", "b": "MCP", "separator": ", "}
        )
        print(f"    concat('Hello', 'MCP', ', ') = {result_concat}")

        print("\n[4] Demo completed successfully!")

    # Cleanup happens automatically when exiting the context manager
    print("\n[5] Disconnected from servers")
    print("\n" + "=" * 60)


async def main() -> None:
    """Entry point for the orchestrator demo."""
    await run_demo()


if __name__ == "__main__":
    asyncio.run(main())
