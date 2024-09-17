# Chat JEJU

[English](README.md) | [한국어](README.ko.md)

## Project Overview

- Jeju Island is home to a multitude of charming, yet undiscovered local accommodations and businesses. Our mission is
  to bridge the gap between these hidden gems and curious travelers through innovative technology.

- Our vision extends beyond mere convenience. We see Chat JEJU as a catalyst for economic growth in the region. By
  shining
  a spotlight on lesser-known local businesses, we hope to create new opportunities for local entrepreneurs and
  distribute
  tourism benefits more evenly across the island. This approach not only supports the local economy but also encourages
  sustainable tourism by directing visitors to a diverse range of locations, potentially easing the pressure on overly
  popular spots. By offering support in multiple languages, Chat JEJU also aims to break down language barriers, making
  Jeju more accessible to international visitors and enhancing their overall experience. Available 24/7, it ensures that
  assistance is always at hand, significantly boosting customer satisfaction.

## Demo Video

<img width="300" src="./resources/demo_video.gif" alt="A demo video is loading..">

## Flow Chart

![Flowchart.png](./resources/Flowchart.png)

## Preparation
Issuing a Service Account Key File for using google Docs API

1. Log in to the Google Cloud Console.
2. In the project selection menu, choose "New Project" and create a new project.
3. In the left menu, go to "APIs & Services" > "Library," search for and enable both the Google Docs API and Google Drive API.
4. In the left menu, navigate to "APIs & Services" > "Credentials," click the "Create Credentials" button, and select "Service Account."
5. Click "Create Key" and choose the "JSON" key type. <- This is the service account key.
6. Open the document you want to access via the API in Google Drive, and add the service account email address in the sharing settings.

## Getting Started

To check out the project:

```
git clone https://github.com/Git-Push-Gang/proxy.git
```

> [!IMPORTANT]
> You need to specify Upstage API key. Create `.env` in `/srcs` and specify `API_KEY="up....."`

> [!IMPORTANT]
> Create `.service-account.json` in `/srcs/solar-backend-fastapi/app/data`.
> This is the Google Cloud Service Account JSON file generated in [Preparation](https://github.com/Git-Push-Gang/proxy?tab=readme-ov-file#preparation).

> [!NOTE]
> Before running the docker services, comment out `driver_opts` in `docker-compose.yml`

To run the docker services:

```
make
```


## Usage

To initialize embedding collections, do the following command:
```
python srcs/solar-backend-fastapi/app/data/init_embedding.py
```

To ask a question to the `Chat JEJU` chatbot and get an answer:

- To get up-to-date information about your accommodation, include `{accommodation_name}` in `utterance` field of request
  body.
  - e.g. `'Can you tell me the Wi-Fi information for {Battie}?'`
- To ask what information you want to get from a region, include `{region_name}` in `utterance` field of request
  body.
  - e.g. `'Can you recommend a cozy cafe in {East Kareum}?'`

```
curl -X POST --location "http://localhost/api/v1/chat/kakao?client_name=solar" \
    -H "accept: application/json" \
    -H "Content-Type: application/json" \
    -d '{
          "intent": {
            "id": "es2mb937ado5bmj04dkzmogn",
            "name": "block_name"
          },
          "userRequest": {
            "timezone": "Asia/Seoul",
            "params": {
              "ignoreMe": "true"
            },
            "block": {
              "id": "es2mb937ado5bmj04dkzmogn",
              "name": "block_name"
            },
            "utterance": "Can you tell me the Wi-Fi information for Battie?",
            "lang": null,
            "user": {
              "id": "945412",
              "type": "accountId",
              "properties": {}
            }
          },
          "bot": {
            "id": "your_bot_id",
            "name": "bot_name"
          },
          "action": {
            "name": "your_action_name",
            "clientExtra": null,
            "params": {
            },
            "id": "your_action_id",
            "detailParams": {}
          }
        }'
```

To retrieve embedding collections in chroma db:

```
curl -X GET --location "http://localhost/api/v1/db/collections" \
    -H "Accept: application/json"
```

> [!NOTE]
> If you would like the presentation, please download the zipped PDF file (the video has been removed due to space
> limitations).
> [PDF file](resources/chat_jeju_presentation.compressed.pdf)
