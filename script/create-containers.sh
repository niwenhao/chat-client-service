podman run --pod chat-service \
           --name mariadb \
           -v $(pwd)/data:/var/lib/mysql \
           -e MYSQL_ROOT_PASSWORD=password \
           -d docker.io/library/mariadb
podman run --pod chat-service \
           --name api \
           -v $(pwd):/app \
           -e OPENAI_API_KEY=${OPENAI_API_KEY} \
           -d api-service