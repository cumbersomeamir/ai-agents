import requests

def test_export_endpoint(prompt):
    url = "http://127.0.0.1:5000/export"
    params = {'prompt': prompt}
    response = requests.get(url, params=params)

    if response.status_code == 200:
        with open('downloaded_report.docx', 'wb') as f:
            f.write(response.content)
        print("File downloaded successfully. Check downloaded_report.docx.")
    else:
        print("Failed to download file:", response.status_code, response.text)

if __name__ == "__main__":
    prompt = "What are CI/CD tools?"
    test_export_endpoint(prompt)
