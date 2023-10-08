from fastapi import Request

from app.config.config import BANNER, AZURE_VISION_ENV, Config

# from app.core.redis.redis import get_redis
from app.initialize import init_logging, azureVision
from app.routers.health import (
    health,
)

from app.routers.ocr import (
    ocr,
)

from app.routers.receipt import (
    receipt,
)


logger = init_logging()

logger.bind(name=None).opt(ansi=True).success(f"AzureVision is running at <red>{AZURE_VISION_ENV}</red>")
logger.bind(name=None).success(BANNER)


async def request_info(request: Request):
    logger.bind(name=None).debug(f"{request.method} {request.url}")
    try:
        body = await request.json()
        logger.bind(payload=body, name=None).debug("request_json: ")
    except ImportError:
        try:
            body = await request.body()
            if len(body) != 0:
                logger.bind(payload=body, name=None).debug(body)
        except ImportError:
            pass


# [ROUTER]
azureVision.include_router(health.router)
azureVision.include_router(ocr.router)
azureVision.include_router(receipt.router)


@azureVision.get("/", tags=["root"])
def root():
    return {"server": Config.API_TITLE}


# @azureVision.on_event("startup")
# async def startup_event():
#     if not await get_redis().ping():
#         raise Exception("Connection to redis failed")


# @azureVision.on_event("shutdown")
# async def shutdown_event():
#     await get_redis().close()


@azureVision.on_event("startup")
async def init_database():
    try:
        logger.bind(name=None).success("Database and tables created success: ✅")
    except Exception as e:
        logger.bind(name=None).error(f"Database and tables  created failed: ❌\nError: {e}")
        raise
