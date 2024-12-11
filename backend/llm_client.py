import os
from openai import AzureOpenAI
from dotenv import load_dotenv
import logging
from typing import Dict, List

# Load environment variables
load_dotenv()


class LLMClient:
    def __init__(self):
        # set the provider, model and api key
        self.api_key = os.getenv("OPENAI_API_KEY")

        # ensure we have the api key for openai if set
        if not self.api_key:
            raise ValueError("The OPENAI_API_KEY environment variable is not set.")

    def create_completion(
        self, messages: List[Dict], tools: List = None
    ):
        """Handle OpenAI chat completions."""# get the openai client
        
        client = AzureOpenAI(
            api_key=self.api_key,
            azure_endpoint="https://renewables-openai-v3.openai.azure.com",
            api_version="2024-07-01-preview",
        )

        try:
            # make a request, passing in tools
            response = client.chat.completions.create(
                model="gpt-4o",
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
