#!/usr/bin/env python
# Author: Robin Wen
# Date: 18:16:54 2014-12-24
# Desc: Test get repo version.
# FileName: test_result.py

import os

os.system("python /Users/robin/get_git_version.py > old.log")
os.system("python /Users/robin/get_git_version.py > new.log")

file = open('old.log', 'r')
old=file.read()
file.close()

file = open('new.log', 'r')
new=file.read()
file.close()

print old
print new

if old == new:
    print "equal"
else:
    print "not"
