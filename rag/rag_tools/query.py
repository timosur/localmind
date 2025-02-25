from langchain.prompts import ChatPromptTemplate, PromptTemplate
from langchain.retrievers.multi_query import MultiQueryRetriever
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import AzureChatOpenAI

from db.vector import get as get_vector_db
from config.env import (
  AZURE_OPENAI_API_KEY,
  AZURE_OPENAI_API_VERSION,
  AZURE_OPENAI_CHAT_MODEL,
  AZURE_OPENAI_ENDPOINT,
)


# Function to get the prompt templates for generating alternative questions and answering based on context
def get_prompt():
  QUERY_PROMPT = PromptTemplate(
    input_variables=["question"],
    template="""You are an AI language model assistant. Your task is to generate five
        different versions of the given user question to retrieve relevant documents from
        a vector database. By generating multiple perspectives on the user question, your
        goal is to help the user overcome some of the limitations of the distance-based
        similarity search. Provide these alternative questions separated by newlines.
        Original question: {question}""",
  )

  template = """Answer the question based ONLY on the following context:
    {context}
    Question: {question}
    """

  prompt = ChatPromptTemplate.from_template(template)

  return QUERY_PROMPT, prompt


# Main function to handle the query process
def query(vector_collection_id, input):
  if input:
    # Initialize the language model with the specified model name
    llm = AzureChatOpenAI(
      openai_api_key=AZURE_OPENAI_API_KEY,
      azure_deployment=AZURE_OPENAI_CHAT_MODEL,
      api_version=AZURE_OPENAI_API_VERSION,
      azure_endpoint=AZURE_OPENAI_ENDPOINT,
    )
    # Get the vector database instance
    db = get_vector_db(vector_collection_id)
    # Get the prompt templates
    QUERY_PROMPT, prompt = get_prompt()

    # Set up the retriever to generate multiple queries using the language model and the query prompt
    retriever = MultiQueryRetriever.from_llm(
      db.as_retriever(), llm, prompt=QUERY_PROMPT
    )

    # Define the processing chain to retrieve context, generate the answer, and parse the output
    chain = (
      {"context": retriever, "question": RunnablePassthrough()}
      | prompt
      | llm
      | StrOutputParser()
    )

    response = chain.invoke(input)

    return response

  return None
