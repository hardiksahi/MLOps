from pydantic import BaseModel


class Request(BaseModel):
    pipeline_name: str
    environment: str


class PipelineRequest(BaseModel):
    # run_params_dict: dict = {"pipeline_name": "__default__"}
    runtime_catalog_dict: dict = {}


# class Response(BaseModel):
#     df: pd.DataFrame
