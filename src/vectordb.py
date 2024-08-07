
# %%

from pymilvus import connections, utility, FieldSchema, CollectionSchema, DataType, Collection
import numpy as np
from src.embedder import encode
from src.chunker import chunk_bible, chunk_quran, chunk_gita, chunk_analects ,analects
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

bible_references, bible_verses = chunk_bible('sacred_data/bible.txt')
quran_references, quran_verses = chunk_quran('sacred_data/quran.txt')
gita_references, gita_verses = chunk_gita('sacred_data/gita.txt')
analects_references, analects_verses = chunk_analects(analects)

# Extracting just the text portions and references from each tuple

# %% 

print( len(bible_references), len(quran_references), len(gita_references), len(analects_references) )

# %% 

#TODO API driven embedding
# Generate embeddings

bible_embeddings = encode(bible_verses)
quran_embeddings = encode(quran_verses)
gita_embeddings = encode(gita_verses)
analects_embeddings = encode(analects_verses)

# %% 

# Connect to Milvus
connections.connect(alias="default", host=host, port="19530")

# Define the schema for your collection
# Define fields and schema for your collection
fields = [
    FieldSchema(name="id", dtype=DataType.INT64, is_primary=True, auto_id=True),
    FieldSchema(name="holytext", dtype=DataType.VARCHAR, max_length=40),
    FieldSchema(name="reference", dtype=DataType.VARCHAR, max_length=100),
    FieldSchema(name="verse", dtype=DataType.VARCHAR, max_length=max([len(verse) for verse in bible_verses + quran_verses + gita_verses + analects_verses])+5),
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

holy_texts = ['Bible', 'Quran', 'Gita', 'Analects']

for partition_name in holy_texts:
    if not collection.has_partition(partition_name):
        collection.create_partition(partition_name)

# %%

# make data

bible_data = [
    len(bible_references) * ['Bible'],
    bible_references,  # List of references
    bible_verses,        # List of verses
    [x for x in bible_embeddings]          # List of embeddings
]

quran_data = [
    len(quran_references) * ['Quran'],
    quran_references,  # List of references
    quran_verses,        # List of verses
    [x for x in quran_embeddings]          # List of embeddings
]

gita_data = [
    len(gita_references) * ['Gita'],
    gita_references,  # List of references
    gita_verses,        # List of verses
    [x for x in gita_embeddings]          # List of embeddings
]

analects_data = [
    len(analects_references) * ['Analects'],
    analects_references,  # List of references
    analects_verses,        # List of verses
    [x for x in analects_embeddings]          # List of embeddings
]


# %%

# insert data

collection.insert(bible_data,partition_name='Bible')

collection.insert(quran_data,partition_name='Quran')

collection.insert(gita_data,partition_name='Gita')

collection.insert(analects_data,partition_name='Analects')

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

print(collection.partitions)
# %%

### health check

# Connect to Milvus
connections.connect("default", host="localhost", port="19530")

# Check if the connection is successful
if connections.has_connection("default"):
    print("Milvus is healthy!")
else:
    print("Milvus is not healthy.")
# %%
