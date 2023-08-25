from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup as soup
import undetected_chromedriver as uc
import time
import telegram
import tts
from get_credentials import get_email, get_pwd
import sys
from playsound import playsound  


# get list of trigger words from .txt file 
trigger_words = []
with open('trigger_words.txt') as fp:
    for line in fp:
        trigger_words.append(str(line).strip('\n'))

# initialize WebDriver
def initialize_driver():
    opt = Options()
    opt.add_argument("--disable-infobars")
    opt.add_argument("start-maximised")
    opt.add_argument("--disable-extensions")
    opt.add_experimental_option("prefs", { \
        "profile.default_content_setting_values.media_stream_mic": 1, 
        "profile.default_content_setting_values.media_stream_camera": 1,
        "profile.default_content_setting_values.geolocation": 1, 
        "profile.default_content_setting_values.notifications": 1 
    })

    driver = uc.Chrome(chrome_options = opt, driver_executable_path = '/home/dyuthi/Zense-Project/chromedriver-linux64/chromedriver')
    driver.implicitly_wait(20)

    #enable mic and camera
    driver.execute_cdp_cmd(
        "Browser.grantPermissions",
        {
            "origin": "https://meet.google.com"  , 
            "permissions": ["geolocation", "audioCapture", "displayCapture", "videoCapture",
                            "videoCapturePanTiltZoom"]
        },
    )
    return driver

# close Web Driver
def close_driver(driver):
    driver.close()

# Sign in to Google
def sign_in_to_google(driver):
    url = 'https://accounts.google.com/signin/v2/identifier?ltmpl=meet&continue=https%3A%2F%2Fmeet.google.com%3Fhs%3D193&&flowName=GlifWebSignIn&flowEntry=ServiceLogin'
    driver.get(url)
    # email ID field 
    SignIn = driver.find_element("id","identifierId") 

    # clicking on the button 
    # get email from encrypted file
    SignIn.send_keys(str(get_email()))
    SignIn.send_keys(Keys.ENTER)

    driver.implicitly_wait(10)

    # password field
    # get password from encrypted file
    EnterPass = driver.find_element("xpath","//*[@id='password']/div[1]/div/div[1]/input")
    EnterPass.send_keys(str(get_pwd()))
    EnterPass.send_keys(Keys.ENTER)

# Enter meeting code 
def enter_meet_code(driver, meet_code):
    EnterCode = driver.find_element("xpath","/html/body/c-wiz/div/div[2]/div/div[1]/div[3]/div/div[2]/div[1]/label/input")
    EnterCode.send_keys(meet_code) 
    driver.implicitly_wait(2000)
    EnterCode.send_keys(Keys.ENTER)

    driver.implicitly_wait(200)

# Mute microphone
def mute(driver):
    driver.find_element("xpath", "/html/body/div[1]/c-wiz/div/div/div[14]/div[3]/div/div[2]/div[4]/div/div/div[1]/div[1]/div/div[6]/div[1]/div/div/div[1]").click()

# Turn off the camera
def turn_off_video(driver):
    driver.find_element("xpath", "/html/body/div[1]/c-wiz/div/div/div[14]/div[3]/div/div[2]/div[4]/div/div/div[1]/div[1]/div/div[6]/div[2]/div/div[1]").click()

# Press on join meeting button
def join_meeting(driver):
    driver.find_element("xpath", "/html/body/div[1]/c-wiz/div/div/div[14]/div[3]/div/div[2]/div[4]/div/div/div[2]/div[1]/div[2]/div[1]/div[1]/button").click()

# Turn on closed captioning
def turn_on_CC(driver):
    TurnOnCaptions = driver.find_element("xpath","/html/body/div[1]/c-wiz/div[1]/div/div[14]/div[3]/div[11]/div/div/div[2]/div/div[3]/span/button")
    TurnOnCaptions.click()

# Close a pop up
def close_pop_up(driver):
    driver.find_element("xpath", "/html/body/div[1]/div[3]/span/div[2]/div/div/div[2]/div/button").click()

# Open Chat Box
def activate_chat(driver):
    driver.find_element("xpath", "/html/body/div[1]/c-wiz/div[1]/div/div[14]/div[3]/div[11]/div/div/div[3]/div/div[3]/div/div/span/button").click()
    driver.implicitly_wait(200)

# function to call initializing driver till meeting join and init stuff
def initial_stuff(meet_code):
    # initialize selenium driver
    driver = initialize_driver()

    # sign in to google
    sign_in_to_google(driver)
    time.sleep(2)

    # entering google meet code
    enter_meet_code(driver, meet_code)
    time.sleep(4)

    # mute microphone and turn off camera
    mute(driver)
    turn_off_video(driver)
    time.sleep(2)

    # join the meeting
    join_meeting(driver)

    time.sleep(2)
    # turn on captions
    turn_on_CC(driver)

    # close a pop up
    close_pop_up(driver)

    # activate chat box
    activate_chat(driver)


    return driver
    
# Send a message in the Chat Box
def send_a_message_in_chat(msg, driver):
    chat = driver.find_element("xpath", "/html/body/div[1]/c-wiz/div[1]/div/div[14]/div[3]/div[4]/div[2]/div/div[2]/div/div[2]/div[1]/div/label/textarea")           
    chat.send_keys(msg) 
    driver.implicitly_wait(200)
    chat.send_keys(Keys.ENTER)

# Scrape the Chat Box using BeautifulSoup
def scrape(driver, chat_dic):
    html = driver.page_source
    page_soup = soup(html, "html.parser")
    x = page_soup.find_all("div", {"class":"GDhqjd"})
    
    new_msg = []
    try:
        for y in x:
            sender = y.find("div", {"class":"YTbUzc"}).get_text()
            time_stamp = ' '.join(y.find("div",{"class":"MuzmKe"}).get_text().split('\u202f'))
            msgs = y.find_all("div",{"class":"oIy2qc"})
            msgs_list = []

            for msg in msgs:
                msgs_list.append(msg.get_text())
            
            # append only new messages to ensure that messages sent to the user are not sent again
            if (sender, time_stamp) not in chat_dic:
                new_msg.append((sender, msgs_list))

            elif chat_dic[(sender, time_stamp)] != msgs_list:
                new_msg.append((sender, [msg for msg in msgs_list if msg not in chat_dic[(sender, time_stamp)]]))
            
            chat_dic[(sender, time_stamp)] = msgs_list
    except:
        pass
    return new_msg

# Get Closed Captions
def get_cc(flag, driver):

    try:
        # get the captions text
        captions = driver.find_element("xpath", "/html/body/div[1]/c-wiz/div[1]/div/div[14]/div[3]/div[7]/div[1]/div[1]")
        #print(captions.text)
        if flag:
            for t in trigger_words:
                # check if any trigger words are in the text
                if t in str(captions.text).lower():
                    msg = 'Trigger word alert!'
                    telegram.send_a_message(msg)
                    time.sleep(2)

                    # take screenshot
                    driver.save_screenshot("image.png")
                    captions = driver.find_element("xpath", "/html/body/div[1]/c-wiz/div[1]/div/div[14]/div[3]/div[7]/div[1]/div[1]")
                    text = captions.text

                    # send the user an alert with the transcript
                    telegram.send_a_message(text)
                    telegram.send_photo()
                    flag = False
                    break

        else:
            # to ensure that once an alert is sent, it should not send the alert again for the same text
            # since we are getting all the captions text at once
            for t in trigger_words:
                if t in str(captions.text).lower():
                    break
            else:
                flag = True
    except:
        pass
    
    return flag

# Get messages from user in telegram
def message_from_telegram(last_msg_id, driver):
    # if new message detected
    if telegram.get_last_msg_id() != last_msg_id:
        messages = telegram.get_all_messages()['result']
        for i in range(len(messages)):
            dic = messages[i]
            if dic['update_id'] == last_msg_id:
                messages = messages[i + 1 : ]
                break
        for m in messages:
            if 'voice' in m['message']:
                driver.find_element("xpath","/html/body/div[1]/c-wiz/div[1]/div/div[14]/div[3]/div[11]/div/div/div[2]/div/div[1]/div/div[2]/span/button").click()
                telegram.get_audio(m['message']['voice']['file_id'])
                playsound("received_audio.wav")
                driver.find_element("xpath","/html/body/div[1]/c-wiz/div[1]/div/div[14]/div[3]/div[11]/div/div/div[2]/div/div[1]/div/div[2]/span/button").click()

            # if the user wants to send this message in chat
            elif 'text' in m['message'] and str(m['message']['text']).startswith("Chat:"):
                m['message']['text'] = str(m['message']['text'][5:]).strip()
                send_a_message_in_chat(m['message']['text'], driver)

            # if the user wants it to be spoken
            elif 'text' in m['message'] and str(m['message']['text']).startswith("Speak:"):
                driver.find_element("xpath","/html/body/div[1]/c-wiz/div[1]/div/div[14]/div[3]/div[11]/div/div/div[2]/div/div[1]/div/div[2]/span/button").click()
                msg = str(m['message']['text'][6:]).strip()

                # convert text to speech using Google TTS
                tts.text_to_speech(msg)
                time.sleep(1)
                driver.find_element("xpath","/html/body/div[1]/c-wiz/div[1]/div/div[14]/div[3]/div[11]/div/div/div[2]/div/div[1]/div/div[2]/span/button").click()

        # update last message ID
        last_msg_id = telegram.get_last_msg_id()

    return last_msg_id

# If trigger word mentioned in chat, sending to telegram
# Sending the sender of the message and timestamp as well
def send_message_to_telegram(new_msg, prev_chat, chat_dic):
    # ensuring that messages already sent are not sent again
    for n in new_msg:
        for p in n[1]:
            for t in trigger_words:
                if t in p.lower():
                    msg = ""
                    for c in chat_dic:
                        if c in prev_chat:
                            if prev_chat[c] != chat_dic[c]:
                                msg += f"Sender: {c[0]}  Time: {c[1]}\n"
                                msg += '\n'.join(x for x in chat_dic[c] if x not in prev_chat[c])
                                msg += '\n'
                        else:
                            msg += f"Sender: {c[0]}  Time: {c[1]}\n"
                            msg += '\n'.join(chat_dic[c])
                            msg += '\n'

                    prev_chat = chat_dic.copy()
                    telegram.send_a_message(msg)
                    break
    return prev_chat

# checking if return to home screen element is appearing
def is_element_appeared(element_Xpath, driver, timeout = 2):
    try:
        wait = WebDriverWait(driver, timeout=timeout)
        driver.implicitly_wait(timeout)
        driver.find_element(By.XPATH,element_Xpath)
        return True
    except Exception as ex:
        return False

# check if meeting has ended yet 
def check_meeting(driver):

    # check if return to home screen button is present
    try:
        if is_element_appeared("/html/body/div[1]/c-wiz/div/div/div[1]/div[2]/div/button",driver):
            # found, so exit meeting
            return False
    except:
        pass
    
    # check if home screen present
    try:
        if is_element_appeared("/html/body/c-wiz/div/div[2]/div/div[1]/div[3]/div/div[1]/div[1]/div/button",driver):
            # found, so exit meeting
            return False
    except:
        pass

    # the meeting has not ended 
    return True
