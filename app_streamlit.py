
import streamlit as st
from src.retriever import *
from src.generation import *

import requests
import json

def verse_uni_verse( query_verse = "In the beginning God created the heaven and the earth."):

    st.title("Verse Uni Verse")

    st.text("Describe a subject you are interested in.")

    selected_texts = st.sidebar.multiselect('Select Holy Texts', ['Bible', 'Quran', 'Gita'])

    results_references, results_verses = connect_and_query_holy_text(query_verse, selected_texts) \
    
    for reference, verse in zip(results_references, results_verses):
        st.text("")
        st.text(reference)
        st.text("")
        st.text(verse)
        st.text("")
        st.button(reference, key=None, help=None, on_click=verse_uni_verse, args=(verse), kwargs=None)


def exploration(): 

    st.title('Retrieval Augmented Genesis!')

    st.text("Describe a subject or an idea you are interested in.")

    st.text("AI will help you find the most relevant verses in the selected holy texts for it!")

    query = st.sidebar.text_input('Enter Query', value = 'God is love')

    selected_texts = st.sidebar.multiselect('Select Holy Texts', ['Bible', 'Quran', 'Gita'])

    results_references, results_verses = connect_and_query_holy_text(query, selected_texts)

    for reference, verse in zip(results_references, results_verses):
        st.text("")
        st.text(reference)
        st.text("")
        st.text(verse)
        st.text("")
        st.button(reference, key=None, help=None, on_click=verse_uni_verse, args=(verse), kwargs=None)


def genesis(): 

    selected_texts = st.sidebar.multiselect('Select Holy Texts', ['Bible', 'Quran', 'Gita'])

    st.title('Retrieval Augmented Genesis!')

    st.text("Speak to the oracle!")

    st.text("Start a conversation! The oracle will respond to you based on the toggled holy texts.")




# # Define a function to get user input.
# def get_input_text():
#     input_text = st.text_input("You: ","Hello!", key="input")
#     return input_text 

# # Define a function to inquire about the data in Pinecone.
# def query(payload, docs, chain):
#     response = chain.run(input_documents=docs, question=payload)
#     thisdict = {
#         "generated_text": response
#     }
#     return thisdict

# # Initialize session state to store user input.
# if 'past' not in st.session_state:
#     st.session_state['past'] = []

# # Initialize session state to store the chatbot-generated output.
# if 'generated' not in st.session_state:
#     st.session_state['generated'] = []

# # Initialize Azure Cognitive Search index and embeddings.
# embed = OpenAIEmbeddings(deployment=OPENAI_EMBEDDING_DEPLOYMENT_NAME, 
#                                     openai_api_key=OPENAI_API_KEY, 
#                                     model=OPENAI_EMBEDDING_MODEL_NAME, 
#                                     openai_api_type=OPENAI_API_TYPE, 
#                                     chunk_size=1)
# vector_store: AzureSearch = AzureSearch(
#     azure_search_endpoint=AZURE_COGNITIVE_SEARCH_ENDPOINT_NAME,
#     azure_search_key=AZURE_COGNITIVE_SEARCH_KEY,
#     index_name=AZURE_COGNITIVE_SEARCH_INDEX_NAME,
#     embedding_function=embed.embed_query,
# )
# user_input = get_input_text()

# # Initialize the similarity search.
# docs = vector_store.similarity_search(user_input)

# # Initialize the Azure OpenAI ChatGPT model.
# llm = AzureChatOpenAI(deployment_name=OPENAI_DEPLOYMENT_NAME, 
#                       openai_api_key=OPENAI_API_KEY,
#                       openai_api_base=OPENAI_API_BASE, 
#                       openai_api_version=OPENAI_API_VERSION, 
#                       openai_api_type = OPENAI_API_TYPE, 
#                       temperature=0)

# # Initialize the question answering chain.
# chain = load_qa_chain(llm, chain_type="stuff")

# # Generate the chatbot response.
# if user_input:
#     output = query({
#         "inputs": {
#             "past_user_inputs": st.session_state.past,
#             "generated_responses": st.session_state.generated,
#             "text": user_input,
#         },"parameters": {"repetition_penalty": 1.33} # The repetition penalty is meant to avoid sentences that repeat themselves without anything really interesting.
#     },
#     docs=docs,
#     chain=chain)
    
#     st.session_state.past.append(user_input)
#     st.session_state.generated.append(output["generated_text"])

# if st.session_state['generated']:
#     for i in range(len(st.session_state['generated'])-1, -1, -1):
#         message(st.session_state["generated"][i], key=str(i))
#         message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')