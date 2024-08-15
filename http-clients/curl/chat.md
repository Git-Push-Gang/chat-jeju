## local

```
curl -X POST --location "http://localhost/api/v1/chat?client_name=solar" \
    -H "accept: application/json" \
    -H "Content-Type: application/json" \
    -d '{
          "messages": [
            "제주도 음식 추천해줘"
          ],
          "model": "solar-1-mini-chat",
          "stream": true,
          "rag": true,
          "collection": "embeddings"
        }'
```

## prod

```
curl -X POST --location "http://chat-jeju.duckdns.org/api/v1/chat?client_name=solar" \
    -H "accept: application/json" \
    -H "Content-Type: application/json" \
    -d '{
          "messages": [
            "제주도 음식 추천해줘"
          ],
          "model": "solar-1-mini-chat",
          "stream": true,
          "rag": true,
          "collection": "embeddings"
        }'
```