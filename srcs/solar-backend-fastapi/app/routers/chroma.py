import traceback

from fastapi import HTTPException, APIRouter

from app.core.db import get_chrome_client
from app.core.logger import logger
from app.models.schemas import ErrorResponse, BaseResponse

router = APIRouter()


@router.get("/db/collections", response_model=BaseResponse, responses={400: {"model": ErrorResponse}})
async def list_collections():
    async with get_chrome_client() as client:
        try:
            collections = await client.list_collections()
            logger.info({"collections": collections})
            collections_serializable = [
                {
                    "id": collection.id,
                    "name": collection.name,
                }
                for collection in collections
            ]
            return BaseResponse(message="OK", statusCode="200", data={"collections": collections_serializable})
        except Exception as e:
            logger.error(f"## Error occurred. error: {traceback.format_exc()}")
            raise HTTPException(status_code=500, detail=str(e))
