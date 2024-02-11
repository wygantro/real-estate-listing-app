## backend-service build image and deploy container locally

1. Build docker image
```
docker build -t backend-service:latest .
```


2. Run local container
```
docker run -d -p 4000:4000 backend-service:latest 
```