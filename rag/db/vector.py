from langchain_chroma import Chroma
from langchain_openai import AzureOpenAIEmbeddings

from config.env import (
  AZURE_OPENAI_API_KEY,
  AZURE_OPENAI_API_VERSION,
  AZURE_OPENAI_EMBEDDINGS_MODEL,
  AZURE_OPENAI_ENDPOINT,
  CHROMA_PATH,
  CHROMA_COLLECTION_NAME,
)


def get(vector_collection_id):
  embeddings = AzureOpenAIEmbeddings(
    openai_api_key=AZURE_OPENAI_API_KEY,
    azure_endpoint=AZURE_OPENAI_ENDPOINT,
    azure_deployment=AZURE_OPENAI_EMBEDDINGS_MODEL,
    api_version=AZURE_OPENAI_API_VERSION,
  )

  db = Chroma(
    collection_name=CHROMA_COLLECTION_NAME + "-" + vector_collection_id,
    persist_directory=CHROMA_PATH,
    embedding_function=embeddings,
  )

  return db
