FROM alpine:latest

# Install SQLite
RUN apk add --no-cache sqlite

# Copy the initialization script into the container
COPY init.sql /docker-entrypoint-initdb.d/

# Keep the container running by running a simple command
CMD ["tail", "-f", "/dev/null"]
