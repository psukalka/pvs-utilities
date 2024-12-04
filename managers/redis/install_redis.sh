# Get latest stack server
docker pull redis/redis-stack-server:latest
# Run the docker on port 6379
docker run -d --name redis-stack-server -p 6379:6379 redis/redis-stack-server:latest