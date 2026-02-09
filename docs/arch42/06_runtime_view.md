# 6. Runtime View

This section describes the behavior and interaction of building blocks during runtime.

---

## 6.1 Startup Sequence

The system initialization follows a specific sequence to ensure all components are ready.

```mermaid
sequenceDiagram
    participant User
    participant Main as main.py
    participant Orch as Orchestrator
    participant SrvA as Server A
    participant SrvB as Server B

    User->>Main: python -m src.orchestrator.main
    Main->>Orch: Create Orchestrator()
    Main->>Orch: add_server(math-server)
    Main->>Orch: add_server(string-server)

    Main->>Orch: connect_all()

    rect rgb(230, 245, 255)
        Note over Orch,SrvA: Server A Connection
        Orch->>SrvA: subprocess.Popen()
        Orch->>SrvA: initialize()
        SrvA-->>Orch: capabilities
        Orch->>SrvA: list_tools()
        SrvA-->>Orch: [add, multiply]
    end

    rect rgb(230, 255, 230)
        Note over Orch,SrvB: Server B Connection
        Orch->>SrvB: subprocess.Popen()
        Orch->>SrvB: initialize()
        SrvB-->>Orch: capabilities
        Orch->>SrvB: list_tools()
        SrvB-->>Orch: [uppercase, concat]
    end

    Orch-->>Main: Ready
    Main-->>User: Connected to all servers
```

---

## 6.2 Tool Execution Flow

When a tool is called, the orchestrator routes it to the appropriate server.

```mermaid
sequenceDiagram
    participant User
    participant Orch as Orchestrator
    participant Reg as ToolRegistry
    participant Srv as MCP Server

    User->>Orch: call_tool("add", {a: 5, b: 3})
    Orch->>Reg: lookup("add")
    Reg-->>Orch: "math-server"

    Orch->>Srv: call_tool("add", {a: 5, b: 3})

    Note over Srv: Execute add(5, 3)

    Srv-->>Orch: TextContent("8")
    Orch-->>User: "8"
```

---

## 6.3 Demo Workflow

The full demo workflow demonstrates all system capabilities.

```mermaid
sequenceDiagram
    participant User
    participant Orch as Orchestrator
    participant Math as Math Server
    participant Str as String Server

    User->>Orch: run_demo()

    rect rgb(255, 245, 230)
        Note over Orch,Math: Math Operations
        Orch->>Math: add(5, 3)
        Math-->>Orch: 8
        Orch->>Math: multiply(7, 6)
        Math-->>Orch: 42
    end

    rect rgb(230, 255, 245)
        Note over Orch,Str: String Operations
        Orch->>Str: uppercase("hello world")
        Str-->>Orch: "HELLO WORLD"
        Orch->>Str: concat("Hello", "MCP", ", ")
        Str-->>Orch: "Hello, MCP"
    end

    Orch-->>User: Display all results
```

---

## 6.4 Shutdown Sequence

Graceful shutdown ensures all resources are properly released.

```mermaid
sequenceDiagram
    participant User
    participant Orch as Orchestrator
    participant SrvA as Server A
    participant SrvB as Server B

    User->>Orch: disconnect_all()

    par Parallel Shutdown
        Orch->>SrvA: close session
        Orch->>SrvB: close session
    end

    SrvA-->>Orch: closed
    SrvB-->>Orch: closed

    Orch->>Orch: Clear registries
    Orch-->>User: Disconnected
```

---

## 6.5 Error Handling

The system handles various error conditions gracefully.

```mermaid
flowchart TB
    Call["call_tool(name, args)"] --> Check{"Tool exists?"}

    Check -->|"No"| Error1["ValueError:<br/>Tool not found"]
    Check -->|"Yes"| Connected{"Server connected?"}

    Connected -->|"No"| Error2["RuntimeError:<br/>Not connected"]
    Connected -->|"Yes"| Execute["Execute tool"]

    Execute --> Success["Return result"]

    style Error1 fill:#ffcdd2,color:#000
    style Error2 fill:#ffcdd2,color:#000
    style Success fill:#c8e6c9,color:#000
```
