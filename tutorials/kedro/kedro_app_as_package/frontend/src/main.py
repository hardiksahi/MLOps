from fastapi import FastAPI
import requests
import os

app = FastAPI()


@app.get("/")
async def get_status():
    return {"status": "running"}


@app.post("/process-data", response_model=None)
async def process_data():
    # url = "http://localhost:8081/run-kedro-pipeline"
    headers = {"Content-Type": "application/json", "accept": "application/json"}
    data = {
        "params": {
            "pipeline_name": os.getenv(
                "KEDRO_PIPELINE_DATA_PROCESSING", "data_processing"
            )
        }
    }

    response = requests.post(
        url=os.getenv("KEDRO_BACKEND_URL"), headers=headers, json=data
    )

    if response.status_code == 200:
        return response.json()
    else:
        return {"status": "fail"}
