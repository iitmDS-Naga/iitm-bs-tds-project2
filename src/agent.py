import os
from openai import OpenAI
from src.models import AgentResponse

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY environment variable is not set")

client = OpenAI(api_key=api_key)

async def get_agent_response(query: str = None) -> AgentResponse:
    if not query:
        return AgentResponse(
            message="Please provide a query",
            data={"status": "no_query"}
        )
    
    try:
        if not api_key:
            return AgentResponse(
                message="OpenAI API key not configured",
                data={"status": "error", "error": "api_key_missing"}
            )
            
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": query}
            ]
        )
        
        return AgentResponse(
            message=response.choices[0].message.content,
            data={"status": "success"}
        )
    except Exception as e:
        error_message = str(e)
        if "api_key" in error_message.lower():
            error_message = "OpenAI API key is invalid or not properly configured"
        return AgentResponse(
            message=f"Error: {error_message}",
            data={"status": "error", "error_type": "api_error"}
        )
