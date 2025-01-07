import logging

from mcp import ClientSession

from llm.client import LLMClient
from tools.tools_handler import convert_to_openai_tools, fetch_tools, handle_tool_call
from chat.system_prompt import generate as generate_system_prompt


async def send_chat_message(
  client_sessions, chat_interaction_history=[], user_message=""
):
  try:
    tools = []
    for server_name, client_session in client_sessions:
      server_tools = await fetch_tools(client_session)
      tools.extend(server_tools)

    if len(tools) == 0:
      yield ("sytem", "error", "No tools available")
      return

    system_prompt = generate_system_prompt(tools)
    openai_tools = convert_to_openai_tools(tools)

    async for role, type, content, interaction_history in process_chat_message(
      client_sessions,
      system_prompt,
      openai_tools,
      chat_interaction_history,
      user_message,
    ):
      yield (role, type, content, interaction_history)

  except Exception as e:
    logging.error(f"Error in processing chat: {e}")
    yield ("system", "error", str(e))


async def process_chat_message(
  client_sessions: list[ClientSession],
  system_prompt,
  openai_tools,
  chat_interaction_history,
  user_message,
):
  client = LLMClient()
  conversation_history = [
    {"role": "system", "content": system_prompt},
    *chat_interaction_history,
  ]

  # Yield user message
  user_interaction_history = [{"role": "user", "content": user_message}]

  yield ("user", "message", user_message, user_interaction_history)

  conversation_history.extend(user_interaction_history)

  while True:
    # Process chat message
    completion = client.create_completion(
      messages=conversation_history, tools=openai_tools
    )

    response_content = completion.get("response", "No response")
    tool_calls = completion.get("tool_calls", [])

    if tool_calls:
      for tool_call in tool_calls:
        yield (
          "assistent",
          "tool_call",
          f"{tool_call.function.name}\n{tool_call.function.arguments}",
          [],
        )

        formatted_response, tool_interaction_history = await handle_tool_call(
          tool_call, conversation_history, client_sessions
        )

        yield (
          "assistent",
          "tool_response",
          formatted_response,
          tool_interaction_history,
        )

        # Append new history to the conversation
        conversation_history.extend(tool_interaction_history)

      continue

    assistant_interaction_history = [{"role": "assistant", "content": response_content}]

    # Yield assistant response
    yield ("assistent", "message", response_content, assistant_interaction_history)

    conversation_history.extend(assistant_interaction_history)

    return
