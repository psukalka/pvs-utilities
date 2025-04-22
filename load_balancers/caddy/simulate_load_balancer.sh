sudo mkdir -p /var/www/server1 /var/www/server2 /var/www/server3
echo "<h1>Server 1</h1>" | sudo tee /var/www/server1/index.html
echo "<h1>Server 2</h1>" | sudo tee /var/www/server2/index.html
echo "<h1>Server 3</h1>" | sudo tee /var/www/server3/index.html