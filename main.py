from typing import Union

from fastapi import FastAPI

from database import models
from database.database import engine, SessionLocal

models.Base.metadata.create_all(bind=engine)
app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


@app.get("/api/get_demo_problem")
def get_demo_problem():
    pass


@app.post("/api/construct_problem")
def construct_problem(graph):
    return graph
