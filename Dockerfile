FROM thenecromancerx/docker-python-serverless:python3.7-nodejs14-slim

WORKDIR /usr/src/app

COPY requirements.txt requirements.txt

COPY package.json package.json

RUN pip install -r requirements.txt

RUN npm install

COPY . .

RUN apt-get update && yes | apt-get install libgl1



