# Keyfile is needed for using authentication with replicaset
# Generate a keyfile with appropriate permissions
openssl rand -base64 756 > mongo-keyfile
chmod 400 mongo-keyfile