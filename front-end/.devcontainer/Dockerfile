FROM node:24-alpine

WORKDIR /workspace

RUN apk update && \
    apk add --no-cache git make

COPY package*.json ./

RUN corepack enable
