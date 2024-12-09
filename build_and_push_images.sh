#!/bin/bash

TAG=$1

docker build -t vovan4/backend:$TAG backend
docker build -t vovan4/auth-backend:$TAG auth_backend
docker build -t vovan4/deploy-backend:$TAG deploy_backend
docker build -t vovan4/frontend:$TAG frontend

docker push vovan4/backend:$TAG
docker push vovan4/auth-backend:$TAG
docker push vovan4/deploy-backend:$TAG
docker push vovan4/frontend:$TAG
