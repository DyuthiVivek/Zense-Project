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
        sys.exit()

    # no meet today
    if not(event_dic['start_time'][:10].strip('T') == str(date.today())):
        sys.exit()
    
    while True:
        if event_dic['start_time'][11:19].strip('T') <= get_time():
            break
        else:
            print('wait')

            time.sleep(30)
    

    meet_code = event_dic['link'][24:]

    driver = initial_stuff(meet_code)

    chat_dic = {}
    new_msg = []
    prev_chat = {}
    last_msg_id = telegram.get_last_msg_id()
    flag = True

    while True:
        # print("Looping...")
        flag = get_cc(flag, driver)
        last_msg_id = message_from_telegram(last_msg_id, driver)
        time.sleep(2)
        new_msg = scrape(driver, chat_dic)
        prev_chat = send_message_to_telegram(new_msg, prev_chat, chat_dic)

        if event_dic['end_time'][11:19].strip('T') <= get_time() and event_dic['end_time'][:10].strip('T') == str(date.today()):
            close_driver(driver)
            sys.exit()


        if not(check_meeting(driver)):
            print('meeting exited')
            break

        # print("After check_meeting...")
    
    close_driver(driver)
    sys.exit()

# fix telegram
# calendar api refresh
# property file, password encryption
# will the program be running all the time?
