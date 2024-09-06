

# Run the processing service locally

## Python setup
```
python3.12 -m venv .env
source .env/bin/activate
poetry install
```

## Run the service
```
uvicorn app.main:app --host 0.0.0.0 --port 8080 --workers 1
```
## Test the service
```
curl localhost:8080/v0/status # To get the service status
curl -F 'file=@/home/test.png' localhost:8080/v0/imgsrv # To Upload an image
curl localhost:8080/v0/imgsrv/{id} # To get the image
```
# Docker 

## Build the image
```
docker build -f dockerfiles/Dockerfile -t processing:0.1.0 .
```
## Run the image
```
docker run -p 8080:8080 processing:0.1.0
```

# Helm Chart [README](chart/README.md)
