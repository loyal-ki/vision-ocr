import requests
from app.config.config import Config
from app.core.enums.content_type_enum import ContentType

from app.utils.logger import Log


AZURE_VISION_PARAMS: dict = {
    "features": "read",
    "language": "ja",
}

log = Log("OCR Route")


def extract_text_from_images(data, content_type: str):
    # Prepare the headers
    headers = {
        # Request headers
        "Content-Type": content_type,
        "Ocp-Apim-Subscription-Key": Config.AZURE_VISION_KEY,
    }

    azure_url = Config.AZURE_VISION_ENDPOINT + Config.AZURE_VISION_API_ENDPOINT

    # Send the REST request
    response = requests.post(
        azure_url,
        headers=headers,
        params=AZURE_VISION_PARAMS,
        json=data if content_type == ContentType.JSON else None,
        data=data if content_type == ContentType.OCTET_STREAM else None,
    )

    # Handle the response
    if response.status_code == 200:
        return response.json()
    else:
        return ("Error:", response.status_code, response.text)
