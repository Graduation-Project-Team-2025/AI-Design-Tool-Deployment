from fastapi import FastAPI
from routes import base, data

app = FastAPI()
app.include_router(base.base_router)
app.include_router(data.data_router)

from fastapi import FastAPI
from routes import base_router, diy_router, image_router
