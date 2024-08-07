# %%

from sentence_transformers import SentenceTransformer

def encode(corpus):
    # Load pre-trained model (you can choose different models here)
    model = SentenceTransformer('all-MiniLM-L6-v2') 
    # Compute the sentence embeddings
    embeddings = model.encode(corpus)
    return(embeddings)

# import boto3
# from botocore.exceptions import ClientError
# import json

# def encode(corpus):
#     # Create a Bedrock Runtime client in the AWS Region you want to use.
#     client = boto3.client("bedrock-runtime", region_name="us-east-1")

#     # Set the model ID
#     model_id = "cohere.embed-english-v3"

#     body = json.dumps({
#         "texts" : corpus,
#         "input_type" : 'search_query'
#     })
#     try:
#         # Send the message to the model, using a basic inference configuration.
#         response = client.invoke_model(
#             body=body,
#             modelId="cohere.embed-english-v3",
#             accept="application/json", 
#             contentType="application/json"
# )
#         response_body = json.loads(response.get("body").read())
#         embedding_output = response_body.get("embeddings")
#         return(embedding_output)

#     except (ClientError, Exception) as e:
#         print(f"ERROR: Can't invoke '{model_id}'. Reason: {e}")
#         exit(1)


# %%
