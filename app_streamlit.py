
# %%

import streamlit as st
from src.retriever import *
from src.generation import *
from src.embedder import encode

# %%

holy_texts = ['Bible', 'Quran', 'Gita', 'Analects']

local = True

# %%

def landing_page(): 

    import streamlit as st

st.title('Holy AI!')

st.markdown("""
Welcome to **Holy AI!**

Explore the holy texts of the **Bible**, the **Quran**, the **Bhagavad Gita**, and the **Analects** with the help of AI!

Select the holy texts you want to explore and start your journey!

There are three main features:

- **Explore the texts**
- **Navigate through the verses**: Click on a verse to find the most semantically similar verses in the selected holy texts.
- **Have a conversation with the oracle!**

The oracle will respond to you based on the toggled holy texts.

**Enjoy your journey!**
""")


def exploration(): 

    st.title('Explore Holy!')

    st.text("Describe a subject or an idea you are interested in.")

    st.text("AI will help you find the most relevant verses in the selected holy texts for it!")

    query = st.text_input('Enter Query', value = 'God is love')

    results_sources, results_references, results_verses = connect_and_query_holy_text(selected_texts, query, local=local)

    for i, source, reference, verse in zip(range(len(results_verses)) ,results_sources,results_references, results_verses):
        st.text(source)
        st.button(reference, key=i, help=None, on_click=verse_uni_verse,   kwargs={"query_verse": verse})
        st.text("")
        st.text(verse)
        st.text("")
        

def verse_uni_verse( query_verse = "In the beginning God created the heaven and the earth."):

    st.title("Verse Uni Verse")

    st.text("Navigate through the verses of the selected holy texts based on semantic similarity.")

    results_sources, results_references, results_verses = connect_and_query_holy_text(selected_texts, query_verse, local=local)
    
    for i, source, reference, verse in zip(range(len(results_verses)), results_sources,results_references, results_verses):
        st.text(source)
        st.button(reference, key=i, help=None, on_click=verse_uni_verse,  kwargs={"query_verse": verse})
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

selected_texts = st.sidebar.multiselect('Select Holy Texts', holy_texts, default=holy_texts)

# st.sidebar.button("Exploration", key=None, help=None, on_click=exploration)
# st.sidebar.button("VerseUniVerse", key=None, help=None, on_click=verse_uni_verse)
# st.sidebar.button("RAGenesis", key=None, help=None, on_click=genesis)


if st.sidebar.button("Exploration"):
    st.session_state.page = 'Exploration'
if st.sidebar.button("VerseUniVerse"):
    st.session_state.page = 'VerseUniVerse'
if st.sidebar.button("RAGenesis"):
    st.session_state.page = 'RAGenesis'

# Main page logic

st.session_state.page = 'Landing'


if st.session_state.page == 'Landing':
    landing_page()
elif st.session_state.page == 'Exploration':
    exploration()
elif st.session_state.page == 'VerseUniVerse':
    verse_uni_verse()
elif st.session_state.page == 'RAGenesis':
    genesis()

#### 



