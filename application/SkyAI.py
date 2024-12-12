# Streamlit user interface
import streamlit as st


# CSS styyling to add home page background image & hide navbar color
css = '''
.stApp {

    background-image: url("https://soundcertified.com/wp-content/uploads/2024/12/sky-ai-background-home-6.png");
    background-size: cover;

}

.stApp > header {
    background-color: transparent;
}

'''

st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)
