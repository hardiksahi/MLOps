## Base image
FROM node:latest

## Copy package.json to app folder in container
COPY package.json /app/
## Copy src folder to ap folder in container
COPY src /app/

## Set working dir for following commands
WORKDIR /app

## Install dependencies from package.json
RUN npm install

## Last CMD to start the process itself
CMD ["node", "server.js"]

