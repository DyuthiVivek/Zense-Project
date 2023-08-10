import time
import telegram
# importing webdriver from selenium 
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup as soup



import undetected_chromedriver as uc

from quickstart import next_event_details
dic = next_event_details()

scrape_url = dic['link']
meet_code = dic['link'][24:]
print(meet_code)

url = 'https://accounts.google.com/signin/v2/identifier?ltmpl=meet&continue=https%3A%2F%2Fmeet.google.com%3Fhs%3D193&&flowName=GlifWebSignIn&flowEntry=ServiceLogin'

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

driver = uc.Chrome(chrome_options = opt)
driver.implicitly_wait(20)

#enable mic and camera
driver.execute_cdp_cmd(
    "Browser.grantPermissions",
    {
        "origin": "https://meet.google.com"  ,   # e.g https://www.google.com
        "permissions": ["geolocation", "audioCapture", "displayCapture", "videoCapture",
                        "videoCapturePanTiltZoom"]
    },
)
# Opening the website 
driver.get(url) 

# email ID field 
SignIn = driver.find_element("id","identifierId") 

# clicking on the button 
SignIn.send_keys("dyuthi.vivek@gmail.com")
SignIn.send_keys(Keys.ENTER)

driver.implicitly_wait(10)

# password field
EnterPass = driver.find_element("xpath","//*[@id='password']/div[1]/div/div[1]/input")
EnterPass.send_keys("Blossom123!")
EnterPass.send_keys(Keys.ENTER)

time.sleep(2)
driver.implicitly_wait(2000)

#meeting code enter
EnterCode = driver.find_element("xpath","/html/body/c-wiz/div/div[2]/div/div[1]/div[3]/div/div[2]/div[1]/label/input")
EnterCode.send_keys(meet_code) 
driver.implicitly_wait(2000)
EnterCode.send_keys(Keys.ENTER)

driver.implicitly_wait(200)
time.sleep(5)

#to allow permissions
#driver.find_element("xpath", "/html/body/div/div[3]/div[2]/div/div/div/div/div[2]/div/div[1]/button").click()

#not allow permissions
#driver.find_element("xpath", "/html/body/div/div[3]/div[2]/div/div/div/div/div[2]/div/div[2]/button").click()

driver.implicitly_wait(20)

#mute mic
driver.find_element("xpath", "/html/body/div[1]/c-wiz/div/div/div[14]/div[3]/div/div[2]/div[4]/div/div/div[1]/div[1]/div/div[6]/div[1]/div/div/div[1]").click()

#switch off video
driver.find_element("xpath", "/html/body/div[1]/c-wiz/div/div/div[14]/div[3]/div/div[2]/div[4]/div/div/div[1]/div[1]/div/div[6]/div[2]/div/div[1]").click()

driver.implicitly_wait(20)
time.sleep(2)

#join meeting 
driver.find_element("xpath", "/html/body/div[1]/c-wiz/div/div/div[14]/div[3]/div/div[2]/div[4]/div/div/div[2]/div[1]/div[2]/div[1]/div[1]/button").click()
time.sleep(2)

#turn on CC
TurnOnCaptions = driver.find_element("xpath","/html/body/div[1]/c-wiz/div[1]/div/div[14]/div[3]/div[11]/div/div/div[2]/div/div[3]/span/button")
TurnOnCaptions.click()

#Got it pop up
driver.find_element("xpath", "/html/body/div[1]/div[3]/span/div[2]/div/div/div[2]/div/button").click()

send_a_message = True

def send_a_message_in_chat(msg):
    driver.find_element("xpath", "/html/body/div[1]/c-wiz/div[1]/div/div[14]/div[3]/div[11]/div/div/div[3]/div/div[3]/div/div/span/button").click()
    driver.implicitly_wait(200)
    chat = driver.find_element("xpath", "/html/body/div[1]/c-wiz/div[1]/div/div[14]/div[3]/div[4]/div[2]/div/div[2]/div/div[2]/div[1]/div/label/textarea")           
    chat.send_keys(msg) 
    driver.implicitly_wait(200)
    chat.send_keys(Keys.ENTER)

def get_cc():
    captions = driver.find_element("xpath", "/html/body/div[1]/c-wiz/div[1]/div/div[14]/div[3]/div[7]/div[1]/div[1]")
    if "Dyuthi" in captions.text:
        print(captions.text)

chat_dic = {}


def scrape():
    html = driver.page_source
    page_soup = soup(html, "html.parser")
    x = page_soup.find_all("div", {"class":"GDhqjd"})
    
    for y in x:
        sender = y.find("div", {"class":"YTbUzc"}).get_text()
        time_stamp = ' '.join(y.find("div",{"class":"MuzmKe"}).get_text().split('\u202f'))
        msgs = y.find_all("div",{"class":"oIy2qc"})
        msgs_list = []

        for msg in msgs:
            msgs_list.append(msg.get_text())

        if (sender, time_stamp) not in chat_dic:
            new_msg.append((sender, msgs_list))

        elif chat_dic[(sender, time_stamp)] != msgs_list:
            new_msg.append((sender, [msg for msg in msgs_list if msg not in chat_dic[(sender, time_stamp)]]))
        
        chat_dic[(sender, time_stamp)] = msgs_list

def compose_msg(chat_dic):
    msg = ""

    for c in chat_dic:
        msg += f'Sender: {c[0]}  Time: {c[1]}\n'
        msg += '\n'.join(chat_dic[c])
        msg += '\n\n'
    
    return msg


new_msg = []
prev_chat = {}

while True:
    get_cc()

    if send_a_message:
        send_a_message_in_chat("hello")
        send_a_message = False
    
    time.sleep(2)

    new_msg = []

    scrape()

    for n in new_msg:
        for p in n[1]:
            if 'Dyuthi' in p:
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

    time.sleep(1)

   
    
    
    #time.sleep(1)

