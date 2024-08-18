from __future__ import annotations

from typing import List, Optional

from fastapi import Depends

from app.models.schemas import EmbeddingContextList
from app.services import EmbeddingService
from app.services.measure_time import measure_time
from app.services.service_factory import ServiceFactory


@measure_time
def get_to_stay_recommendation(region_name: str,
                               messages: List[str],
                               embedding_service: EmbeddingService = Depends(ServiceFactory.get_embedding_service),
                               ) -> Optional[EmbeddingContextList]:
    collection_name = "embeddings-" + region_name + "_" + "stay"

    return embedding_service.rag(messages=messages, embedding_collection=collection_name)


description = {
    "type": "function",
    "function": {
        "name": "get_to_stay_recommendation",
        "description": "Get a list of to-stay recommendations asked by a user, \
            such as to-stay options nearby or in a specific region",
        "parameters": {
            "type": "object",
            "properties": {
                "region_name": {
                    "type": "string",
                    "description": "Choose region in Jeju Island categorized regarding direction.\
                        Region name e.g. east-kareum, al-kareum",
                },
                "message": {
                    "type": "string",
                    "description": "User inquiry about to-stay options",
                },
            },
            "required": ["region_name", " mesage"],
        },
    },
}
