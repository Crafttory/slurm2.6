import requests
import time
import csv

API_URL = "http://5.159.103.79:4000"
OUTPUT_FILE = "customs_data.csv"
RETRY_AFTER = 180  # 3 minutes

def fetch_data(page):
    response = requests.get(API_URL, params={'page': page})
    if response.status_code == 429:
        time.sleep(RETRY_AFTER)
        response = requests.get(API_URL, params={'page': page})
    response.raise_for_status()
    return response.json()

def save_data_to_csv(data, file_name):
    with open(file_name, 'a', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=data[0].keys(), delimiter='\t')
        if csvfile.tell() == 0:  # write header only if file is empty
            writer.writeheader()
        writer.writerows(data)

def main():
    page = 1
    while True:
        data = fetch_data(page)
        if not data:  # Break if no more data
            break
        save_data_to_csv(data, OUTPUT_FILE)
        page += 1

if __name__ == "__main__":
    main()
