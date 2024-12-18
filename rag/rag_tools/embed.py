import os
from datetime import datetime

from db.vector import get as get_vector_db
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from werkzeug.utils import secure_filename

TEMP_FOLDER = os.getenv("TEMP_FOLDER", "./_temp")


# Function to check if the uploaded file is allowed (only PDF files)
def allowed_file(filename):
  return "." in filename and filename.rsplit(".", 1)[1].lower() in {"pdf"}


# Function to save the uploaded file to the temporary folder
def save_file(file):
  # Save the uploaded file with a secure filename and return the file path
  ct = datetime.now()
  ts = ct.timestamp()
  filename = str(ts) + "_" + secure_filename(file.filename)
  file_path = os.path.join(TEMP_FOLDER, filename)
  file.save(file_path)

  return file_path


# Function to load and split the data from the PDF file
def load_and_split_data(file_path):
  # Load the PDF file and split the data into chunks
  loader = PyPDFLoader(file_path)
  data = loader.load()
  text_splitter = RecursiveCharacterTextSplitter(chunk_size=7500, chunk_overlap=100)
  chunks = text_splitter.split_documents(data)

  print(chunks)

  return chunks


# Main function to handle the embedding process
def embed_file(vector_collection_id, file_path):
  # Check if the file is valid, load and split the data, add to the database, and remove the temporary file
  if os.path.isfile(file_path) and allowed_file(file_path):
    chunks = load_and_split_data(file_path)
    db = get_vector_db(vector_collection_id)
    db.add_documents(chunks)
    db.persist()

    return True

  return False
