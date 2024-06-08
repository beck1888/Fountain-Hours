import json
import datetime
import pytz

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