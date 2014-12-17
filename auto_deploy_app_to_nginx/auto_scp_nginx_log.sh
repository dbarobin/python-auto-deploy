#!/bin/bash

# Author: Robin Wen
# Date: 11:12:29 17/12/2014
# Desc: Auto scp nginx logs.

# Nginx access log of shop repo.
access_log=

# Nginx error log of shop repo.
error_log=

# Copy the nginx access log of shop repo.
if [ -f "$access_log" ]
then
	scp YOUR_NAME@YOUR_IP:$access_log ~/logs/nginx 2>/dev/null
fi

# Copy the nginx error log of shop repo.
if [ -f "$error_log" ]
then
	scp YOUR_NAME@YOUR_IP:$error_log ~/logs/nginx 2>/dev/null
fi
