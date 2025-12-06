import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("BROWSERLESS_API_KEY")
print(f"API Key found: {api_key[:5]}...{api_key[-5:] if api_key else 'None'}")

url = f"https://chrome.browserless.io/content?token={api_key}"
payload = json.dumps({"url": "http://example.com"})
headers = {'cache-control': 'no-cache', 'content-type': 'application/json'}

try:
    response = requests.request("POST", url, headers=headers, data=payload)
    print(f"Status Code: {response.status_code}")
    # print(f"Response: {response.text}") # Don't print full content if it works
except Exception as e:
    print(f"Error: {e}")
