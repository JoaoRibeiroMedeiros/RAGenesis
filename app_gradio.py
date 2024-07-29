# import torch
# from transformers import AutoTokenizer, AutoModel, GPT2Tokenizer, GPT2LMHeadModel
# from src.chunker import chunk_bible
# from embedder import encode
# from src.generation import generate_response
# from src.retriever import rag_system
# import faiss

import numpy as np
import gradio as gr
from src.retriever import query_holy_text
# Documents corpus (replace these with your actual documents)


iface = gr.Interface(fn=query_holy_text, 
                     inputs="text", 
                     outputs="text", 
                     title="Query the Bible verses!", 
                     description="Describe a subject you are interested in. AI will help you find the most relevant Bible verses for it!")

iface.launch(server_port=8080, server_name="0.0.0.0")

