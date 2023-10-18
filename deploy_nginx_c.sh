#!/bin/bash

# Define the Nginx configuration file path
nginx_conf="/etc/nginx/sites-available/web_static"

# Check if Nginx is installed
if ! command -v nginx &> /dev/null; then
    echo "Nginx is not installed. Installing..."
    sudo apt-get update
    sudo apt-get install -y nginx
fi

# Create the Nginx configuration file
echo "server {
    listen 80 default_server;
    listen [::]:80 default_server;
    add_header X-Served-By \"\$host\";
    root /var/www/html;
    index index.html index.htm;
    
    location /hbnb_static {
        alias /data/web_static/current;
        index index.html index.htm;
    }
    location /redirect_me {
        return 301 http://lorkorblaq.tech;
    }
    error_page 404 /404.html;
    location /404 {
        root /var/www/html;
        internal;
    }
}" | sudo tee "$nginx_conf" > /dev/null

  

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

        location /hbnb_static {
            alias /data/webstatic/current;
            index index.html index.htm;
        }

        error_page 404 /404.html;
        location /404 {
            root /var/www/html;
            internal;
        }
}" | sudo tee "$nginx_conf"> /dev/null


# Create a symbolic link to enable the site
sudo ln -s "$nginx_conf" "/etc/nginx/sites-enabled/"

# Restart Nginx to apply changes
sudo service nginx restart

echo "Nginx deployment complete."
