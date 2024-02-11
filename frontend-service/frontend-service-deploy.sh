#!/bin/bash

# check if the script has execution permissions
if [[ ! -x $0 ]]; then
    echo "making the script executable"
    chmod +x $0
    exec $0 "$@"
fi

# frontend-service ENV variables
IMAGE_NAME="app-service"
PROJECT_ID="$(gcloud config get-value project)"

# Google Cloud VM ENV variables
GCR_HOSTNAME="gcr.io"
GCR_VM_NAME="relist-vm-instance"
GCR_VM_ZONE="us-central1-a"

# build and push image to Google Cloud
docker build -t "${GCR_HOSTNAME}/${PROJECT_ID}/${IMAGE_NAME}:latest" -f ./app/Dockerfile ./app
gcloud auth configure-docker
docker push "${GCR_HOSTNAME}/${PROJECT_ID}/${IMAGE_NAME}:latest"
echo "app-service images built and pushed successfully"


# configure cluster
gcloud container clusters get-credentials relist-cluster 
#--location us-central1 #-a

# apply frontend-service deployment and service
kubectl apply -f frontend-deployment.yaml
kubectl apply -f frontend-service.yaml

echo "frontend-service deployed to GKE"