# Give permission to nginx
sudo chmod -R 755 /var/www/
sudo chown -R nginx:nginx /var/www/


# Test syntax
sudo nginx -t

# reload nginx to apply changes
sudo systemctl reload nginx 