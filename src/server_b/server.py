#!/usr/bin/env python3
"""
MCP Server B - String/Format Tools

This server provides string manipulation tools via the Model Context Protocol.
It demonstrates how to:
1. Create an MCP server for text processing
2. Handle string parameters and return formatted text
3. Implement tools with multiple optional parameters

Tools exposed:
- uppercase(text: str) -> str: Converts text to uppercase
- concat(a: str, b: str, separator: str) -> str: Joins strings with a separator
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
        self.name = name
        self.server = Server(name)
        self._register_handlers()
    
    def _register_handlers(self) -> None:
        """Register all MCP protocol handlers with the server."""
        
        @self.server.list_tools()
        async def list_tools() -> list[Tool]:
            """
            Return the list of available string tools.
            
            Each tool is defined with a JSON Schema for its parameters,
            enabling clients to validate inputs before sending requests.
            """
            return [
                Tool(
                    name="uppercase",
                    description="Convert a string to uppercase letters.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "text": {
                                "type": "string",
                                "description": "The text to convert to uppercase"
                            }
                        },
                        "required": ["text"]
                    }
                ),
                Tool(
                    name="concat",
                    description="Concatenate two strings with a separator between them.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "a": {
                                "type": "string",
                                "description": "First string"
                            },
                            "b": {
                                "type": "string",
                                "description": "Second string"
                            },
                            "separator": {
                                "type": "string",
                                "description": "Separator to place between the strings",
                                "default": " "
                            }
                        },
                        "required": ["a", "b", "separator"]
                    }
                )
            ]
        
        @self.server.call_tool()
        async def call_tool(name: str, arguments: dict) -> list[TextContent]:
            """
            Execute a string tool by name with the given arguments.
            
            Args:
                name: The tool to execute ("uppercase" or "concat")
                arguments: Dictionary containing the tool parameters
                
            Returns:
                List containing a TextContent with the result
                
            Raises:
                ValueError: If the tool name is not recognized
            """
            if name == "uppercase":
                result = self._uppercase(arguments["text"])
            elif name == "concat":
                result = self._concat(
                    arguments["a"],
                    arguments["b"],
                    arguments.get("separator", " ")
                )
            else:
                raise ValueError(f"Unknown tool: {name}")
            
            return [TextContent(type="text", text=result)]
    
    def _uppercase(self, text: str) -> str:
        """
        Convert text to uppercase.
        
        Args:
            text: The input string
            
        Returns:
            The input string converted to uppercase
        """
        return text.upper()
    
    def _concat(self, a: str, b: str, separator: str) -> str:
        """
        Concatenate two strings with a separator.
        
        Args:
            a: First string
            b: Second string
            separator: String to place between a and b
            
        Returns:
            The concatenated result: "{a}{separator}{b}"
        """
        return f"{a}{separator}{b}"
    
    async def run(self) -> None:
        """
        Start the MCP server using stdio transport.
        
        This method blocks until the server is shut down.
        Communication happens via stdin/stdout using JSON-RPC 2.0.
        """
        async with stdio_server() as (read_stream, write_stream):
            await self.server.run(
                read_stream,
                write_stream,
                self.server.create_initialization_options()
            )


async def main() -> None:
    """Entry point for running the String Tools Server."""
    server = StringToolsServer()
    await server.run()


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
