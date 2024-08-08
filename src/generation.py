# %%

import boto3
from botocore.exceptions import ClientError


def get_oracle_response(user_query):
    # Create a Bedrock Runtime client in the AWS Region you want to use.
    client = boto3.client("bedrock-runtime", region_name="us-east-1")

    # Set the model ID
    model_id = "meta.llama3-70b-instruct-v1:0"

    # Start a conversation with the user message.
    instruction = """[INST]You are an oracle who will be fed a user query and several 
                    verses which are semnatically connected to that query
                    make sure your response explores the theme shared by user with wisdom
                    making reference to the passages that were given together with the user query[/INST]"""

    user_message = instruction + user_query

    conversation = [
        {
            "role": "user",
            "content": [{"text": user_message}],
        }
    ]
    try:
        # Send the message to the model, using a basic inference configuration.
        response = client.converse(
            modelId=model_id,
            messages=conversation,
            inferenceConfig={"maxTokens":512,"temperature":0.5,"topP":0.9},
            additionalModelRequestFields={}
        )
        # Extract and print the response text.
        response_text = response["output"]["message"]["content"][0]["text"]

        return(response_text)

    except (ClientError, Exception) as e:
        print(f"ERROR: Can't invoke '{model_id}'. Reason: {e}")
        exit(1)




# %%

# response = get_oracle_response('God is love')

# # %%

# print(response)

# # %%
