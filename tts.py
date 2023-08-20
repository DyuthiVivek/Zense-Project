import gtts  
from playsound import playsound  
import os

# Convert text to speech using Google TTS
def text_to_speech(msg):
    t1 = gtts.gTTS(msg, tld = "co.in")
    t1.save("welcome.mp3")   
    playsound("welcome.mp3")    
    os.remove("welcome.mp3")
