import os
import aiohttp
from openai import OpenAI
from src.models import AgentResponse

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY environment variable is not set")

client = OpenAI(api_key=api_key)

class MCPClient:
    def __init__(self):
        self.puppeteer_url = "http://mcp-puppeteer:3000"
        self.github_url = "http://mcp-github:3001"
        self.brave_search_url = "http://mcp-brave-search:3002"
        self.sqlite_url = "http://mcp-sqlite:3003"
        
    async def query_service(self, service_url: str, endpoint: str, data: dict) -> dict:
        async with aiohttp.ClientSession() as session:
            async with session.post(f"{service_url}/{endpoint}", json=data) as response:
                return await response.json()

mcp_client = MCPClient()

async def get_agent_response(query: str = None) -> AgentResponse:
    if not query:
        return AgentResponse(message="Please provide a query", data={"status": "no_query"})
    
    try:
        # First get GPT guidance on which MCP service to use
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": """You are a helpful assistant that decides which MCP service to use.
                Available services:
                - puppeteer: For web automation
                - github: For GitHub operations
                - brave-search: For web searches
                - sqlite: For database operations"""},
                {"role": "user", "content": query}
            ]
        )
        
        service_decision = response.choices[0].message.content
        
        # Route to appropriate MCP service
        try:
            if "puppeteer" in service_decision.lower():
                result = await mcp_client.query_service(mcp_client.puppeteer_url, "automate", {"query": query})
            elif "github" in service_decision.lower():
                result = await mcp_client.query_service(mcp_client.github_url, "github", {"query": query})
            elif "brave" in service_decision.lower():
                result = await mcp_client.query_service(mcp_client.brave_search_url, "search", {"query": query})
            elif "sqlite" in service_decision.lower():
                result = await mcp_client.query_service(mcp_client.sqlite_url, "query", {"query": query})
            else:
                # Fallback to normal GPT response
                return AgentResponse(
                    message=response.choices[0].message.content,
                    data={"status": "success"}
                )
                
            return AgentResponse(
                message=result.get("message", "Operation completed"),
                data={"status": "success", "result": result}
            )
            
        except Exception as mcp_error:
            return AgentResponse(
                message=f"MCP Service Error: {str(mcp_error)}",
                data={"status": "error", "error_type": "mcp_error"}
            )
            
    except Exception as e:
        error_message = str(e)
        if "api_key" in error_message.lower():
            error_message = "OpenAI API key is invalid or not properly configured"
        return AgentResponse(
            message=f"Error: {error_message}",
            data={"status": "error", "error_type": "api_error"}
        )
