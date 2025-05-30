<b> Tutorials to learn FastAPI </b>
1. https://www.youtube.com/watch?v=cbASjoZZGIw
2. https://www.youtube.com/watch?v=iWS9ogMPOI0
3. Official tutorial: https://fastapi.tiangolo.com/tutorial/

<b>Deploy FastAPI application to AWS</b>
* This uses free tier AWS services as provided at https://aws.amazon.com/free/?all-free-tier.sort-by=item.additionalFields.SortRank&all-free-tier.sort-order=asc&awsf.Free%20Tier%20Types=*all&awsf.Free%20Tier%20Categories=*all

1. Deploy on AWS EC2 instance: https://www.youtube.com/watch?v=SgSnz7kW-Ko
2. Deploy on AWS Lambda: https://www.youtube.com/watch?v=RGIM4JfsSk0

<b>Commands to run FastAPI application on local machine</b>
1. Install uv package manager (https://docs.astral.sh/uv/getting-started/installation/).
2. Get clone of this repo. cd into the repo.
3. Create virtual env using uv: uv venv mlops_env (https://docs.astral.sh/uv/pip/environments/)
4. Activate mlops_env: source mlops_env/bin/activate.
5. Ensure pyproject.ml has fastapi[standard] installed. If not, execute uv add fastapi --extra standard (https://docs.astral.sh/uv/guides/integration/fastapi/#migrating-an-existing-fastapi-project).
5. Install packages mentioned in pyproject.ml: uv pip install -r pyproject.toml (https://docs.astral.sh/uv/pip/packages/#installing-packages-from-files)
6. cd into tutorials/fastapi/ec2 and run app on uvicorn server: fastapi dev main.py (Works only when you have installed fastapi[standard])

<b>Commands to run FastAPI application on EC2 machine</b>
1. Create an EC2 machine. Please follow steps in Deploy on AWS EC2 instance (https://www.youtube.com/watch?v=SgSnz7kW-Ko) to know the details.
2. Update nginx mapping file to reflect the correct ip address of EC2 virtual machine: sudo vim /etc/nginx/sites-enabled/
3. Restart nginx server: sudo service nginx restart

<b>Commands to run FastAPI application on AWS lambda as a zip archive</b>

We need to zip all the required python files and their dependencies in a zip folder and upload it to AWS Lambda.
Every time a hit is made to the Lambda URL, a server is spinned up, zip is copied and code is executed.
After successful/ failed execution, server shuts down, deleting all the context with it.
We primarily follow steps mentioned in Deploy on AWS Lambda: https://www.youtube.com/watch?v=RGIM4JfsSk0. However, some commands should be modified/ added owing to the usage of uv as package manager.
1. Export dependencies mentioned in `pyproject.ml` into `requirements.txt`: `uv export --frozen --no-dev --no-editable -o requirements.txt` (https://docs.astral.sh/uv/guides/integration/aws-lambda/#deploying-a-zip-archive). This command is executed at the location where `pyproject.ml` is present.
2. Install dependencies into a local directory named `packages` using: uv pip install \
   --no-installer-metadata \
   --no-compile-bytecode \
   --python-platform x86_64-manylinux2014 \
   --python 3.x \
   --target packages \
   -r requirements.txt (https://docs.astral.sh/uv/guides/integration/aws-lambda/#deploying-a-zip-archive)
3. Zip packages folder:
- cd packages
- zip -r ../package.zip .
- cd .. (https://docs.astral.sh/uv/guides/integration/aws-lambda/#deploying-a-zip-archive)
4. Update zip folder by adding relevant fastapi files. These files should be at the root of the zip folder as mentioned in https://docs.aws.amazon.com/lambda/latest/dg/python-package.html#python-package-create-dependencies.
- cd into tutorials/fastapi/aws_lambda
- zip ../../../package.zip -u lambda_handler.py
- zip ../../../package.zip -u models.py
5. Upload zip to AWS lambda function.