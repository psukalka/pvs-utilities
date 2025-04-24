sudo mkdir -p /var/www/server1 /var/www/server2 /var/www/server3

echo "<html><body><h1>Server 1</h1><p>This is server 1 responding.</p></body></html>" | sudo tee /var/www/server1/index.html
echo "<html><body><h1>Server 2</h1><p>This is server 2 responding.</p></body></html>" | sudo tee /var/www/server2/index.html
echo "<html><body><h1>Server 3</h1><p>This is server 3 responding.</p></body></html>" | sudo tee /var/www/server3/index.html

# Run these commands in separate terminal sessions or use nohup to run them in the background
# Server 1 on port 8081
cd /var/www/server1 && sudo python3 -m http.server 8081 &

# Server 2 on port 8082
cd /var/www/server2 && sudo python3 -m http.server 8082 &

# Server 3 on port 8083
cd /var/www/server3 && sudo python3 -m http.server 8083 &