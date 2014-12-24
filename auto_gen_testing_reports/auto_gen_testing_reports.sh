#!/bin/bash

# Author: Robin Wen
# Date: 16:36:14  22/12/2014
# Desc: Auto gen testing reports via crontab.

script_path=YOUR_PATH

if [ $? -eq 0 ];then
	# Update the repo via git.
	cd $script_path && ./auto_deploy_app_remote.py -u
fi

if [ $? -eq 0 ];then
	# Auto generate testing reports.
	cd $script_path && ./auto_deploy_app_remote.py -a
fi

if [ $? -eq 0 ];then
	# Scp generated reports.
	cd $script_path && ./auto_deploy_app_remote.py -s
fi
