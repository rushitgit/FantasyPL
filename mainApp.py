import base64
import streamlit as st


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

col1, col2 = st.columns((1,5))

with col1:
    st.image('images/logo2.png', width= 150)

with col2:
    st.markdown("<h1 style='text-align: center; color: black;'></h1>", unsafe_allow_html=True)
    st.markdown("<h1 style='text-align: center; color: black;'>Fantasy Premier League</h1>", unsafe_allow_html=True)
    st.markdown("<h1 style='text-align: center; color: black;'></h1>", unsafe_allow_html=True)
    # st.markdown("<div style='text-align: center; color: black; border: 2px solid rgba(0, 0, 0, 0.3); border-radius: 10px; padding: 10px; margin: 10px;'>"
    #             "<h2 style= 'color: black;'>Average: 40</h2>"
    #             "<h2 style= 'color: black;'>Score: 60</h2>"
    #             "</div>", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align: center; color: black;'>Average:40</h2>", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align: center; color: black;'>Score:60</h2>", unsafe_allow_html=True)
    st.markdown("<h1 style='text-align: center; color: black;'></h1>", unsafe_allow_html=True)

#st.title("Fantasy Premier League")


col3,col4,col5,col6 = st.columns((4,6,30,6))
with col4:
    st.image('images/final_team.png', width= 500)
    #st.image('teamnew.png')
    st.markdown("<h2 style='text-align: left; color: black;'>Substitutes:</h2>", unsafe_allow_html=True) 
    st.markdown("<h5 style='text-align: left; color: black;'>Neto(4.6m)</h5>", unsafe_allow_html=True) 
    st.markdown("<h5 style='text-align: left; color: black;'>Mainoo(4.4m)</h5>", unsafe_allow_html=True) 
    st.markdown("<h5 style='text-align: left; color: black;'>Gusto(4.1m)</h5>", unsafe_allow_html=True) 
    st.markdown("<h5 style='text-align: left; color: black;'>Kelleher(4.0m)</h5>", unsafe_allow_html=True) 


with col6:
   st.markdown("<h1 style='text-align: center; color: white;'>News</h2>", unsafe_allow_html=True) 
   st.image('images/fplnews.png', width= 225)
   st.image('images/rightnews.png', width= 225)
   st.image('images/leftnews1.png', width= 225) 

st.image('images/pep.png')
st.image('images/palmer.png')
st.image('images/debruyne.png')
st.image('images/miley.png')


video_path = "images\My Movie.mp4"
st.video(video_path)


st.markdown("[Redirect to Chatbot](http://localhost:8502)")

