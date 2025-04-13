from fastapi import FastAPI
from app.db import models, database
from app.api.routes import router

app = FastAPI()
models.Base.metadata.create_all(bind=database.engine)

app.include_router(router)
