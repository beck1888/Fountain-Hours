# Imports block
import streamlit as st

# Setup the streamlit web app
st.set_page_config(page_title='TAB_TITLE', page_icon='👋🏻', layout='wide')

if ['step'] not in st.session_state: # Items must be created to avoid errors later
    st.session_state.step = 'init'

# Helper functions
def do_a_thing():
    ...

# Main streamlit code
st.title('APP')