import requests
import json
import time

def get_transcript():
  base_url = "https://api.assemblyai.com/v2"

  headers = {
      "authorization": "0bd8f34e52ae49039d8bb4a0f6c8d280"
  }

  with open("output.wav", "rb") as f:
    response = requests.post(base_url + "/upload",
                            headers=headers,
                            data=f)

  upload_url = response.json()["upload_url"]

  data = {
      "audio_url": upload_url,
      "summarization": True,
      "summary_model": "informative",
      "summary_type": "bullets"
  }

  url = base_url + "/transcript"
  response = requests.post(url, json=data, headers=headers)

  transcript_id = response.json()['id']
  polling_endpoint = f"https://api.assemblyai.com/v2/transcript/{transcript_id}"

  while True:
    transcription_result = requests.get(polling_endpoint, headers=headers).json()

    if transcription_result['status'] == 'completed':
      summary = transcription_result.get('summary', '')
      # print("Transcription completed!")
      print(f"Transcription: {transcription_result['text']}")
      print()
      print(f"Summary: {summary}")
      break

    elif transcription_result['status'] == 'error':
      print("Transcription failed")

    else:
      time.sleep(3)
