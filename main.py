from typing import Union

from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware

from config import sample_file_path, solver_info
from utils import file_utils
from multiprocessing.connection import Listener

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://192.168.16.169:8080"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

address = ('localhost', 6000)     # family is deduced to be 'AF_INET'
listener = Listener(address, authkey=b'secret password')
conn = listener.accept()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.websocket("/api/test_ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    cmd = await websocket.receive_text()
    print(cmd)
    counter = 0
    while True:
        msg = conn.recv()
        await websocket.send_text(f"Counting: {msg}")
        counter += 1


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


@app.get("/api/get_demo_problem")
def get_demo_problem():
    json_tree = file_utils.read_json_tree(sample_file_path)
    return json_tree


@app.get("/api/get_all_solvers")
def get_all_solvers():
    return solver_info


@app.post("/api/construct_problem")
def construct_problem(graph: dict):
    return graph
