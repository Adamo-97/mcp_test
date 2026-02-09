#!/usr/bin/env python3
"""
SOLUTION FILE - MCP Server A (Math Tools)

This is the complete solution for src/server_a/server.py.
Compare your implementation with this file to verify correctness.

DO NOT LOOK AT THIS FILE UNTIL YOU'VE ATTEMPTED THE EXERCISE!
"""

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent


class MathToolsServer:
    """MCP Server that provides mathematical operation tools."""

    def __init__(self, name: str = "math-server") -> None:
        self.name = name
        self.server = Server(name)
        self._register_handlers()

    def _register_handlers(self) -> None:
        """Register all MCP protocol handlers with the server."""

        @self.server.list_tools()
        async def list_tools() -> list[Tool]:
            return [
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
                # SOLUTION: Complete tool definition for multiply
                Tool(
                    name="multiply",
                    description="Multiply two integers and return the product.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "a": {"type": "integer", "description": "First operand"},
                            "b": {"type": "integer", "description": "Second operand"},
                        },
                        "required": ["a", "b"],
                    },
                ),
            ]

        @self.server.call_tool()
        async def call_tool(name: str, arguments: dict) -> list[TextContent]:
            if name == "add":
                result = self._add(arguments["a"], arguments["b"])
            elif name == "multiply":
                # SOLUTION: Call _multiply with arguments
                result = self._multiply(arguments["a"], arguments["b"])
            else:
                raise ValueError(f"Unknown tool: {name}")

            return [TextContent(type="text", text=str(result))]

    def _add(self, a: int, b: int) -> int:
        """Add two integers."""
        return a + b

    def _multiply(self, a: int, b: int) -> int:
        """Multiply two integers."""
        # SOLUTION: Use the * operator
        return a * b

    async def run(self) -> None:
        """Start the MCP server using stdio transport."""
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
