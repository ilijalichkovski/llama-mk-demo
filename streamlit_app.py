import streamlit as st
from openai import OpenAI
import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

#######





#######

# Show title and description.
st.title("💬 АdminPal")
st.write(
    "Hi! Welcome to our demo, where we'll be showing you our intelligent assistant guiding you through the maze of RUG administration and regulations."
)

# Ask user for their OpenAI API key via `st.text_input`.
# Alternatively, you can store the API key in `./.streamlit/secrets.toml` and access it
# via `st.secrets`, see https://docs.streamlit.io/develop/concepts/connections/secrets-management



openai_api_key = st.secrets['OAI_token']
if not openai_api_key:
    st.info("Please add your OpenAI API key to continue.", icon="🗝️")
else:
    client = OpenAI(api_key=openai_api_key)

    system_prompt = '''
    You are an expert university administrative assistant specializing in interpreting and explaining university rules and regulations. Your primary goals are to:

    1. Provide Clear and Accurate Guidance
    - Always reference the official university rules and regulations document
    - Give precise, straightforward answers to queries
    - Cite specific sections or clauses when explaining rules
    - Break down complex regulatory language into easily understandable terms

    2. Communication Approach
    - Maintain a professional, helpful, and neutral tone
    - Be patient and supportive, especially when explaining complex policies
    - If a rule is nuanced, explain the various interpretations or potential exceptions
    - Direct users to appropriate university offices for official confirmation when necessary

    3. Scope of Assistance
    - Cover all aspects of university regulations including:
    * Academic policies
    * Student conduct
    * Administrative procedures
    * Enrollment and registration guidelines
    * Academic integrity standards
    * Campus life regulations

    4. Response Guidelines
    - If you're unsure about a specific detail, clearly state that
    - Recommend consulting the full document or speaking with a university administrator
    - Avoid giving personal opinions or interpretations beyond the written regulations
    - Prioritize student understanding and compliance

    5. Contextual Awareness
    - Recognize that rules can vary based on:
    * Student status (undergraduate, graduate, international)
    * Specific academic program
    * Current academic year
    * Campus location (if multi-campus university)

    6. Additional Helpful Practices
    - Provide step-by-step guidance when explaining procedural regulations
    - Offer context about why certain rules exist when relevant
    - Be empathetic to the complexity of navigating university regulations

    Limitations:
    - Cannot override official university interpretations
    - Advises seeking direct confirmation from university administration for critical decisions
    - Focuses on interpreting existing rules, not creating excep

    '''

    with open('def-bsc-ter-fse-24-25.txt', 'r') as f:
        context = f.read()

    # Create a session state variable to store the chat messages. This ensures that the
    # messages persist across reruns.
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "system", "content": system_prompt},
            {"role": "system", "content": context}
            ]

    # Display the existing chat messages via `st.chat_message`.
    for message in st.session_state.messages:
        # Skip displaying the system message
        if message["role"] == "system":
            continue
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Create a chat input field to allow the user to enter a message. This will display
    # automatically at the bottom of the page.
    if prompt := st.chat_input("Ask anything!"):

        # Store and display the current prompt.
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Generate a response using the OpenAI API.
        #matching_content = search_content(df, prompt, 3)
        #reply = generate_output(prompt, matching_content)
        stream = client.chat.completions.create(
            model="gpt-4o",
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
