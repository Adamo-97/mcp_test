#!/usr/bin/env python3
"""
SOLUTION FILE - MCP Server B (String Tools)

This is the complete solution for src/server_b/server.py.
Compare your implementation with this file to verify correctness.

DO NOT LOOK AT THIS FILE UNTIL YOU'VE ATTEMPTED THE EXERCISE!
"""

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent


class StringToolsServer:
    """MCP Server that provides string manipulation tools."""

    def __init__(self, name: str = "string-server") -> None:
        self.name = name
        self.server = Server(name)
        self._register_handlers()

    def _register_handlers(self) -> None:
        """Register all MCP protocol handlers with the server."""

        @self.server.list_tools()
        async def list_tools() -> list[Tool]:
            return [
                # SOLUTION: Complete 'uppercase' tool definition
                Tool(
                    name="uppercase",
                    description="Convert a string to uppercase letters.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "text": {
                                "type": "string",
                                "description": "The text to convert to uppercase",
                            }
                        },
                        "required": ["text"],
                    },
                ),
                # SOLUTION: Complete 'concat' tool definition
                Tool(
                    name="concat",
                    description="Concatenate two strings with a separator between them.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "a": {"type": "string", "description": "First string"},
                            "b": {"type": "string", "description": "Second string"},
                            "separator": {
                                "type": "string",
                                "description": "Separator to place between the strings",
                                "default": " ",
                            },
                        },
                        "required": ["a", "b", "separator"],
                    },
                ),
            ]

        @self.server.call_tool()
        async def call_tool(name: str, arguments: dict) -> list[TextContent]:
            # SOLUTION: Implement routing logic
            if name == "uppercase":
                result = self._uppercase(arguments["text"])
            elif name == "concat":
                result = self._concat(
                    arguments["a"], arguments["b"], arguments.get("separator", " ")
                )
            else:
                raise ValueError(f"Unknown tool: {name}")

            # SOLUTION: Return result wrapped in TextContent
            return [TextContent(type="text", text=result)]

    def _uppercase(self, text: str) -> str:
        """Convert text to uppercase."""
        # SOLUTION: Use Python's built-in .upper() method
        return text.upper()

    def _concat(self, a: str, b: str, separator: str) -> str:
        """Concatenate two strings with a separator."""
        # SOLUTION: Use f-string formatting
        return f"{a}{separator}{b}"

    async def run(self) -> None:
        """Start the MCP server using stdio transport."""
        async with stdio_server() as (read_stream, write_stream):
            await self.server.run(
                read_stream, write_stream, self.server.create_initialization_options()
            )


async def main() -> None:
    """Entry point for running the String Tools Server."""
    server = StringToolsServer()
    await server.run()


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
