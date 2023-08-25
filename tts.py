import gtts  
from playsound import playsound  
import os

# Convert text to speech using Google TTS
def text_to_speech(msg):
    t1 = gtts.gTTS(msg, tld = "co.in")
    t1.save("audio.mp3")   
    playsound("audio.mp3")    
    os.remove("audio.mp3")
