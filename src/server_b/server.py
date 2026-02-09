#!/usr/bin/env python3
"""
MCP Server B - String/Format Tools (Learning Exercise - Incomplete)

This server provides string manipulation tools via the Model Context Protocol.
It demonstrates how to:
1. Create an MCP server for text processing
2. Handle string parameters and return formatted text
3. Implement tools with multiple optional parameters

"""

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent


class StringToolsServer:
    """
    MCP Server that provides string manipulation tools.

    This class encapsulates the server logic for text formatting operations.
    It follows clean OOP principles with clear separation of concerns.

    Attributes:
        server: The MCP Server instance
        name: Server identifier for logging and debugging
    """

    def __init__(self, name: str = "string-server") -> None:
        """
        Initialize the String Tools Server.

        Args:
            name: Identifier for this server instance
        """

    def _register_handlers(self) -> None:
        """Register all MCP protocol handlers with the server."""

        @self.server.list_tools()
        async def list_tools() -> list[Tool]:
            """
            Return the list of available string tools.

            Each tool is defined with a JSON Schema for its parameters,
            enabling clients to validate inputs before sending requests.

            TODO: Complete the Tool definitions below.

            Reference for JSON Schema:
            - "type": "object" indicates the input is an object
            - "properties": defines each parameter with type and description
            - "required": list of parameter names that must be provided
            """
            return [
                # TODO: Define the 'uppercase' tool
                # It should accept a single parameter 'text' of type string
                # Hint: Look at server_a for the pattern

                # TODO: Define the 'concat' tool
                # It should accept: a (string), b (string), separator (string)
                # All three parameters are required

            ]

        @self.server.call_tool()
        async def call_tool(name: str, arguments: dict) -> list[TextContent]:
            """
            Execute a string tool by name with the given arguments.

            TODO: Implement the routing logic to call the appropriate method.

            Args:
                name: The tool to execute ("uppercase" or "concat")
                arguments: Dictionary containing the tool parameters

            Returns:
                List containing a TextContent with the result

            Raises:
                ValueError: If the tool name is not recognized
            """
            # TODO: Implement the routing logic
            # if name == "uppercase":
            #     result = self._uppercase(arguments["text"])
            # elif name == "concat":
            #     result = self._concat(arguments["a"], arguments["b"], arguments.get("separator", " "))
            # else:
            #     raise ValueError(f"Unknown tool: {name}")

            # TODO: Replace the placeholder below with proper routing
            raise NotImplementedError("TODO: Implement tool routing logic")

            # TODO: Return the result wrapped in TextContent
            # return [TextContent(type="text", text=result)]

    def _uppercase(self, text: str) -> str:
        """
        Convert text to uppercase.

        Args:
            text: The input string

        Returns:
            The input string converted to uppercase

        TODO: Implement this method.
        Hint: Python strings have .upper() method
        """
        # TODO: Return the uppercase version of text

    def _concat(self, a: str, b: str, separator: str) -> str:
        """
        Concatenate two strings with a separator.

        Args:
            a: First string
            b: Second string
            separator: String to place between a and b

        Returns:
            The concatenated result: "{a}{separator}{b}"

        TODO: Implement this method.
        Hint: Use f-strings or string concatenation
        """
        # TODO: Return the concatenated string
        # Example: _concat("Hello", "World", ", ") should return "Hello, World"

    async def run(self) -> None:
        """
        Start the MCP server using stdio transport.

        This method blocks until the server is shut down.
        Communication happens via stdin/stdout using JSON-RPC 2.0.
        """



async def main() -> None:
    """Entry point for running the String Tools Server."""



if __name__ == "__main__":
    import asyncio
