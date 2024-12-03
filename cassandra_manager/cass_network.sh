# Run these commands after the cluster is up
docker exec -it cn1 nodetool status

# Get CQL access
docker exec -it cn1 cqlsh

# Creating database
CREATE KEYSPACE my_app 
WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 2};

# Use key space
USE my_app;

# Create table
CREATE TABLE users (
    user_id UUID PRIMARY KEY,
    username text,
    email text,
    age int,
    created_at timestamp
);