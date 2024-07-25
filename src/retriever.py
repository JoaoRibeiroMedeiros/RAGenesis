import torch
from transformers import AutoTokenizer, AutoModel, GPT2Tokenizer, GPT2LMHeadModel
from chunker import chunk_bible
from embedder import encode
from generation import generate_response
import faiss
import numpy as np
import gradio as gr

# Documents corpus (replace these with your actual documents)

def rag_system(query):
    documents = chunk_bible('sacred_data/bible.txt')
    document_embeddings = encode(documents)

    index = faiss.IndexFlatL2(document_embeddings.shape[1])
    index.add(document_embeddings)
    # Step 1: Retrieve relevant documents
    query_embedding = encode([query])[0]
    top_k = 3  # Number of documents to retrieve
    distances, indices = index.search(np.array([query_embedding]), top_k)
    retrieved_docs = [documents[i] for i in indices[0]]

    # Step 2: Generate a response using the retrieved documents
    response = generate_response(query, retrieved_docs)
    return response
