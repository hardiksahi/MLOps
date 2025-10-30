Kedro application as a Docker container:
1. We need to use package: kedro-docker
2. Follow steps in https://github.com/kedro-org/kedro-plugins/tree/main/kedro-docker OR https://www.youtube.com/watch?v=lA-Ivuxmakw.
3. Steps:
- Create kedro application e.g. Follow https://docs.kedro.org/en/1.0.0/tutorials/tutorial_template/#create-a-new-project to setup spaceflights project.
- Install kedro-docker python package.
- Initiate project as a docker project: kedro docker init (from project's root directory). This step automatically generates Dockerfile, .dockerignore
- Build docker image using Dockerfile: kedro docker build --image=kedro_pipeline_docker:v1.0 --base-image=python:3.11-slim --docker-args="--no-cache"
- Run kedro in docker container: kedro docker run --image kedro_pipeline_docker:v1.0 --pipeline=data_processing. If --pipeline is not mentioned, all pipelines are run.
- Run custom commands in docker container: 
-- kedro docker cmd  --image kedro_pipeline_docker:v1.0 kedro run
-- Run in interactive way: kedro docker cmd --image kedro_pipeline_docker:v1.0 --docker-args="-it --env KEDRO_DISABLE_TELEMETRY=True" /bin/bash