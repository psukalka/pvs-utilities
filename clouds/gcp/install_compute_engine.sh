# Disable Ops agent while creating instance
# Install docker
sudo apt update
sudo apt install -y apt-transport-https ca-certificates curl gnupg lsb-release

# Add docker's official GPG key
curl -fsSL https://download.docker.com/linux/debian/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

# Set up stable docker repository
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/debian $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Install docker
sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io
sudo usermod -aG docker $USER


# Install python
sudo apt install -y python3 python3-pip python3-venv

# Install build tools (optional)
sudo apt install -y build-essential libssl-dev libffi-dev python3-dev

# Create venv
python3 -m venv db-test-env
source db-test-env/bin/activate


# Clone project
git clone https://github.com/psukalka/pvs-utilities.git
cd pvs-utilities
pip install -r requirements.txt