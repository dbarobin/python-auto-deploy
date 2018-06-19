#!/bin/bash

# Author: Robin Wen
# Date: 10:52:26 12/17/2014
# Desc: Auto deploy to remote nginx via crontab.

# Script path.
script_path=YOUR_PATH

# Update the shop.
if [ $? -eq 0 ];then
	cd $script_path && ./auto_deploy_app_remote.py -u
fi

# Shutdown the nginx. 
if [ $? -eq 0 ];then
	cd $script_path && ./auto_deploy_app_remote.py -s
fi

# Deploy the shop.
if [ $? -eq 0 ];then
	cd $script_path && ./auto_deploy_app_remote.py -d
fi

# Startup the nginx.
if [ $? -eq 0 ];then
	cd $script_path && ./auto_deploy_app_remote.py -t
fi
