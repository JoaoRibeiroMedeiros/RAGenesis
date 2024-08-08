
# %%

import streamlit as st
from src.retriever import *
from src.generation import *

# %%

st.session_state.counter = 0

holy_texts = ['Bible', 'Quran', 'Gita', 'Analects']

st.session_state.query = "God is love"

local = 'localdocker'

# %%

def landing_page(): 

    st.title('Holy AI!')

    st.markdown("""

    Explore the holy texts of the **Bible**, the **Quran**, the **Bhagavad Gita**, and the **Analects** with the help of AI!

    - **Exploration** : Explore the texts
    - **VerseUniVerse** : Navigate through the verses: Click on a verse to find the most semantically similar verses in the selected holy texts.
    - **RAGenesis** : Have a conversation with the oracle! Retrieval Augmented Genesis!

    **Enjoy your journey!**            
                
    """)

#### sidebar

selected_texts = st.sidebar.multiselect('Select Holy Texts', holy_texts, default=holy_texts)

# st.sidebar.button("Exploration", key=None, help=None, on_click=exploration)
# st.sidebar.button("VerseUniVerse", key=None, help=None, on_click=verse_uni_verse)
# st.sidebar.button("RAGenesis", key=None, help=None, on_click=genesis)



def exploration(): 

    st.title('Explore Holy!')

    st.markdown("Describe a subject or an idea you are interested in.")

    st.markdown("AI will help you find the most relevant verses in the selected holy texts for it!")

    query = st.text_input('Enter Query', value= st.session_state.query , on_change=exploration)

    st.session_state.query = query

    # if query:

    results_sources, results_references, results_verses = connect_and_query_holy_text(selected_texts, st.session_state.query, local=local)

    for source, reference, verse in zip(results_sources,results_references, results_verses):
        st.session_state.counter += 1
        st.markdown(source)
        st.button(reference, key=st.session_state.counter, help=None, on_click=verse_uni_verse,   kwargs={"query_verse": verse})
        st.markdown("")
        st.markdown(verse)
        st.markdown("")
    

def verse_uni_verse( query_verse = "In the beginning God created the heaven and the earth."):

    st.title("Verse Uni Verse")

    st.markdown("Navigate through the verses of the selected holy texts based on semantic similarity.")

    results_sources, results_references, results_verses = connect_and_query_holy_text(selected_texts, query_verse, local=local)

    
    for source, reference, verse in zip( results_sources,results_references, results_verses):
        st.session_state.counter += 1
        st.markdown(source)
        st.button(reference, key=st.session_state.counter, help=None, on_click=verse_uni_verse,  kwargs={"query_verse": verse})
        st.markdown("")
        st.markdown(verse)
        st.markdown("")
        

def genesis(): 

    st.title('Retrieval Augmented Genesis!')

    st.markdown("Speak to the oracle!")

    st.markdown("Start a conversation! The oracle will respond to you based on the toggled holy texts.")

    query = st.text_input('Speak to me...', value= st.session_state.query, on_change=genesis)

    st.session_state.query = query

    # if query:

    results_sources, results_references, results_verses = connect_and_query_holy_text(selected_texts, query, local=local)

    retrieval = join_retrieved_references(results_references, results_verses)

    response = get_oracle_response(query + retrieval)

    st.markdown(response)

st.session_state.page = 'Landing'

if st.sidebar.button("Exploration"):
    st.session_state.page = 'Exploration'
if st.sidebar.button("VerseUniVerse"):
    st.session_state.page = 'VerseUniVerse'
if st.sidebar.button("RAGenesis"):
    st.session_state.page = 'RAGenesis'

# Main page logic

if st.session_state.page == 'Landing':
    landing_page()
elif st.session_state.page == 'Exploration':
    exploration()
elif st.session_state.page == 'VerseUniVerse':
    verse_uni_verse()
elif st.session_state.page == 'RAGenesis':
    genesis()



#### 
