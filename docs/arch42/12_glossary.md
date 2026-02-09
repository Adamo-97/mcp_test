# 12. Glossary

This section defines important terms used throughout the documentation.

---

## Domain Terms

| Term             | Definition                                                                                                          |
| ---------------- | ------------------------------------------------------------------------------------------------------------------- |
| **MCP**          | Model Context Protocol - A standardized protocol for communication between AI assistants and external tools/servers |
| **Tool**         | A callable function exposed by an MCP server that performs a specific operation                                     |
| **Orchestrator** | The central client component that coordinates communication with multiple MCP servers                               |
| **Server**       | An MCP-compliant process that exposes tools and handles tool execution requests                                     |

---

## Technical Terms

| Term             | Definition                                                                                             |
| ---------------- | ------------------------------------------------------------------------------------------------------ |
| **stdio**        | Standard Input/Output - A transport mechanism using stdin/stdout pipes for inter-process communication |
| **JSON-RPC 2.0** | A stateless, light-weight remote procedure call protocol encoded in JSON                               |
| **Handshake**    | The initial protocol exchange where client and server negotiate capabilities                           |
| **Transport**    | The communication layer that carries MCP messages (stdio, HTTP, WebSocket)                             |
| **Session**      | An active connection between an MCP client and server                                                  |

---

## Architecture Terms

| Term         | Definition                                                                                                     |
| ------------ | -------------------------------------------------------------------------------------------------------------- |
| **Arc42**    | A template for documenting software and system architectures                                                   |
| **C4 Model** | A set of hierarchical abstractions (Context, Container, Component, Code) for visualizing software architecture |
| **ADR**      | Architecture Decision Record - A document capturing an important architectural decision                        |
| **DTO**      | Data Transfer Object - A simple object used to transfer data between layers                                    |
| **Fixture**  | In pytest, a function that provides test data or setup/teardown logic                                          |

---

## Python Terms

| Term                | Definition                                                                                          |
| ------------------- | --------------------------------------------------------------------------------------------------- |
| **async/await**     | Python syntax for writing asynchronous, non-blocking code                                           |
| **dataclass**       | A Python decorator that automatically generates special methods for classes used as data containers |
| **type hint**       | Annotations that indicate the expected types of variables, parameters, and return values            |
| **context manager** | An object that defines `__enter__` and `__exit__` methods for use with the `with` statement         |
| **subprocess**      | A module for spawning new processes and communicating with them                                     |

---

## Protocol Message Types

| Message      | Direction        | Description                              |
| ------------ | ---------------- | ---------------------------------------- |
| `initialize` | Client to Server | Start MCP session, exchange capabilities |
| `tools/list` | Client to Server | Request list of available tools          |
| `tools/call` | Client to Server | Execute a specific tool with arguments   |
| `result`     | Server to Client | Return tool execution results            |

---

## Abbreviations

| Abbreviation | Full Form                          |
| ------------ | ---------------------------------- |
| **API**      | Application Programming Interface  |
| **CI**       | Continuous Integration             |
| **CLI**      | Command Line Interface             |
| **IDE**      | Integrated Development Environment |
| **JSON**     | JavaScript Object Notation         |
| **OOP**      | Object-Oriented Programming        |
| **PEP**      | Python Enhancement Proposal        |
| **RPC**      | Remote Procedure Call              |
| **SDK**      | Software Development Kit           |
| **venv**     | Virtual Environment                |

---

## File Structure Terms

| Path                 | Description                      |
| -------------------- | -------------------------------- |
| `src/`               | Source code directory            |
| `tests/`             | Test files directory             |
| `docs/`              | Documentation directory          |
| `docs/arch42/`       | Arc42 architecture documentation |
| `docs/c4/`           | C4 model diagrams                |
| `.github/workflows/` | GitHub Actions CI configuration  |

---

## Quality Terms

| Term             | Definition                                                     |
| ---------------- | -------------------------------------------------------------- |
| **Learnability** | How easily new users can understand and use the system         |
| **Modularity**   | The degree to which components can be separated and recombined |
| **Testability**  | How easily the system can be tested                            |
| **Type Safety**  | The extent to which the type system prevents type errors       |
