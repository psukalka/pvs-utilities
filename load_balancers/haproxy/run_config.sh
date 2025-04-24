# Test validity of file
sudo haproxy -c -f /etc/haproxy/haproxy.cfg

# Restart haproxy
sudo systemctl restart haproxy

# Loadbalancing test
for i in {1..1000}; do curl http://localhost; echo; done

# Check stats at
http://localhost/haproxy?stats