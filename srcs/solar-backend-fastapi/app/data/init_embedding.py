import time

import pandas as pd
import requests


def send_request(message, id):
    payload = {
        "messages": [message],
        "model": "solar-embedding-1-large-passage",
        "id": id
    }
    headers = {
        "Content-Type": "application/json"
    }
    response = requests.post("http://localhost/api/v1/embeddings/passage?client_name=solar", json=payload,
                             headers=headers)
    if response.status_code == 200:
        print(f"Request successful for ID: {id}")
    else:
        print(f"Request failed for ID: {id} with status code: {response.status_code}")


def init_embedding():
    df = pd.read_csv('locations.csv')
    # print(df.head(5))

    for i in range(len(df)):
        message = df.iloc[i]["location_description"]
        id = df.iloc[i]["region_name"] + "_" + df.iloc[i]["category_name"] + "_" + str(df.iloc[i]["location_name"])
        send_request(message, id)
        time.sleep(1)

# init_embedding()
