
import torch
from transformers import AutoTokenizer, AutoModel

# Documents corpus (replace these with your actual documents)
documents = [
    "Deep learning is a subset of machine learning.",
    "Natural Language Processing is a fascinating field.",
    "GPT models are quite powerful for text generation.",
    "Autonomous vehicles use multiple AI technologies.",
    "Python is a popular programming language."
]


# Load a transformer model for embeddings
tokenizer = AutoTokenizer.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")
model = AutoModel.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")

def encode(texts):
    encoded_input = tokenizer(texts, padding=True, truncation=True, return_tensors='pt')
    with torch.no_grad():
        model_output = model(**encoded_input)
    embeddings = model_output.last_hidden_state.mean(dim=1)
    return embeddings.cpu().numpy()

document_embeddings = encode(documents)
index = faiss.IndexFlatL2(document_embeddings.shape[1])
index.add(document_embeddings)

gpt2_tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
gpt2_model = GPT2LMHeadModel.from_pretrained("gpt2")

def generate_response(query, retrieved_docs):
    context = " ".join(retrieved_docs) + " " + query
    inputs = gpt2_tokenizer.encode(context, return_tensors="pt")
    outputs = gpt2_model.generate(inputs, max_length=100, num_return_sequences=1)
    response = gpt2_tokenizer.decode(outputs[0], skip_special_tokens=True)
    return response

def rag_system(query):
    # Step 1: Retrieve relevant documents
    query_embedding = encode([query])[0]
    top_k = 3  # Number of documents to retrieve
    distances, indices = index.search(np.array([query_embedding]), top_k)
    retrieved_docs = [documents[i] for i in indices[0]]

    # Step 2: Generate a response using the retrieved documents
    response = generate_response(query, retrieved_docs)
    return response

iface = gr.Interface(
    fn=rag_system, 
    inputs="text", 
    outputs="text",
    title="Retrieval-Augmented Generation",
    description="A simple POC for retrieval-augmented generation using Gradio."
)

iface.launch()