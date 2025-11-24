# LangChain Agent MCP Server

A robust, standalone backend service that exposes the advanced reasoning and tool-use capabilities of a LangChain agent to any Model Context Protocol (MCP) compliant client.

## Overview

This server acts as a bridge, wrapping a complex, multi-step LangChain agent as a single, high-level **MCP Tool**. This abstraction allows LLMs within MCP clients to delegate complex tasks to the specialized LangChain agent via a simple, standardized API call.

## Features

- ✅ **MCP Compliance**: Full compliance with Model Context Protocol specifications
- ✅ **LangChain Integration**: Built with LangChain/LangGraph for production-ready agents
- ✅ **Tool Support**: Configurable tools (web search, weather, etc.)
- ✅ **Error Handling**: Comprehensive error handling with structured responses
- ✅ **Authentication**: Optional API key-based authentication
- ✅ **Docker Support**: Containerized for easy deployment
- ✅ **Logging**: Comprehensive logging for observability

## Quick Start

### Prerequisites

- Python 3.11+
- OpenAI API key (or compatible LLM provider)
- Docker (optional, for containerized deployment)

### Installation

1. **Clone the repository** (if not already done):
   ```bash
   git clone <repository-url>
   cd restful-data-gateway-main
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   
   **On Windows:**
   ```powershell
   py -m pip install -r requirements.txt
   ```
   
   **On Linux/Mac:**
   ```bash
   pip install -r requirements.txt
   ```
   
   Note: If you encounter issues with `pip` not being recognized on Windows, use `py -m pip` instead.

4. **Set up environment variables**:
   Create a `.env` file in the root directory:
   ```env
   OPENAI_API_KEY=your-api-key-here
   OPENAI_MODEL=gpt-4o-mini
   PORT=8000
   HOST=0.0.0.0
   VERBOSE=false
   MAX_ITERATIONS=10
   API_KEY=optional-api-key-for-authentication
   CORS_ORIGINS=*
   ```
   
   **Important**: The `.env` file is automatically loaded from the project root. Make sure your API key is set correctly.

5. **Run the server**:
   
   **Recommended (using helper script):**
   ```bash
   py run_server.py
   ```
   or on Linux/Mac:
   ```bash
   python run_server.py
   ```
   
   **Alternative methods:**
   ```bash
   python -m src.main
   ```
   
   Or using uvicorn directly:
   ```bash
   uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload
   ```

The server will be available at `http://localhost:8000`

## API Endpoints

### Root Endpoint
- **GET** `/` - Server information and available endpoints

### Health Check
- **GET** `/health` - Health check endpoint

### MCP Endpoints

#### Get Manifest
- **GET** `/mcp/manifest`
- Returns the MCP manifest JSON declaring available tools
- **Response**: JSON object with tool definitions

#### Invoke Tool
- **POST** `/mcp/invoke`
- Executes the LangChain agent with a user query
- **Request Body**:
  ```json
  {
    "tool": "agent_executor",
    "arguments": {
      "query": "What is the weather in New York?"
    }
  }
  ```
- **Response**:
  ```json
  {
    "content": [
      {
        "type": "text",
        "text": "Agent response here..."
      }
    ],
    "isError": false
  }
  ```

## Docker Deployment

### Build the Docker image:
```bash
docker build -t langchain-agent-mcp-server .
```

### Run the container:
```bash
docker run -p 8000:8000 \
  -e OPENAI_API_KEY=your-api-key \
  -e OPENAI_MODEL=gpt-4o-mini \
  langchain-agent-mcp-server
```

### Using Docker Compose:
Create a `docker-compose.yml`:
```yaml
version: '3.8'
services:
  mcp-server:
    build: .
    ports:
      - "8000:8000"
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - OPENAI_MODEL=${OPENAI_MODEL:-gpt-4o-mini}
      - API_KEY=${API_KEY}
    env_file:
      - .env
```

Then run:
```bash
docker-compose up
```

## Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `OPENAI_API_KEY` | OpenAI API key (required) | - |
| `OPENAI_MODEL` | OpenAI model to use | `gpt-4o-mini` |
| `PORT` | Server port | `8000` |
| `HOST` | Server host | `0.0.0.0` |
| `API_KEY` | Optional API key for authentication | - |
| `VERBOSE` | Enable verbose agent logging | `false` |
| `MAX_ITERATIONS` | Maximum agent iterations | `10` |
| `CORS_ORIGINS` | Comma-separated CORS origins | `*` |

## Testing

Run the test suite:
```bash
py -m pytest tests/ -v
```
or on Linux/Mac:
```bash
pytest tests/ -v
```

For tests that require API access, set `OPENAI_API_KEY` in your `.env` file or environment.

## Project Structure

```
.
├── src/
│   ├── __init__.py
│   ├── main.py              # FastAPI application, MCP endpoints
│   ├── agent.py             # LangChain agent definition and tools
│   └── mcp_manifest.json    # Static manifest file
├── tests/
│   ├── __init__.py
│   └── test_mcp_endpoints.py
├── Dockerfile
├── requirements.txt
├── README_BACKEND.md
└── .env                      # Environment variables (create this)
```

## Customizing the Agent

### Adding New Tools

Edit `src/agent.py` and add new tools to the `create_agent_tools()` function:

```python
def my_custom_tool(query: str) -> str:
    """Description of what the tool does."""
    # Implementation here
    return result

def create_agent_tools() -> List[Tool]:
    tools = [
        # ... existing tools ...
        Tool(
            name="my_custom_tool",
            func=my_custom_tool,
            description="Description for the LLM"
        ),
    ]
    return tools
```

### Changing the Agent Prompt

The agent uses the ReAct prompt from LangChain Hub by default. To customize:

1. Modify the prompt loading in `src/agent.py`
2. Or create a custom prompt template

## Architecture

The server follows a simple, stateless architecture:

1. **Agent Initialization**: The LangChain agent is initialized once at server startup
2. **Request Handling**: FastAPI handles incoming HTTP requests
3. **Manifest Endpoint**: Returns static JSON from `mcp_manifest.json`
4. **Invoke Endpoint**: Executes the pre-initialized agent and returns results

## Security Considerations

- Set `API_KEY` environment variable to enable authentication
- Use environment variables for sensitive data (never commit `.env`)
- Deploy behind a firewall for production
- Consider rate limiting for production deployments

## Performance

- **Stateless Design**: Allows horizontal scaling
- **Agent Reuse**: Agent initialized once, reused for all requests
- **Target Latency**: P95 under 5 seconds for standard 3-step ReAct chain

## Troubleshooting

### Agent fails to initialize
- Check that `OPENAI_API_KEY` is set correctly
- Verify the API key has sufficient credits
- Check logs for specific error messages

### Slow responses
- Reduce `MAX_ITERATIONS` if agent is taking too long
- Consider using a faster model (e.g., `gpt-4o-mini` instead of `gpt-4`)
- Check network latency to OpenAI API

### Authentication errors
- Verify `API_KEY` is set if authentication is enabled
- Check that the `Authorization: Bearer <key>` header is included in requests

## License

See the main project LICENSE file.

## Windows-Specific Notes

### Using Python on Windows

On Windows, you may need to use `py` instead of `python`:
- `py -m pip install -r requirements.txt`
- `py run_server.py`
- `py -m pytest tests/ -v`

### Environment Variables

The `.env` file is automatically loaded from the project root. Make sure:
- The file is named exactly `.env` (with the dot)
- It's located in the project root directory
- The API key is on a single line without quotes

## References

- [Model Context Protocol](https://modelcontextprotocol.io/)
- [LangChain Documentation](https://docs.langchain.com/)
- [LangGraph Documentation](https://docs.langchain.com/oss/python/langgraph/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)

## Additional Resources

- **Client Handoff Document:** See `CLIENT_HANDOFF.md` for a client-facing overview
- **Product Requirements:** See `Product Requirements Document_ LangChain Agent MCP Server.md` for original specifications

