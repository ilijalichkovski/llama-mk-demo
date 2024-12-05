import streamlit as st
from openai import OpenAI

#from transformers import AutoModelForCausalLM, AutoTokenizer, TextStreamer
#import os
#from dotenv import load_dotenv, dotenv_values


### log into huggingface ###

#load_dotenv() 
# accessing and printing value
#print(os.getenv("HF_API_KEY"))


### load model and adapter

#base_model_id = "meta-llama/Llama-3.2-1B"
#peft_model_id = "ilijalichkovski/llama-3.2-1b-mk"
#model = AutoModelForCausalLM.from_pretrained(base_model_id)
#model.load_adapter(peft_model_id)


# Show title and description.
st.title("💬 Асистет за претпријатие")
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
