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




st.write ("If I need Cameron Archer to come on, then that's what he's there for. Yeah, right. Oscar, your team's up next. Now, of course, you told us you'd already sold Haaland. So, who have you brought in to replace him? Drumroll. Yeah, it was Solanke. Solanke’s come in for a hit. Yeah, I think I've already had Watkins. I think he's just the obvious pick with those fixtures. He's second for expected goal-in-a-bombing over the last four game weeks. He's taken 14 shots in the box, which is topping the league over that run.")