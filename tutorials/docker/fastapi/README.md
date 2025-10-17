Each docker application has to be self contained.
This means code + dependencies etc should be copied to docker container and executed as per Dockerfile

<b>Commands to run FastAPI application in a Docker on local machine</b>
1. cd into docker/fastapi
2. Create a Docker Image using: docker build -t fastapi-app:1.1 . (. at the end is the location of Dockerfile).
3. Create an instance of Docker Image called Docker container using: docker run -d -p 8080:9000 fastapi-app:1.1 (9000 is port on docker container, 8080 is port on local)
