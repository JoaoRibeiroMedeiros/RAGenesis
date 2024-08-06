
# %%

from pymilvus import connections, utility, FieldSchema, CollectionSchema, DataType, Collection
import numpy as np
from sentence_transformers import SentenceTransformer
from src.chunker import chunk_bible, chunk_quran
import json

# %%

local= True

if local == True:

    host = 'localhost'

else:
    with open('config.json', 'r') as file: # Read the config file
        config = json.load(file)
    # Fetch the EC2 public IP
    ec2_public_ip = config['EC2_PUBLIC_IP']
    host = ec2_public_ip


# Documents corpus (replace these with your actual documents)
bible_verses = chunk_bible('sacred_data/bible.txt')
quran_verses = chunk_quran('sacred_data/quran.txt')

# Extracting just the text portions and references from each tuple
bible_verses_text = [verse[1] for verse in bible_verses]
bible_verses_references = [verse[0] for verse in bible_verses]

quran_verses_text = [verse[1] for verse in quran_verses]
quran_verses_references = [verse[0] for verse in quran_verses]

# %% 

# Load SentenceTransformer model
model = SentenceTransformer('paraphrase-MiniLM-L6-v2')

#TODO API driven embedding
# Generate embeddings

bible_embeddings = model.encode(bible_verses_text)
quran_embeddings = model.encode(quran_verses_text)

 
# %% 

# Connect to Milvus
connections.connect(alias="default", host=host, port="19530")

# Define the schema for your collection
# Define fields and schema for your collection
fields = [
    FieldSchema(name="id", dtype=DataType.INT64, is_primary=True, auto_id=True),
    FieldSchema(name="holytext", dtype=DataType.VARCHAR, max_length=40),
    FieldSchema(name="reference", dtype=DataType.VARCHAR, max_length=100),
    FieldSchema(name="verse", dtype=DataType.VARCHAR, max_length=max([len(verse) for verse in bible_verses_text + quran_verses_text])+5),
    FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR, dim=len(bible_embeddings[0]))
]

# %%

# Create a schema
schema = CollectionSchema(fields, description="Collection for embeddings")

# Create a collection
collection_name = "embeddings_collection"

# Drop the existing collection if it exists
if utility.has_collection(collection_name):
    Collection(name=collection_name).drop()

# Create the collection with the new schema
collection = Collection(name=collection_name, schema=schema)

holy_texts = ['Bible', 'Quran']

for partition_name in holy_texts:
    if not collection.has_partition(partition_name):
        collection.create_partition(partition_name)

# %%

# Insert data

bible_data = [
    len(bible_verses_references) * ['Bible'],
    bible_verses_references,  # List of references
    bible_verses_text,        # List of verses
    [x for x in bible_embeddings]          # List of embeddings
]

quran_data = [
    len(quran_verses_references) * ['Quran'],
    quran_verses_references,  # List of references
    quran_verses_text,        # List of verses
    [x for x in quran_embeddings]          # List of embeddings
]

# %%

collection.insert(bible_data,partition_name='Bible')

collection.insert(quran_data,partition_name='Quran')

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
