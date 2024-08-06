# %%

import boto3
from botocore.exceptions import ClientError
import json


def get_cohere_embedding(corpus):
    # Create a Bedrock Runtime client in the AWS Region you want to use.
    client = boto3.client("bedrock-runtime", region_name="us-east-1")

    # Set the model ID
    model_id = "cohere.embed-english-v3"

    body = json.dumps({
        "texts" : corpus,
        "input_type" : 'search_query'
    })
    try:
        # Send the message to the model, using a basic inference configuration.
        response = client.invoke_model(
            body=body,
            modelId="cohere.embed-english-v3",
            accept="application/json", 
            contentType="application/json"
)
        response_body = json.loads(response.get("body").read())
        embedding_output = response_body.get("embeddings")
        return(embedding_output)

    except (ClientError, Exception) as e:
        print(f"ERROR: Can't invoke '{model_id}'. Reason: {e}")
        exit(1)




# %%


corpus = [
"I love playing football",
"Football is my favorite sport",
"I like shoot three points in Basketball"
"Basketball is an exciting game",
"I like swimming in the ocean"
]

response = get_cohere_embedding(corpus)

# %%


# # %%


print (embedding_output)    

# %%
