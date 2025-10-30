from fastapi import FastAPI, Query
import requests
import os
import sys

extra_path = os.path.abspath(os.path.dirname(__file__))
sys.path.append(extra_path)
from models.model import PipelineRequest

app = FastAPI()


@app.get("/")
async def get_status():
    return {"status": "running"}


@app.post("/process-data", response_model=None)
async def process_data(
    request: PipelineRequest,
    use_runtime_input: bool = Query(
        False, description="Use in-memory DataFrame instead of on-disk dataset"
    ),
):
    headers = {"Content-Type": "application/json", "accept": "application/json"}
    data = {
        "run_params_dict": {
            "pipeline_name": os.getenv(
                "KEDRO_PIPELINE_DATA_PROCESSING", "data_processing"
            )
        },
        "runtime_catalog_dict": request.runtime_catalog_dict,
    }
    # data = {"runtime_catalog_dict": request.runtime_catalog_dict}
    params = {"use_runtime_input": use_runtime_input}
    response = requests.post(
        url=os.getenv("KEDRO_BACKEND_URL"), params=params, headers=headers, json=data
    )

    if response.status_code == 200:
        return response.json()
    else:
        return {"status": "fail", "reason": "POST hit not successful"}
