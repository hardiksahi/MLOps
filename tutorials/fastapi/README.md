<b> Tutorials to learn FastAPI </b>
1. https://www.youtube.com/watch?v=cbASjoZZGIw
2. https://www.youtube.com/watch?v=iWS9ogMPOI0
3. Official tutorial: https://fastapi.tiangolo.com/tutorial/

<b>Deploy FastAPI application to AWS</b>
* This uses free tier AWS services as provided at https://aws.amazon.com/free/?all-free-tier.sort-by=item.additionalFields.SortRank&all-free-tier.sort-order=asc&awsf.Free%20Tier%20Types=*all&awsf.Free%20Tier%20Categories=*all

1. Deploy on AWS EC2 instance: https://www.youtube.com/watch?v=SgSnz7kW-Ko
2. Deploy on AWS Lambda: https://www.youtube.com/watch?v=RGIM4JfsSk0

<b>Commands to run FastAPI application</b>
1. Install uv package manager (https://docs.astral.sh/uv/getting-started/installation/).
2. Get clone of this repo. cd into the repo.
3. Create virtual env using uv: uv venv mlops_env (https://docs.astral.sh/uv/pip/environments/)
4. Activate mlops_env: source mlops_env/bin/activate.
5. Ensure pyproject.ml has fastapi[standard] installed. If not, execute uv add fastapi --extra standard (https://docs.astral.sh/uv/guides/integration/fastapi/#migrating-an-existing-fastapi-project).
5. Install packages mentioned in pyproject.ml: uv pip install -r pyproject.toml (https://docs.astral.sh/uv/pip/packages/#installing-packages-from-files)
6. cd into tutorials/fastapi and run app on uvicorn server: fastapi dev main.py (Works only when you have installed fastapi[standard])