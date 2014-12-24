#!/usr/bin/env python

import subprocess, os

os.chdir('YOUR_PATH')
lcmd='git rev-list --count HEAD'
res=subprocess.call(lcmd, shell=True)
