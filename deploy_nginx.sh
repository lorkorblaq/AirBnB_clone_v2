#!/bin/bash

# Define the Nginx configuration file path
nginx_conf="/etc/nginx/sites-available/web_static"

# Check if Nginx is installed
if ! command -v nginx &> /dev/null; then
    echo "Nginx is not installed. Installing..."
    sudo apt-get update
    sudo apt-get install -y nginx
fi

sudo mkdir -p /data/web_static/releases/test/
sudo mkdir -p /data/web_static/shared/
echo "Holberton School" > /data/web_static/releases/test/index.html
sudo ln -sf /data/web_static/releases/test/ /data/web_static/current

chown -R ubuntu /data/
chgrp -R ubuntu /data/

# Create the Nginx configuration file
echo "server {
    listen 80;
    listen [::]:80;
    server_name www.lorkorblaq.tech;
    return 301 https://lorkorblaq.tech$request_uri;
    
}

server {
    server_name lorkorblaq.tech;

    location / {
        root /var/www/html/;
        index index.html index.htm;
        
    }

    location /hbnb_static/ {
        alias /data/web_static/current/;
        index 0-index.html index.htm;
        try_files $uri $uri/ =404;
    }

    error_page 404 /404.html;
    location /404 {
        root /var/www/html;
        internal;
    }
}" | sudo tee "$nginx_conf"> /dev/null


# Create a symbolic link to enable the site
sudo ln -sf "$nginx_conf" "/etc/nginx/sites-enabled/"

# Restart Nginx to apply changes
sudo service nginx restart

echo "Nginx deployment complete."

