# Create a test page if you haven't already
sudo mkdir -p /var/www/html
echo "<h1>Hello from Pavan!</h1>" | sudo tee /var/www/html/index.html

# TODO:
# Go and update path /var/www/html in /etc/caddy/Caddyfile