#!/usr/bin/python3
# Fabric script (based on the file 1-pack_web_static.py) that distributes an archive to your web servers
import os.path
from fabric.api import env
from fabric.api import put
from fabric.api import run

env.hosts = ["18.235.233.229", "54.236.47.100"]


def do_deploy(archive_path):
    """Fabric script (based on the file 1-pack_web_static.py) that distributes an archive to your web servers

    Args:
        archive_path (str): The path of the archive to distribute.
    Returns:
        If the file doesn't exist at archive_path or an error occurs - False.
        Otherwise - True.
    """
    if os.path.isfile(archive_path) is False:
        return False
    file = archive_path.split("/")[-1]
    name = file.split(".")[0]

    if put(archive_path, "/tmp/{}".format(file)).failed is True:
        return False
    if run("rm -rf /data/static/releases/{}/".
           format(name)).failed is True:
        return False
    if run("mkdir -p /data/static/releases/{}/".
           format(name)).failed is True:
        return False
    if run("tar -xzf /tmp/{} -C /data/static/releases/{}/".
           format(file, name)).failed is True:
        return False
    if run("rm /tmp/{}".format(file)).failed is True:
        return False
    if run("mv /data/static/releases/{}/static/* "
           "/data/static/releases/{}/".format(name, name)).failed is True:
        return False
    if run("rm -rf /data/static/releases/{}/static".
           format(name)).failed is True:
        return False
    if run("rm -rf /data/static/current").failed is True:
        return False
    if run("ln -s /data/static/releases/{}/ /data/static/current".
           format(name)).failed is True:
        return False
    return True
