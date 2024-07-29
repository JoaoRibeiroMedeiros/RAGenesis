
# %%

from pymilvus import connections, utility, FieldSchema, CollectionSchema, DataType, Collection
import numpy as np
from sentence_transformers import SentenceTransformer
from src.chunker import chunk_bible
import json

# Read the config file
with open('credentials/config.json', 'r') as file:
    config = json.load(file)

# Fetch the EC2 public IP
ec2_public_ip = config['EC2_PUBLIC_IP']


# Documents corpus (replace these with your actual documents)
verses = chunk_bible('sacred_data/bible.txt')

# Extracting just the text portions and references from each tuple
verses_text = [verse[1] for verse in verses]
verses_references = [verse[0] for verse in verses]

# %%   

# Load SentenceTransformer model
model = SentenceTransformer('paraphrase-MiniLM-L6-v2')

# Generate embeddings
embeddings = model.encode(verses_text)

# %%

# Connect to Milvus
connections.connect(alias="default", host=ec2_public_ip, port="19530")


# %%
# Define the schema for your collection
# Define fields and schema for your collection
fields = [
    FieldSchema(name="id", dtype=DataType.INT64, is_primary=True, auto_id=True),
    FieldSchema(name="reference", dtype=DataType.VARCHAR, max_length=100),
    FieldSchema(name="verse", dtype=DataType.VARCHAR, max_length=max([len(verse) for verse in verses_text])+5),
    FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR, dim=len(embeddings[0]))
]

# %%

# Create a schema
schema = CollectionSchema(fields, description="Collection for embeddings")

# %%
# Create a collection
collection_name = "embeddings_collection"

# Drop the existing collection if it exists
if utility.has_collection(collection_name):
    Collection(name=collection_name).drop()

# Create the collection with the new schema
collection = Collection(name=collection_name, schema=schema)

# %%

# Insert data

data = [
    verses_references,  # List of references
    verses_text,        # List of verses
    [x for x in embeddings]          # List of embeddings
]

# %%
collection.insert(data)
# %%

# Create an IVF_FLAT index for collection.
index_params = {
    'metric_type':'L2',
    'index_type':"IVF_FLAT",
    'params':{'nlist': 1536}
}

collection.create_index(field_name="embedding", index_params=index_params)

collection.load()

# %%

# Check insertion
print(f"Number of entities in Milvus: {collection.num_entities}")

# %%
