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

#st.title("Fantasy Premier League")


col3,col4 = st.columns((1,5))

with col4:
    st.image('images/custom.png', width= 500)
    #st.image('teamnew.png')