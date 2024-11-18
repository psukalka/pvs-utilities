# Getting latest postgres image
docker pull postgres:latest

# Running postgres container    
docker run -d --name pg_test -e POSTGRES_PASSWORD=pvs123 -p 5432:5432 postgres:latest

# Second docker
docker run -d --name pg_backup -e POSTGRES_PASSWORD=pvs123 -p 5433:5433 postgres:latest