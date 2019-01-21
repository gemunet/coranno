docker build -t coranno .
docker run -it --rm -v "$(pwd)"/data:/app/data -p8000:8000 coranno
