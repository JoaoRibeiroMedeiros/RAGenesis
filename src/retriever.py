
# %%

from src.embedder import encode
from pymilvus import connections, Collection
import numpy as np
import json
import random
# Documents corpus (replace these with your actual documents)

# Step 3: Create a function to retrieve similar data
def retrieve_similar(collection, query_embedding, holy_texts, top_k):
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
        output_fields=["holytext","reference","verse","embedding"],
        partition_names=holy_texts
    )
    
    return results


def from_query_results_to_dicts(results):
    results_as_dicts = []
    for hits in results:
        for hit in hits:
            hit_dict = {
                "holytext": hit.entity.holytext, 
                "reference": hit.entity.reference, 
                "verse": hit.entity.verse, 
                "embedding": hit.entity.embedding,                  # Access the ID of the hit
            }
            results_as_dicts.append(hit_dict)
    return results_as_dicts



def query_holy_text(ec2_public_ip, query, text, top_k):
   
    # Step 1: Connect to Milvus
    connections.connect(alias="default", host=ec2_public_ip, port="19530")

    collection_name = "embeddings_collection"
    collection = Collection(collection_name)

    query_embedding = encode(query)

    collection.load()  # Load collection
    results = retrieve_similar(collection, query_embedding, [text], top_k)
    results_as_dicts = from_query_results_to_dicts(results)

    return results_as_dicts

# %%

def query_many_holy_text(ec2_public_ip, query, holy_texts, top_k):
   
    # Step 1: Connect to Milvus
    connections.connect(alias="default", host=ec2_public_ip, port="19530")

    collection_name = "embeddings_collection"
    collection = Collection(collection_name)

    query_embedding = encode(query)

    collection.load()  # Load collection

    results = retrieve_similar(collection, query_embedding, holy_texts, top_k = top_k)
    results_as_dicts = from_query_results_to_dicts(results)

    return results_as_dicts


def connect_and_query_holy_texts(holy_texts, query, top_k, local=False):

    if local=='localdocker':
        ec2_public_ip = "host.docker.internal"
    elif local=='local':
        ec2_public_ip = "localhost"
    else:
        # Fetch the EC2 public IP
        with open('config.json', 'r') as file:
            config = json.load(file)
            ec2_public_ip = config['EC2_PUBLIC_IP']

    results_as_dicts = query_many_holy_text(ec2_public_ip, query, holy_texts, top_k)
    results_sources = [result["holytext"] for result in results_as_dicts]
    results_references = [result["reference"] for result in results_as_dicts]
    results_verses = [result["verse"] for result in results_as_dicts]
    return results_sources, results_references, results_verses

def connect_and_query_holy_texts_ecumenical(holy_texts, query, top_k, local=False):

    if local=='localdocker':
        ec2_public_ip = "host.docker.internal"
    elif local=='local':
        ec2_public_ip = "localhost"
    else:
        # Fetch the EC2 public IP
        with open('config.json', 'r') as file:
            config = json.load(file)
            ec2_public_ip = config['EC2_PUBLIC_IP']

    results_sources = [] 
    results_references = []
    results_verses = []

    for text in random.sample(holy_texts, len(holy_texts)):
        results_as_dicts = query_holy_text(ec2_public_ip, query, text, top_k)
        results_sources = results_sources + [result["holytext"] for result in results_as_dicts]
        results_references = results_references + [result["reference"] for result in results_as_dicts]
        results_verses = results_verses + [result["verse"] for result in results_as_dicts]

    return results_sources, results_references, results_verses


def join_retrieved_references(results_references, results_verses):
    consolidated_retrieval = ""
    for reference, verse in zip(results_references, results_verses):
        consolidated_retrieval = consolidated_retrieval + reference + '\n' + verse + '\n\n'
    return consolidated_retrieval    

# %%

def main():
    
    with open('credentials/config.json', 'r') as file:
        config = json.load(file)
        # Fetch the EC2 public IP
    ec2_public_ip = config['EC2_PUBLIC_IP']

    query = "love is all you need"
    results_as_dicts = query_holy_text(ec2_public_ip, query)
    
    for result in results_as_dicts:
        print(result["reference"], result["verse"])
    
    


if __name__ == "__main__":
    main()
# %%
