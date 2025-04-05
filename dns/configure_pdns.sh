# Follow these steps after PDNS docker is installed
sudo docker exec -it pdns /bin/bash

# Check that sqlite backend is enabled
cat /etc/powerdns/pdns.conf

# Create zone
pdnsutil create-zone pvsukalkar.in

# Add NS record
pdnsutil add-record pvsukalkar.in @ NS ns1.pvsukalkar.in

# Add A record
pdnsutil add-record pvsukalkar.in ns1 A 44.204.216.247

# TODO: Go to Security group settings and enable port 53 (UDP and TCP) for DNS traffic

# Test locally (outside docker)
dig @localhost pvsukalkar.in