from multiprocessing.connection import Listener
from typing import Union

from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from config import sample_file_path, solver_info
from utils import file_utils
from custom_benchmark_problems.diamon_problem.core import algs

app = FastAPI()

origins = ["http://localhost", "http://localhost:8080", "http://192.168.16.169:8080"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# address = ("localhost", 6000)  # family is deduced to be 'AF_INET'
# listener = Listener(address, authkey=b"secret password")
# conn = listener.accept()


@app.get("/")
def read_root():
    return {"Hello": "World"}


# @app.websocket("/api/test_ws")
# async def websocket_endpoint(websocket: WebSocket):
#     await websocket.accept()
#     cmd = await websocket.receive_text()
#     if cmd == "run_program":
#         pass
#     else:
#         counter = 0
#         while True:
#             msg = conn.recv()
#             await websocket.send_text(f"Counting: {msg}")
#             counter += 1
#             if counter >= 1000:
#                 await websocket.close()


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


@app.get("/api/density_filter")
def density_filter(start_step:int,end_step:int):
    pass


@app.get("/api/demo_data")
def demo_data():
    demo_log = file_utils.load_evaluation_log(
        "test_runx_2023-01-16T10-30-27.298413.csv"
    )
    demo_tree = file_utils.read_json_tree("sample.json")
    sequence_dict = {}
    for node in demo_tree["nodes"]:
        sequence_dict[node["id"]] = node
        sequence_dict[node["id"]]["label"] = (
            f"Node ID: {node['id']}, Minimal: {node['minima']}, "
            f"Symbol: {node['symbol']}"
        )
    link_map = {}
    for link in algs.compute_links(demo_tree):
        source_id = link["source"]
        if source_id in link_map.keys():
            link_map[source_id].append(link["target"])
        else:
            link_map[source_id] = [link["target"]]
    all_ids = list(sequence_dict.keys())
    all_ids.append(0)
    response = {
        "all_ids": all_ids,
        "tree": [
            {
                "id": 0,
                "label": "Root,  ID:0, minima: 0",
                "children": construct_tree_structure(
                    0, link_map, sequence_dict=sequence_dict
                ),
            }
        ],
        "solver_log": demo_log,
    }

    return JSONResponse(content=jsonable_encoder(response))


def construct_tree_structure(current_key, links_map: dict, sequence_dict: dict):
    result = []
    for sub_key in links_map[current_key]:
        if sub_key in links_map.keys():
            sequence_dict[sub_key]["children"] = construct_tree_structure(
                sub_key, links_map, sequence_dict
            )
            result.append(sequence_dict[sub_key])
        else:
            result.append(sequence_dict[sub_key])
    return result
