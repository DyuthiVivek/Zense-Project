import requests
token = '6526565187:AAFzvJUgnB-9Two9SSKyGcf7FlsDYkRmbFk'

# send a message to telegram
def send_a_message(msg):
    data = {'chat_id': 5430419326, 'text': msg}
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
    print(requests.post(url).json()['result'][-1]['message']['text'])

