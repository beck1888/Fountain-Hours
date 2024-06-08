import json
import datetime

def minutes_into_day() -> int:
    """Get the number of minutes into the current day
    
    Args:
        None
    
    Returns:
        int: The number of minutes into the current day
    """
    now = datetime.datetime.now()
    current_time = now.replace(hour=0, minute=0, second=0, microsecond=0)
    delta = now - current_time
    minutes = delta.total_seconds() / 60
    return int(minutes)

def get_day() -> str:
    """Get the current day of the week
    
    Args:
        None
    
    Returns:
        str: The current day of the week
    """
    return datetime.datetime.now().strftime("%A")

def get_todays_schedule() -> dict:
    """Get the schedule for the current day
    
    Args:
        None
    
    Returns:
        dict: The schedule for the current day
    """
    with open("schedule.json", "r") as f:
        schedule = json.load(f)
    return schedule[get_day()]

def find_time_slot(minutes: int, schedule: dict) -> str:
    """Find the current time slot based on the number of minutes into the day
    
    Args:
        minutes (int): Number of minutes into the day
        schedule (dict): The schedule for the current day
    
    Returns:
        str: The time slot range in the format 'start-end'
    """
    for time_range in schedule:
        start, end = map(int, time_range.split('-'))
        if start <= minutes <= end:
            return time_range
    return None  # Return None if no matching time slot is found

def is_open() -> bool:
    """Checks what time slot it is, and returns true if the slot is open or not
    
    Args:
        None
    
    Returns:
        bool: True if the slot is open, False if it is closed
    """
    minutes = minutes_into_day()
    schedule = get_todays_schedule()
    time_slot = find_time_slot(minutes, schedule)
    if time_slot:
        return schedule[time_slot]
    return False  # Default to False if no matching time slot is found

def how_long_to_open() -> int:
    """Gets the number of minutes until the next open time slot
    
    Args:
        None
        
    Returns:
        int: The number of minutes until the next open time slot, or 0 if already open, or -1 if no more open slots today
    """
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

def main() -> None:
    print(how_long_to_open())

if __name__ == '__main__':
    main()