from app.routers.chat import router as chat_router
from app.routers.chat_kakao import router as chat_kako_router
from app.routers.embedding import router as embedding_router
from app.routers.chroma import router as chroma_router
from fastapi import APIRouter

v1_router = APIRouter(prefix="/api/v1")

v1_router.include_router(chat_router, tags=["chat"])
v1_router.include_router(embedding_router, tags=["embedding"])
v1_router.include_router(chat_kako_router, tags=["chat/kakao"])
v1_router.include_router(chroma_router, tags=["db/collections"])
