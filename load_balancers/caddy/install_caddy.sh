# First, let's install the required dependencies
sudo yum install -y yum-utils

# Add the official Caddy repo
sudo yum-config-manager --add-repo https://copr.fedorainfracloud.org/coprs/g/caddy/caddy/repo/epel-7/group_caddy-caddy-epel-7.repo

# Now install Caddy
sudo yum install -y caddy