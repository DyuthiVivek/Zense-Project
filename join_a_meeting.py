import webbrowser
import time
import math
# importing webdriver from selenium 
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select


import undetected_chromedriver as uc



url = 'https://accounts.google.com/signin/v2/identifier?ltmpl=meet&continue=https%3A%2F%2Fmeet.google.com%3Fhs%3D193&&flowName=GlifWebSignIn&flowEntry=ServiceLogin'

opt = Options()
opt.add_argument("--disable-infobars")
opt.add_argument("start-maximised")
opt.add_argument("--disable-extensions")
# Pass the argument 1 to allow and 2 to block
opt.add_experimental_option("prefs", { \
    "profile.default_content_setting_values.media_stream_mic": 1, 
    "profile.default_content_setting_values.media_stream_camera": 1,
    "profile.default_content_setting_values.geolocation": 1, 
    "profile.default_content_setting_values.notifications": 1 
  })

driver = uc.Chrome(chrome_options = opt)
driver.implicitly_wait(20)

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

# geeting the button by class name 
SignIn = driver.find_element("id","identifierId") 

# clicking on the button 
SignIn.send_keys("dyuthi.vivek@gmail.com")
SignIn.send_keys(Keys.ENTER)

driver.implicitly_wait(10)

EnterPass = driver.find_element("xpath","//*[@id='password']/div[1]/div/div[1]/input")
EnterPass.send_keys("Blossom123!")
EnterPass.send_keys(Keys.ENTER)

time.sleep(2)
driver.implicitly_wait(2000)


EnterCode = driver.find_element("xpath","/html/body/c-wiz/div/div[2]/div/div[1]/div[3]/div/div[2]/div[1]/label/input")
EnterCode.send_keys("rwk-afvc-imv") 
driver.implicitly_wait(2000)
EnterCode.send_keys(Keys.ENTER)

driver.implicitly_wait(2000)
time.sleep(5)

#to allow permissions
#driver.find_element("xpath", "/html/body/div/div[3]/div[2]/div/div/div/div/div[2]/div/div[1]/button").click()
driver.implicitly_wait(200)

#not allow permissions
#driver.find_element("xpath", "/html/body/div/div[3]/div[2]/div/div/div/div/div[2]/div/div[2]/button").click()

time.sleep(2)
driver.implicitly_wait(200)

driver.find_element("xpath", "/html/body/div[1]/c-wiz/div/div/div[14]/div[3]/div/div[2]/div[4]/div/div/div[2]/div[1]/div[2]/div[1]/div[1]/button").click()
time.sleep(5)

TurnOnCaptions = driver.find_element("xpath","/html/body/div[1]/c-wiz/div[1]/div/div[14]/div[3]/div[11]/div/div/div[2]/div/div[3]/span/button")
TurnOnCaptions.click()

#Got it pop up
driver.find_element("xpath", "/html/body/div[1]/div[3]/span/div[2]/div/div/div[2]/div/button").click()

while True:
    time.sleep(1)


