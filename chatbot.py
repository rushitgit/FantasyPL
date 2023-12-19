from dotenv import load_dotenv
import streamlit as st
import pandas as pd
import openai
import os 

load_dotenv()
# Set your OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")
background_path = "images/background.png"
# Function to set the background image

background_code = f"""
<style>
    body {{
        background-image: url("{background_path}");
        background-size: cover;
    }}
</style>
"""
st.markdown(background_code, unsafe_allow_html=True)

# Load CSV function
def load_csv(file_path):
    return pd.read_csv(file_path)

# Function to generate text
def generate_text(query, data_frame_1):
    combined_data = data_frame_1
    prompt = f"You are a Fantasy Premier League Manager, your role is to offer the best advice to users from the datasets given to you. In the datasets, give less weightage to sentiments and positivity and prioritize highly upon predicted points and bonus and minutes. Certain rules are: team budget should not exceed 100 million, and one team cannot contain more than 3 players of the same team. Give unbiased and statistical advice to users to his query. User Query: {query}\n Data:\n{combined_data}"
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=200
    )
    return response.choices[0].text.strip()

# Main function
def main():
    #set_background('images/background.png')  # Change 'images/background.png' to your actual background image path
    st.title("OpenAI Chatbot with CSV Payloads")
    # st.image("chatbot_logo.png", width=200)  # Add your chatbot logo or emoticon

    # Load CSV data (Default file paths, change as needed)
    data_frame_1 = load_csv("datasets\TopPlayersWithSentiments.csv")

    # User query input
    query = st.text_input("Ask a question:")
    
    if query:
        # Generate and display textual information
        result = generate_text(query, data_frame_1)
        st.subheader("Generated Text:")
        st.write(result)
    else:
        st.info("Enter a question to get started.")

if __name__ == "__main__":
    main()
