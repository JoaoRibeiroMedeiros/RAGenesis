
from pymilvus import connections, utility, FieldSchema, CollectionSchema, DataType, Collection
import numpy as np
from sentence_transformers import SentenceTransformer

from chunker import chunk_bible


# Connect to Milvus
connections.connect(alias="default", host="localhost", port="19530")

# Define the schema for your collection
fields = [
    FieldSchema(name="id", dtype=DataType.INT64, is_primary=True, auto_id=True),  # Notice auto_id=True
    FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR, dim=768)  # Change dim according to your embeddings
]

# Create a schema
schema = CollectionSchema(fields, description="Collection for embeddings")

# Create a collection
collection_name = "embeddings_collection"
if not utility.has_collection(collection_name):
    collection = Collection(name=collection_name, schema=schema)
else:
    collection = Collection(name=collection_name)

# Load SentenceTransformer model
model = SentenceTransformer('paraphrase-MiniLM-L6-v2')


# Documents corpus (replace these with your actual documents)


def rag_system(query):
    documents = chunk_bible('sacred_data/bible.txt')
    document_embeddings = encode(documents)
# Generate embeddings
embeddings = model.encode(sentences)

# Convert embeddings to list
embeddings_list = embeddings.tolist()

# Prepare data for insertion
# An empty list for IDs since auto_id=True
data = [
    [],  # Empty as IDs will be auto-generated
    embeddings_list  # List of embeddings
]

# Insert data into collection
collection.insert(data)

# Check insertion
print(f"Number of entities in Milvus: {collection.num_entities}")
