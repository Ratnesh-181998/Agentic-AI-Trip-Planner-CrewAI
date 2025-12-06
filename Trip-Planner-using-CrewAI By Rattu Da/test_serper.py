import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("SERPER_API_KEY")
print(f"API Key found: {api_key[:5]}...{api_key[-5:] if api_key else 'None'}")

url = "https://google.serper.dev/search"
payload = json.dumps({"q": "test"})
headers = {
  'X-API-KEY': api_key,
  'content-type': 'application/json'
}

try:
    response = requests.request("POST", url, headers=headers, data=payload)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")
except Exception as e:
    print(f"Error: {e}")
