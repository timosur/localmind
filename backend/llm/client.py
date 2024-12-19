import logging
from typing import Dict, List

from openai import AzureOpenAI

from config import APP_CONFIG


class LLMClient:
  def create_completion(self, messages: List[Dict], tools: List = None):
    """Handle OpenAI chat completions."""  # get the openai client

    client = AzureOpenAI(
      api_key=APP_CONFIG.openai.api_key,
      azure_endpoint=APP_CONFIG.openai.azure_endpoint,
      api_version=APP_CONFIG.openai.openai_api_version,
    )

    try:
      # make a request, passing in tools
      response = client.chat.completions.create(
        model=APP_CONFIG.openai.openai_chat_model,
        messages=messages,
        tools=tools or [],
      )

      # return the response
      return {
        "response": response.choices[0].message.content,
        "tool_calls": getattr(response.choices[0].message, "tool_calls", []),
      }
    except Exception as e:
      # error
      logging.error(f"OpenAI API Error: {str(e)}")
      raise ValueError(f"OpenAI API Error: {str(e)}")
