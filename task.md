# Task: MCP Multi-Server Orchestration Exercise

## Objective

Build a minimalistic **Model Context Protocol (MCP)** system demonstrating client-server communication patterns using Python's MCP SDK.

---

## Background

The Model Context Protocol (MCP) is a standardized protocol for communication between AI assistants and external tools/servers. This exercise will teach you:

1. How to create MCP servers that expose tools
2. How to build a client (orchestrator) that connects to multiple servers
3. How MCP's handshake and tool execution flow works
4. Clean OOP patterns with Python type hints

---

## Requirements

### Functional Requirements

1. **MCP Server A (Math/Logic)**
   - Expose an `add(a: int, b: int) -> int` tool
   - Expose a `multiply(a: int, b: int) -> int` tool

2. **MCP Server B (String/Format)**
   - Expose a `uppercase(text: str) -> str` tool
   - Expose a `concat(a: str, b: str, separator: str) -> str` tool

3. **Orchestrator**
   - Connect to both servers via stdio transport
   - Discover available tools from each server
   - Execute tools and aggregate results
   - Provide a simple interface to run a demo workflow

### Non-Functional Requirements

- Python 3.10+ with strict type hints
- Clean OOP design (classes, abstractions)
- All code must pass `pytest` tests
- Follow PEP 8 style guidelines

---

## Acceptance Criteria

- [ ] Both MCP servers start and respond to the handshake
- [ ] Orchestrator can list tools from both servers
- [ ] Orchestrator can call `add(5, 3)` and receive `8`
- [ ] Orchestrator can call `uppercase("hello")` and receive `"HELLO"`
- [ ] Integration tests pass in CI pipeline
- [ ] Documentation is complete and accurate

---

## Deliverables

1. Source code in `src/` directory
2. Tests in `tests/` directory
3. Documentation in `docs/` directory
4. CI workflow in `.github/workflows/`
5. `README.md` with setup instructions

---

## Resources

- [MCP SDK Documentation](https://modelcontextprotocol.io/docs)
- [Python Typing Module](https://docs.python.org/3/library/typing.html)
- [Pytest Documentation](https://docs.pytest.org/)
