"""
FastAPI Application - LangChain Agent MCP Server

This module implements the FastAPI application with MCP endpoints.
"""

import json
import logging
import os
from pathlib import Path
from typing import Dict, Any, Optional
from fastapi import FastAPI, HTTPException, Header
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from dotenv import load_dotenv

from src.agent import get_agent

# Load environment variables from project root
project_root = Path(__file__).parent.parent
env_file = project_root / ".env"
if env_file.exists():
    load_dotenv(env_file)
else:
    # Fallback to current directory
    load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="LangChain Agent MCP Server",
    description="MCP-compliant server exposing LangChain agent capabilities",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("CORS_ORIGINS", "*").split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Request/Response Models
class MCPInvokeRequest(BaseModel):
    """MCP Invoke Request Model"""
    tool: str = Field(..., description="The name of the tool to invoke")
    arguments: Dict[str, Any] = Field(..., description="Tool arguments")


class MCPErrorResponse(BaseModel):
    """MCP Error Response Model"""
    error: str = Field(..., description="Error message")
    code: Optional[str] = Field(None, description="Error code")


class MCPSuccessResponse(BaseModel):
    """MCP Success Response Model"""
    content: list = Field(..., description="Response content")
    isError: bool = Field(False, description="Whether this is an error response")


@app.on_event("startup")
async def startup_event():
    """Initialize the agent on server startup"""
    logger.info("Starting LangChain Agent MCP Server...")
    try:
        # Initialize the agent (lazy loading - will initialize on first use)
        # Don't fail startup if API key is missing - will fail on first request instead
        if os.getenv("OPENAI_API_KEY"):
            agent = get_agent()
            logger.info("Server started successfully. Agent ready.")
        else:
            logger.warning("OPENAI_API_KEY not set. Agent will initialize on first request.")
            logger.info("Server started successfully. Agent will initialize on first use.")
    except Exception as e:
        logger.error(f"Failed to initialize agent: {e}")
        # Don't raise - allow server to start, will fail on first request
        logger.warning("Server starting without agent pre-initialization")


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "name": "LangChain Agent MCP Server",
        "version": "1.0.0",
        "status": "running",
        "endpoints": {
            "manifest": "/mcp/manifest",
            "invoke": "/mcp/invoke"
        }
    }


@app.get("/health")
async def health():
    """Health check endpoint"""
    return {"status": "healthy"}


@app.get("/mcp/manifest")
async def get_manifest():
    """
    MCP Manifest Endpoint (FR1)
    
    Returns the MCP manifest JSON declaring the wrapped LangChain agent as a tool.
    """
    logger.info("GET /mcp/manifest - Returning manifest")
    try:
        manifest_path = os.path.join(
            os.path.dirname(__file__),
            "mcp_manifest.json"
        )
        with open(manifest_path, "r") as f:
            manifest = json.load(f)
        return manifest
    except FileNotFoundError:
        logger.error("Manifest file not found")
        raise HTTPException(status_code=500, detail="Manifest file not found")
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON in manifest: {e}")
        raise HTTPException(status_code=500, detail="Invalid manifest format")
    except Exception as e:
        logger.error(f"Error loading manifest: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/mcp/invoke")
async def invoke_tool(
    request: MCPInvokeRequest,
    authorization: Optional[str] = Header(None)
):
    """
    MCP Invoke Endpoint (FR2, FR3, FR4, FR6)
    
    Accepts a POST request with MCP invocation payload, executes the LangChain agent,
    and returns the result in MCP response format.
    """
    logger.info(f"POST /mcp/invoke - Tool: {request.tool}")
    
    # Optional API key authentication (NFR2)
    api_key = os.getenv("API_KEY")
    if api_key and authorization != f"Bearer {api_key}":
        logger.warning("Unauthorized request - invalid or missing API key")
        raise HTTPException(
            status_code=401,
            detail="Unauthorized - Invalid or missing API key"
        )
    
    # Validate tool name
    if request.tool != "agent_executor":
        logger.warning(f"Unknown tool requested: {request.tool}")
        return JSONResponse(
            status_code=400,
            content={
                "error": f"Unknown tool: {request.tool}",
                "code": "UNKNOWN_TOOL"
            }
        )
    
    # Extract user query from arguments (FR3)
    query = request.arguments.get("query")
    if not query:
        logger.warning("Missing 'query' in arguments")
        return JSONResponse(
            status_code=400,
            content={
                "error": "Missing required argument: 'query'",
                "code": "MISSING_ARGUMENT"
            }
        )
    
    logger.info(f"Executing agent with query: {query[:100]}...")
    
    try:
        # Get the agent executor
        agent_executor = get_agent()
        
        # Execute the agent (FR3)
        result = agent_executor.invoke({"input": query})
        
        # Extract the final answer
        final_answer = result.get("output", "No output generated")
        
        logger.info("Agent execution completed successfully")
        
        # Map result to MCP response format (FR4)
        return {
            "content": [
                {
                    "type": "text",
                    "text": final_answer
                }
            ],
            "isError": False
        }
        
    except Exception as e:
        # Error handling (FR6)
        logger.error(f"Error during agent execution: {e}", exc_info=True)
        return JSONResponse(
            status_code=500,
            content={
                "content": [
                    {
                        "type": "text",
                        "text": f"Agent execution failed: {str(e)}"
                    }
                ],
                "isError": True
            }
        )


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", "8000"))
    host = os.getenv("HOST", "0.0.0.0")
    uvicorn.run(app, host=host, port=port)

