import requests
import os
OLLAMA_URL = os.getenv("OLLAMA_URL")

def request_ai_agent(payload):
  print('===OLLAMA_URL', OLLAMA_URL)
  print('===payload', payload)

  try:
    response = requests.post(OLLAMA_URL, json=payload)
    print("==========response", response.json())
    return response.json().get("response")
  except:
    raise Exception("Something went wrong")


