# Create a directory for SSL files
sudo mkdir -p /etc/nginx/ssl

# Generate a self-signed certificate valid for 365 days
sudo openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout /etc/nginx/ssl/nginx.key \
  -out /etc/nginx/ssl/nginx.crt