# from fastapi import FastAPI
# from kedro2package.__main__ import main
# from typing import Dict

from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
from typing import Dict

# from kedro2package.__main__ import main
# from run_kedro_pipeline import run_kedro


import os
import sys
import pandas as pd
from kedro.framework.project import configure_project
from kedro.framework.session import KedroSession
from kedro2package.hooks import RUNTIME_DATASETS_CTX

extra_path = os.path.abspath(os.path.dirname(__file__))
sys.path.append(extra_path)
from models.model import PipelineRequest
from helper import is_list_of_dicts


app = FastAPI(title="Kedro application packaged as a python dependency")

PROJECT_PACKAGE_NAME = "kedro2package"
configure_project(PROJECT_PACKAGE_NAME)


@app.get("/")
async def get_status():
    return {"status": "running"}


@app.post("/run-kedro-pipeline", response_model=None)
async def run_kedro_pipeline(
    request: PipelineRequest,
    use_runtime_input: bool = Query(
        False, description="Use in-memory DataFrame instead of on-disk dataset"
    ),
) -> Dict[str, pd.DataFrame]:

    if use_runtime_input and len(request.runtime_catalog_dict) > 0:
        for dataset_name, dataset in request.runtime_catalog_dict.items():
            if is_list_of_dicts(dataset):
                RUNTIME_DATASETS_CTX.set({dataset_name: pd.DataFrame(dataset)})
            else:
                RUNTIME_DATASETS_CTX.set({dataset_name: pd.DataFrame(dataset)})

    with KedroSession.create(env=os.getenv("KEDRO_ENV", "base")) as session:

        pipeline_outputs_dict = session.run(**request.run_params_dict)

        pipeline_name = request.run_params_dict["pipeline_name"]
        output_env_var = f"KEDRO_PIPELINE_{pipeline_name.upper()}_OUTPUT"
        output_env_var_value = os.getenv(
            output_env_var,
            None,
        )

        return_dict = {}
        if (
            output_env_var_value is not None
            and output_env_var_value in pipeline_outputs_dict
        ):
            return_obj = pipeline_outputs_dict[output_env_var_value].load()
            if isinstance(return_obj, pd.DataFrame):
                return_obj = return_obj.to_dict("records")
                return_dict["output"] = JSONResponse(content=return_obj)
            else:
                return_dict["output"] = str(return_obj)

            return_dict["output_name"] = output_env_var_value
            return_dict["status"] = "success"
        else:
            return_dict["status"] = "fail"
            return_dict["reason"] = f"{output_env_var} not present in env file"

    return_dict["pipeline_name"] = pipeline_name

    return return_dict
