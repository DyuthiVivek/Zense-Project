import requests
from get_credentials import get_telegram_token
from pydub import AudioSegment
import os

# .ogg to .wav file
def ogg2wav(ofn):
    wfn = ofn.replace('.ogg','.wav')
    x = AudioSegment.from_file(ofn)
    x.export(wfn, format='wav') 

token = get_telegram_token()
chat_id = 5430419326

# send a message to telegram
def send_a_message(msg):
    data = {'chat_id': chat_id, 'text': msg}
    url = f'https://api.telegram.org/bot{token}/sendMessage'
    requests.post(url, data).json()

# Get ID of last message
def get_last_msg_id():
    url = f'https://api.telegram.org/bot{token}/getUpdates'
    return requests.post(url).json()['result'][-1]['update_id']

# Get all messages sent
def get_all_messages():
    url = f'https://api.telegram.org/bot{token}/getUpdates'
    return requests.post(url).json()

# get newest message sent
def get_new_message():
    url = f'https://api.telegram.org/bot{token}/getUpdates'
    return requests.post(url).json()['result'][-1]['message']['text']

# send screenshot
def send_photo():
    params = {'chat_id': chat_id}
    files = {'photo': open('image.png', 'rb')}
    url = f'https://api.telegram.org/bot{token}/sendPhoto'
    requests.post(url, params, files=files)

# get audio sent
def get_audio(file_id):
    file_info_url = f"https://api.telegram.org/bot{token}/getFile?file_id={file_id}"
    response = requests.get(file_info_url)
    file_path = response.json()['result']['file_path']
    file_url = f"https://api.telegram.org/file/bot{token}/{file_path}"
    response = requests.get(file_url)
    if response.status_code == 200:
        with open("received_audio.ogg", "wb") as f:
            f.write(response.content)

        # convert ogg to wav file
        ogg2wav("received_audio.ogg")
        os.remove("received_audio.ogg")
