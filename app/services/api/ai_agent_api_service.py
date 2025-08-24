import requests
import os
OLLAMA_URL = os.getenv("OLLAMA_URL")

def request_ai_agent(payload):
  try:
    response = requests.post(OLLAMA_URL, json=payload)
    return response.json().get("response")
  except:
    raise Exception("Something went wrong")


