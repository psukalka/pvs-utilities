# Connect to the container
docker exec -it s1n1 mongosh -u admin -p pvs123

# Inside mongosh, initialize the replica set
rs.initiate({
  _id: "rs0",
  members: [
    {_id: 0, host: "s1n1:27017"},
    {_id: 1, host: "s1n2:27017"},
    {_id: 2, host: "s1n3:27017"}
  ]
})

# Check replica set status
rs.status()

########

docker exec -it s2n1 mongosh -u admin -p pvs123

# Inside mongosh of s2n1
rs.initiate({
    _id: "rs1",
    members: [
        {_id: 0, host: "s2n1:27017"},
        {_id: 1, host: "s2n2:27017"},
        {_id: 2, host: "s2n3:27017"}
    ]
})

rs.status()

#######
docker exec -it cs1 mongosh

rs.initiate({
    _id: "config_rs",
    configsvr: true,
    members: [
        {_id: 0, host: "cs1:27017"},
        {_id: 1, host: "cs2:27017"},
        {_id: 2, host: "cs3:27017"}
    ]
})

#######
docker exec -it mongo_router mongosh

sh.addShard("rs0/s1n1:27017,s1n2:27017,s1n3:27017")
sh.addShard("rs1/s2n1:27017,s2n2:27017,s2n3:27017")

