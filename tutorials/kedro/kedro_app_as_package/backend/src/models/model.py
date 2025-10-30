from pydantic import BaseModel


class Request(BaseModel):
    pipeline_name: str
    environment: str


class PipelineRequest(BaseModel):
    params: dict = {"pipeline_name": "__default__"}


# class Response(BaseModel):
#     df: pd.DataFrame
