## Imports block
import streamlit as st
import hour_manager as hm
import datetime
import json

## Setup the streamlit web app
st.set_page_config(page_title='The Fountain', page_icon='🍫', layout='centered')

## Main streamlit code
st.title('The Fountain')

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

## Check if it is open
if hm.is_open():
    st.success('It is open!')
else:
    st.error('It is closed!')
    ## Check how long until open again
    wait_time = hm.how_long_to_open()
    if wait_time == 0:
        st.success('It is now open!')
    elif wait_time == -1:
        st.warning('There are no more open slots today!')
    else:
        st.warning(f'It will be open at {convert_minutes_to_12_hour_format(wait_time + hm.minutes_into_day())} ({convert_minutes_to_minutes_and_hours(wait_time)})')

## Debug info
with st.expander('Show debug info', expanded=False):
    st.markdown('## Information calculated')
    st.markdown('**Calculated minutes into the day:** ' + str(hm.minutes_into_day()))
    st.markdown('**Calculated day:** ' + str(hm.get_day()))
    st.markdown('**Calculated todays schedule:** ' + str(hm.get_todays_schedule()))
    st.markdown('**Calculated time slot:** ' + str(hm.find_time_slot(0, hm.get_todays_schedule())))
    st.markdown('**Calculated open status:** ' + str(hm.is_open()))
    st.markdown('**Calculated time until open:** ' + str(hm.how_long_to_open()))
    st.divider()
    st.markdown('## Data sources')
    st.markdown('**System timestamp:** ' + str(datetime.datetime.now()))
    st.markdown('**Formatted system timestamp:** ' + datetime.datetime.now().strftime("%I:%M %p"))

    st.markdown('**Full schedule from json file:**')

    with open('schedule.json', 'r') as f:
        st.json(json.load(f))

    st.markdown('**Table of times from sign outside store**')
    table_of_times = """
| Day       | Morning      | Afternoon    | Evening         |
|-----------|--------------|--------------|-----------------|
| Sunday    | 9am - 12pm   | 1pm - 5:45pm | 9pm - 10:30pm   |
| Monday    | 9am - 12pm   | 1pm - 5:45pm | 7:30pm - 10pm   |
| Tuesday   | 9am - 12pm   | 1pm - 5:45pm | 7:30pm - 10pm   |
| Wednesday | 9am - 11am   | 2pm - 2:45pm | 8:30pm - 10:30pm|
| Thursday  | 9am - 12pm   | 1pm - 5:45pm | 9pm - 10:30pm   |
| Friday    | 9am - 12pm   | 1pm - 5:45pm | 9:15pm - 10:45pm|
| Saturday  | Closed       | Closed       | 9pm - 10pm      |
"""
    st.markdown(table_of_times)