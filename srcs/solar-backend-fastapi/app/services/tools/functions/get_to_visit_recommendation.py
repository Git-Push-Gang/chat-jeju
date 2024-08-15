from __future__ import annotations

import traceback
from typing import List, Optional

from fastapi import Depends

from app.core.logger import logger
from app.services import EmbeddingService
from app.services.service_factory import ServiceFactory
from app.models.schemas import EmbeddingContextList

def get_to_visit_recommendation(region_name:str, 
                              messages: List[str],
                              embedding_service: EmbeddingService = Depends(ServiceFactory.get_embedding_service),
                              ) -> Optional[EmbeddingContextList]:
    collection_name = region_name + "_" + "attraction"
    
    return embedding_service.rag(messages=messages, embedding_collection=collection_name)


description = {
    "type": "function",
    "function": {
        "name": "get_to_visit_recommendation",
        "description": "Get a list of to-visit recommendations asked by a user, \
            such as to-visit options nearby or in a specific region",
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
                    "description": "User inquiry about to-visit options",
                },
            },
            "required": ["region_name", " mesage"],
        },
    },
}
