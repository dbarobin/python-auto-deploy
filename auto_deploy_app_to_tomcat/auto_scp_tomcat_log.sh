#!/bin/bash

# Author: Robin Wen
# Date: 10:23:20 12/12/2014
# Desc: Auto scp tomcat logs.

# Copy the tomcat logs.
date_yesterday=`date -d yesterday +%F`
date_today=`date +%F`
date_tomorrow=`date -d next-day +%F`

if [ ! -f "localhost.$date_yesterday.log" ]
then
	scp YOUR_NAME@YOUR_IP:YOUR_TOMCAT_HOME/logs/localhost.$date_yesterday.log YOUR_PATH/logs/tomcat 2>/dev/null
fi

if [ ! -f "localhost.$date_today.log" ]
then
	scp YOUR_NAME@YOUR_IP:YOUR_TOMCAT_HOME/logs/localhost.$date_today.log YOUR_PATH/logs/tomcat 2>/dev/null
fi

if [ ! -f "localhost.$date_tomorrow.log" ]
then
	scp YOUR_NAME@YOUR_IP:YOUR_TOMCAT_HOME/logs/localhost.$date_tomorrow.log YOUR_PATH/logs/tomcat 2>/dev/null
fi
