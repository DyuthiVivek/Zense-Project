# AutoMeet

## Overview

Are you tired of endless meeting or classes that seem to take up most of your day? Wish you could be more productive while still appearing fully engaged? Look no further! Introducing AutoMeet, a Google Meet Automation tool. Seamlessly integrating with Google Calendar, it ensures timely meeting attendance. From intelligent alerts to voice response, it enables selective engagement and even records meetings and provides a transcript and summary for future reference. 

## Objectives

- **Automated meeting attendance:** Automatically joining meetings at scheduled time
- **Real time engagement:** Intelligent alerts based on trigger words and response back to them
- **Meeting Documentation:** Record audio, transcribe meeting content and generate a summary
- **Efficient time management and convenience:** Attend specific portions of the meeting (or None) but still ensure your participation and attendance


## Implementation and Tech Stack

1. **Google Calendar API** to fetch details of upcoming meetings
2. **Selenium** to automate all interactions will Google Meet
3. **BeautifulSoup** to scrape live captions and chat box messages
4. **Telegram Bot API** to send and receive alerts/responses to and from the user
5. **Tortoise-TTS module** to generate your voice from text
6. **ConfigParserCrypt** to store encrypted user credentials in a config file
7. **PyAudio** to record meeting audio
8. **Popen** and **Signal** to start recording audio as a subprocess and send a stop recording signal
9. **AssemblyAI API** to generate a meeting transcript and a summary

## Challenges 

- **Selenium Google Login Block**
    
    The error,   

    > *This browser or app may not be secure.*
    
    makes it hard for an automation driver to login to Google.

    This was solved by:

    - Turning off Two-Factor Authentication
    - Using `undetected_chromedriver`

    Unfortunately, `undetected_chromedriver` is unable to connect with ChromeDriver at times. The workaround for this is to kill any existing ChromeDriver process and wait for a few seconds.   

    
- **Browser Level Notifications**

    They include notifications such as: *"Allow/Decline camera access"* and *"Allow/Decline microphone access"*. The recommended method of solving this problem, using Chrome Options did not seem to be working in this scenario. 

    This was solved using: 
    `driver.execute_cdp_cmd()`

- **Tool for meeting summary**

    Identifying a free tool for meeting transcription and summary generation was challenging. Most of the popular ones like Tactiq and Laxis offer only limited free transcriptions.


## Future Scope

- **Integration with More Platforms:** Expand the bot's compatibility to include other popular video conferencing platforms like Zoom and Teams to cater to a wider audience.

- **Intelligent response system:** Reduce user involvement further by using AI to provide context-sensitive responses during meetings.

- **Advanced Personalization:** Customizing how the bot engages in different types of meetings.

- **Virtual Avatar:** Creating an personal video avatar of you that can automatically respond to simple questions in the meeting.