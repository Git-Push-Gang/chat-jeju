## local

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
            "utterance": "Hi, Please recommend the place to drink near east-kareum",
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
            "params": {},
            "id": "your_action_id",
            "detailParams": {}
          }
        }'
```

## prod

```
curl -X POST --location "http://chat-jeju.duckdns.org/api/v1/chat/kakao?client_name=solar" \
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
            "utterance": "Hi, Please recommend the place to drink near east-kareum",
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
            "params": {},
            "id": "your_action_id",
            "detailParams": {}
          }
        }'
```