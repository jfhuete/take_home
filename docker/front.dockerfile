FROM node:14-buster

WORKDIR /app

COPY ./front/package*.json ./

RUN npm install --production
COPY ./front .
