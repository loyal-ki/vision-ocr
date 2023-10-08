from fastapi import APIRouter, File, UploadFile, status
from app.core.azure.azure_receipt import analyze_receipt
from app.core.schema.base_response import BaseResponse
from app.core.schema.error_schema import Error, ErrorCode
from app.helpers.file import handle_upload_file, remove_file_tmp

from app.utils.logger import Log

log = Log("Receipt Route")

router = APIRouter(prefix="/receipt", tags=["receipt"])


@router.post(
    "/upload",
    summary="OCR Upload Testing",
    status_code=status.HTTP_200_OK,
)
async def upload_file(
    file: UploadFile = File(...),
):
    try:
        file_location = handle_upload_file(file)
        result = analyze_receipt(file_location)
        remove_file_tmp(file_location)
        return BaseResponse.success(data=result)

    except Exception:
        return BaseResponse.failed(Error(ErrorCode.INTERNAL_SERVER_ERROR))
