#!/usr/bin/python3
"""
Fabric script that generates a tg archive
"""

from fabric.api import local
from datetime import datetime

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
