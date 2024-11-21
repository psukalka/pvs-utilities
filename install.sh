# Install docker
sudo yum update -y
sudo yum install -y docker
sudo service docker start
sudo usermod -a -G docker ec2-user

# Install git
sudo yum install git -y

# Install pip
sudo yum install python-pip -y

# Install docker-compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
sudo ln -s /usr/local/bin/docker-compose /usr/bin/docker-compose
docker-compose --version

# Keyfile is needed for using authentication with replicaset
# Generate a keyfile with appropriate permissions
openssl rand -base64 756 > mongo-keyfile
chmod 400 mongo-keyfile
sudo chown 999:999 mongo-keyfile

# Make venv
python3 -m venv db-test-env

# Install packages
git clone https://github.com/psukalka/pvs-utilities.git
cd pvs-utilities
pip install -r requirements.txt