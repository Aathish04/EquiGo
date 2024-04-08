import requests
import time
import shutil

def download_file(url, destination):
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(destination, 'wb') as f:
            response.raw.decode_content = True
            shutil.copyfileobj(response.raw, f)
        print("File downloaded successfully.")
    else:
        print("Failed to download file. Status code:", response.status_code)

def main():
    url = "http://192.168.175.1:5000/documents.jsonl"  # Replace with your URL
    destination = "/Users/aathishs/Projects/EquiGo/llm/data/pathway-docs-small/documents.jsonl"  # Replace with your local file name
    while True:
        download_file(url, destination)
        time.sleep(20)

if __name__ == "__main__":
    main()
