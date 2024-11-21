# Connect to the container
docker exec -it mongo-test mongosh -u admin -p pvs123

# Inside mongosh, initialize the replica set
rs.initiate({
  _id: "rs0",
  members: [
    {_id: 0, host: "localhost:27017"}
  ]
})

# Check replica set status
rs.status()