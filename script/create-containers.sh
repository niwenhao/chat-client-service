podman run --pod chat-service --name mariadb -v $(pwd)/data:/var/lib/mysql -e MYSQL_ROOT_PASSWORD=password -d docker.io/library/mariadb
podman run --pod chat-service --name api -v $(pwd):/app -d api-service