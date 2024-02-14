# build image 

```bash
docker build -t gender-recognizer:[cpu|gpu] -f Dockerfile.[cpu|gpu] .
```

# run container 
```bash
# cpu
docker run --rm --name gender -it -p 8000:8000 gender:cpu deploy-server --host '0.0.0.0' --port 8000 --model_name weights/detector.pt --mounting_path '/'
#gpu 
docker run --rm --name gender -it -p 8000:8000 --gpus all gender:gpu deploy-server --host '0.0.0.0' --port 8000 --model_name weights/detector.pt --mounting_path '/'
```
