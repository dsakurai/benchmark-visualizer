from typing import Union

from fastapi import FastAPI

from utils import file_utils
from config import sample_file_path

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


@app.get("/api/get_demo_problem")
def get_demo_problem():
    json_tree = file_utils.read_json_tree(sample_file_path)
    return json_tree


@app.post("/api/construct_problem")
def construct_problem(graph:dict):
    return graph
