from fastapi import APIRouter, status
from app.core.schema.base_response import BaseResponse

from app.utils.logger import Log

log = Log("Health Route")

router = APIRouter(prefix="/health", tags=["health"])


@router.get(
    "/",
    summary="Health check",
    status_code=status.HTTP_200_OK,
)
async def health_check():
    return BaseResponse.success()
