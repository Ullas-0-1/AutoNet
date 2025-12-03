FROM nginx:latest

# Install simple tools needed for the script
RUN apt-get update && apt-get install -y procps

COPY nginx.conf /etc/nginx/nginx.conf

# Copy and setup the watcher script
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Override default Nginx startup
ENTRYPOINT ["/entrypoint.sh"]