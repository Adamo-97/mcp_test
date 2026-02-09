#!/usr/bin/env python3
"""
MCP Server A - Math/Logic Tools (Learning Exercise - Partially Complete)

This server provides mathematical computation tools via the Model Context Protocol.
It demonstrates how to:
1. Create an MCP server using the SDK
2. Register tools with typed parameters
3. Handle tool execution requests
4. Return structured results

Tools exposed:
- add(a: int, b: int) -> int: Adds two integers
- multiply(a: int, b: int) -> int: Multiplies two integers

LEARNING OBJECTIVES:
- Understand Tool registration with JSON Schema
- Implement the multiply tool following the add pattern
- Learn how tool routing works in call_tool handler

DIFFICULTY: Beginner (some gaps to fill)
"""

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent


class MathToolsServer:
    """
    MCP Server that provides mathematical operation tools.

    This class encapsulates the server logic for mathematical computations.
    It follows the Single Responsibility Principle by focusing only on
    math-related tools.

    Attributes:
        server: The MCP Server instance
        name: Server identifier for logging and debugging
    """

    def __init__(self, name: str = "math-server") -> None:
        """
        Initialize the Math Tools Server.

        Args:
            name: Identifier for this server instance
        """
        self.name = name
        self.server = Server(name)
        self._register_handlers()

    def _register_handlers(self) -> None:
        """Register all MCP protocol handlers with the server."""

        @self.server.list_tools()
        async def list_tools() -> list[Tool]:
            """
            Return the list of available tools.

            This handler is called when a client requests tool discovery.
            Each tool is defined with:
            - name: Unique identifier for the tool
            - description: Human-readable explanation
            - inputSchema: JSON Schema defining the expected parameters
            """
            return [
                # EXAMPLE: Complete tool definition for 'add'
                Tool(
                    name="add",
                    description="Add two integers together and return the sum.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "a": {"type": "integer", "description": "First operand"},
                            "b": {"type": "integer", "description": "Second operand"},
                        },
                        "required": ["a", "b"],
                    },
                ),
                # TODO: Complete the multiply tool definition
                # Follow the same pattern as 'add' above
                # Hint: The inputSchema structure is identical
            ]

        @self.server.call_tool()
        async def call_tool(name: str, arguments: dict) -> list[TextContent]:
            """
            Execute a tool by name with the given arguments.

            This handler is called when a client wants to execute a tool.
            It routes the request to the appropriate implementation based
            on the tool name.

            Args:
                name: The tool to execute ("add" or "multiply")
                arguments: Dictionary containing the tool parameters

            Returns:
                List containing a TextContent with the result

            Raises:
                ValueError: If the tool name is not recognized
            """
            if name == "add":
                result = self._add(arguments["a"], arguments["b"])
            elif name == "multiply":
                # TODO: Call the _multiply method with the appropriate arguments
                # Hint: Follow the same pattern as _add above
            else:
                raise ValueError(f"Unknown tool: {name}")

            return [TextContent(type="text", text=str(result))]

    def _add(self, a: int, b: int) -> int:
        """
        Add two integers.

        Args:
            a: First operand
            b: Second operand

        Returns:
            Sum of a and b
        """
        # EXAMPLE: Complete implementation

    def _multiply(self, a: int, b: int) -> int:
        """
        Multiply two integers.

        Args:
            a: First operand
            b: Second operand

        Returns:
            Product of a and b
        """
        # TODO: Implement the multiplication logic

    async def run(self) -> None:
        """
        Start the MCP server using stdio transport.

        This method blocks until the server is shut down.
        Communication happens via stdin/stdout using JSON-RPC 2.0.
        """
        async with stdio_server() as (read_stream, write_stream):
            await self.server.run(
                read_stream, write_stream, self.server.create_initialization_options()
            )


async def main() -> None:
    """Entry point for running the Math Tools Server."""
    server = MathToolsServer()
    await server.run()


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
