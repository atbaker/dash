"""
Shared chat service for DASH AI agent integration.
Provides both streaming and non-streaming interfaces to DigitalOcean Agent.
"""
import asyncio
from typing import AsyncGenerator, List, Dict, Any
from openai import OpenAI


async def get_chat_response(client: OpenAI, message: str, history: List[Dict[str, str]]) -> str:
    """Get complete chat response from DigitalOcean Agent (non-streaming)."""
    try:
        # Build full conversation messages including history
        messages = []
        messages.extend(history)
        messages.append({"role": "user", "content": message})
        
        # Create non-streaming request with debugging parameters
        response = client.chat.completions.create(
            model="n/a",  # Model is configured in DO Agent
            messages=messages,
            stream=False,
            extra_body={
                "include_retrieval_info": True,
                "include_functions_info": True,
                "include_guardrails_info": True
            }
        )
        
        # Log debugging info if available (for tool call performance monitoring)
        if hasattr(response, 'usage') and response.usage:
            print(f"DEBUG: Token usage - {response.usage}")
        if hasattr(response, 'system_fingerprint'):
            print(f"DEBUG: System fingerprint - {response.system_fingerprint}")
        
        return response.choices[0].message.content or ""
        
    except Exception as e:
        return f"Error: {str(e)}"


async def stream_chat_response(client: OpenAI, message: str, history: List[Dict[str, str]]) -> AsyncGenerator[str, None]:
    """Stream chat response from DigitalOcean Agent."""
    try:        
        # Build full conversation messages including history
        messages = []
        messages.extend(history)
        messages.append({"role": "user", "content": message})
        
        # Create streaming request with debugging parameters
        stream = client.chat.completions.create(
            model="n/a",  # Model is configured in DO Agent
            messages=messages,
            stream=True,
            extra_body={
                "include_retrieval_info": True,
                "include_functions_info": True,
                "include_guardrails_info": True
            }
        )
        
        # Stream chunks
        for chunk in stream:
            if chunk.choices[0].delta.content:
                content = chunk.choices[0].delta.content
                yield content
                # Small delay to ensure chunk is sent
                await asyncio.sleep(0.01)
                
    except Exception as e:
        yield f"Error: {str(e)}"