import numpy as np
import gradio as gr
from src.retriever import *
# from src.generation import generate_response

# Documents corpus (replace these with your actual documents)

def connect_and_query_holy_text(query):

    with open('config.json', 'r') as file:
        config = json.load(file)
    # Fetch the EC2 public IP
    ec2_public_ip = config['EC2_PUBLIC_IP']
    results_as_dicts = query_holy_text(query, ec2_public_ip)
    results_as_text = [result["reference"]+ ' - '+ result["verse"] for result in results_as_dicts]
    return results_as_text


iface = gr.Interface(fn=connect_and_query_holy_text, 
                     inputs="text", 
                     outputs="text", 
                     title="Query the Bible verses!", 
                     description="Describe a subject you are interested in. AI will help you find the most relevant Bible verses for it!")

iface.launch(server_port=8080, server_name="0.0.0.0")

