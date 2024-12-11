from llm_client import LLMClient
from tools_handler import handle_tool_call, convert_to_openai_tools, fetch_tools
from system_prompt_generator import SystemPromptGenerator
from rich import print
import logging
import asyncio


async def send_chat_message(
    read_stream, write_stream, user_conversation_history=[], user_message=""
):
    """Process the conversation loop, handling tool calls and responses.
    Yields different types of messages for streaming the conversation flow.

    Types of yielded messages:
    - message: User or assistant messages
    - tool_call: Function calls made by the assistant
    - tool_result: Results from tool executions
    - content: Content responses from the assistant
    """
    try:
        tools = await fetch_tools(read_stream, write_stream)
        if not tools:
            yield {"error": "No tools available"}
            return

        system_prompt = generate_system_prompt(tools)
        openai_tools = convert_to_openai_tools(tools)

        return await process_chat_message(
            read_stream,
            write_stream,
            system_prompt,
            openai_tools,
            user_conversation_history,
            user_message,
        )

    except Exception as e:
        logging.debug(e)
        logging.debug(f"[red]Error in processing chat:[/red] {e}")
        yield {"type": "error", "content": str(e)}


async def process_chat_message(
    read_stream,
    write_stream,
    system_prompt,
    openai_tools,
    user_conversation_history,
    user_message,
):
    client = LLMClient()
    conversation_history = [
        {"role": "system", "content": system_prompt},
        *user_conversation_history,
    ]

    # Yield user message
    yield {"type": "message", "role": "user", "content": user_message}

    conversation_history.append({"role": "user", "content": user_message})

    while True:
        # Process chat message
        completion = client.create_completion(
            messages=conversation_history, tools=openai_tools
        )

        response_content = completion.get("response", "No response")
        tool_calls = completion.get("tool_calls", [])

        if tool_calls:
            for tool_call in tool_calls:
                yield {
                    "type": "tool_call",
                    "content": {
                        "name": tool_call.function.name,
                        "arguments": tool_call.function.arguments,
                    },
                }

                formatted_response, tool_interaction_history = await handle_tool_call(
                    tool_call, conversation_history, read_stream, write_stream
                )

                yield {"type": "tool_call_response", "content": formatted_response}

                # Append new history to the conversation
                conversation_history.extend(tool_interaction_history)
            logging.info(
                "Continue to the next iteration of the while loop, further processing the conversation"
            )
            continue

        # Assistant panel with Markdown
        conversation_history.append({"role": "assistant", "content": response_content})

        yield {"type": "content", "content": response_content}

        return


def generate_system_prompt(tools):
    """
    Generate a concise system prompt for the assistant.
    This prompt is internal and not displayed to the user.
    """
    prompt_generator = SystemPromptGenerator()
    tools_json = {"tools": tools}

    system_prompt = prompt_generator.generate_prompt(tools_json)
    system_prompt += """

**GENERAL GUIDELINES:**

1. Step-by-step reasoning:
   - Analyze tasks systematically.
   - Break down complex problems into smaller, manageable parts.
   - Verify assumptions at each step to avoid errors.
   - Reflect on results to improve subsequent actions.

2. Effective tool usage:
   - Explore:
     - Identify available information and verify its structure.
     - Check assumptions and understand data relationships.
   - Iterate:
     - Start with simple queries or actions.
     - Build upon successes, adjusting based on observations.
   - Handle errors:
     - Carefully analyze error messages.
     - Use errors as a guide to refine your approach.
     - Document what went wrong and suggest fixes.

3. Clear communication:
   - Explain your reasoning and decisions at each step.
   - Share discoveries transparently with the user.
   - Outline next steps or ask clarifying questions as needed.

EXAMPLES OF BEST PRACTICES:

- Working with databases:
  - Check schema before writing queries.
  - Verify the existence of columns or tables.
  - Start with basic queries and refine based on results.

- Processing data:
  - Validate data formats and handle edge cases.
  - Ensure integrity and correctness of results.

- Accessing resources:
  - Confirm resource availability and permissions.
  - Handle missing or incomplete data gracefully.

REMEMBER:
- Be thorough and systematic.
- Each tool call should have a clear and well-explained purpose.
- Make reasonable assumptions if ambiguous.
- Minimize unnecessary user interactions by providing actionable insights.

EXAMPLES OF ASSUMPTIONS:
- Default sorting (e.g., descending order) if not specified.
- Assume basic user intentions, such as fetching top results by a common metric.
"""
    return system_prompt
