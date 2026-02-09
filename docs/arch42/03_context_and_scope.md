# 3. Context and Scope

This section defines the boundaries of the system and describes its external interfaces.

---

## 3.1 Business Context

The MCP Multi-Server System operates within a learning/development environment where developers explore the Model Context Protocol.

```mermaid
graph TB
    subgraph "Business Context"
        Developer["Developer<br/>[Person]"]

        MCPSystem["MCP Multi-Server<br/>System"]

        Terminal["Terminal/Console<br/>[Interface]"]

        Docs["Documentation<br/>[Resource]"]
    end

    Developer -->|"Runs commands"| Terminal
    Terminal -->|"Executes"| MCPSystem
    MCPSystem -->|"Outputs results"| Terminal
    Developer -->|"References"| Docs

    style Developer fill:#08427b,color:#fff
    style MCPSystem fill:#1168bd,color:#fff
    style Terminal fill:#85bbf0,color:#000
    style Docs fill:#e8f5e9,color:#000
```

### Business Partners and Interfaces

| Partner       | Interface      | Description                 |
| ------------- | -------------- | --------------------------- |
| Developer     | CLI / Terminal | Primary interaction point   |
| CI System     | GitHub Actions | Automated testing           |
| Documentation | Markdown files | Architecture and usage docs |

---

## 3.2 Technical Context

The system uses stdio transport for inter-process communication between the orchestrator and MCP servers.

```mermaid
graph TB
    subgraph "Technical Context"
        subgraph "Orchestrator Process"
            Orch["Orchestrator<br/>(Python)"]
        end

        subgraph "Server A Process"
            SrvA["Math Server<br/>(Python)"]
        end

        subgraph "Server B Process"
            SrvB["String Server<br/>(Python)"]
        end
    end

    Orch <-->|"stdin/stdout<br/>JSON-RPC 2.0"| SrvA
    Orch <-->|"stdin/stdout<br/>JSON-RPC 2.0"| SrvB

    style Orch fill:#1168bd,color:#fff
    style SrvA fill:#438dd5,color:#fff
    style SrvB fill:#438dd5,color:#fff
```

### Technical Interfaces

| Interface                | Protocol | Format       | Description       |
| ------------------------ | -------- | ------------ | ----------------- |
| Orchestrator to Server A | stdio    | JSON-RPC 2.0 | Math tool calls   |
| Orchestrator to Server B | stdio    | JSON-RPC 2.0 | String tool calls |
| User to Orchestrator     | CLI      | Text         | Command execution |

---

## 3.3 External Interfaces

### Input Interfaces

| Interface      | Type         | Data Format         |
| -------------- | ------------ | ------------------- |
| Command Line   | User Input   | Shell commands      |
| Tool Arguments | Programmatic | Python dictionaries |

### Output Interfaces

| Interface      | Type         | Data Format       |
| -------------- | ------------ | ----------------- |
| Console Output | Text         | Formatted strings |
| Tool Results   | Programmatic | MCP TextContent   |
| Test Reports   | File         | pytest output     |
