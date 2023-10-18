#!/usr/bin/python3
"""
Fabric script based on the file 2-do_deploy_web_static.py that creates and
distributes an archive to the web servers
"""
# fabfile.py

from fabric.api import *
from datetime import datetime
from os.path import exists, isdir

env.use_ssh_config = True
# env.key_filename = '/home/blaq/.ssh/school'
env.hosts = ['blaq1', 'blaq2']
#env.user= 'ubuntu'


@runs_once
def do_pack(delete_previous=True):
    """
        Compress before sending
    """
    if delete_previous:
        # Delete the previous archive
        local("rm -f versions/web_static*.tgz")

    local("mkdir -p versions")
    date = datetime.now().strftime("%Y%m%d%H%M%S")
    archive_path = "versions/web_static_{}.tgz".format(date)
    t_gzip_archive = local("tar -cvzf {} web_static".format(archive_path))
    print("archived created")
    if t_gzip_archive.succeeded:
        return archive_path
    else:
        return None
    
def nginx_sites():
    nginx_conf = "/etc/nginx/sites-available/web_static"

    nginx_config = """
    server {
        listen 80;
        listen [::]:80;
        server_name www.lorkorblaq.tech;
        return 301 https://lorkorblaq.tech$request_uri;
    }

    server {
        server_name lorkorblaq.tech;
        location / {
            root /data/web_static/current/;
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
    }
    """
    sudo("echo '{}' | sudo tee '{}' > /dev/null".format(nginx_config,   nginx_conf))



def do_deploy(archive_path):
    """distributes an archive to the web servers"""
    if exists(archive_path) is False:
        return False
    try:
        file_n = archive_path.split("/")[-1]
        no_ext = file_n.split(".")[0]
        path = "/data/web_static/releases/"
        put(archive_path, '/tmp/')
        sudo('mkdir -p {}{}/'.format(path, no_ext))
        sudo('tar -xzf /tmp/{} -C {}{}/'.format(file_n, path,no_ext))
        sudo('rm /tmp/{}'.format(file_n))
        sudo('mv {0}{1}/web_static/* {0}{1}/'.format(path, no_ext))
        sudo('rm -rf {}{}/web_static'.format(path, no_ext))
        sudo('rm -rf /data/web_static/current')
        sudo('ln -s {}{}/ /data/web_static/current'.format(path, no_ext))
        sudo('chown -R www-data:www-data /data/web_static/current/')
        sudo('chmod 755 /data/web_static/current/')
        sudo('service nginx restart')
        return True 
    except:
        return False


def deploy():
    """creates and distributes an archive to the web servers"""
    
    archive_path = do_pack()
    nginx_sites()
    if archive_path is None:
        return print("Failed to create archive")
    return do_deploy(archive_path)


