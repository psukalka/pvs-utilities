# Update system packages
sudo yum update -y

# Install java 8 or higher
sudo yum install java-11-amazon-corretto -y

# Verify java version
java -version

# Create a new repository file
sudo bash -c 'cat << EOF > /etc/yum.repos.d/cassandra.repo
[cassandra]
name=Apache Cassandra
baseurl=https://redhat.cassandra.apache.org/41x/
gpgcheck=1
repo_gpgcheck=1
gpgkey=https://downloads.apache.org/cassandra/KEYS
EOF'

sudo yum install cassandra -y

sudo systemctl enable cassandra
sudo systemctl start cassandra

sudo systemctl status cassandra
nodetool status

# sudo vim /etc/cassandra/conf/cassandra.yaml
# Make sure these settings are correct:

# listen_address: Should be set to your EC2 instance's private IP
# rpc_address: Set to 0.0.0.0
# broadcast_rpc_address: Should be set to your EC2 instance's private IP
# seeds: Should include your instance's private IP
# Make sure endpoint_snitch is set to SimpleSnitch for a single-node setup