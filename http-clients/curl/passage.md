## local

```
curl -X POST --location "http://localhost/api/v1/embeddings/passage?client_name=solar" \
    -H "accept: application/json" \
    -H "Content-Type: application/json" \
    -d '{
          "messages": [
            "제주도는 흑돼지, 갈치조림, 전복죽이 유명하고 정말 맛있어"
          ],
          "model": "solar-embedding-1-large-passage",
          "id": "test"
        }'
```

## prod

```
curl -X POST --location "http://chat-jeju.duckdns.org/api/v1/embeddings/passage?client_name=solar" \
    -H "accept: application/json" \
    -H "Content-Type: application/json" \
    -d '{
          "messages": [
            "제주도는 흑돼지, 갈치조림, 전복죽이 유명하고 정말 맛있어"
          ],
          "model": "solar-embedding-1-large-passage",
          "id": "test"
        }'
```