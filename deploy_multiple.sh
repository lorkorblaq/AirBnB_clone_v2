#!/bin/bash
# Define the Nginx configuration file path
nginx_conf="/etc/nginx/sites-available/web_static"

# Function to deploy Nginx on a remote server
deploy_nginx() {
    server_ip="$1"
    
    echo "Deploying Nginx on $server_ip..."
    
    # Copy the script to the remote server
    scp deploy_nginx.sh "ubuntu@$server_ip:/tmp/deploy_nginx.sh"
    
    # Execute the script on the remote server
    ssh "ubuntu@$server_ip" "sudo /tmp/deploy_nginx.sh"
    
    echo "Nginx deployment on $server_ip complete."
}
# Deploy on multiple servers
deploy_nginx "54.90.8.129"
deploy_nginx "18.234.169.154"
