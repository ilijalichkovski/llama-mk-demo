import streamlit as st
from openai import OpenAI
import numpy as np
import pandas as pd


#######


import re

def chunk_law_text(file_path):
    """
    Chunk a law text file into individual articles.
    
    Args:
        file_path (str): Path to the .txt file containing the law text
    
    Returns:
        list: A list of strings, each representing an individual article
    """
    # Read the entire file
    with open(file_path, 'r', encoding='utf-8') as file:
        full_text = file.read()
    
    # Use regex to split the text into articles
    # This pattern looks for 'Article' followed by a number at the start of a line
    # The (?=\n|\s) ensures it's followed by a newline or whitespace to avoid 
    # catching references within the text
    articles = re.split(r'\n(Член \d+)\n', full_text)[1:]
    
    # Reconstruct the articles 
    # The split will alternate between article headers and content
    chunked_articles = []
    for i in range(0, len(articles), 2):
        # Combine the article header with its content
        if i+1 < len(articles):
            article = articles[i] + '\n' + articles[i+1]
            chunked_articles.append(article.strip())
    
    return chunked_articles

articles = chunk_law_text('/content/konsolidiran_tekst.txt')

#######


# Show title and description.
st.title("💬 Асистент за претпријатие")
st.write(
    "Здраво! Тука имате разговорен пристап со базите на знаење во вашата организација, како и релевантните законски прописи."
)

# Ask user for their OpenAI API key via `st.text_input`.
# Alternatively, you can store the API key in `./.streamlit/secrets.toml` and access it
# via `st.secrets`, see https://docs.streamlit.io/develop/concepts/connections/secrets-management



openai_api_key = st.text_input("OpenAI API Key", type="password")
if not openai_api_key:
    st.info("Please add your OpenAI API key to continue.", icon="🗝️")
else:

    # Create an OpenAI client.
    client = OpenAI(api_key=openai_api_key)

    # Create a session state variable to store the chat messages. This ensures that the
    # messages persist across reruns.
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display the existing chat messages via `st.chat_message`.
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Create a chat input field to allow the user to enter a message. This will display
    # automatically at the bottom of the page.
    if prompt := st.chat_input("What is up?"):

        # Store and display the current prompt.
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Generate a response using the OpenAI API.
        stream = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        )

        # Stream the response to the chat using `st.write_stream`, then store it in 
        # session state.
        with st.chat_message("assistant"):
            response = st.write_stream(stream)
        st.session_state.messages.append({"role": "assistant", "content": response})



#tok = AutoTokenizer.from_pretrained("openai-community/gpt2")
#model = AutoModelForCausalLM.from_pretrained("openai-community/gpt2")
#inputs = tok(["An increasing sequence: one,"], return_tensors="pt")
#streamer = TextStreamer(tok)

# Despite returning the usual output, the streamer will also print the generated text to stdout.
#_ = model.generate(**inputs, streamer=streamer, max_new_tokens=20)
