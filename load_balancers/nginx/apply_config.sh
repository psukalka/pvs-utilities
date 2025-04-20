# Give permission to nginx
sudo chmod -R 755 /usr/share/nginx/html
sudo chown -R nginx:nginx /usr/share/nginx/html


# Test syntax
sudo nginx -t

# reload nginx to apply changes
sudo systemctl reload nginx 