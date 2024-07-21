import torch
from transformers import AutoTokenizer, AutoModel, GPT2Tokenizer, GPT2LMHeadModel
from src.chunker import chunk_bible
from embedder import encode
from src.generation import generate_response
from src.retriever import rag_system
import faiss
import numpy as np
import gradio as gr

# Documents corpus (replace these with your actual documents)


iface = gr.Interface(
    fn=rag_system, 
    inputs="text", 
    outputs="text",
    title="Retrieval-Augmented Generation",
    description="A simple POC for retrieval-augmented generation using Gradio."
)

iface.launch()