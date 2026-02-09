"""
MCP Multi-Server System

A minimalistic reference implementation demonstrating the Model Context Protocol (MCP)
with Python. This package showcases how a central Orchestrator communicates with
multiple MCP Servers to execute tools.

Modules:
    orchestrator: MCP client that connects to and coordinates multiple servers
    server_a: MCP server providing mathematical tools (add, multiply)
    server_b: MCP server providing string tools (uppercase, concat)
"""

__version__ = "0.1.0"
__author__ = "MCP Learning Project"
