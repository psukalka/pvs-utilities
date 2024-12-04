# Getting latest postgres image
docker pull postgres:latest

# Create volume to store data
docker volume create my_db_data

# Running postgres container    
docker run -d --name pg_test -v my_db_data:/var/lib/postgresql/data -e POSTGRES_PASSWORD=pvs123 -p 5432:5432 postgres:latest

# Second docker
docker run -d --name pg_backup -v my_db_data:/var/lib/postgresql/data -e POSTGRES_PASSWORD=pvs123 -p 5433:5433 postgres:latest