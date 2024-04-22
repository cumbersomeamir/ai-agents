import requests
import json

# URL of the Flask app's endpoint
url = "http://34.66.196.174:5000/export?prompt=The Impact of Artificial Intelligence"

# Data to send in the request, including a sample text, prompt, and optional filename
data = {
    "text": "This is a summary of the impact of AI. \n\nQuestion: What are the economic impacts of AI?\nAI has various economic implications including increased productivity.\n\nQuestion: How does AI affect employment?\nAI changes job landscapes, creating some jobs while displacing others.",
    "prompt": "The Impact of Artificial Intelligence",
    "filename": "AI_Impact_Report.docx"
}

# Headers to specify that the data is JSON
headers = {
    "Content-Type": "application/json"
}

# Make the POST request
response = requests.post(url, headers=headers, data=json.dumps(data))

# Check if the request was successful
if response.status_code == 200:
    # Save the received file
    with open('downloaded_report.docx', 'wb') as f:
        f.write(response.content)
    print("File successfully downloaded and saved as 'downloaded_report.docx'.")
else:
    print("Failed to generate document. Status code:", response.status_code)

