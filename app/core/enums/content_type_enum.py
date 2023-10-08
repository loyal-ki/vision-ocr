from enum import Enum


class ContentType(str, Enum):
    JSON = "application/json"
    OCTET_STREAM = "application/octet-stream"
