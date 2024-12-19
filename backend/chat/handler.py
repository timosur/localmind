import logging

from mcp import ClientSession

from llm.client import LLMClient
from tools.tools_handler import convert_to_openai_tools, fetch_tools, handle_tool_call
from chat.system_prompt import generate as generate_system_prompt


async def send_chat_message(
  client_sessions, user_conversation_history=[], user_message=""
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
    tools = []
    for server_name, client_session in client_sessions:
      server_tools = await fetch_tools(client_session)
      tools.extend(server_tools)

    if len(tools) == 0:
      yield {"error": "No tools available"}
      return

    system_prompt = generate_system_prompt(tools)
    openai_tools = convert_to_openai_tools(tools)

    async for msg in process_chat_message(
      client_sessions,
      system_prompt,
      openai_tools,
      user_conversation_history,
      user_message,
    ):
      yield msg

  except Exception as e:
    logging.debug(e)
    logging.debug(f"[red]Error in processing chat:[/red] {e}")
    yield {"type": "error", "content": str(e)}


async def process_chat_message(
  client_sessions: list[ClientSession],
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
          tool_call, conversation_history, client_sessions
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
