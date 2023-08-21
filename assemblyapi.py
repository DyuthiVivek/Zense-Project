import requests
import json
import time
from get_credentials import get_assembyai_api

# given the voice recording in output.wav, generates the transcript and summary
def get_transcript():
  base_url = "https://api.assemblyai.com/v2"

  token = get_assembyai_api()

  headers = {
      "authorization": token
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
      print("Transcription completed!")

      dic = {}
      dic['Transcription'] = transcription_result['text']
      dic['Summary'] = summary

      return dic
      # print(f"Transcription: {transcription_result['text']}")
      # print()
      # print(f"Summary: {summary}")
      # break

    elif transcription_result['status'] == 'error':
      print("Transcription failed")

    else:
      time.sleep(3)
