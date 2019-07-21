# -*-coding:utf-8 -*-
# !/usr/bin/env python3
import os
import subprocess
from logs import logs


def call(cmd):
    logs.info("Exec cmd: %s" % cmd)
    status, output = subprocess.getstatusoutput(cmd)
    if status:
        logs.error(output)
        raise Exception("Exec cmd fail, cmd: %s" % cmd)
    return output

def mkdirs(path):
    if not os.path.exists(path):
        mkdirs(path)

def clone_repo(repo_path, url):
    """
    clone repo by url
    """
    if not os.path.exists(repo_path):
        current_path = os.getcwd()
        os.chdir(os.path.dirname(repo_path))
        call("git clone %s" % url)
        os.chdir(current_path)