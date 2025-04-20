# Create directories in the correct location
sudo mkdir -p /usr/share/nginx/html/server1
sudo mkdir -p /usr/share/nginx/html/server2
sudo mkdir -p /usr/share/nginx/html/server3

# Create test HTML files
sudo bash -c 'cat > /usr/share/nginx/html/server1/index.html << EOF
<!DOCTYPE html>
<html>
<head>
    <title>Server 1</title>
    <style>
        body { background-color: #f0f8ff; font-family: Arial, sans-serif; text-align: center; padding-top: 50px; }
        h1 { color: #0066cc; }
    </style>
</head>
<body>
    <h1>This is Server 1</h1>
    <p>Hostname: $(hostname)</p>
    <p>Date and Time: $(date)</p>
</body>
</html>
EOF'

sudo bash -c 'cat > /usr/share/nginx/html/server2/index.html << EOF
<!DOCTYPE html>
<html>
<head>
    <title>Server 2</title>
    <style>
        body { background-color: #f5f5dc; font-family: Arial, sans-serif; text-align: center; padding-top: 50px; }
        h1 { color: #cc6600; }
    </style>
</head>
<body>
    <h1>This is Server 2</h1>
    <p>Hostname: $(hostname)</p>
    <p>Date and Time: $(date)</p>
</body>
</html>
EOF'

sudo bash -c 'cat > /usr/share/nginx/html/server3/index.html << EOF
<!DOCTYPE html>
<html>
<head>
    <title>Server 3</title>
    <style>
        body { background-color: #e6ffe6; font-family: Arial, sans-serif; text-align: center; padding-top: 50px; }
        h1 { color: #006600; }
    </style>
</head>
<body>
    <h1>This is Server 3</h1>
    <p>Hostname: $(hostname)</p>
    <p>Date and Time: $(date)</p>
</body>
</html>
EOF'