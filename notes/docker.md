# Images

## Getting Image

`docker pull <image_name>`

Ex. docker pull mongo:latest to pull latest image of mongo

- Local Images

`docker images`

- Install Image

`docker run -d <image_name>`

You can optionally name the container as --name <container_name>

You can optionally provide environment variables -e k1=v1

You can optionally provide volumes (i.e. storage from local machine) -v <local_volume>:<container_path>

Ex. `docker run -d --name mongo-test -v mongo-keyfile:/data/mongo-keyfile -e MONGO_INITDB_ROOT_USERNAME=admin MONGO_INITDB_ROOT_PASSWORD=pvs123 mongo:latest`



# Debugging

## Containers

`docker ps` → to list active containers

`docker ps -a` → to list all containers

## SSH

`docker exec -it <container_name> bash`

Ex. `docker exec -it mongo-test bash`

## Logs

`docker logs <container_name>` → if any container is not running check its logs

## Stats

`docker stats` → to check networks, memory usage, cpu usage, …


# Multi Containers

Create a docker-compose.yml file orchestrating your architecture

`docker-compose up -d` → to run default docker-compose.yml file

`docker-compose -f staging.yml up -d` → to run staging services

`docker-compose up -d <service_name>` → to bring up a particular service from yml file

`docker-compose down` → to bring all services down

`docker-compose down -v` → to bring all services down and even delete volumes

`docker-compose down <service_name>` → to bring down a particular service


# Miscellaneous

## Volumes

`docker volume ls`

`docker volume create <volume_name>`

`docker volume rm <volume_name>`

`docker volume inspect <volume_name>`

`docker volume rm <volume_name>`

## Network

`docker network ls`