#!/usr/bin/python3
""" a Fabric script (based on the file 1-pack_web_static.py)
"""

from fabric.api import *
from datetime import datetime
from os.path import exists


env.hosts = ['54.237.11.197', '35.153.16.149']

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
    """
    Distributes an archive to web servers and deploys it.
    Args:
        archive_path: Path to the archive file.
    Returns:
        True if all operations have been done correctly, otherwise False.
    """
    if not archive_path or not os.path.exists(archive_path):
        print("Invalid archive path or archive file does not exist.")
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

def deploy():
    """
    Creates and distributes an archive to web servers, using do_pack and do_deploy functions.
    Returns:
        True if deployment is successful, otherwise False.
    """
    # Create the archive
    archive_path = do_pack()

    # Return False if no archive has been created
    if not archive_path:
        print("No archive has been created.")
        return False

    # Call do_deploy function using the new path of the new archive
    return do_deploy(archive_path)
