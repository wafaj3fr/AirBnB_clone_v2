#!/usr/bin/python3
"""
Fabric script based on the file 1-pack_web_static.py
"""

from fabric.api import *
import os

env.hosts = ['54.237.11.197', '35.153.16.149']
env.user = 'ubuntu'

def do_pack():
    """
    Generates a .tgz archive from the contents of the web_static folder.
    Returns:
        Archive path if the archive has been correctly generated, otherwise None.
    """
    try:
        # Create versions folder if it doesn't exist
        local("mkdir -p versions")

        # Generate timestamp for the archive name
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

        # Create the archive
        archive_name = "versions/web_static_{}.tgz".format(timestamp)
        local("tar -cvzf {} web_static".format(archive_name))

        return archive_name
    except Exception as e:
        print("An error occurred:", e)
        return None

def do_deploy(archive_path):
    """distributes an archive to the web servers"""
    if exists(archive_path) is False:
        return False
    try:
        file_n = archive_path.split("/")[-1]
        no_ext = file_n.split(".")[0]
        path = "/data/web_static/releases/"
        put(archive_path, '/tmp/')
        run('mkdir -p {}{}/'.format(path, no_ext))
        run('tar -xzf /tmp/{} -C {}{}/'.format(file_n, path, no_ext))
        run('rm /tmp/{}'.format(file_n))
        run('mv {0}{1}/web_static/* {0}{1}/'.format(path, no_ext))
        run('rm -rf {}{}/web_static'.format(path, no_ext))
        run('rm -rf /data/web_static/current')
        run('ln -s {}{}/ /data/web_static/current'.format(path, no_ext))
        return True
    except:
        return False
