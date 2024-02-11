## frontend-service Google Kubernetes Deployment

1. Initialize Google Cloud
```bash
gcloud init
# set project to relist
```


2. Build and push images to Google Cloud Container Registry
```bash
./frontend-service-deploy.sh
```


3. View logs
```bash
kubectl get pods --all-namespaces
kubectl logs POD_NAME

# reset pod
kubectl delete pod my-pod
```