# Install docker
sudo yum update -y
sudo yum install -y docker
sudo service docker start
sudo usermod -a -G docker ec2-user

# Install git
sudo yum install git -y

# Install pip
sudo yum install python-pip -y

# Make venv
python3 -m venv db-test-env

# Install packages
git clone https://github.com/psukalka/pvs-utilities.git
cd pvs-utilities
pip install -r requirements.txt