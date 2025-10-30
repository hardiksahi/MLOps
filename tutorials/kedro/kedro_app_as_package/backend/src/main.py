# from fastapi import FastAPI
# from kedro2package.__main__ import main
# from typing import Dict

from fastapi import FastAPI
from typing import Dict

# from kedro2package.__main__ import main
# from run_kedro_pipeline import run_kedro


import os
import sys
import pandas as pd

extra_path = os.path.abspath(os.path.dirname(__file__))
sys.path.append(extra_path)
from models.model import PipelineRequest

from kedro.framework.project import configure_project
from kedro.framework.session import KedroSession

app = FastAPI(title="Kedro application packaged as a python dependency")

PROJECT_PACKAGE_NAME = "kedro2package"
configure_project(PROJECT_PACKAGE_NAME)


@app.get("/")
async def get_status():
    return {"status": "running"}


@app.post("/run-kedro-pipeline", response_model=None)
async def run_kedro_pipeline(
    request: PipelineRequest,
) -> Dict[str, pd.DataFrame]:
    # result_dict = main(["--pipeline", pipeline_name, "--env", environment])
    # result_dict = run_kedro(pipeline_name=request.pipeline_name, env=environment)

    # return_df = result_dict["model_input_table"].load()
    # return {"df": return_df.shape}

    with KedroSession.create(env=os.getenv("KEDRO_ENV", "base")) as session:
        outputs = session.run(**request.params)

    return {"status": "success", "outputs": list(outputs.keys())}
