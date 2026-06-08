from fastapi import FastAPI

from autodoc.api.webhook_router import router

app = FastAPI()

app.include_router(router)
