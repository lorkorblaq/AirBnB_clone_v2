#!/usr/bin/python3
"""
Fabric script that distributes an archive to your web servers
"""

from datetime import datetime
from fabric.api import *
import os

env.use_ssh_config = True
env.hosts = ["blaq1", "blaq2"]
# env.user = "ubuntu"
# env.key_filename = '/home/blaq/.ssh/school'

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


def do_deploy(archive_path):
    """
        Distribute archive.
    """ 
    if os.path.exists(archive_path):
        archived_file = archive_path[9:]
        newest_version = "/data/web_static/releases/" + archived_file[:-4]
        archived_file = "/tmp/" + archived_file
        put(archive_path, "/tmp/")
        sudo("mkdir -p {}".format(newest_version))
        sudo("tar -xzf {} -C {}/".format(archived_file, newest_version))
        sudo("rm {}".format(archived_file))
        sudo("mv {}/web_static/* {}".format(newest_version, newest_version))
        sudo("rm -rf {}/web_static".format(newest_version))
        sudo("rm -rf /data/web_static/current")
        sudo("ln -sf {} /data/web_static/current".format(newest_version))

        print("New version deployed!")
        return True
    return False

@task
def run_all():
    """
    Run all
    """
    archive_path = do_pack()
    return do_deploy(archive_path)