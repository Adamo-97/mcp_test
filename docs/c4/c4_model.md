# C4 Model - MCP Multi-Server System

This document describes the system architecture using the C4 model notation with MermaidJS diagrams.

---

## Level 0: System Landscape Diagram

The System Landscape shows the broader context in which the MCP Multi-Server System exists.

```mermaid
graph TB
    subgraph Enterprise ["Enterprise Context"]
        User["Developer/User<br/>[Person]<br/>Uses MCP tools for<br/>distributed task execution"]

        MCPSystem["MCP Multi-Server System<br/>[Software System]<br/>Orchestrates multiple tool servers"]

        ExternalAI["AI Assistant<br/>[External System]<br/>Could integrate with MCP<br/>for extended capabilities"]
    end

    User -->|"Executes tasks"| MCPSystem
    ExternalAI -.->|"Future integration"| MCPSystem

    style User fill:#08427b,color:#fff
    style MCPSystem fill:#1168bd,color:#fff
    style ExternalAI fill:#999999,color:#fff
```

### Landscape Description

| Element                 | Type            | Description                            |
| ----------------------- | --------------- | -------------------------------------- |
| Developer/User          | Person          | Primary user who runs the orchestrator |
| MCP Multi-Server System | Software System | The system being documented            |
| AI Assistant            | External System | Potential future integration point     |

---

## Level 1: System Context Diagram

The System Context diagram shows the MCP Multi-Server System and its interactions with external actors.

```mermaid
graph TB
    subgraph External
        User["Developer/User<br/>[Person]<br/>Runs the orchestrator to<br/>execute distributed tasks"]
    end

    subgraph System ["MCP Multi-Server System"]
        MCP["MCP System<br/>[Software System]<br/>Coordinates multiple MCP servers<br/>to execute tools and aggregate results"]
    end

    User -->|"Runs demo,<br/>views results"| MCP

    style User fill:#08427b,color:#fff
    style MCP fill:#1168bd,color:#fff
```

### Context Description

| Element        | Type            | Description                                                |
| -------------- | --------------- | ---------------------------------------------------------- |
| Developer/User | Person          | Executes the orchestrator to perform tasks using MCP tools |
| MCP System     | Software System | The complete system including orchestrator and servers     |

---

## Level 2: Container Diagram

The Container diagram shows the high-level components that make up the MCP System.

```mermaid
graph TB
    subgraph External
        User["Developer/User<br/>[Person]"]
    end

    subgraph MCPSystem ["MCP Multi-Server System"]
        Orchestrator["Orchestrator<br/>[Python Application]<br/>MCP Client that connects to<br/>servers and executes tools"]

        subgraph Transport ["Stdio Transport Layer"]
            Pipe1["stdin/stdout<br/>[Pipe]"]
            Pipe2["stdin/stdout<br/>[Pipe]"]
        end

        ServerA["Server A<br/>[Python Application]<br/>MCP Server providing<br/>Math tools: add, multiply"]

        ServerB["Server B<br/>[Python Application]<br/>MCP Server providing<br/>String tools: uppercase, concat"]
    end

    User -->|"Executes"| Orchestrator
    Orchestrator -->|"JSON-RPC/MCP"| Pipe1
    Orchestrator -->|"JSON-RPC/MCP"| Pipe2
    Pipe1 -->|"Tool calls"| ServerA
    Pipe2 -->|"Tool calls"| ServerB
    ServerA -->|"Results"| Pipe1
    ServerB -->|"Results"| Pipe2

    style User fill:#08427b,color:#fff
    style Orchestrator fill:#1168bd,color:#fff
    style ServerA fill:#438dd5,color:#fff
    style ServerB fill:#438dd5,color:#fff
    style Pipe1 fill:#85bbf0,color:#000
    style Pipe2 fill:#85bbf0,color:#000
```

### Container Descriptions

| Container             | Technology            | Description                                                       |
| --------------------- | --------------------- | ----------------------------------------------------------------- |
| **Orchestrator**      | Python 3.10+, MCP SDK | Central client that manages server connections and tool execution |
| **Server A (Math)**   | Python 3.10+, MCP SDK | Exposes mathematical operations as MCP tools                      |
| **Server B (String)** | Python 3.10+, MCP SDK | Exposes string manipulation as MCP tools                          |
| **Stdio Transport**   | subprocess pipes      | Communication channel using stdin/stdout                          |

---

## Level 3: Component Diagram - Orchestrator

```mermaid
graph TB
    subgraph Orchestrator ["Orchestrator Container"]
        Main["Main<br/>[Component]<br/>Entry point and<br/>demo workflow"]

        MCPConn["MCPConnection<br/>[Component]<br/>Manages connection<br/>to a single MCP server"]

        ToolReg["ToolRegistry<br/>[Component]<br/>Maps tools to<br/>their source servers"]

        Orch["Orchestrator<br/>[Component]<br/>High-level API for<br/>tool discovery and execution"]
    end

    Main --> Orch
    Orch --> MCPConn
    Orch --> ToolReg
    MCPConn -->|"Subprocess"| ServerProcess["Server Process<br/>[External Process]"]

    style Main fill:#85bbf0,color:#000
    style MCPConn fill:#85bbf0,color:#000
    style ToolReg fill:#85bbf0,color:#000
    style Orch fill:#85bbf0,color:#000
    style ServerProcess fill:#999,color:#fff
```

---

## MCP Communication Sequence

```mermaid
sequenceDiagram
    participant User
    participant Orchestrator
    participant ServerA as Server A (Math)
    participant ServerB as Server B (String)

    User->>Orchestrator: Run demo

    rect rgb(200, 220, 240)
        Note over Orchestrator,ServerB: Initialization Phase
        Orchestrator->>ServerA: Spawn process
        Orchestrator->>ServerB: Spawn process
        Orchestrator->>ServerA: Initialize (MCP handshake)
        ServerA-->>Orchestrator: Capabilities
        Orchestrator->>ServerB: Initialize (MCP handshake)
        ServerB-->>Orchestrator: Capabilities
    end

    rect rgb(220, 240, 220)
        Note over Orchestrator,ServerB: Discovery Phase
        Orchestrator->>ServerA: list_tools()
        ServerA-->>Orchestrator: [add, multiply]
        Orchestrator->>ServerB: list_tools()
        ServerB-->>Orchestrator: [uppercase, concat]
    end

    rect rgb(240, 220, 200)
        Note over Orchestrator,ServerB: Execution Phase
        Orchestrator->>ServerA: call_tool("add", {a: 5, b: 3})
        ServerA-->>Orchestrator: Result: 8
        Orchestrator->>ServerB: call_tool("uppercase", {text: "hello"})
        ServerB-->>Orchestrator: Result: "HELLO"
    end

    Orchestrator-->>User: Aggregated results
```

---

## Transport Layer Detail

The MCP protocol uses **JSON-RPC 2.0** over the stdio transport:

```mermaid
graph LR
    subgraph Orchestrator Process
        Client["MCP Client"]
    end

    subgraph "Stdio Channel"
        stdin["stdin<br/>(→ Server)"]
        stdout["stdout<br/>(← Server)"]
    end

    subgraph Server Process
        Server["MCP Server"]
    end

    Client -->|"JSON-RPC Request"| stdin
    stdin --> Server
    Server -->|"JSON-RPC Response"| stdout
    stdout --> Client
```

### Message Format Examples

**Request (Client → Server)**:

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/call",
  "params": {
    "name": "add",
    "arguments": { "a": 5, "b": 3 }
  }
}
```

**Response (Server → Client)**:

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "content": [{ "type": "text", "text": "8" }]
  }
}
```

---

## Deployment View

```mermaid
graph TB
    subgraph "Developer Machine"
        subgraph "Python Virtual Environment"
            OrchestratorProc["Orchestrator<br/>(Main Process)"]
            ServerAProc["Server A<br/>(Subprocess)"]
            ServerBProc["Server B<br/>(Subprocess)"]
        end
    end

    OrchestratorProc -.->|"spawn"| ServerAProc
    OrchestratorProc -.->|"spawn"| ServerBProc

    style OrchestratorProc fill:#1168bd,color:#fff
    style ServerAProc fill:#438dd5,color:#fff
    style ServerBProc fill:#438dd5,color:#fff
```

All components run locally within a single Python virtual environment. The orchestrator spawns the servers as subprocesses, which simplifies deployment and testing.
