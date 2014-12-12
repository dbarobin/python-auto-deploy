#!/bin/bash

# Author: Robin Wen
# Date: 10:23:20 12/12/2014
# Desc: Auto scp tomcat logs.

# Copy the tomcat logs.

# Yesterdate date. Fommat 2014-12-12.
date_yesterday=`date -d yesterday +%F`
# Today date. Fommat 2014-12-12.
date_today=`date +%F`
# Tomorrow date. Fommat 2014-12-12.
date_tomorrow=`date -d next-day +%F`

# Copy the yesterday's tomcat log.
if [ ! -f "localhost.$date_yesterday.log" ]
then
	scp YOUR_NAME@YOUR_IP:YOUR_TOMCAT_HOME/logs/localhost.$date_yesterday.log YOUR_PATH/logs/tomcat 2>/dev/null
fi

# Copy the today's tomcat log.
if [ ! -f "localhost.$date_today.log" ]
then
	scp YOUR_NAME@YOUR_IP:YOUR_TOMCAT_HOME/logs/localhost.$date_today.log YOUR_PATH/logs/tomcat 2>/dev/null
fi

# Copy the tomorrow's tomcat log.
if [ ! -f "localhost.$date_tomorrow.log" ]
then
	scp YOUR_NAME@YOUR_IP:YOUR_TOMCAT_HOME/logs/localhost.$date_tomorrow.log YOUR_PATH/logs/tomcat 2>/dev/null
fi
