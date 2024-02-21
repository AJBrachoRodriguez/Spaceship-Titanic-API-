# Step 1: Use the official lightweight Python image as base OS
FROM tiangolo/uvicorn-gunicorn:python3.8-slim

# Step 2: Copy local code to the container image
WORKDIR /app
COPY . .

# Step 3: Install production dependencies
RUN pip install -r requirements.txt

# Step 4: Start the web service on container startup using gunicorn webserver
ENV PORT=8080
CMD gunicorn main:app --bind 0.0.0.0:$PORT --worker-class uvicorn.workers.UvicornWorker

## commands 1: docker build -t projectapi .run
## command 2: docker run -p 8080:8080 projectapi
## i need to change "0.0.0.0" to "192.168.1.8"