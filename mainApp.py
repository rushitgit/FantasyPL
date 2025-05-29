"""
This script is a Streamlit web application for displaying Fantasy Premier League data.
It includes features like setting a background image, displaying team information,
latest news, a video, and a link to a chatbot.
"""
import base64
import streamlit as st


def get_base64(bin_file):
    """Converts a binary file to a base64 encoded string."""
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()


def set_background(png_file):
    """Sets the background image for the Streamlit application."""
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

# Set the background image for the application
set_background('images/background.png')

# Define columns for layout
col1, col2 = st.columns((1,5))

# Display logo and title
with col1:
    st.image('images/logo2.png', width= 150)

with col2:
    st.markdown("<h1 style='text-align: center; color: black;'></h1>", unsafe_allow_html=True)
    st.markdown("<h1 style='text-align: center; color: black;'>Fantasy Premier League</h1>", unsafe_allow_html=True)
    st.markdown("<h1 style='text-align: center; color: black;'></h1>", unsafe_allow_html=True)
    # Commented out section for average and score display
    # st.markdown("<div style='text-align: center; color: black; border: 2px solid rgba(0, 0, 0, 0.3); border-radius: 10px; padding: 10px; margin: 10px;'>"
    #             "<h2 style= 'color: black;'>Average: 40</h2>"
    #             "<h2 style= 'color: black;'>Score: 60</h2>"
    #             "</div>", unsafe_allow_html=True)
    # TODO: Load Average and Score dynamically.
    # These could come from a configuration file or a future game state data source.
    st.markdown("<h2 style='text-align: center; color: black;'>Average:40</h2>", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align: center; color: black;'>Score:60</h2>", unsafe_allow_html=True)
    st.markdown("<h1 style='text-align: center; color: black;'></h1>", unsafe_allow_html=True)

#st.title("Fantasy Premier League") # Alternative way to set title

# Define columns for team and news display
col3,col4,col5,col6 = st.columns((4,6,30,6))

# Display team information
with col4:
    # TODO: Dynamically generate or select team display.
    # This could be based on player data from 'datasets/PredictedPlayerPoints_All.csv'
    # or 'datasets/TopPlayersWithSentiments.csv'.
    st.image('images/final_team.png', width= 500)
    #st.image('teamnew.png') # Alternative team image
    st.markdown("<h2 style='text-align: left; color: black;'>Substitutes:</h2>", unsafe_allow_html=True)
    # TODO: Populate substitutes list dynamically.
    # This list should be generated from a player dataset, e.g., 'datasets/PredictedPlayerPoints_All.csv',
    # selecting players not in the main team.
    st.markdown("<h5 style='text-align: left; color: black;'>Neto(4.6m)</h5>", unsafe_allow_html=True) 
    st.markdown("<h5 style='text-align: left; color: black;'>Mainoo(4.4m)</h5>", unsafe_allow_html=True) 
    st.markdown("<h5 style='text-align: left; color: black;'>Gusto(4.1m)</h5>", unsafe_allow_html=True) 
    st.markdown("<h5 style='text-align: left; color: black;'>Kelleher(4.0m)</h5>", unsafe_allow_html=True) 

# Display news items
with col6:
   st.markdown("<h1 style='text-align: center; color: white;'>News</h2>", unsafe_allow_html=True)
   # TODO: Dynamically select news images.
   # These could be selected based on content from 'datasets/articles_set.csv'
   # or sentiment analysis results in 'datasets/TopPlayersWithSentiments.csv'.
   st.image('images/fplnews.png', width= 225)
   st.image('images/rightnews.png', width= 225)
   st.image('images/leftnews1.png', width= 225) 

# Display additional images
# TODO: Dynamically choose player images.
# These could be selected based on top players from 'datasets/PredictedPlayerPoints_All.csv'
# or players featured in news/sentiment data from 'datasets/TopPlayersWithSentiments.csv'.
st.image('images/pep.png')
st.image('images/palmer.png')
st.image('images/debruyne.png')
st.image('images/miley.png')

# Display video
video_path = "images\My Movie.mp4" # Note: Backslash in path might cause issues on non-Windows systems
st.video(video_path)

# Display link to chatbot
st.markdown("[Redirect to Chatbot](http://localhost:8502)")

