#!/usr/bin/python3
"""
Fabric script based on the file 1-pack_web_static.py
"""

from fabric.api import *
import os

env.hosts = ['54.237.11.197', '35.153.16.149']
env.user = 'ubuntu'

def do_deploy(archive_path):
    """
    Distributes an archive to web servers and deploys it.
    Args:
        archive_path: Path to the archive file.
    Returns:
        True if all operations have been done correctly, otherwise False.
    """
    if not os.path.exists(archive_path):
        print("Archive file does not exist.")
        return False

    try:
        # Upload the archive to /tmp/ directory of the web server
        put(archive_path, "/tmp/")

        # Extract archive filename without extension
        archive_filename = os.path.basename(archive_path)
        archive_name = os.path.splitext(archive_filename)[0]

        # Uncompress the archive to /data/web_static/releases/ directory on the web server
        run("mkdir -p /data/web_static/releases/{}/".format(archive_name))
        run("tar -xzf /tmp/{} -C /data/web_static/releases/{}/"
            .format(archive_filename, archive_name))

        # Delete the archive from the web server
        run("rm /tmp/{}".format(archive_filename))

        # Delete the symbolic link /data/web_static/current from the web server
        run("rm -rf /data/web_static/current")

        # Create a new symbolic link to the new version of code
        run("ln -s /data/web_static/releases/{}/ /data/web_static/current"
            .format(archive_name))

        print("New version deployed!")
        return True
    except Exception as e:
        print("An error occurred:", e)
        return False
