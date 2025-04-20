# Steps to use this folder
- Install nginx with `install_nginx.sh` file
- Create dummy server files using `simulate_web_servers.sh` . A more practical way would have been creating some web server under docker but that would need more memory. Serving index.html file as aim is to learn load balancing.
- Copy `server1.conf` , `server2.conf` , `server3.conf` file under `/etc/nginx/conf.d/` folder
- Test their validity by running `apply_config.sh` script
- Copy `load_balancer.conf` file under `/etc/nginx/conf.d/` folder