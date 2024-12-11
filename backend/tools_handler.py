import json
import logging
import re
from typing import Optional, Dict, Any
from messages.tools import send_call_tool, send_tools_list

def parse_tool_response(response: str) -> Optional[Dict[str, Any]]:
    """Parse tool call from Llama's XML-style format."""
    function_regex = r"<function=(\w+)>(.*?)</function>"
    match = re.search(function_regex, response)
    
    if match:
        function_name, args_string = match.groups()
        try:
            args = json.loads(args_string)
            return {
                "function": function_name,
                "arguments": args,
            }
        except json.JSONDecodeError as error:
            logging.debug(f"Error parsing function arguments: {error}")
    return None

async def handle_tool_call(tool_call, conversation_history, read_stream, write_stream):
    """
    Handle a single tool call for both OpenAI and Llama formats.
    This function no longer prints directly to stdout. It updates the conversation_history
    with the tool call and its response. The calling function can then display the results.
    """
    tool_name = "unknown_tool"
    raw_arguments = {}
    
    try:
        tool_name = tool_call.function.name
        raw_arguments = tool_call.function.arguments

        # Parse the tool arguments
        if raw_arguments is not None and raw_arguments != "":
            tool_args = json.loads(raw_arguments) if isinstance(raw_arguments, str) else raw_arguments
        else:
            tool_args = {}
        
        logging.debug(f"Calling tool '{tool_name}' with arguments: {tool_args}")
        
        # Call the tool (no direct print here)
        tool_response = await send_call_tool(tool_name, tool_args, read_stream, write_stream)
        
        logging.debug(f"Tool '{tool_name}' Response: {tool_response}")
        
        if tool_response is None:
            logging.debug(f"Tool '{tool_name}' did not return a response.")
            raise Exception(f"Tool '{tool_name}' did not return a response.")
        
        if tool_response.get("isError"):
            logging.debug(f"Error calling tool '{tool_name}': {tool_response.get('error')}")
            raise Exception(f"Error calling tool '{tool_name}': {tool_response.get('error')}")

        # Format the tool response
        formatted_response = format_tool_response(tool_response.get("content", []))
        logging.debug(f"Tool '{tool_name}' Response: {formatted_response}")

        tool_interaction_history = []

        # Update the conversation history with the tool call
        # Add the tool call itself (for OpenAI tracking)
        tool_interaction_history.append({
            "role": "assistant",
            "content": None,
            "tool_calls": [{
                "id": f"call_{tool_name}",
                "type": "function",
                "function": {
                    "name": tool_name,
                    "arguments": json.dumps(tool_args) if isinstance(tool_args, dict) else tool_args
                }
            }]
        })

        # Add the tool response to conversation history
        tool_interaction_history.append({
            "role": "tool",
            "name": tool_name,
            "content": formatted_response,
            "tool_call_id": f"call_{tool_name}"
        })
        
        return formatted_response, tool_interaction_history

    except json.JSONDecodeError:
        logging.debug(f"Error decoding arguments for tool '{tool_name}': {raw_arguments}")
    except Exception as e:
        logging.debug(f"Error handling tool call '{tool_name}': {str(e)}")

def format_tool_response(response_content):
    """Format the response content from a tool."""
    if isinstance(response_content, list):
        return "\n".join(
            item.get("text", "No content") for item in response_content if item.get("type") == "text"
        )
    return str(response_content)

async def fetch_tools(read_stream, write_stream):
    """Fetch tools from the server."""
    logging.debug("\nFetching tools for chat mode...")

    # get the tools list
    tools_response = await send_tools_list(read_stream, write_stream)
    tools = tools_response.get("tools", [])

    # check if tools are valid
    if not isinstance(tools, list) or not all(isinstance(tool, dict) for tool in tools):
        logging.debug("Invalid tools format received.")
        return None
    
    return tools

def convert_to_openai_tools(tools):
    """Convert tools into OpenAI-compatible function definitions."""
    return [
        {
            "type": "function",
            "function": {
                "name": tool["name"],
                "parameters": tool.get("inputSchema", {}),
            },
        }
        for tool in tools
    ]
