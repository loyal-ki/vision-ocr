from pydantic import BaseModel, Field


class OCRRequest(BaseModel):
    url_image: str = Field(title="facebook id", example="https://example.png")

    class Config:
        schema_extra = {
            "description": "Image url",
            "example": {
                "url_image": "https://example.png",
            },
        }

