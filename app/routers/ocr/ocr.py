import cv2
import numpy as np

from fastapi import APIRouter, File, UploadFile, status
from app.core.azure.azure_vision import extract_text_from_images
from app.core.enums.content_type_enum import ContentType
from app.core.schema.base_response import BaseResponse
from app.core.schema.error_schema import Error, ErrorCode
from app.core.schema.ocr.ocr_schema import OCRRequest
from app.helpers.converter import convert_image_to_bytes

from app.utils.logger import Log

log = Log("OCR Route")

router = APIRouter(prefix="/ocr", tags=["ocr"])


@router.post(
    "/",
    summary="OCR Testing",
    status_code=status.HTTP_200_OK,
)
async def extract_text(
    ocr_request: OCRRequest,
):
    image_url = ocr_request.url_image

    log.info(f"ocr_request: {ocr_request}.")

    try:
        result = extract_text_from_images({"url": image_url}, ContentType.JSON)

        return BaseResponse.success(data=result)

    except Exception:
        return BaseResponse.failed(Error(ErrorCode.INTERNAL_SERVER_ERROR))


@router.post(
    "/upload",
    summary="OCR upload Testing",
    status_code=status.HTTP_200_OK,
)
async def upload_file(
    file: UploadFile = File(...),
):
    try:
        img_arr = np.fromstring(await file.read(), np.uint8)
        img = cv2.imdecode(img_arr, -1)
        img_bytes = convert_image_to_bytes(image=img)

        result = extract_text_from_images(img_bytes, ContentType.OCTET_STREAM)

        return BaseResponse.success(data=result)

    except Exception:
        return BaseResponse.failed(Error(ErrorCode.INTERNAL_SERVER_ERROR))
