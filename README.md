# LangchainMCP

> **LangchainMCP: Production-grade MCP server for multi-agent workflows using LangGraph + FastAPI.**

[![GitHub Stars](https://img.shields.io/github/stars/mcpmessenger/LangchainMCP?style=social)](https://github.com/mcpmessenger/LangchainMCP)
[![GitHub Forks](https://img.shields.io/github/forks/mcpmessenger/LangchainMCP?style=social)](https://github.com/mcpmessenger/LangchainMCP)
[![PyPI Downloads](https://img.shields.io/pypi/dm/langchain-mcp?label=PyPI%20Downloads)](https://pypi.org/project/langchain-mcp/)
[![License](https://img.shields.io/github/license/mcpmessenger/LangchainMCP)](https://github.com/mcpmessenger/LangchainMCP/blob/main/LICENSE)

## 🚀 Why LangchainMCP?

Building reliable, scalable, and production-ready AI agents is hard. LangchainMCP solves this by providing a **high-performance, standardized server** for your multi-agent applications. Leverage the power of **LangGraph** for complex state management and **FastAPI** for blazing-fast, asynchronous serving.

| Feature | LangchainMCP | Traditional Agent Setup |
| :--- | :--- | :--- |
| **Protocol** | Model Context Protocol (MCP) | Custom/Ad-hoc API |
| **Orchestration** | LangGraph (Stateful, Cyclic) | Simple Chains (Stateless, Linear) |
| **Performance** | **&lt;5s P95 Latency** (Placeholder) | Highly Variable |
| **Deployment** | FastAPI (Scalable, Async) | Single-threaded scripts |
| **Tooling** | Standardized, Discoverable | Manual Definition |

## ✨ Quick Demo: Document-to-Insight Workflow

See how quickly you can go from a raw document to a structured, agent-verified output.

**(Placeholder for GIF/Video Demo: Please create a visual that shows the following flow)**

1.  **Input:** A user uploads a PDF document (e.g., a financial report).
2.  **Agent Chain:**
    *   **Extraction Agent:** Uses a tool to read the PDF and extract raw text.
    *   **Analysis Agent:** Takes the raw text, identifies key metrics (e.g., revenue, profit), and stores them in a structured format.
    *   **Verification Agent:** Cross-references the extracted metrics with a secondary source or a pre-defined schema, flagging any inconsistencies.
3.  **Output:** The final, verified, structured JSON data is returned to the user.

## 🛠️ Installation

### PyPI (Recommended)

```bash
pip install langchain-mcp
```

### Docker

For a production-ready, isolated environment, use our official Docker image:

```bash
docker pull mcpmessenger/langchain-mcp:latest
docker run -d -p 8000:8000 mcpmessenger/langchain-mcp:latest
```

## 💻 Usage

### 1. Define Your Agent Graph

Create your LangGraph workflow in a file (e.g., `graph.py`).

```python
# graph.py
from langgraph.graph import StateGraph, END
from typing import TypedDict, Annotated, List
import operator

# Define the state
class AgentState(TypedDict):
    document: str
    metrics: dict
    verified: bool
    
# Define the nodes (agents)
def extract_agent(state):
    # Logic to extract text from state['document']
    return {"metrics": {"revenue": 1000000, "profit": 50000}}

def verify_agent(state):
    # Logic to verify metrics
    return {"verified": True}

# Build the graph
workflow = StateGraph(AgentState)
workflow.add_node("extract", extract_agent)
workflow.add_node("verify", verify_agent)
workflow.set_entry_point("extract")
workflow.add_edge("extract", "verify")
workflow.add_edge("verify", END)

app = workflow.compile()
```

### 2. Run the MCP Server

LangchainMCP automatically discovers and serves your LangGraph application via FastAPI.

```bash
# Start the server, pointing to your compiled graph object
langchain-mcp serve graph:app
```

### 3. Client Interaction

Use the `langchain-mcp-client` to interact with your new server.

```python
from langchain_mcp.client import MCPClient

# Initialize the client
client = MCPClient(server_url="http://localhost:8000")

# Define the initial state for the workflow
initial_state = {"document": "path/to/financial_report.pdf"}

# Run the workflow
result = client.run_workflow(
    workflow_name="default", # The default workflow name for a single graph
    input_state=initial_state
)

print(result)
# Expected Output: {'document': '...', 'metrics': {'revenue': 1000000, 'profit': 50000}, 'verified': True}
```

## 📊 Benchmarks

LangchainMCP is built for speed and reliability. Our performance targets ensure your agents can handle high-throughput, low-latency demands.

| Metric | Target | Notes |
| :--- | :--- | :--- |
| **P95 Latency** | **&lt;5s** | End-to-end workflow execution time. |
| **Throughput** | **50+ RPS** | Requests per second on standard hardware. |
| **Memory Footprint** | **&lt;100MB** | Minimal overhead for the server process. |

*(Note: These are target benchmarks. Actual performance may vary based on the complexity of your LangGraph and the LLM provider's latency.)*

## 🧑‍💻 Tech Stack

| Component | Technology | Purpose |
| :--- | :--- | :--- |
| **Core** | ![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white) | The primary language for the entire stack. |
| **Server** | ![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=flat-square&logo=fastapi&logoColor=white) | High-performance, asynchronous web framework. |
| **Orchestration** | ![LangChain](https://img.shields.io/badge/LangChain-222222?style=flat-square&logo=langchain&logoColor=white) / ![LangGraph](https://img.shields.io/badge/LangGraph-222222?style=flat-square&logo=langchain&logoColor=white) | State management and multi-agent coordination. |
| **Protocol** | Model Context Protocol (MCP) | Standardized tool and context sharing. |

## 🤝 Contributing

We welcome contributions! Please see our [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## 📜 License

This project is licensed under the [MIT License](LICENSE).
