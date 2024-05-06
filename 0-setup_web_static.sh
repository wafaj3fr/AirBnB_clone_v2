#!/usr/bin/env bash
# script for setting up the web servers for deployment of web_static

#!/usr/bin/env bash
# This script sets up web servers for the deployment of web_static.

# Install nginx if not already installed
if ! [ -x "$(command -v nginx)" ]; then
    apt-get update
    apt-get -y install nginx
fi

# Create necessary directories if they don't exist
mkdir -p /data/web_static/releases/test /data/web_static/shared

# Create a fake HTML file
echo "<html>
    <head>
        <title>Test Page</title>
    </head>
    <body>
        <p>This is a test page for web_static deployment.</p>
    </body>
</html>" | tee /data/web_static/releases/test/index.html

# Create symbolic link, recreate if already exists
ln -sf /data/web_static/releases/test/ /data/web_static/current

# Give ownership of /data/ folder to ubuntu user and group recursively
chown -R ubuntu:ubuntu /data/

# Update nginx configuration
sed -i '/hbnb_static/ {
    s/^\(\s*location\s*\)\(.*\)\(\{\)/\1\2\n\n\1\/hbnb_static\/ {\n\talias \/data\/web_static\/current\/;\n/g
}' /etc/nginx/sites-available/default

# Restart nginx
service nginx restart

if sudo nginx -t && sudo service nginx reload && curl -s localhost/hbnb_static | grep -q "This is a test page for web_static deployment."; then
    echo "Nginx configuration updated and localhost/hbnb_static available"
else
    echo "Nginx configuration update failed or localhost/hbnb_static not available"
fi
