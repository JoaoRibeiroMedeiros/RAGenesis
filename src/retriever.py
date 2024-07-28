
# %%

from transformers import AutoTokenizer, AutoModel, GPT2Tokenizer, GPT2LMHeadModel
from src.embedder import encode
from pymilvus import connections, Collection
import numpy as np

# Documents corpus (replace these with your actual documents)

# Step 3: Create a function to retrieve similar data
def retrieve_similar(collection, query_embedding, top_k=10):
    search_params = {
        "metric_type": "L2",  # Choose the similarity metric
        "params": {}
    }
    
    results = collection.search(
        data=[query_embedding],
        anns_field="embedding",  # This should match your field name
        param=search_params,
        limit=top_k,
        expr=None,
        output_fields=["reference","embedding"]
    )
    
    return results


def from_query_results_to_dicts(results):
    results_as_dicts = []
    for hits in results:
        for hit in hits:
            hit_dict = {
                "reference": hit.entity.reference, 
                "embedding": hit.entity.embedding,                  # Access the ID of the hit
            }
            results_as_dicts.append(hit_dict)
    return results_as_dicts

# %%

def main():
    import json
    
    from sentence_transformers import SentenceTransformer


    # Read the config file
    with open('credentials/config.json', 'r') as file:
        config = json.load(file)
    # Fetch the EC2 public IP
    ec2_public_ip = config['EC2_PUBLIC_IP']

    # Step 1: Connect to Milvus
    connections.connect(alias="default", host=ec2_public_ip, port="19530")

    collection_name = "embeddings_collection"
    collection = Collection(collection_name)

    model = SentenceTransformer('paraphrase-MiniLM-L6-v2')

    query = "sex"

    query_embedding = model.encode(query)

    collection.load()  # Load collection

    results = retrieve_similar(collection, query_embedding)
    results_as_dicts = from_query_results_to_dicts(results)

    for result in results_as_dicts:

        print(result["reference"], model.decode(result["embedding"]))
    
    
    

if __name__ == "__main__":
    main()
# %%
