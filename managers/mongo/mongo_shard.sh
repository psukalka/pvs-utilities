# Connect to the container
docker exec -it s1n1 mongosh --port 27018

rs.initiate({
  _id: "rs0",
  members: [
    {_id: 0, host: "s1n1:27018"},
    {_id: 1, host: "s1n2:27018"},
    {_id: 2, host: "s1n3:27018"}
  ]
})

# Check replica set status
rs.status()

########

docker exec -it s2n1 mongosh --port 27018

rs.initiate({
  _id: "rs1",
  members: [
    {_id: 0, host: "s2n1:27018"},
    {_id: 1, host: "s2n2:27018"},
    {_id: 2, host: "s2n3:27018"}
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

sh.addShard("rs0/s1n1:27018,s1n2:27018,s1n3:27018")
sh.addShard("rs1/s2n1:27018,s2n2:27018,s2n3:27018")

sh.enableSharding("test")

use test

db.createCollection("users")
db.users.createIndex({ "user_id": "hashed" })
sh.shardCollection("test.users", { "user_id": "hashed" })


db.users.insertOne({
    user_id: 1,
    name: "Pavan Sukalkar",
    email: "pvsukalkar@gmail.com"
})

db.users.insertMany([
    {
        user_id: 2,
        name: "Sonali Ghogare",
        email: "sona@gmail.com"
    },
    {
        user_id: 3,
        name: "Shivam Sukalkar",
        email: "shivam@gmail.com"
    }
])

db.users.insertMany([
    {
        user_id: 4,
        name: "John Doe",
        email: "john@example.com"
    },
    {
        user_id: 5,
        name: "Jane Doe",
        email: "jane@example.com"
    },
    {
        user_id: 6,
        name: "Bob Smith",
        email: "bob@example.com"
    }
])

db.users.getShardDistribution()