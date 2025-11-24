"""
LangChain Agent Definition and Tools

This module defines the LangChain agent with its tools and execution logic.
"""

import os
from typing import List, Optional
from langchain_openai import ChatOpenAI
from langchain.tools import Tool
from langchain.agents import AgentExecutor, create_react_agent
from langchain import hub
from langchain.prompts import PromptTemplate
import logging

logger = logging.getLogger(__name__)


def search_web(query: str) -> str:
    """
    Search the web for information.
    
    This is a placeholder tool. In production, you would integrate with
    a real search API like Tavily, Serper, or Google Search.
    
    Args:
        query: The search query
        
    Returns:
        Search results as a string
    """
    logger.info(f"Searching web for: {query}")
    # Placeholder implementation
    return f"Search results for '{query}': This is a placeholder. Integrate with a real search API in production."


def get_weather(location: str) -> str:
    """
    Get weather information for a location.
    
    This is a placeholder tool. In production, you would integrate with
    a weather API like OpenWeatherMap.
    
    Args:
        location: The location to get weather for
        
    Returns:
        Weather information as a string
    """
    logger.info(f"Getting weather for: {location}")
    # Placeholder implementation
    return f"Weather for {location}: This is a placeholder. Integrate with a real weather API in production."


def create_agent_tools() -> List[Tool]:
    """
    Create the list of tools available to the agent.
    
    Returns:
        List of Tool objects
    """
    tools = [
        Tool(
            name="search_web",
            func=search_web,
            description="Search the web for current information. Use this tool when you need to find recent information, facts, or data that might not be in your training data. Input should be a search query string."
        ),
        Tool(
            name="get_weather",
            func=get_weather,
            description="Get current weather information for a specific location. Input should be a location name (e.g., 'New York', 'London')."
        ),
    ]
    return tools


def initialize_agent() -> AgentExecutor:
    """
    Initialize the LangChain agent with tools.
    
    The agent is initialized once at server startup and reused for all requests.
    
    Returns:
        AgentExecutor instance
    """
    logger.info("Initializing LangChain agent...")
    
    # Get OpenAI API key from environment
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        logger.warning("OPENAI_API_KEY not set. Agent will use default or fail.")
    
    # Initialize the LLM
    llm = ChatOpenAI(
        model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
        temperature=0,
        api_key=api_key,
    )
    
    # Get tools
    tools = create_agent_tools()
    
    # Try to pull the ReAct prompt from LangChain Hub
    try:
        prompt = hub.pull("hwchase17/react")
        logger.info("Loaded ReAct prompt from LangChain Hub")
    except Exception as e:
        logger.warning(f"Could not load prompt from hub: {e}. Using default prompt.")
        # Fallback to a basic ReAct prompt
        prompt = PromptTemplate.from_template(
            """You are a helpful AI assistant. You have access to the following tools:

{tools}

Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Begin!

Question: {input}
Thought: {agent_scratchpad}"""
        )
    
    # Create the agent
    agent = create_react_agent(llm, tools, prompt)
    
    # Create the agent executor
    agent_executor = AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=os.getenv("VERBOSE", "false").lower() == "true",
        handle_parsing_errors=True,
        max_iterations=int(os.getenv("MAX_ITERATIONS", "10")),
    )
    
    logger.info("Agent initialized successfully")
    return agent_executor


# Global agent instance (initialized at startup)
_agent_executor: Optional[AgentExecutor] = None


def get_agent() -> AgentExecutor:
    """
    Get the global agent executor instance.
    
    Returns:
        AgentExecutor instance
    """
    global _agent_executor
    if _agent_executor is None:
        _agent_executor = initialize_agent()
    return _agent_executor

