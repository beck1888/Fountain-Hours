# Imports block
import streamlit as st
import hour_manager as hm

# Setup the streamlit web app
st.set_page_config(page_title='The Fountain', page_icon='🍫', layout='centered')

# Main streamlit code
st.title('The Fountain')

# Functions block
def pluralize(number: int, singular: str, plural: str) -> str:
    """Pluralize a word
    
    Args:
        number (int): The number to check
        singular (str): The singular word
        plural (str): The plural word
    
    Returns:
        str: The pluralized word
    """
    if number == 1:
        return singular
    return plural

def convert_minutes_to_minutes_and_hours(minutes: int) -> str:
    """Convert minutes into minutes and hours
    
    Args:
        minutes (int): Minutes to convert
    
    Returns:
        str: Minutes and hours
    """
    hours = minutes // 60
    minutes = minutes % 60
    return f'{hours} {pluralize(hours, "hour", "hours")} and {minutes} {pluralize(minutes, "minute", "minutes")}'

# Check if it is open
if hm.is_open():
    st.success('It is open!')
else:
    st.error('It is closed!')
    # Check how long until open again
    wait_time = hm.how_long_to_open()
    if wait_time == 0:
        st.success('It is now open!')
    elif wait_time == -1:
        st.warning('There are no more open slots today!')
    else:
        st.warning(f'It will be open in {convert_minutes_to_minutes_and_hours(wait_time)} minutes!')