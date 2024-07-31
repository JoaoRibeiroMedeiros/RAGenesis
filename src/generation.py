from transformers import AutoTokenizer, AutoModel, GPT2Tokenizer, GPT2LMHeadModel


def generate_response(query, retrieved_docs):

    gpt2_tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
    gpt2_model = GPT2LMHeadModel.from_pretrained("gpt2")
    context = " ".join(retrieved_docs) + " " + query
    inputs = gpt2_tokenizer.encode(context, return_tensors="pt")
    outputs = gpt2_model.generate(inputs, max_length=100, num_return_sequences=1)
    response = gpt2_tokenizer.decode(outputs[0], skip_special_tokens=True)

    return response

