
import os
from docx2txt import process as Docx2txtLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Milvus

# Load the document
loader = Docx2txtLoader("../data/document.docx")
documents = loader.load()

# Split the document into chunks
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
docs = text_splitter.split_documents(documents)

# Perform embeddings and store in Milvus
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
vector_db = Milvus.from_documents(
    docs,
    embeddings,
    collection_name="example_collection",
    connection_args={"host": os.getenv('HOST', ''), "port": os.getenv('HOST_PORT', '')},
)

