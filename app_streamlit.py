
# %%

import streamlit as st
from src.retriever import *
from src.generation import *
from src.embedder import encode

# %%

local = True

# %%

def landing_page(): 

    st.title('Holy AI!')

    st.text("Welcome to Holy AI!")

    st.text("Explore the holy texts of the Bible, the Quran, the Bhagavad Gita and the Analects with the help of AI!")

    st.text("Select the holy texts you want to explore and start your journey!")

    st.text("There are three main features:")

    st.text("You can explore the texts,") 
            
    st.text("navigate through the verses,") 
            
    st.text("and even have a conversation with the oracle!")

    st.text("The oracle will respond to you based on the toggled holy texts.")

    st.text("Enjoy your journey!")

def exploration(): 

    st.title('Explore Holy!')

    st.text("Describe a subject or an idea you are interested in.")

    st.text("AI will help you find the most relevant verses in the selected holy texts for it!")

    query = st.text_input('Enter Query', value = 'God is love')

    results_sources, results_references, results_verses = connect_and_query_holy_text(selected_texts, query, local=local)

    for source, reference, verse in zip(results_sources,results_references, results_verses):
        st.text("")
        st.button(reference, key=None, help=None, on_click=verse_uni_verse,   kwargs={"query_verse": verse})
        st.text("")
        st.text(verse)
        st.text("")
        

def verse_uni_verse( query_verse = "In the beginning God created the heaven and the earth."):

    st.title("Verse Uni Verse")

    st.text("Navigate through the verses of the selected holy texts based on semantic similarity.")

    results_sources, results_references, results_verses = connect_and_query_holy_text(selected_texts, query_verse, local=local)
    
    for source, reference, verse in zip(results_sources,results_references, results_verses):
        st.text("")
        st.button(reference, key=None, help=None, on_click=verse_uni_verse,  kwargs={"query_verse": verse})
        st.text("")
        st.text(verse)
        st.text("")
        

def genesis(): 

    st.title('Retrieval Augmented Genesis!')

    st.text("Speak to the oracle!")

    st.text("Start a conversation! The oracle will respond to you based on the toggled holy texts.")

    query = st.text_input('Speak to me...', value = 'God is love')

    results_sources, results_references, results_verses = connect_and_query_holy_text(selected_texts, query, local=local)

    retrieval = join_retrieved_references(results_references, results_verses)

    response = get_oracle_response(query + retrieval)

    st.text(response)


#### sidebar
selected_texts = st.sidebar.multiselect('Select Holy Texts', ['Bible', 'Quran'], default=['Bible', 'Quran'])
st.sidebar.button("Exploration", key=None, help=None, on_click=exploration)
st.sidebar.button("VerseUniVerse", key=None, help=None, on_click=verse_uni_verse)
st.sidebar.button("RAGenesis", key=None, help=None, on_click=genesis)
#### 

exploration()

