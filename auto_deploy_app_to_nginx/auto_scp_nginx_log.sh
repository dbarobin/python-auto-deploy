#!/bin/bash

# Author: Robin Wen
# Date: 11:12:29 17/12/2014
# Desc: Auto scp nginx logs.

# Nginx access log of shop repo.
access_log=/var/log/nginx/e1shop.access.log

# Nginx error log of shop repo.
error_log=/var/log/nginx/e1shop.error.log

# Copy the nginx access log of shop repo.
if [ -f "$access_log" ]
then
	scp shop@10.10.1.105:$access_log ~/logs/nginx 2>/dev/null
fi

# Copy the nginx error log of shop repo.
if [ -f "$error_log" ]
then
	scp shop@10.10.1.105:$error_log ~/logs/nginx 2>/dev/null
fi
