## app-service build image and deploy container locally

1. Build docker image
```
docker build -t app-service:latest .
```


2. Run local container
```
docker run -d -p 80:80 app-service:latest 
```