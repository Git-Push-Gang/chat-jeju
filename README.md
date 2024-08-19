# Chat JEJU

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

## Flow Chart

![Flowchart.png](Flowchart.png)

## Getting Started

To check out the project:

```
git clone https://github.com/Git-Push-Gang/proxy.git
cd proxy
```

> [!NOTE]
> Before running the docker services, comment out `driver_opts` in `docker-compose.yml`

To run the docker services:

```
make
```


## Usage

- To call `Chat JEJU` API

```
curl -X POST --location "http://localhost/api/v1/chat/kakao?client_name=solar" \
    -H "accept: application/json" \
    -H "Content-Type: application/json" \
    -d '{
          "intent": {
            "id": "es2mb937ado5bmj04dkzmogn",
            "name": "블록 이름"
          },
          "userRequest": {
            "timezone": "Asia/Seoul",
            "params": {
              "ignoreMe": "true"
            },
            "block": {
              "id": "es2mb937ado5bmj04dkzmogn",
              "name": "블록 이름"
            },
            "utterance": "하효일 정보 알려줘",
            "lang": null,
            "user": {
              "id": "945412",
              "type": "accountId",
              "properties": {}
            }
          },
          "bot": {
            "id": "your_bot_id",
            "name": "봇 이름"
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
