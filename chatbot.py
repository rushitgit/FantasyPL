from dotenv import load_dotenv
import streamlit as st
import pandas as pd
import openai
import os 
import base64
load_dotenv()
# Set your OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")
background_path = "images\background.png"
# Function to set the background image


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
set_background('images/background.png')


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
    st.title("Fantasy Premier League Chatbot")
    # st.image("chatbot_logo.png", width=200)  # Add your chatbot logo or emoticon

    # Load CSV data (Default file paths, change as needed)
    data_frame_1 = load_csv("datasets\TopPlayersWithSentiments.csv")

    # User query input
    query = st.text_input("Chat with us.")
    
    if query:
        # Generate and display textual information
        result = generate_text(query, data_frame_1)
        st.subheader("Generated Text:")
        st.write(result)
    else:
        st.info("Enter a question to get started.")


    st.write("We are a statistical based chatbot for aiding you to make the best decisions for your Fantasy Premier League team.")

if __name__ == "__main__":
    main()
