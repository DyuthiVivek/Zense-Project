import time
import sys
from datetime import date, datetime
from meet_functions import *
from quickstart import next_event_details
import telegram

def get_time():
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    return str(current_time)

if __name__ == "__main__":
    # get details from calendar
    event_dic = next_event_details()
    if event_dic is None:
        print('No upcoming events')