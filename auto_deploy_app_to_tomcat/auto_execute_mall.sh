#!/bin/bash

# Author: Robin Wen
# Date: 17:35:20 12/11/2014
# Desc: Auto deploy to remote tomcat via crontab.

# Script path.
script_path=YOUR_PATH

# Update the mall admin.
if [ $? -eq 0 ];then
	cd $script_path && ./auto_deploy_app_remote.py -u
fi

# Update the mall api.
if [ $? -eq 0 ];then
	cd $script_path && ./auto_deploy_app_remote.py -m
fi

# Shutdown the tomcat.
if [ $? -eq 0 ];then
	cd $script_path && ./auto_deploy_app_remote.py -s
fi

# Deploy the mall admin.
if [ $? -eq 0 ];then
	cd $script_path && ./auto_deploy_app_remote.py -w
fi

# Deploy the mall api.
if [ $? -eq 0 ];then
	cd $script_path && ./auto_deploy_app_remote.py -d
fi

if [ $? -eq 0 ];then
	# Startup the tomcat.
	cd $script_path && ./auto_deploy_app_remote.py -t
fi
