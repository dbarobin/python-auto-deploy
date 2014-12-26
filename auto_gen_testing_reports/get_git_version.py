#!/usr/bin/env python
# Author: Robin Wen
# Date: 18:15:25 2014-12-24
# Desc: Get repo version.
# FileName: get_git_version.py

import subprocess, os

os.chdir('YOUR_PATH')
lcmd='git rev-list --count HEAD'
res=subprocess.call(lcmd, shell=True)
