import logging
import os
from typing import Dict, List

from dotenv import load_dotenv
from openai import AzureOpenAI

# Load environment variables
load_dotenv()


class LLMClient:
  def __init__(self):
    # set the provider, model and api key
    self.api_key = os.getenv("AZURE_OPENAI_API_KEY")
    self.azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
    self.openai_api_version = os.getenv("AZURE_OPENAI_API_VERSION")
    self.openai_model = os.getenv("AZURE_OPENAI_CHAT_MODEL")

    # ensure we have the api key for openai if set
    if not self.api_key:
      raise ValueError("The AZURE_OPENAI_API_KEY environment variable is not set.")

    # ensure we have the deployment name for openai if set
    if not self.azure_endpoint:
      raise ValueError("The AZURE_OPENAI_ENDPOINT environment variable is not set.")

    # ensure we have the api version for openai if set
    if not self.openai_api_version:
      raise ValueError("The AZURE_OPENAI_API_VERSION environment variable is not set.")

    # ensure we have the model for openai if set
    if not self.openai_model:
      raise ValueError("The AZURE_OPENAI_CHAT_MODEL environment variable is not set.")

  def create_completion(self, messages: List[Dict], tools: List = None):
    """Handle OpenAI chat completions."""  # get the openai client

    client = AzureOpenAI(
      api_key=self.api_key,
      azure_endpoint=self.azure_endpoint,
      api_version=self.openai_api_version,
    )

    try:
      # make a request, passing in tools
      response = client.chat.completions.create(
        model=self.openai_model,
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
