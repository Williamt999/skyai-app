# Streamlit user interface
import streamlit as st

# CSS styyling to add home page background image & hide navbar color
# st.image('./data/sky-ai-background-home-6.png',use_container_width=True)

#css = '''
#.stApp {

#    background-image: url('https://github.com/Williamt999/skyai-app/blob/main/data/sky-ai-background-home-6.png');
#    background-size: cover;

#}

#.stApp > header {
#    background-color: transparent;
#}

#'''

#st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)

st.markdown(
    """
    <style>
    .reportview-container {
        background: url('https://github.com/Williamt999/skyai-app/blob/main/data/sky-ai-background-home-6.png')
    }
   .sidebar .sidebar-content {
        background: url('https://github.com/Williamt999/skyai-app/blob/main/data/sky-ai-background-home-6.png')
    }
    </style>
    """,
    unsafe_allow_html=True
)

