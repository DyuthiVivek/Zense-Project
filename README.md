# AutoMeet

## Overview

Are you tired of endless meeting or classes that seem to take up most of your day? Wish you could be more productive while still appearing fully engaged? Look no further! Introducing AutoMeet, a Google Meet Automation tool. Seamlessly integrating with Google Calendar, it ensures timely meeting attendance. From intelligent alerts to voice response, it enables selective engagement and even records meetings and provides a transcript and summary for future reference. 

## Objectives

- **Automated meeting attendance:** Automatically joining meetings at scheduled time.
- **Real time engagement:** Intelligent alerts based on trigger words. Receive live transcript and a screenshot, and respond back to them.
- **Meeting Documentation:** Record audio, transcribe meeting content and generate a summary.
- **Efficient time management and convenience:** Attend specific portions of the meeting (or None) but still ensure your participation and attendance.


## Implementation and Tech Stack

1. **Google Calendar API** to fetch details of upcoming meetings
2. **Selenium** to automate all interactions will Google Meet
3. **BeautifulSoup** to scrape live captions and chat box messages
4. **Telegram Bot API** to send and receive alerts/responses to and from the user
5. **GTTS module** to generate speech from text
6. **ConfigParserCrypt** to store encrypted user credentials in a config file
7. **PyAudio** to record meeting audio
8. **Popen** and **Signal** to start recording audio as a subprocess and stop recording
9. **AssemblyAI API** to generate a meeting transcript and a summary
10. **Smtplib** and **Email Python Library** to mail the transcript and summary


## Installation

1. Clone/download this repository.
2. Ensure that python3.10 is installed.
3. Create a virtual environment.

    > `virtualenv -p <path to python3.10> venv`

4. Activate the virtual environment.

    > `source venv/bin/activate`

5. Install requirements.

    > `pip install -r requirements.txt`

6. Turn off Two-Factor Authentication for the account you want to join the meeting with.

7. Enter your email ID and password in `set_up_config.py`.

8. Sign up at  https://www.assemblyai.com/dashboard/signup and get your API key. Paste it in `set_up_config.py`.

9. Go to telegram and search for @BotFather. Follow the displayed steps to create a new bot. Paste the API token at `set_up_config.py`. Add your chat ID in `telegram.py`.

    You will be required to send a message to the bot the first time to complete authentication.

10. Run `set_up_config.py`. Now all your credentials will be saved in an encrypted config file. Paste the AES key that is printed in `get_credentials.py`. 

11. Go to https://developers.google.com/calendar/api/quickstart/python and follow the given steps to create a Google Cloud Project and enable Google Calendar API. A JSON file will be downloaded. Save it as `credentials.json` and move it to the current working directory.

    You will be required to sign in to your account when running the program for the first time to complete authentication.

12. Save the trigger words for which you want alerts during the call in `trigger_words.txt`. Each word should be typed on a separate line. You will get the alerts on telegram.

13. Install a ChromeDriver according to your Chrome version from https://chromedriver.chromium.org/downloads. Save it in the current working directory.

14. Run `chromedriver` in a different terminal. Run `main.py` from the same terminal with the virtual environment.

15. The transcript and summary of the meeting will be mailed to you at the end of the meeting.

## Challenges 

- **Selenium Google Login Block**
    
    The error,   

    > *This browser or app may not be secure.*
    
    makes it hard for an automation driver to login to Google.

    This was solved by:

    - Turning off Two-Factor Authentication
    - Using `undetected_chromedriver`

    `undetected_chromedriver` is unable to connect with ChromeDriver at times. The workaround for this is to kill any existing ChromeDriver process and wait for a few seconds. It appears to be more stable with python version 3.10.  

    
- **Browser Level Notifications**

    Includes notifications such as: *"Allow/Decline camera access"* and *"Allow/Decline microphone access"*. The recommended method of solving this problem, using Chrome Options did not work in this scenario. 

    This was solved using: 
    `driver.execute_cdp_cmd()`

- **Your voice TTS**

    Tortoise-TTS module generates text-to-speech for your own voice. Despite adding many voice samples, my voice was not replicated as this module was trained with American accents.  Tortoise also takes a long time to generate audio, making it unviable for realtime responses in meetings.

- **Tool for meeting transcript and summary**

    Identifying a free tool for meeting transcription and summary generation was challenging. Most of the popular ones like Tactiq and Laxis offer only limited free transcriptions. Obtaining the transcript from the live captions in Google Meet by scraping the captions periodically resulted in occasional overlapping and missed content.

    This problem was solved by recording the audio and using AssemblyAI to generate the transcript and summary.


## Future Scope

- **Integration with More Platforms:** Expand the bot's compatibility to include other popular video conferencing platforms like Zoom and Teams to cater to a wider audience.

- **Intelligent response system:** Reduce user involvement further by using AI to provide context-sensitive responses during meetings.

- **Advanced Personalization:** Customizing voice to make it sound like you.

- **Virtual Avatar:** Creating an personal video avatar of you that can automatically respond to simple questions in the meeting.