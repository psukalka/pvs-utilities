# Generating random-uuid
docker run --rm confluentinc/cp-kafka:7.5.0 kafka-storage random-uuid

# Creating a topic
docker exec kafka-kraft kafka-topics --create --topic orders --partitions 1 --replication-factor 1 --bootstrap-server localhost:29092

# list topics
docker exec kafka-kraft kafka-topics --list --bootstrap-server localhost:29092