# 5. Building Block View

## 5.1 Whitebox Overall System

The system is decomposed into three main building blocks connected via the MCP protocol over stdio transport.

```mermaid
graph TB
    subgraph MCPSystem ["MCP Multi-Server System"]
        subgraph Orchestrator ["Orchestrator (MCP Client)"]
            ServerConn["ServerConn"]
            ToolRegistry["ToolRegistry"]
            ResultAggr["ResultAggr"]
        end

        subgraph ServerA ["MCP Server A (Math/Logic)"]
            add["add()"]
            multiply["multiply()"]
        end

        subgraph ServerB ["MCP Server B (String/Format)"]
            uppercase["uppercase()"]
            concat["concat()"]
        end
    end

    Orchestrator -->|"stdio"| ServerA
    Orchestrator -->|"stdio"| ServerB

    style Orchestrator fill:#1168bd,color:#fff
    style ServerA fill:#438dd5,color:#fff
    style ServerB fill:#438dd5,color:#fff
```

## 5.2 Level 1: Building Blocks

### 5.2.1 Orchestrator (MCP Client)

**Purpose**: Central coordinator that manages connections to MCP servers and executes tools.

**Responsibilities**:

- Spawn and manage server processes
- Establish MCP sessions with each server
- Discover available tools from all servers
- Execute tool calls and handle responses
- Aggregate results from multiple servers

**Interfaces**:
| Interface | Type | Description |
|-----------|------|-------------|
| `connect()` | Method | Establishes connections to all servers |
| `list_tools()` | Method | Returns all available tools from all servers |
| `call_tool()` | Method | Executes a specific tool by name |
| `disconnect()` | Method | Gracefully closes all connections |

**Files**: `src/orchestrator/main.py`

---

### 5.2.2 MCP Server A (Math/Logic)

**Purpose**: Provides mathematical computation tools via MCP.

**Responsibilities**:

- Register mathematical tools with MCP SDK
- Handle tool execution requests
- Return computed results in MCP format

**Exposed Tools**:
| Tool | Signature | Description |
|------|-----------|-------------|
| `add` | `(a: int, b: int) -> int` | Adds two integers |
| `multiply` | `(a: int, b: int) -> int` | Multiplies two integers |

**Files**: `src/server_a/server.py`

---

### 5.2.3 MCP Server B (String/Format)

**Purpose**: Provides string manipulation tools via MCP.

**Responsibilities**:

- Register string tools with MCP SDK
- Handle text transformation requests
- Return formatted strings in MCP format

**Exposed Tools**:
| Tool | Signature | Description |
|------|-----------|-------------|
| `uppercase` | `(text: str) -> str` | Converts text to uppercase |
| `concat` | `(a: str, b: str, separator: str) -> str` | Joins strings with separator |

**Files**: `src/server_b/server.py`

---

## 5.3 Level 2: Orchestrator Internal Structure

```mermaid
graph TB
    subgraph Orchestrator ["Orchestrator"]
        ConnA["MCPConnection<br/>(Server A)"]
        ConnB["MCPConnection<br/>(Server B)"]

        ConnA --> ToolReg
        ConnB --> ToolReg

        ToolReg["ToolRegistry<br/>- tools: Dict<br/>- servers: Dict"]

        ToolReg --> Orch["Orchestrator<br/>- run_demo()<br/>- call_tool()"]
    end

    style ConnA fill:#85bbf0,color:#000
    style ConnB fill:#85bbf0,color:#000
    style ToolReg fill:#85bbf0,color:#000
    style Orch fill:#85bbf0,color:#000
```

### Components

| Component         | Responsibility                                         |
| ----------------- | ------------------------------------------------------ |
| **MCPConnection** | Wraps subprocess and MCP client session for one server |
| **ToolRegistry**  | Maps tool names to their source servers                |
| **Orchestrator**  | High-level API for demo and tool execution             |

## 5.4 Data Flow

```mermaid
flowchart TB
    User["User"] --> Orchestrator["Orchestrator"]
    Orchestrator --> ToolRegistry["ToolRegistry"]

    Orchestrator --> SpawnA["Spawn Server A"]
    Orchestrator --> SpawnB["Spawn Server B"]
    Orchestrator --> SpawnN["Spawn Server N"]

    SpawnA --> HandshakeA["Handshake"]
    SpawnB --> HandshakeB["Handshake"]
    SpawnN --> HandshakeN["Handshake"]

    HandshakeA --> Ready["Tools Ready<br/>for Execution"]
    HandshakeB --> Ready
    HandshakeN --> Ready

    style User fill:#08427b,color:#fff
    style Orchestrator fill:#1168bd,color:#fff
    style Ready fill:#2e7d32,color:#fff
```

## 5.5 Technology Mapping

| Building Block | Technology               |
| -------------- | ------------------------ |
| Orchestrator   | Python 3.10+, `mcp` SDK  |
| MCP Servers    | Python 3.10+, `mcp` SDK  |
| Transport      | stdio (subprocess pipes) |
| Message Format | JSON-RPC 2.0             |
| Testing        | pytest                   |
| CI/CD          | GitHub Actions           |
