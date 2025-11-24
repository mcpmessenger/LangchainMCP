# LangChain Agent MCP Server

> **A production-ready MCP server exposing LangChain agent capabilities through the Model Context Protocol, deployed on Google Cloud Run.**

[![GitHub Stars](https://img.shields.io/github/stars/mcpmessenger/LangchainMCP?style=social)](https://github.com/mcpmessenger/LangchainMCP)
[![GitHub Forks](https://img.shields.io/github/forks/mcpmessenger/LangchainMCP?style=social)](https://github.com/mcpmessenger/LangchainMCP)
[![License](https://img.shields.io/github/license/mcpmessenger/LangchainMCP)](https://github.com/mcpmessenger/LangchainMCP/blob/main/LICENSE)

## 🚀 Overview

This is a **standalone backend service** that wraps a LangChain agent as a single, high-level MCP Tool. The server is built with **FastAPI** and deployed on **Google Cloud Run**, providing a scalable, production-ready solution for exposing AI agent capabilities to any MCP-compliant client.

**Live Service:** https://langchain-agent-mcp-server-554655392699.us-central1.run.app

## ✨ Features

- ✅ **MCP Compliance** - Full Model Context Protocol support
- ✅ **LangChain Agent** - Multi-step reasoning with ReAct pattern
- ✅ **Google Cloud Run** - Scalable, serverless deployment
- ✅ **Tool Support** - Extensible framework for custom tools
- ✅ **Production Ready** - Error handling, logging, and monitoring
- ✅ **Docker Support** - Containerized for easy deployment

## 🏗️ Architecture

| Component | Technology | Purpose |
| :--- | :--- | :--- |
| **Backend Framework** | FastAPI | High-performance, asynchronous web server |
| **Agent Framework** | LangChain | Multi-step reasoning and tool execution |
| **Deployment** | Google Cloud Run | Serverless, auto-scaling hosting |
| **Containerization** | Docker | Consistent deployment environment |
| **Protocol** | Model Context Protocol (MCP) | Standardized tool and context sharing |

## 🛠️ Quick Start

### Prerequisites

- Python 3.11+
- OpenAI API key
- Google Cloud account (for Cloud Run deployment)
- Docker (optional, for local testing)

### Local Development

1. **Clone the repository:**
   ```bash
   git clone https://github.com/mcpmessenger/LangchainMCP.git
   cd LangchainMCP
   ```

2. **Install dependencies:**
   ```powershell
   # Windows
   py -m pip install -r requirements.txt
   
   # Linux/Mac
   pip install -r requirements.txt
   ```

3. **Set up environment variables:**
   Create a `.env` file:
   ```env
   OPENAI_API_KEY=your-openai-api-key-here
   OPENAI_MODEL=gpt-4o-mini
   PORT=8000
   ```

4. **Run the server:**
   ```powershell
   # Windows
   py run_server.py
   
   # Linux/Mac
   python run_server.py
   ```

5. **Test the endpoints:**
   - Health: http://localhost:8000/health
   - Manifest: http://localhost:8000/mcp/manifest
   - API Docs: http://localhost:8000/docs

## ☁️ Google Cloud Run Deployment

The server is designed for deployment on **Google Cloud Run**. See our comprehensive deployment guides:

- **[DEPLOY_CLOUD_RUN_WINDOWS.md](DEPLOY_CLOUD_RUN_WINDOWS.md)** - Windows deployment guide
- **[DEPLOY_CLOUD_RUN.md](DEPLOY_CLOUD_RUN.md)** - General deployment guide
- **[QUICK_DEPLOY.md](QUICK_DEPLOY.md)** - Quick reference

### Quick Deploy

```powershell
# Windows PowerShell
.\deploy-cloud-run.ps1 -ProjectId "your-project-id" -Region "us-central1"

# Linux/Mac
./deploy-cloud-run.sh your-project-id us-central1
```

### Current Deployment

- **Service URL:** https://langchain-agent-mcp-server-554655392699.us-central1.run.app
- **Project:** slashmcp
- **Region:** us-central1
- **Status:** ✅ Live and operational

## 📡 API Endpoints

### MCP Endpoints

#### Get Manifest
```http
GET /mcp/manifest
```

Returns the MCP manifest declaring available tools.

**Response:**
```json
{
  "name": "langchain-agent-mcp-server",
  "version": "1.0.0",
  "tools": [
    {
      "name": "agent_executor",
      "description": "Execute a complex, multi-step reasoning task...",
      "inputSchema": {
        "type": "object",
        "properties": {
          "query": {
            "type": "string",
            "description": "The user's query or task"
          }
        },
        "required": ["query"]
      }
    }
  ]
}
```

#### Invoke Tool
```http
POST /mcp/invoke
Content-Type: application/json

{
  "tool": "agent_executor",
  "arguments": {
    "query": "What is the capital of France?"
  }
}
```

**Response:**
```json
{
  "content": [
    {
      "type": "text",
      "text": "The capital of France is Paris."
    }
  ],
  "isError": false
}
```

### Other Endpoints

- `GET /` - Server information
- `GET /health` - Health check
- `GET /docs` - Interactive API documentation (Swagger UI)

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `OPENAI_API_KEY` | OpenAI API key | - | ✅ Yes |
| `OPENAI_MODEL` | OpenAI model to use | `gpt-4o-mini` | No |
| `PORT` | Server port | `8000` | No |
| `API_KEY` | Optional API key for authentication | - | No |
| `MAX_ITERATIONS` | Maximum agent iterations | `10` | No |
| `VERBOSE` | Enable verbose logging | `false` | No |

## 📚 Documentation

📖 **[Full Documentation Site](https://mcpmessenger.github.io/LangchainMCP/)** - Complete documentation with examples (GitHub Pages)

**Quick Links:**
- **[Getting Started](docs/getting-started.md)** - Set up and run locally
- **[Examples](docs/examples.md)** - Code examples including **"Build a RAG agent in 10 lines"**
- **[Deployment Guide](docs/deployment.md)** - Deploy to Google Cloud Run
- **[API Reference](docs/api-reference.md)** - Complete API documentation
- **[Troubleshooting](docs/troubleshooting.md)** - Common issues and solutions

**Build Docs Locally:**
```powershell
# Windows
.\build-docs.ps1 serve

# Linux/Mac
./build-docs.sh serve
```

**Additional Guides:**
- **[README_BACKEND.md](README_BACKEND.md)** - Complete technical documentation
- **[DEPLOY_CLOUD_RUN_WINDOWS.md](DEPLOY_CLOUD_RUN_WINDOWS.md)** - Windows deployment guide
- **[INSTALL_PREREQUISITES.md](INSTALL_PREREQUISITES.md)** - Prerequisites installation
- **[SLASHMCP_INTEGRATION.md](SLASHMCP_INTEGRATION.md)** - SlashMCP integration guide

## 🧪 Testing

```powershell
# Test health endpoint
Invoke-WebRequest -Uri "https://langchain-agent-mcp-server-554655392699.us-central1.run.app/health"

# Test agent invocation
$body = @{
    tool = "agent_executor"
    arguments = @{
        query = "What is 2+2?"
    }
} | ConvertTo-Json

Invoke-WebRequest -Uri "https://langchain-agent-mcp-server-554655392699.us-central1.run.app/mcp/invoke" `
    -Method POST `
    -ContentType "application/json" `
    -Body $body
```

## 🏗️ Project Structure

```
.
├── src/
│   ├── main.py              # FastAPI application with MCP endpoints
│   ├── agent.py             # LangChain agent definition and tools
│   ├── mcp_manifest.json    # MCP manifest configuration
│   └── start.sh             # Cloud Run startup script
├── tests/
│   └── test_mcp_endpoints.py # Test suite
├── Dockerfile               # Container configuration
├── requirements.txt         # Python dependencies
├── deploy-cloud-run.ps1     # Windows deployment script
├── deploy-cloud-run.sh      # Linux/Mac deployment script
└── cloudbuild.yaml          # Cloud Build configuration
```

## 🚀 Deployment Options

### Google Cloud Run (Recommended)

- **Scalable** - Auto-scales based on traffic
- **Serverless** - Pay only for what you use
- **Managed** - No infrastructure to manage
- **Fast** - Low latency with global CDN

See [DEPLOY_CLOUD_RUN_WINDOWS.md](DEPLOY_CLOUD_RUN_WINDOWS.md) for detailed instructions.

### Docker (Local/Other Platforms)

```bash
docker build -t langchain-agent-mcp-server .
docker run -p 8000:8000 -e OPENAI_API_KEY=your-key langchain-agent-mcp-server
```

## 📊 Performance

- **P95 Latency:** < 5 seconds for standard 3-step ReAct chains
- **Scalability:** Horizontal scaling on Cloud Run
- **Uptime:** 99.9% target (Cloud Run SLA)
- **Throughput:** Handles concurrent requests efficiently

## 🔒 Security

- API key authentication (optional)
- Environment variable management
- Secret Manager integration (Cloud Run)
- HTTPS by default (Cloud Run)
- CORS configuration

## 🤝 Contributing

We welcome contributions! Please see our contributing guidelines.

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📜 License

This project is licensed under the MIT License.

## 🔗 Links

- **GitHub Repository:** https://github.com/mcpmessenger/LangchainMCP
- **Live Service:** https://langchain-agent-mcp-server-554655392699.us-central1.run.app
- **API Documentation:** https://langchain-agent-mcp-server-554655392699.us-central1.run.app/docs
- **Model Context Protocol:** https://modelcontextprotocol.io/

## 🙏 Acknowledgments

- Built with [LangChain](https://www.langchain.com/)
- Deployed on [Google Cloud Run](https://cloud.google.com/run)
- Uses [FastAPI](https://fastapi.tiangolo.com/) for the web framework

---

**Status:** ✅ Production-ready and deployed on Google Cloud Run
