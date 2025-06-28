from fastapi import FastAPI
from routes import base_router, router, image_router

app = FastAPI()
app.include_router(base_router)
app.include_router(router)
app.include_router(image_router)
