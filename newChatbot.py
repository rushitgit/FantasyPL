from dotenv import load_dotenv
import streamlit as st
import pandas as pd
import openai
import os
import base64
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
background_path = "images/background.png"

def get_base64(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def set_background(png_file):
    bin_str = get_base64(png_file)
    page_bg_img = '''
    <style>
    .stApp {
    background-image: url("data:image/png;base64,%s");
    background-size: cover;
    }
    </style>
    ''' % bin_str
    st.markdown(page_bg_img, unsafe_allow_html=True)

set_background(background_path)

@st.cache_data
def load_csv(file_path):
    return pd.read_csv(file_path)

def generate_text(query, data_frame_1):
    combined_data = data_frame_1
    prompt = f"You are a Fantasy Premier League Manager, your role is to offer the best advice to users from the datasets given to you. In the datasets, give less weightage to sentiments and positivity and prioritize highly upon predicted points and bonus and minutes. Certain rules are: team budget should not exceed 100 million, and one team cannot contain more than 3 players of the same team. Give unbiased and statistical advice to users to his query. User Query: {query}\n Data:\n{combined_data}"
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=200
    )
    return response.choices[0].text.strip()

# Function to find the most similar previous question
def find_similar_question(new_query, queries, threshold=0.8):
    if not queries:
        return None, None
    vectorizer = TfidfVectorizer().fit_transform(queries + [new_query])
    vectors = vectorizer.toarray()
    cosine_similarities = cosine_similarity(vectors[-1], vectors[:-1])
    max_similarity = np.max(cosine_similarities)
    if max_similarity >= threshold:
        most_similar_idx = np.argmax(cosine_similarities)
        return queries[most_similar_idx], max_similarity
    return None, None

def main():
    st.title("Fantasy Premier League Chatbot")
    data_frame_1 = load_csv("datasets/TopPlayersWithSentiments.csv")
    
    # Cache responses
    if "response_cache" not in st.session_state:
        st.session_state.response_cache = {}
        st.session_state.previous_queries = []

    query = st.text_input("Chat with us.")
    
    if query:
        similar_query, similarity = find_similar_question(query, st.session_state.previous_queries)
        if similar_query and similarity:
            result = st.session_state.response_cache[similar_query]
            st.info(f"Reusing response for a similar question (similarity: {similarity:.2f}).")
        else:
            result = generate_text(query, data_frame_1)
            st.session_state.previous_queries.append(query)
            st.session_state.response_cache[query] = result
        
        st.subheader("Generated Text:")
        st.write(result)
    else:
        st.info("Enter a question to get started.")

    st.write("We are a statistical based chatbot for aiding you to make the best decisions for your Fantasy Premier League team.")

if __name__ == "__main__":
    main()
