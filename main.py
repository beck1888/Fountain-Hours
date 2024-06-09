## Imports block
import streamlit as st
import hour_manager as hm
from streamlit.components.v1 import html

## Setup the streamlit web app
st.set_page_config(page_title='The Fountain', page_icon='🍫', layout='centered')

## Remove the whitespace from the top bar
st.markdown("""
        <style>
               .block-container {
                    padding-top: 3rem;
                    padding-bottom: 0rem;
                    padding-left: 5rem;
                    padding-right: 5rem;
                }
        </style>
        """, unsafe_allow_html=True)

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

with st.container(border=True):
    ## Check how long until open again
    wait_time = hm.how_long_to_open()
    if wait_time == 0:
        html(hm.make_html_message('green', 'The Fountain Is Now Open!', '30'))
    elif wait_time == -1:
        html(hm.make_html_message('black','The Fountain Is Closed for the Rest of Today.', '30'))
    else:
        html(hm.make_html_message('red', 'The Fountain is Closed!', '30'))
        html(hm.make_html_message('orange', 'The Fountain Will Open In', '18'))
        html(hm.make_html_countdown_timer(hm.get_start_minutes_of_next_open_slot()))

# Show full schedule
with st.expander('View Full Schedule', expanded=False):
    table_of_times = """
    | Day       | Morning      | Afternoon    | Evening         |
    |-----------|--------------|--------------|-----------------|
    | **Sunday**    | 9am - 12pm   | 1pm - 5:45pm | 9pm - 10:30pm   |
    | **Monday**    | 9am - 12pm   | 1pm - 5:45pm | 7:30pm - 10pm   |
    | **Tuesday**   | 9am - 12pm   | 1pm - 5:45pm | 7:30pm - 10pm   |
    | **Wednesday** | 9am - 11am   | 2pm - 2:45pm | 8:30pm - 10:30pm|
    | **Thursday**  | 9am - 12pm   | 1pm - 5:45pm | 9pm - 10:30pm   |
    | **Friday**    | 9am - 12pm   | 1pm - 5:45pm | 9:15pm - 10:45pm|
    | **Saturday**  | Closed       | Closed       | 9pm - 10pm      |
    """
    st.markdown(table_of_times)