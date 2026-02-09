# 7. Deployment View

This section describes the technical infrastructure and how the system components are deployed.

---

## 7.1 Infrastructure Overview

The MCP Multi-Server System runs entirely on the local developer machine without external dependencies.

```mermaid
graph TB
    subgraph "Developer Machine"
        subgraph "Operating System"
            subgraph "Python Virtual Environment"
                Main["Orchestrator<br/>(Main Process)<br/>PID: parent"]

                SrvA["Server A<br/>(Subprocess)<br/>PID: child-1"]

                SrvB["Server B<br/>(Subprocess)<br/>PID: child-2"]
            end

            FS["File System<br/>- src/<br/>- tests/<br/>- docs/"]
        end
    end

    Main -.->|"spawn"| SrvA
    Main -.->|"spawn"| SrvB
    Main -->|"read"| FS

    style Main fill:#1168bd,color:#fff
    style SrvA fill:#438dd5,color:#fff
    style SrvB fill:#438dd5,color:#fff
    style FS fill:#e8f5e9,color:#000
```

---

## 7.2 Development Environment

### Requirements

| Component        | Requirement              |
| ---------------- | ------------------------ |
| Operating System | Windows, macOS, or Linux |
| Python           | 3.10 or higher           |
| pip              | Latest version           |
| Git              | For version control      |

### Setup Steps

```mermaid
flowchart LR
    A["Clone Repo"] --> B["Create venv"]
    B --> C["Activate venv"]
    C --> D["pip install"]
    D --> E["Ready"]

    style E fill:#c8e6c9,color:#000
```

---

## 7.3 CI/CD Pipeline

GitHub Actions provides the continuous integration environment.

```mermaid
graph TB
    subgraph "GitHub Actions Runner"
        subgraph "ubuntu-latest / windows-latest / macos-latest"
            Checkout["Checkout Code"]
            Setup["Setup Python"]
            Install["Install Dependencies"]
            Test["Run Tests"]
            Lint["Lint Check"]
        end
    end

    Push["Git Push"] --> Checkout
    Checkout --> Setup
    Setup --> Install
    Install --> Test
    Install --> Lint
    Test --> Report["Test Report"]

    style Push fill:#08427b,color:#fff
    style Report fill:#c8e6c9,color:#000
```

---

## 7.4 Process Architecture

```mermaid
graph TB
    subgraph "Process Tree"
        Parent["python -m src.orchestrator.main<br/>(Parent Process)"]

        Child1["python -m src.server_a.server<br/>(Child Process 1)"]

        Child2["python -m src.server_b.server<br/>(Child Process 2)"]
    end

    Parent -->|"stdin/stdout pipe"| Child1
    Parent -->|"stdin/stdout pipe"| Child2

    style Parent fill:#1168bd,color:#fff
    style Child1 fill:#438dd5,color:#fff
    style Child2 fill:#438dd5,color:#fff
```

---

## 7.5 Resource Requirements

| Resource | Minimum      | Recommended  |
| -------- | ------------ | ------------ |
| RAM      | 256 MB       | 512 MB       |
| Disk     | 50 MB        | 100 MB       |
| CPU      | 1 core       | 2 cores      |
| Network  | Not required | Not required |

---

## 7.6 Deployment Artifacts

| Artifact      | Location             | Description       |
| ------------- | -------------------- | ----------------- |
| Source Code   | `src/`               | Python modules    |
| Tests         | `tests/`             | pytest test files |
| Documentation | `docs/`              | Architecture docs |
| Dependencies  | `requirements.txt`   | pip packages      |
| CI Config     | `.github/workflows/` | GitHub Actions    |
