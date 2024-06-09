## Imports block
import streamlit as st
import hour_manager as hm
from streamlit.components.v1 import html
import datetime

## Setup the streamlit web app
st.set_page_config(page_title='The Fountain', page_icon='🍫', layout='centered')

## Functions block
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

def convert_minutes_to_12_hour_format(minutes: int) -> str:
    """Convert minutes into 12 hour format
    
    Args:
        minutes (int): Minutes to convert
    
    Returns:
        str: 12 hour format
    """
    hours = minutes // 60
    minutes = minutes % 60
    if hours > 12:
        hours = hours - 12
        am_pm = 'PM'
    else:
        am_pm = 'AM'
    return f'{hours}:{minutes:02d} {am_pm}'

## Main streamlit code

## Check how long until open again
wait_time = hm.how_long_to_open()
if wait_time == 0:
    html(hm.make_html_message('green', 'The fountain is now open!', '30'))
elif wait_time == -1:
    html(hm.make_html_message('black','The Fountain Is Closed for the Rest of Today.', '30'))
else:
    html(hm.make_html_message('red', 'The fountain will open in', '30'))
    html(hm.make_html_countdown_timer(hm.get_start_minutes_of_next_open_slot()))
