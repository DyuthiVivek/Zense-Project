import time
import sys
from datetime import date, datetime
from meet_functions import *
from google_calendar import next_event_details
import telegram
from subprocess import Popen
import os
import signal
from assemblyapi import get_transcript
from mail import send_mail

# function to get current time
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
    
    # not yet time for the meeting
    while True:
        if event_dic['start_time'][11:19].strip('T') <= get_time():
            break
        else:
            print('wait')

            time.sleep(30)
    
    # get meet code from event details
    meet_code = event_dic['link'][24:]

    # initialize driver, join meeting, turn on CC and chat 
    driver = initial_stuff(meet_code)

    chat_dic = {}
    new_msg = []
    prev_chat = {}
    last_msg_id = telegram.get_last_msg_id()
    flag = True

    # start recording audio
    p = Popen('/home/dyuthi/Zense-Project/record.py', shell=False)
    processId = p.pid
    # print("Process ID is", processId)

    while True:
        # print("Looping...")

        # get CC
        flag = get_cc(flag, driver)

        # get the last message from telegram
        last_msg_id = message_from_telegram(last_msg_id, driver)
        time.sleep(2)

        # scrape chatbox
        new_msg = scrape(driver, chat_dic)

        # send any messages to telegram
        prev_chat = send_message_to_telegram(new_msg, prev_chat, chat_dic)

        # if meeting end time reached, exit the meeting
        if event_dic['end_time'][11:19].strip('T') <= get_time() and event_dic['end_time'][:10].strip('T') == str(date.today()):
            print('meeting exited')
            break
        
        # check if the meeting has been ended
        if not(check_meeting(driver)):
            print('meeting exited')
            break

        # print("After check_meeting...")
    
    # outside the meeting

    # close driver
    close_driver(driver)

    # stop recording
    os.kill(processId, signal.SIGINT)
    time.sleep(1)
    print("Done")

    # print the transcript and summary
    content = get_transcript()
    mail_body = "Transcription:\n" + content['Transcription'] + '\n\n' + 'Summary:\n' + content['Summary']
    mail_subject = 'Transcript and summary from '
    if 'details' in event_dic:
        mail_subject += event_dic['details']
        mail_subject += ' '
    mail_subject += event_dic['start_time']
    send_mail(mail_body, mail_subject)
    sys.exit()

# fix telegram
# calendar api refresh
