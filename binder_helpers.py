import os
import subprocess


def start_services():
    if os.path.exists('/usr/sbin/service'):
        if subprocess.call("sudo /usr/sbin/service postgresql status", shell=True):
            subprocess.call("sudo /usr/sbin/service postgresql start", shell=True)
        if subprocess.call("sudo /usr/sbin/service redis-server status", shell=True):
            subprocess.call("sudo /usr/sbin/service redis-server start", shell=True)
