# Installing PowerDNS through dnf isn't working. Using docker build for testing
# Install Docker
sudo dnf install -y docker
sudo systemctl enable docker
sudo systemctl start docker

# Run PowerDNS in Docker
sudo docker run -d --name pdns \
  --restart=always \
  -p 53:53/tcp -p 53:53/udp \
  powerdns/pdns-auth-45