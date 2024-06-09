import json
import pytz
import datetime
from datetime import timedelta

def minutes_into_day() -> int:
    """Get the number of minutes into the current day in Lake Tahoe (Pacific Time Zone)"""
    pacific = pytz.timezone("America/Los_Angeles")
    now = datetime.datetime.now(pacific)
    current_time = now.replace(hour=0, minute=0, second=0, microsecond=0)
    delta = now - current_time
    minutes = delta.total_seconds() / 60
    return int(minutes)

def get_day() -> str:
    """Get the current day of the week in Lake Tahoe (Pacific Time Zone)"""
    pacific = pytz.timezone("America/Los_Angeles")
    now = datetime.datetime.now(pacific)
    return now.strftime("%A")

def get_todays_schedule() -> dict:
    """Get the schedule for the current day"""
    with open("schedule.json", "r") as f:
        schedule = json.load(f)
    return schedule[get_day()]

def find_time_slot(minutes: int, schedule: dict) -> str:
    """Find the current time slot based on the number of minutes into the day"""
    for time_range in schedule:
        start, end = map(int, time_range.split('-'))
        if start <= minutes <= end:
            return time_range
    return None  # Return None if no matching time slot is found

def is_open() -> bool:
    """Checks what time slot it is, and returns true if the slot is open or not"""
    minutes = minutes_into_day()
    schedule = get_todays_schedule()
    time_slot = find_time_slot(minutes, schedule)
    if time_slot:
        return schedule[time_slot]
    return False  # Default to False if no matching time slot is found

def how_long_to_open() -> int:
    """Gets the number of minutes until the next open time slot"""
    minutes = minutes_into_day()
    schedule = get_todays_schedule()
    
    # Check if currently open
    for time_range, status in schedule.items():
        start, end = map(int, time_range.split('-'))
        if start <= minutes <= end:
            if status:
                return 0
    
    # Find the next open slot
    for time_range, status in sorted(schedule.items(), key=lambda x: int(x[0].split('-')[0])):
        start, end = map(int, time_range.split('-'))
        if minutes < start and status:
            return start - minutes
    
    # If no more open slots today
    return -1

def get_start_minutes_of_next_open_slot() -> int:
    """Get the start minutes of the next open time slot"""
    minutes = minutes_into_day()
    schedule = get_todays_schedule()
    
    # Find the next open slot
    for time_range, status in sorted(schedule.items(), key=lambda x: int(x[0].split('-')[0])):
        start, end = map(int, time_range.split('-'))
        if minutes < start and status:
            return start
    return None  # Return None if no matching time slot is found

def make_html_countdown_timer(minutes_into_day) -> str:
    """Make a html countdown timer

    Args:
        minutes_into_day (int): Minutes into the day

    Returns:
        str: HTML countdown timer
    """
    # Get current time in California
    cali_tz = pytz.timezone('America/Los_Angeles')
    now = datetime.datetime.now(cali_tz)
    
    # Calculate the target time based on minutes into the day
    target_time = now.replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(minutes=minutes_into_day)
    if target_time < now:
        target_time += timedelta(days=1)  # Move to the next day if the target time is in the past
    
    target_epoch = int(target_time.timestamp())
    
    my_html = f"""
    <script>
    function startTimer(targetTime, display) {{
        display.textContent = "Loading...";
        setTimeout(function() {{
            setInterval(function () {{
                var now = Math.floor(new Date().getTime() / 1000);
                var diff = targetTime - now;
                var hours = Math.floor(diff / 3600).toString().padStart(2, '0');
                var minutes = Math.floor((diff % 3600) / 60).toString().padStart(2, '0');
                var seconds = Math.floor(diff % 60).toString().padStart(2, '0');

                display.textContent = hours + " : " + minutes + " : " + seconds + "";

                if (diff <= 0) {{
                    clearInterval(this);
                    display.textContent = "The Fountain Has Opened!";
                }}
            }}, 1000);
        }}, 1000); // Simulate loading time
    }}

    window.onload = function () {{
        var targetTime = {target_epoch};
        var display = document.querySelector('#time');
        startTimer(targetTime, display);
    }};
    </script>

    <style>
    #time {{
        font-size: 26px;
        color: blue;
        font-weight: bold;
        display: flex;
        justify-content: center;
        align-items: center;
        height: 100vh;
    }}
    </style>

    <body>
      <div id="time">00 : 00 : 00</div>
    </body>
    """
    return my_html

def make_html_message(color: str, message: str, size: str = '26') -> str:
    """Make a html message with the specified color

    Args:
        color (str): Color of the message text
        size (str): Size of the message text, default is 26   
        message (str): Message text to display

    Returns:
        str: HTML message
    """
    my_html = f"""
    <style>
    #message {{
        font-size: {size}px;
        color: {color};
        font-weight: bold;
        display: flex;
        justify-content: center;
        align-items: center;
        height: 100vh;
    }}
    </style>

    <body>
      <div id="message">{message}</div>
    </body>
    """
    return my_html