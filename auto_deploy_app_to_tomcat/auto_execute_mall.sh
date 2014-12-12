#!/bin/bash

# Author: Robin Wen
# Date: 17:35:20 12/11/2014
# Desc: Auto deploy to remote tomcat via crontab.

script_path=YOUR_PATH

if [ $? -eq 0 ];then
	# Update the mall admin.
	cd $script_path && ./auto_deploy_app_remote.py -u
fi

if [ $? -eq 0 ];then
	# Update the mall api.
	cd $script_path && ./auto_deploy_app_remote.py -m
fi

if [ $? -eq 0 ];then
	# Shutdown the tomcat.
	cd $script_path && ./auto_deploy_app_remote.py -s
fi

if [ $? -eq 0 ];then
	# Deploy the mall admin.
	cd $script_path && ./auto_deploy_app_remote.py -w
fi

if [ $? -eq 0 ];then
	# Deploy the mall api.
	cd $script_path && ./auto_deploy_app_remote.py -d
fi

if [ $? -eq 0 ];then
	# Startup the tomcat.
	cd $script_path && ./auto_deploy_app_remote.py -t
fi
