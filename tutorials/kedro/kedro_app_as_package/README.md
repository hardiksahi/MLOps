# kedro2package
1.  This is an example of kedro application that will be packaged. This is spaceflights example that can be downloaded as a kedro starter package (https://docs.kedro.org/en/1.0.0/tutorials/tutorial_template/)
2. Package kedro project to get .whl file that can be installed as a dependency (https://docs.kedro.org/en/1.0.0/deploy/package_a_project/#package-a-kedro-project)
    1. Run ```kedro package``` command from the project root directory (parent directory, kedro2package)
    2. This creates a dist folder with .whl and tar.gz files.
    3. This distribution is to be copied to and installed in backend service.

# backend
1. This is a service that exposes kedro pipeline run as a FastAPI endpoint. (/run-kedro-pipeline)
2. Copy dist folder generated from kedro2package. This package will be installed as a .whl file using uv add 'whl' file. Check **Dockerfile** to see how it happens.
3. Depending on whether you read datasets from local or not, you may or may not need data folder. In this case, I read starting datasets from data/01_raw. Make sure that needed datasets are present in this folder.
4. Update .env file to use correct ```KEDRO_ENV``` environment variable. Here we are using ```KEDRO_ENV=base```
5. Steps to dockerize backend as a standalone container
    - cd into backend folder
    - Run on CLI ```docker build -t kedro_as_fasapi:v1.0 .```. This builds Docker image using Dockerfile.
    - Run on CLI ```docker run -d -p 8081:8000 --env-file ./env --name kedro_as_fastapi1 --mount type=bind,src=<path-to-data-folder-on-local>,dst=/app/data kedro_as_fasapi:v1.0```
    - backend fastapi application is now accessible at http://localhost:8081

Note: This service will be dockerized using docker-compose (in conjunction with frontend)


# frontend
1. This is just a FasAPI application that is customer facing. It contains an endpoint that hits /run-kedro-pipeline endpoint in backend for a specific pipeline_name
2. Make sure to update .env file with correct pipeline names. For example ```KEDRO_PIPELINE_DATA_PROCESSING```
3. Can be used dockerized in standalone manner but ensure ```KEDRO_BACKEND_URL``` is correctly configured in .env file.

# Dockerize using docker-compose.yml
1. Contains information to dockerize both backend and frontend services.
2. Steps:
    - cd into kedro_app_as_package folder
    - Run on CLI: ```docker compose -f docker-compose.yml up```
    - Both frontend and backend services are nor dockerized
