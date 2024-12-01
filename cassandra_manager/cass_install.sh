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
baseurl=https://downloads.apache.org/cassandra/redhat/41x/
gpgcheck=1
repo_gpgcheck=1
gpgkey=https://downloads.apache.org/cassandra/KEYS
EOF'

sudo yum install cassandra -y

sudo systemctl start cassandra
sudo systemctl enable cassandra

sudo systemctl status cassandra
nodetool status

