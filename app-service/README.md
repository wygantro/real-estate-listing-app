# app-service container build, push and run locally


### app-service

1. Build docker file
```
docker build -t app-service:latest -f Dockerfile .
```


2. Mount docker managed dataframe_volume and run
```
docker run -d -p 5000:5000 app-service:latest
```


## Frontend Service Google Cloud Kubernetes Deployment

1. Initialize Google Cloud
```bash
gcloud init
```


2. Build and push images to Google Cloud Container Registry
```bash
./frontend-service-gcke.sh
```


3. View logs
```bash
kubectl get pods --all-namespaces
kubectl logs POD_NAME

# reset pod
kubectl delete pod my-pod
```