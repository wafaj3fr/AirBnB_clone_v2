#!/usr/bin/python3
# Fabfile to delete out-of-date archives.
from fabric.api import *
import os


env.hosts = ['54.237.11.197', '35.153.16.149']

def do_clean(number=0):
    """
    Deletes out-of-date archives.
    Args:
        number: Number of archives to keep.
    """
    try:
        # Delete unnecessary archives in the versions folder
        local("ls -t versions | tail -n +{} | xargs -I {{}} rm versions/{{}}".format(number + 1))

        # Delete unnecessary archives in /data/web_static/releases folder on both servers
        run("ls -t /data/web_static/releases | tail -n +{} | xargs -I {{}} rm -rf /data/web_static/releases/{{}}"
            .format(number + 1))

        print("Cleaned up old archives successfully.")
    except Exception as e:
        print("An error occurred:", e)
