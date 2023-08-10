import requests
token = '6526565187:AAFzvJUgnB-9Two9SSKyGcf7FlsDYkRmbFk'

def send_a_message(msg):
    data = {'chat_id': 5430419326, 'text': msg}
    url = f'https://api.telegram.org/bot{token}/sendMessage'
    requests.post(url, data).json()